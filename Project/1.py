#Adapt SmallParsimony to Unrooted Trees
#http://rosalind.info/problems/ba7g/

graph = {}
marked = set()
labels_sets = {}
labels = {}
gene_length = 0
internal_edge = None
score = 0


def parsimony_dfs(node):
    if node in marked:
        return
    marked.add(node)
    if not node.isdecimal():
        labels_sets[node] = [{x} for x in node]
        return labels_sets[node]
    child_labels = []
    for child in graph[node]:
        if child not in marked:
            child_labels.append(parsimony_dfs(child))

    if len(child_labels) == 1:
        labels_sets[node] = child_labels[0]
        return labels_sets[node]
    labels_sets[node] = []
    left_child, right_child = child_labels
    for i in range(gene_length):
        intersection = left_child[i].intersection(right_child[i])
        if len(intersection):
            labels_sets[node].append(intersection)
        else:
            labels_sets[node].append(left_child[i].union(right_child[i]))
    return labels_sets[node]


def set_labels(node, parent):
    global score
    if parent is None:
        labels[node] = ''.join(s.pop() for s in labels_sets[node])
    else:
        temp = []
        for i, s in enumerate(labels_sets[node]):
            if parent[i] in s:
                temp.append(parent[i])
            else:
                # print(parent, i, s)
                temp.append(s.pop())
                score += 1
        labels[node] = ''.join(temp)
    for child in graph[node]:
        if child not in labels.keys():
            set_labels(child, labels[node])


def read_data(file):
    global gene_length, internal_edge
    n = int(file.readline())
    for line in file:
        u, v = line.strip().split('->')
        if not u.isdecimal():
            gene_length = len(u)
        if u.isdecimal() and v.isdecimal():
            internal_edge = (u, v)
        if u not in graph.keys():
            graph[u] = []
        graph[u].append(v)
    # print(graph)


def single_score(parent, child):
    return sum(parent[i] != child[i] for i in range(gene_length))


if __name__ == "__main__":
    read_data(open("input.txt", "r"))
    u, v = internal_edge
    graph["0"] = [u, v]
    graph[u].pop(graph[u].index(v))
    graph[v].pop(graph[v].index(u))

    parsimony_dfs("0")
    set_labels("0", None)

    graph[u].append(v)
    graph[v].append(u)

    print(score)
    for node in graph:
        if node == "0":
            continue
        for child in graph[node]:
            print('{}->{}:{}'.format(labels[node], labels[child], single_score(labels[node], labels[child])))

