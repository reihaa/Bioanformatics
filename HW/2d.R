#Working with GSE32962 expression data 
load("expressionMatrix.RData")
library(limma)
groups = c(rep("SensitiveInfant",13), rep("ResistantInfant",12), rep("SensitiveNonInfant",14), rep("ResistantNonInfant", 13))
f = factor(groups,levels=c("SensitiveInfant", "ResistantInfant","SensitiveNonInfant", "ResistantNonInfant"))
design = model.matrix(~ 0 + f)
colnames(design) = c("SensitiveInfant", "ResistantInfant","SensitiveNonInfant", "ResistantNonInfant")
data.fit = lmFit(expressionMatrix,design)
contrast.matrix = makeContrasts(ResistantNonInfant-ResistantInfant,levels=design)
data.fit.con = contrasts.fit(data.fit,contrast.matrix)
data.fit.eb = eBayes(data.fit.con)
table = topTable(data.fit.eb,number=12248,adjust.method="BH",sort.by="none",p.value = 0.05)
table = as.data.frame(table)
fileConn<-file("2d.txt")
writeLines(row.names(table), fileConn)
close(fileConn)
data.fit.eb$coefficients[1:10,]
data.fit.eb$p.value[1:10,]


