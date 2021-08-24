
# Find the Shortest Non-Shared Substring of Two Strings
#http://rosalind.info/problems/ba9f/


def generalized_suffixArray(s, t):
    suffix_list_t = [t[j:] for j in range(len(t))]
    suffix_list_s = [s[i:] for i in range(len(s))]
    suffix_array = suffix_list_s + suffix_list_t
    suffix_array.sort()
    return suffix_array


def generalized_lcp_array(sufix_array):
    lcp_array = []
    for i in range(len(sufix_array) - 1):
        for j in range(min(len(sufix_array[i]), len(sufix_array[i + 1]))):
            if (sufix_array[i][j] != sufix_array[i + 1][j]):
                lcp_array.append(j)
                break
    return lcp_array


def shortest_nonshared_substring(lcp_array, suffix_array):
    ans_list = []
    ans1, ans2 = '', ''
    pre_pointer, next_pointer = 0, 0
    for i in range(len(suffix_array)):
        p1, p2 = 1, 1
        if suffix_array[i][-1] == '#':
            pre_pointer = i
        else:
            if next_pointer < i:
                for j in range(i + 1, len(suffix_array)):
                    if suffix_array[j][-1] == '#':
                        next_pointer = j
                        break
            if pre_pointer + 1 == i:
                if lcp_array[i - 1] < len(suffix_array[i]) - 1:
                    ans1 = suffix_array[i][0:lcp_array[i - 1] + 1]
                else:
                    ans1 = suffix_array[i][0:lcp_array[i - 1]]
                    p1 = 0
                if i > next_pointer:
                    if p1:
                        ans_list.append(ans1)

            if i + 1 == next_pointer:
                if lcp_array[i] < len(suffix_array[i]) - 1:
                    ans2 = suffix_array[i][0:lcp_array[i] + 1]
                    a = 2
                    while ans1.startswith(ans2):
                        ans2 = suffix_array[i][0:lcp_array[i] + a]
                        a += 1
                else:
                    ans2 = suffix_array[i][0:lcp_array[i]]
                    p2 = 0
                if p2 and (not ans1.startswith(ans2)):
                    ans_list.append(ans2)
                if p1 and not ans2.startswith(ans1):
                    ans_list.append(ans1)
            if i + 1 != next_pointer and i != pre_pointer + 1:
                if i == len(suffix_array) - 1 or not (suffix_array[i + 1].startswith(suffix_array[i][:-1])):
                    b = 1
                    while ans1.startswith(suffix_array[i][0:b]) or (len(suffix_array)>i+1 and suffix_array[i+1].startswith(suffix_array[i][0:b])):
                        b += 1
                    ans_list.append(suffix_array[i][0:b])
    return ans_list


s = input()
t = input()
s = s + "$"
t = t + '#'
suffix_array = generalized_suffixArray(s, t)
# print(suffix_array,"\n")
lcp_array = generalized_lcp_array(suffix_array)
# print(lcp_array,"\n")
ans_list = shortest_nonshared_substring(lcp_array, suffix_array)
ans = ans_list[0]
j= 0
for i in ans_list:
    if i[0] in t:
        # print(i)
        j+=1
        # print(suffix_array[i[1]-1], suffix_array[i[1]],suffix_array[i[1]+1])
    if len(i) < len(ans):
        ans = i

print(ans)
