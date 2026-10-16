from __future__ import annotations

from dataclasses import dataclass
from typing import overload


@dataclass
class Node:
    key: int
    left: Node | None = None
    right: Node | None = None
    height: int = 1


class AVL:
    root: Node | None

    def __init__(self) -> None:
        self.root = None

    def left_rotation(self, key: int, node: Node | None) -> Node | None:
        if node is None:
            return None
        if node.key == key:
            if node.right is None:
                return node
            new_node = node.right
            new_left_node = node
            new_left_node.right = node.right.left
            new_left_node.height = 1 + max(
                self.height(new_left_node.left),
                self.height(new_left_node.right),
            )
            new_node.left = new_left_node
            new_node.height = 1 + max(
                self.height(new_node.left), self.height(new_node.right),
            )
            return new_node
        elif key < node.key:
            node.left = self.left_rotation(key, node.left)
        else:
            node.right = self.left_rotation(key, node.right)
        node.height = max(self.height(node.left), self.height(node.right)) + 1
        return node

    def right_rotation(self, key: int, node: Node | None) -> Node | None:
        if node is None:
            return None
        if node.key == key:
            if node.left is None:
                return node
            new_node = node.left
            new_right_node = node
            new_right_node.left = node.left.right
            new_right_node.height = 1 + max(
                self.height(new_right_node.left),
                self.height(new_right_node.right),
            )
            new_node.right = new_right_node
            new_node.height = 1 + max(
                self.height(new_node.left), self.height(new_node.right),
            )
            return new_node
        elif key < node.key:
            node.left = self.right_rotation(key, node.left)
        else:
            node.right = self.right_rotation(key, node.right)
        node.height = max(self.height(node.left), self.height(node.right)) + 1
        return node

    def rebalance(self, node: Node) -> Node | None:
        left = self.height(node.left)
        right = self.height(node.right)
        balance = right - left
        if balance == 2:
            assert node.right is not None
            right_balance = (
                self.height(node.right.right) - self.height(node.right.left)
            )
            if right_balance >= 0:
                return self.left_rotation(node.key, node)
            else:
                node.right = self.right_rotation(node.right.key, node.right)
            return self.left_rotation(node.key, node)
        elif balance == -2:
            assert node.left is not None
            left_balance = (
                self.height(node.left.right) - self.height(node.left.left)
            )
            if left_balance <= 0:
                return self.right_rotation(node.key, node)
            else:
                node.left = self.left_rotation(node.left.key, node.left)
            return self.right_rotation(node.key, node)
        else:
            return node

    def add(self, key: int, node: Node | None) -> Node | None:
        if node is None:
            return Node(key)
        if key < node.key:
            node.left = self.add(key, node.left)
        elif key > node.key:
            node.right = self.add(key, node.right)
        else:
            return node

        node.height = 1 + max(self.height(node.left), self.height(node.right))

        return self.rebalance(node)

    def delete(self, key: int, node: Node | None) -> Node | None:
        if node is None:
            return None
        if node.key == key:
            if node.left is None and node.right is None:
                return None
            elif node.left is not None and node.right is not None:
                min_node = self.find_min(node.right)
                assert min_node is not None
                node.key = min_node.key
                node.right = self.delete(min_node.key, node.right)
            else:
                if node.left is not None:
                    node = node.left
                else:
                    assert node.right is not None
                    node = node.right
        elif key < node.key:
            node.left = self.delete(key, node.left)
        else:
            node.right = self.delete(key, node.right)
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        return self.rebalance(node)

    def find_min(self, node: Node | None) -> Node | None:
        if node is None:
            return None
        curr_node = node
        while curr_node.left is not None:
            curr_node = curr_node.left
        return curr_node

    def exists(self, key: int, curr_node: Node | None) -> bool:
        if curr_node is None:
            return False
        if key < curr_node.key:
            return self.exists(key, curr_node.left)
        elif key > curr_node.key:
            return self.exists(key, curr_node.right)
        else:
            return True

    def find(
        self, key: int, node: Node | None, direction: str = "next",
    ) -> Node | None:
        if node is None:
            return None
        if key < node.key:
            if direction == "prev":
                return self.find(key, node.left, direction)
            elif direction == "next":
                val = self.find(key, node.left, direction)
                if val is not None:
                    return val
                else:
                    return node
            else:
                return None
        elif key > node.key:
            if direction == "next":
                return self.find(key, node.right, direction)
            elif direction == "prev":
                val = self.find(key, node.right, direction)
                if val is not None:
                    return val
                else:
                    return node
            else:
                return None
        else:
            return node

    def height(self, node: Node | None) -> int:
        if node is None:
            return 0
        else:
            return node.height

    def get_root_key(self) -> int | str:
        if self.root is None:
            return "Empty"
        else:
            return self.root.key

    def print(self) -> None:
        if self.root is None:
            print("Empty")
            return
        stack: list[Node] = []
        output: list[int] = []
        stack.append(self.root)
        while stack:
            curr_node = stack.pop()
            output.append(curr_node.key)
            if curr_node.right is not None:
                stack.append(curr_node.right)
            if curr_node.left is not None:
                stack.append(curr_node.left)
        print(*output)


def main() -> None:
    command_count = int(input())
    tree = AVL()
    for _ in range(command_count):
        command = input().split()
        command_type = command[0]

        if command_type == "add":
            tree.root = tree.add(int(command[1]), tree.root)
        elif command_type == "del":
            tree.root = tree.delete(int(command[1]), tree.root)
        elif command_type == "exists":
            response = tree.exists(int(command[1]), tree.root)
            if response:
                print("YES")
            else:
                print("NO")
        elif command_type == "next":
            res = tree.find(int(command[1]), tree.root, "next")
            print(res.key if res is not None else None)
        elif command_type == "prev":
            res = tree.find(int(command[1]), tree.root, "prev")
            print(res.key if res is not None else None)
        elif command_type == "height":
            print(tree.height(tree.root))
        elif command_type == "root":
            print(tree.get_root_key())
        elif command_type == "print":
            tree.print()


if __name__ == "__main__":
    main()
