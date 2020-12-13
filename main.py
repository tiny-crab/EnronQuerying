
import trie
import search

if __name__ == "__main__":
    trie_root = trie.trie_create("./split_tokens/sample_data/")

    query_results = search.search("Can", trie_root)
    [print(node.to_string()) for node in query_results]
