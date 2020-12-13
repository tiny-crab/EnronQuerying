import os
import json


class TrieNode:

    def __init__(self, char='', ladder_string="", children=None, hits=None):
        self.char = char  # char in word represented by node
        self.ladder_string = ladder_string  # full word represented by traversal through trie
        self.children = children if children is not None else []
        self.hits = hits if hits is not None else []  # file paths for any email that hits on this node

    def child_with_char(self, target_char):
        return next(child for child in self.children if child.char == target_char)

    def child_chars(self):
        return map(lambda node: node.char, self.children)

    def insert(self, key, hits):
        cur_node = self
        for char in key:
            if char not in cur_node.child_chars():
                new_child = TrieNode(char=char, ladder_string=cur_node.ladder_string+char)
                new_child.parent = cur_node
                cur_node.children.append(new_child)
                cur_node = new_child
            else:
                cur_node = cur_node.child_with_char(char)

        cur_node.hits.extend(hits)

    def find_node(self, key):
        cur_node = self
        for char in key:
            if char not in cur_node.child_chars():
                return None
            else:
                cur_node = cur_node.child_with_char(char)
        return cur_node

    def traverse(self,
                 agg_init=None,
                 process_node=lambda node, agg: agg.append(node)):
        cur_node = self

        traversal_stack = [cur_node]
        traversed_nodes = [cur_node]
        processed_nodes = agg_init if agg_init is not None else []
        process_node(cur_node, processed_nodes)

        while traversal_stack:
            visited_all_children = True
            if not traversal_stack[-1].children:
                traversal_stack.pop()
            else:
                cur_node = traversal_stack[-1]
            for child in cur_node.children:
                if child not in traversed_nodes:
                    visited_all_children = False
                    traversal_stack.append(child)
                    traversed_nodes.append(child)
                    process_node(child, processed_nodes)
                    break
            if visited_all_children and traversal_stack:
                traversal_stack.pop()

        return processed_nodes

    def serialize(self):
        def agg_on_dict(node, agg):
            if not node.children and node.ladder_string not in agg.keys():
                agg[node.ladder_string] = node.hits

        return self.traverse(
            agg_init={},
            process_node=agg_on_dict
        )


def trie_create(tokens_dir):
    trie_root = TrieNode()

    for dirpath, dirnames, files in os.walk(tokens_dir):
        print(f'Adding directory to trie: {dirpath}')
        for filename in files:
            if filename == "trie.txt":
                name = os.path.join(dirpath, filename)
                with open(name, 'r') as tokens_file:
                    email_by_tokens = json.loads(tokens_file.read())
                    for token, emails in email_by_tokens.items():
                        trie_root.insert(token, emails)

    return trie_root
