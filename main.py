import preprocess
import trie
import search
import os
import json

if __name__ == "__main__":
    trie_out_dir = "./trie_out/"
    query = "C"

    # server side - serialized tries are loaded on device per first character
    # preprocess.preprocess()

    # client side
    # print(json.dumps(mem_trie.serialize(), indent=4))
    # if os.path.exists(trie_out_file):
    #     with open(trie_out_file, 'r') as trie_file:
    #         trie_dict = json.loads(trie_file.read())
    #         mem_trie = trie.TrieNode.deserialize(trie_dict)
    #
    # in_mem = json.dumps(mem_trie.serialize(), indent=4)
    # print(in_mem)

    print(f"Searching for {query}")

    path = os.path.join(trie_out_dir, query[0])
    if os.path.exists(path):
        mem_trie = trie.trie_create(path)
        query_results = search.search(query, mem_trie)
        for result in query_results:
            print(json.dumps(result.serialize(), indent=4))
    else:
        print("No results")
