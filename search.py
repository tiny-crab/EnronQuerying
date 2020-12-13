def search(term, trie):
    term_hit = trie.find_node(term)
    if term_hit:
        results = term_hit.traverse(process_node=lambda node, agg: agg.append(node) if node.hits else None)
        results.sort(key=lambda node: node.ladder_string)
        return results
