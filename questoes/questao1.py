import pandas as pd

def questao1(file_path, min_support=300, min_confidence=0.3):
    df = pd.read_csv(file_path, header=None)
    transactions = (
        df.stack()
          .groupby(level=0)
          .apply(list)
          .tolist()
    )

    freq = {}
    for trans in transactions:
        for item in trans:
            freq[item] = freq.get(item, 0) + 1
    freq = {item: cnt for item, cnt in freq.items() if cnt >= min_support}

    top_items = pd.DataFrame(
        sorted(freq.items(), key=lambda x: x[1], reverse=True),
        columns=['item', 'count']
    )

    class FPNode:
        def __init__(self, name, count, parent):
            self.name = name
            self.count = count
            self.parent = parent
            self.children = {}
            self.link = None

    header = {item: [cnt, None] for item, cnt in freq.items()}
    root = FPNode(None, 1, None)

    def insert_tree(items, node, hdr):
        if not items:
            return
        first, *rest = items
        if first in node.children:
            node.children[first].count += 1
            child = node.children[first]
        else:
            child = FPNode(first, 1, node)
            node.children[first] = child
            # Atualiza links no header
            if hdr[first][1] is None:
                hdr[first][1] = child
            else:
                current = hdr[first][1]
                while current.link:
                    current = current.link
                current.link = child
        insert_tree(rest, child, hdr)

    for trans in transactions:
        valid = [itm for itm in trans if itm in freq]
        valid.sort(key=lambda x: freq[x], reverse=True)
        insert_tree(valid, root, header)

    patterns = []

    def ascend(node):
        path = []
        while node and node.parent and node.parent.name:
            node = node.parent
            path.append(node.name)
        return path

    def find_prefix_paths(base):
        paths = {}
        node = header[base][1]
        while node:
            p = ascend(node)
            if p:
                paths[tuple(p)] = paths.get(tuple(p), 0) + node.count
            node = node.link
        return paths

    def mine(prefix, hdr):
        for item, (support, _) in sorted(hdr.items(), key=lambda x: x[1][0]):
            new_pref = prefix + [item]
            patterns.append((new_pref, support))
            cond_paths = find_prefix_paths(item)
            cond_txns = []
            for p, cnt in cond_paths.items():
                for _ in range(cnt):
                    cond_txns.append(list(p))
            new_freq = {}
            for txn in cond_txns:
                for itm in txn:
                    new_freq[itm] = new_freq.get(itm, 0) + 1
            new_freq = {itm: c for itm, c in new_freq.items() if c >= min_support}
            if not new_freq:
                continue
            new_hdr = {itm: [c, None] for itm, c in new_freq.items()}
            new_root = FPNode(None, 1, None)
            for txn in cond_txns:
                valid = [itm for itm in txn if itm in new_freq]
                valid.sort(key=lambda x: new_freq[x], reverse=True)
                insert_tree(valid, new_root, new_hdr)
            mine(new_pref, new_hdr)

    mine([], header)

    freq_itemsets = pd.DataFrame([
        {'itemset': p, 'support': s} for p, s in patterns
    ])

    def powerset(items):
        res = [[]]
        for itm in items:
            res += [r + [itm] for r in res]
        return res

    support_dict = {tuple(p): s for p, s in patterns}
    rules = []
    for p, sup in patterns:
        if len(p) > 1:
            for ant in powerset(p):
                if 0 < len(ant) < len(p):
                    cons = [i for i in p if i not in ant]
                    conf = sup / support_dict[tuple(ant)]
                    if conf >= min_confidence:
                        rules.append({
                            'antecedent': ant,
                            'consequent': cons,
                            'support': sup,
                            'confidence': conf
                        })
    rules_df = pd.DataFrame(rules)

    return top_items, freq_itemsets, rules_df