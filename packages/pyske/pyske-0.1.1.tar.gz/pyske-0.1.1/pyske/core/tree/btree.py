from abc import ABC  # abstract classes library


class BTree(ABC):
    """An abstract class used to represent a Binary Tree

    ...

    Methods
    -------
    is_leaf()
        Indicates if the BTree is a leaf
    get_value()
        Get the value contained in the leaf
    """

    def is_leaf(self):
        """ Indicates if the BTree is a leaf
        """
        return False

    def is_node(self):
        """ Indicates if the BTree is a node
        """
        return False


class Leaf(BTree):
    """A class that overrides BTree used to represent a Leaf

    ...

    Attributes
    ----------
    value
        A value describing the current leaf

    Methods
    -------
    is_leaf()
        Indicates if the BTree is a leaf
    get_value()
        Get the value contained in the current leaf
    set_value(v)
        Set the value contained in the current leaf
    map(kl, kn)
        Applies functions to every leaf and to every node values
    mapt(kl, kn)
        Applies kl to every leaf values the current instance, and kn to every subtrees that are nodes
    reduce(k)
        Reduces a BTree into a single value using k
    uacc(k)
        Makes an upward accumulation of the values in a BTree using k
    dacc(gl, gr, c)
        Makes an downward accumulation of the values in a BTree using gl, gr and c
    zip(t)
        Zip the values contained in a second BTree with the ones in the current instance
    map2(t, f)
        Zip the values contained in a tree with the ones in the current instance using a function
    getchl(c)
        Shift all the values contained in the current instance by the left
    getchr(c)
        Shift all the values contained in the current instance by the right
    size()
        Gives the number of elements in the current instance
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "leaf " + str(self.value)

    def __eq__(self, other):
        if isinstance(other, Leaf):
            return self.get_value() == other.get_value()
        return False

    def is_leaf(self):
        """Indicates if the BTree is a leaf
        """
        return True

    def get_value(self):
        """Get the value contained in the current leaf
        """
        return self.value

    def set_value(self, v):
        """Set the value contained in the current leaf

        Parameters
        ----------
        v
            The new value to set in the current instance
        """
        self.value = v

    def map(self, kl, kn):
        """Applies functions to every leaf and to every node values

        Parameters
        ----------
        kl : callable
            A function to apply to every leaf values of the current instance
        kn : callable
            A function to apply to every node values of the current instance
        """
        return Leaf(kl(self.get_value()))

    def mapt(self, kl, kn):
        """Applies a function to every leaf values the current instance, and another one to every subtrees that are nodes

        Parameters
        ----------
        kl : callable
            The function to apply to every leaf values of the current instance
        kn : callable
            The function to apply to every node subtrees of the current instance
        """
        return Leaf(kl(self.get_value()))

    def reduce(self, k):
        """Reduces a BTree into a single value using a function k

        If the BTree is a leaf, the single reduced value is the value contained in the structure.

        Parameters
        ----------
        k : callable
            The function used to reduce a BTree into a single value
        """
        return self.get_value()

    def uacc(self, k):
        """Makes an upward accumulation of the values in the current instance using a function k

        If the BTree is a leaf, the tree doesn't change.

        Parameters
        ----------
        k : callable
            The function used to reduce a BTree into a single value
        """
        return Leaf(self.get_value())

    def dacc(self, gl, gr, c):
        """Makes an downward accumulation of the values in a BTree using gl, gr and c

        Parameters
        ----------
        gl : callable
            Function to make an accumulation to the left part of a node
        gr : callable
            Function to make an accumulation to the right part of a node
        c
            Accumulator for the downward computation
        """
        return Leaf(c)

    def zip(self, t):
        """Zip the values contained in t with the ones in the current instance

        Precondition
        -------------
        t should be a Leaf instance

        Parameters
        ----------
        t : :obj:`BTree`
            The BTree to zip with the current instance
        """
        assert t.is_leaf(), "A leaf can only be zipped with another leaf"
        return Leaf((self.get_value(), t.get_value()))

    def map2(self, f, t):
        """Zip the values contained in a tree with the ones in the current instance using a function

        Precondition
        -------------
        t should be a Leaf instance

        Parameters
        ----------
        t : :obj:`BTree`
            The BTree to zip with the current instance
        f : callable
            A function to zip values
        """
        assert t.is_leaf(), "A leaf can only be zipped with another leaf"
        return Leaf(f(self.get_value(), t.get_value()))

    def getchl(self, c):
        """Shift all the values contained in the current instance by the left

        Parameters
        ----------
        c
            The default value for elements that doesn't have left children
        """
        return Leaf(c)

    def getchr(self, c):
        """Shift all the values contained in the current instance by the right

        Parameters
        ----------
        c
            The default value for elements that doesn't have right children
        """
        return Leaf(c)

    def size(self):
        """Gives the number of elements in the current instance
        """
        return 1


class Node(BTree):
    """A class that overrides BTree used to represent a Node

    ...

    Attributes
    ----------
    value
        A value describing the current node
    left : :obj:`BTree`
        The left-subtree of the current node
    right : :obj:`BTree`
        The right-subtree of the current node

    Methods
    -------
    is_node()
        Indicates if the BTree is a node
    get_value()
        Get the value contained in the current node
    set_value(v)
        Set the value contained in the current node
    get_left()
        Get the left subtree of the current node
    get_right()
        Get the right subtree of the current node
    map(kl, kn)
        Applies functions to every leaf and to every node values
    mapt(kl, kn)
        Applies kl to every leaf values the current instance, and kn to every subtrees that are nodes
    reduce(k)
        Reduces a BTree into a single value using a function k
    uacc(k)
        Makes an upward accumulation of the values in a BTree using a function k
    dacc(gl, gr, c)
        Makes an downward accumulation of the values in a BTree using gl, gr and c
    zip(t)
        Zip the values contained in t with the ones in the current instance
    map2(t, f)
        Zip the values contained in a tree with the ones in the current instance using a function
    getchl(c)
        Shift all the values contained in the current instance by the left
    getchr(c)
        Shift all the values contained in the current instance by the right
    size()
        Gives the number of elements in the current instance
    """

    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return "node " + str(self.value) + " (" + str(self.left) + ") (" + str(self.right) + ")"

    def __eq__(self, other):
        if isinstance(other, Node):
            return (self.get_value() == other.get_value()) and (self.get_left() == other.get_left()) and (
                        self.get_right() == other.get_right())
        return False

    def is_node(self):
        """Indicates if the BTree is a node
        """
        return True

    def set_value(self, v):
        """Set the value contained in the current node

        Parameters
        ----------
        v
            The new value to set in the current instance
        """
        self.value = v

    def get_value(self):
        """Get the value contained in the current node
        """
        return self.value

    def get_right(self):
        """Get the right subtree of the current node
        """
        return self.right

    def get_left(self):
        """Get the left subtree of the current node
        """
        return self.left

    def map(self, kl, kn):
        """Applies functions to every leaf and to every node values

        Parameters
        ----------
        kl : callable
            A function to apply to every leaf values of the current instance
        kn : callable
            A function to apply to every node values of the current instance
        """
        new_val = kn(self.get_value())
        left = self.get_left().map(kl, kn)
        right = self.get_right().map(kl, kn)
        return Node(new_val, left, right)

    def mapt(self, kl, kn):
        """Applies kl to every leaf values the current instance, and kn to every subtrees that are nodes

        Parameters
        ----------
        kl : callable
            The function to apply to every leaf values of the current instance
        kn : callable
            The function to apply to every node subtrees of the current instance
        """
        new_val = kn(self.get_value(), self.get_left(), self.get_right())
        left = self.get_left().mapt(kl, kn)
        right = self.get_right().mapt(kl, kn)
        return Node(new_val, left, right)

    def reduce(self, k):
        """Reduces a BTree into a single value using a function k

        We use recursive calls of sub-reduction to make a total reduction.

        Parameters
        ----------
        k : callable
            The function used to reduce a BTree into a single value
        """
        left = self.get_left().reduce(k)
        right = self.get_right().reduce(k)
        return k(left, self.get_value(), right)

    def uacc(self, k):
        """Makes an upward accumulation of the values in the current instance using a function k

        Every values in nodes are replaced by the reduced value of the BTree considering the current node as the root.

        Parameters
        ----------
        k : callable
            The function used to reduce a BTree into a single value
        """
        r = self.reduce(k)
        return Node(r, self.get_left().uacc(k), self.get_right().uacc(k))

    def dacc(self, gl, gr, c):
        """Makes an downward accumulation of the values in a BTree using gl, gr and c

        Parameters
        ----------
        gl : callable
            Function to make an accumulation to the left part of a node
        gr : callable
            Function to make an accumulation to the right part of a node
        c
            Accumulator for the downward computation
        """
        b = self.get_value()
        left = self.get_left().dacc(gl, gr, gl(c, b))
        right = self.get_right().dacc(gl, gr, gr(c, b))
        return Node(c, left, right)

    def zip(self, t):
        """Zip the values contained in t with the ones in the current instance

        Precondition
        -------------
        f should be a Node instance

        Parameters
        ----------
        t : :obj:`BTree`
            The BTree to zip with the current instance
        """
        assert t.is_node(), "A node can only be zipped with another node"

        v = (self.get_value(), t.get_value())
        left = self.get_left().zip(t.get_left())
        right = self.get_right().zip(t.get_right())
        return Node(v, left, right)

    def map2(self, f, t):
        """Zip the values contained in a tree with the ones in the current instance using a function

        Precondition
        -------------
        f should be a Node instance

        Parameters
        ----------
        t : :obj:`BTree`
            The BTree to zip with the current instance
        f : callable
            A function to zip values
        """
        assert t.is_node(), "A node can only be zipped with another node"
        v = f(self.get_value(), t.get_value())
        left = self.get_left().map2(f, t.get_left())
        right = self.get_right().map2(f, t.get_right())
        return Node(v, left, right)

    def getchl(self, c):
        """Shift all the values contained in the current instance by the left

        Parameters
        ----------
        c
            The default value for elements that doesn't have left children
        """
        v = self.get_left().get_value()
        left = self.get_left().getchl(c)
        right = self.get_right().getchl(c)
        return Node(v, left, right)

    def getchr(self, c):
        """Shift all the values contained in the current instance by the right

        Parameters
        ----------
        c
            The default value for elements that doesn't have right children
        """
        v = self.get_right().get_value()
        left = self.get_left().getchr(c)
        right = self.get_right().getchr(c)
        return Node(v, left, right)

    def size(self):
        """Gives the number of elements in the current instance
        """
        return 1 + self.get_left().size() + self.get_right().size()
