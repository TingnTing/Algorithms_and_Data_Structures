""" AVL Tree implemented on top of the standard BST. """

__author__ = 'Alexey Ignatiev'
__docformat__ = 'reStructuredText'

from bst import BinarySearchTree
from typing import TypeVar, Generic
from node import AVLTreeNode

K = TypeVar('K')
I = TypeVar('I')


class AVLTree(BinarySearchTree, Generic[K, I]):
    """ Self-balancing binary search tree using rebalancing by sub-tree
        rotations of Adelson-Velsky and Landis (AVL).
    """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        BinarySearchTree.__init__(self)

    def get_height(self, current: AVLTreeNode) -> int:
        """
            Get the height of a node. Return current. Height if current is
            not None. Otherwise, return 0.
            :complexity: O(1)
        """
        if current is not None:
            return current.height
        return 0

    def get_weight(self, current: AVLTreeNode) -> int:
        """
            Get the weight of a node. Return current. Weight if current is
            not None. Otherwise, return 0.
            :complexity: O(1)
        """
        if current is not None:
            return current.weight
        return 0

    def get_balance(self, current: AVLTreeNode) -> int:
        """
            Compute the balance factor for the current sub-tree as the value
            (right.height - left.height). If current is None, return 0.
            :complexity: O(1)
        """

        if current is None:
            return 0
        return self.get_height(current.right) - self.get_height(current.left)

    def insert_aux(self, current: AVLTreeNode, key: K, item: I) -> AVLTreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert
            it. After insertion, performs sub-tree rotation whenever it becomes
            unbalanced.
            returns the new root of the subtree.
        """
        if current is None:
            current = AVLTreeNode(key, item)
            self.length += 1  # self.length added in insert_aux already
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:
            # key == current.key:
            # it'll raise ValueError anyway
            current.right = self.insert_aux(current.right, key, item)

        current.height_update()  # always update height and weight before balancing
        current.weight_update()
        current = self.rebalance(current)
        return current

    def delete_aux(self, current: AVLTreeNode, key: K) -> AVLTreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete. After deletion,
            performs sub-tree rotation whenever it becomes unbalanced.
            returns the new root of the subtree.
        """
        if current is None:
            raise ValueError("Empty tree, can't delete node")
        elif key < current.key:
            current.left = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:
            # actual key found to do deletion  (key == current.key)
            if self.is_leaf(current):  # if current is a leaf, no child to return (both left right is None)
                self.length -= 1
                return None
            elif current.left is None:  # there exist a right node
                self.length -= 1
                return current.right
            elif current.right is None: # there exist a left node
                self.length -= 1
                return current.left

            # Find the successor to replace
            successor = self.get_successor(current)
            current.key = successor.key
            current.item = successor.item
            current.right = self.delete_aux(current.right, successor.key)

        current.height_update()  # always update height and weight before balancing
        current.weight_update()
        current = self.rebalance(current)
        return current

    def left_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform left rotation of the sub-tree.
            Right child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                 current                                       child
                /       \                                      /   \
            l-tree     child           -------->        current     r-tree
                      /     \                           /     \
                 center     r-tree                 l-tree     center

            :complexity: O(1)
        """
        child = current.right
        center = current.right.left

        current.right = center
        current.height_update()
        current.weight_update()

        child.left = current
        child.height_update()
        child.weight_update()
        return child

    def right_rotate(self, current: AVLTreeNode) -> AVLTreeNode:
        """
            Perform right rotation of the sub-tree.
            Left child of the current node, i.e. of the root of the target
            sub-tree, should become the new root of the sub-tree.
            returns the new root of the subtree.
            Example:

                       current                                child
                      /       \                              /     \
                  child       r-tree     --------->     l-tree     current
                 /     \                                           /     \
            l-tree     center                                 center     r-tree

            :complexity: O(1)
        """
        child = current.left
        center = current.left.right

        current.left = center
        current.height_update()
        current.weight_update()

        child.right = current
        child.height_update()
        child.weight_update()
        return child

    def rebalance(self, current: AVLTreeNode) -> AVLTreeNode:
        """ Compute the balance of the current node.
            Do rebalancing of the sub-tree of this node if necessary.
            Rebalancing should be done either by:
            - one left rotate
            - one right rotate
            - a combination of left + right rotate
            - a combination of right + left rotate
            returns the new root of the subtree.
        """
        if self.get_balance(current) >= 2:
            child = current.right
            if self.get_height(child.left) > self.get_height(child.right):
                current.right = self.right_rotate(child)
            return self.left_rotate(current)

        if self.get_balance(current) <= -2:
            child = current.left
            if self.get_height(child.right) > self.get_height(child.left):
                current.left = self.left_rotate(child)
            return self.right_rotate(current)

        return current

    def kth_largest(self, k: int) -> AVLTreeNode:
        """
            Returns the kth largest element in the tree. k = 1 would return the largest.
            :pre: must be 1 < k < num of available potions
            :complexity: O(log(n)) , where n is length of tree
        """
        # Exception for k
        if k < 1:
            raise IndexError("Can't be less than 1")
        elif k > self.length:
            raise IndexError("Can't be more than the number of available potions")

        current = self.root
        iterator = self.get_weight(current.right) + 1

        if iterator == k:  # base case is when root is the only node in tree
            return current
        else:
            return self.kth_largest_aux(current, k, iterator)

    def kth_largest_aux(self,current: AVLTreeNode, k: int, iterator: int) -> AVLTreeNode:
        if current is None:
            raise IndexError('Empty tree')

        left = current.left
        right = current.right

        if iterator < k:  # if iterators node is smaller than k
            iterator += 1 + self.get_weight(left.right)
            return self.kth_largest_aux(left, k, iterator)  # iterate to left node
        elif iterator > k:  # if iterators node is larger than k
            iterator -= 1 + self.get_weight(right.left)
            return self.kth_largest_aux(right, k, iterator)  # iterate to right node
        else:  # iterators node == k
            return current

