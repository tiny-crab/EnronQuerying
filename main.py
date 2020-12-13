import preprocess
import trie
import search
import os
import json
import sys

if __name__ == "__main__":
    trie_out_dir = "./trie_out/"
    query = sys.argv[1] if sys.argv[1] is not None else "Can"

    # server side - serialized tries are loaded on device per first character
    # preprocess.preprocess()

    # client side
    print(f"Searching for {query}")

    path = os.path.join(trie_out_dir, query[0])
    if os.path.exists(path):
        mem_trie = trie.trie_create(path)
        # entry point for mobile app "search" text field
        query_results = search.search(query, mem_trie)
        for result in query_results:
            print(json.dumps(result.serialize(), indent=4))
    else:
        print("No results")
