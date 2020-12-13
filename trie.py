import os
import json


class TrieNode:

    def __init__(self, char='', ladder_string = "", children=None, hits=None):
        self.char = char  # char in word represented by node
        self.ladder_string = ladder_string # full word represented by traversal through trie
        self.children = children if children is not None else []
        self.hits = hits if hits is not None else []  # file paths for any email that hits on this node

    def child_with_char(self, target_char):
        return next(child for child in self.children if child.char == target_char)

    def child_chars(self):
        return map(lambda node: node.char, self.children)

    def insert(self, key, hit):
        cur_node = self
        for char in key:
            if char not in cur_node.child_chars():
                new_child = TrieNode(char=char, ladder_string=cur_node.ladder_string+char)
                cur_node.children.append(new_child)
                cur_node = new_child
            else:
                cur_node = cur_node.child_with_char(char)

        cur_node.hits.append(hit)

    def find_node(self, key):
        cur_node = self
        for char in key:
            if char not in cur_node.child_chars():
                return None
            else:
                cur_node = cur_node.child_with_char(char)
        return cur_node

    def traverse(self, process_node=lambda x: x):
        cur_node = self

        traversal_stack = [cur_node]
        traversed_nodes = [cur_node]
        processed_nodes = []
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

    def to_string(self): return json.dumps({
        "ladder_string": self.ladder_string,
        "children": [child.ladder_string for child in self.children],
        "hits": self.hits
    })

    def to_dict(self):
        self.traverse()
        pass

    def from_dict(self):
        pass


def trie_create(tokens_dir):
    trie_root = TrieNode()

    for dirpath, dirnames, files in os.walk(tokens_dir):
        print(f'Adding directory to trie: {dirpath}')
        for filename in files:
            if filename == "tokens.txt":
                name = os.path.join(dirpath, filename)
                with open(name, 'r') as tokens_file:
                    tokens_by_email = json.loads(tokens_file.read())
                    for email, tokens in tokens_by_email.items():
                        for token in tokens:
                            trie_root.insert(token, email)

    return trie_root


def trie_encode(root):
    pass
