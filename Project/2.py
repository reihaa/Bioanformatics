
#Find Patterns Forming Clumps in a String
#http://rosalind.info/problems/ba1e/


def find_clumps(dna,k,L,t):
    ans_list = set()
    ans_dict = dict()

    for start in range(len(dna) - k + 1):
        word = dna[start:start+k]
        if word not in ans_dict.keys():
            ans_dict[word] = []
        if len(ans_dict[word]) and start - ans_dict[word][-1] < k:
            ans_dict[word].pop()
        ans_dict[word].append(start)
        while start - ans_dict[word][0] > L-k:
            ans_dict[word] = ans_dict[word][1:]
        if len(ans_dict[word]) >= t:
            ans_list.add(word)

    return ans_list


dna = input()
k, L, t = map(int, input().split())
ans_list = find_clumps(dna,k,L,t)
print(" ".join(sorted(list(ans_list))))
