workingDir = "~/Desktop/bio";
setwd(workingDir);

install.packages("hgu133ahsentrezgcdf_25.0.0.tar.gz", repos = NULL, type="source")
install.packages("hgu133ahsentrezgprobe_25.0.0.tar.gz", repos = NULL, type="source")
install.packages("hgu133ahsentrezg.db_25.0.0.tar.gz", repos = NULL, type="source")
# if (!requireNamespace("BiocManager", quietly = TRUE))
  # install.packages("BiocManager")

BiocManager::install("gcrma", version = "3.13")
BiocManager::install("affy", versiaon = "3.13")
# BiocManager::install("GEOquery", version = "3.13")

library(affy)
library(gcrma)
library(GEOquery)
library(hgu133ahsentrezgcdf)
#cdfname="HGU133A2_HS_ENTREZG"
library(hgu133ahsentrezgprobe)
library(hgu133ahsentrezg.db)

getGEOSuppFiles("GSE19143")

setwd(paste(getwd(),"/GSE19143/", sep=""))
untar("GSE19143_RAW.tar", exdir="data")
cels = list.files("data/", pattern = "CEL")
sapply(paste("data", cels, sep="/"), gunzip)
cels = list.files("data/", pattern = "CEL")
# Extract Pheno Data
# pData=raw.data@phenoData@data
setwd(paste(getwd(),"/data/", sep=""))

raw.data=ReadAffy(verbose=TRUE, filenames=cels, cdfname="HGU133A_Hs_ENTREZG") 

data.norm=rma(raw.data)
# cdata.norm=gcrma(raw.data)

# Extract expression values
expressionMatrix=exprs(data.norm)
list=grep("AFFX",row.names(expressionMatrix))
expressionMatrix=expressionMatrix[-list,] 

probes=row.names(expressionMatrix)
symbol = unlist(mget(probes, hgu133ahsentrezgSYMBOL))
ID = unlist(mget(probes, hgu133ahsentrezgENTREZID))
expressionMatrix=data.frame(probes,ID,symbol,expressionMatrix,stringsAsFactors=FALSE)
expressionMatrix=na.omit(expressionMatrix)

row.names(expressionMatrix)=expressionMatrix$symbol
expressionMatrix=expressionMatrix[,-c(1:3)]
setwd(workingDir)
pdf("boxplot.pdf")
boxplot(expressionMatrix)
dev.off()
expressionMatrix=as.matrix(expressionMatrix)
pdf("heatmap.pdf")
heatmap(expressionMatrix[1:10,])
dev.off()
save(probes,expressionMatrix, file="expressionMatrix.RData")
