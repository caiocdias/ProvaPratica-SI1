import pandas as pd
import matplotlib.pyplot as plt

def load_transactions(filepath):
    df = pd.read_csv(filepath, header=None)
    transactions = df.apply(lambda row: [item for item in row if pd.notna(item)], axis=1).tolist()
    return transactions

class FPTreeNode:
    def __init__(self, item_name, parent_node=None):
        self.name = item_name
        self.count = 1
        self.parent = parent_node
        self.children = {}
        self.link = None

def count_items(transactions):
    item_counts = {}
    for txn in transactions:
        for item in txn:
            item_counts[item] = item_counts.get(item, 0) + 1
    return item_counts

def build_tree(transactions, min_support):
    freq = count_items(transactions)
    freq = {item: sup for item, sup in freq.items() if sup >= min_support}
    if not freq:
        return None, None

    header = {item: [sup, None] for item, sup in freq.items()}
    root = FPTreeNode(None)

    for txn in transactions:
        filtered = [it for it in txn if it in freq]
        filtered.sort(key=lambda it: freq[it], reverse=True)
        current = root
        for it in filtered:
            if it in current.children:
                current.children[it].count += 1
            else:
                node = FPTreeNode(it, current)
                current.children[it] = node
                if header[it][1] is None:
                    header[it][1] = node
                else:
                    hp = header[it][1]
                    while hp.link:
                        hp = hp.link
                    hp.link = node
            current = current.children[it]

    return root, header

def extract_patterns(header, min_support):
    def ascend(node):
        path = []
        while node.parent and node.parent.name is not None:
            node = node.parent
            path.append(node.name)
        return path[::-1]

    patterns = []

    for item, (sup, node) in sorted(header.items(), key=lambda x: x[1][0]):

        patterns.append((frozenset([item]), sup))

        base_paths = []
        while node:
            prefix = ascend(node)
            if prefix:
                base_paths.extend([prefix] * node.count)
            node = node.link

        cond_root, cond_header = build_tree(base_paths, min_support)
        if cond_header:
            for pset, psup in extract_patterns(cond_header, min_support):
                patterns.append((pset.union({item}), psup))

    return patterns

def custom_combinations(items, r):

    items = list(items)
    n = len(items)
    result = []

    def recurse(start, comb):
        if len(comb) == r:
            result.append(tuple(comb))
            return
        for i in range(start, n):
            recurse(i+1, comb + [items[i]])

    recurse(0, [])
    return result

def generate_rules(frequent_itemsets, min_confidence):

    freq_dict = {fs: sup for fs, sup in frequent_itemsets}
    rules = []
    for itemset, sup in frequent_itemsets:
        if len(itemset) < 2:
            continue
        for r in range(1, len(itemset)):
            for ant in custom_combinations(itemset, r):
                ant = frozenset(ant)
                cons = itemset - ant
                if freq_dict.get(ant, 0) > 0:
                    conf = sup / freq_dict[ant]
                    if conf >= min_confidence:
                        rules.append((ant, cons, sup, conf))
    return rules

def plot_graph(data, title, xlabel):

    labels, values = zip(*data)

    plt.figure(figsize=(12, 6))
    bars = plt.barh(labels[::-1], values[::-1])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.tight_layout()

    for bar in bars:
        w = bar.get_width()
        plt.text(w + max(values)*0.01, bar.get_y() + bar.get_height()/2,
                 str(int(w)), va='center')

    plt.show()
    plt.close()

def questao1(file_path, min_support=300, min_confidence=0.3):
    txns = load_transactions(file_path)
    root, header = build_tree(txns, min_support)
    freq_itemsets = extract_patterns(header, min_support) if header else []
    rules_list = generate_rules(freq_itemsets, min_confidence)

    indiv = sorted([(next(iter(fs)), sup) for fs, sup in freq_itemsets if len(fs) == 1],
                   key=lambda x: -x[1])
    multi = sorted([(tuple(fs), sup) for fs, sup in freq_itemsets if len(fs) > 1],
                   key=lambda x: -x[1])

    plot_graph(indiv[:15], f"Itens Mais Frequentes (sup ≥ {min_support})", "Suporte")
    plot_graph([(" & ".join(x), sup) for x, sup in multi[:15]],
               f"Conjuntos Frequentes (sup ≥ {min_support})", "Suporte")
    plot_graph([(" → ".join(map(str,a)) + f" | sup {sup:.0f}; conf {conf:.2f}", conf)
                for a, b, sup, conf in rules_list[:15]],
               "Regras de Associação (conf ≥ {min_confidence})", "Confiança")

    return indiv, multi, rules_list