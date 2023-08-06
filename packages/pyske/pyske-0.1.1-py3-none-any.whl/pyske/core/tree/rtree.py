from pyske.core.support.errors import ConstructorError
from pyske.core.list.slist import SList
from pyske.core.tree.btree import Node, Leaf, BTree


class RNode:
    """
    A class used to represent a Rose Tree (a tree with an arbitrary shape)

    ...

    Methods
    -------
    b2r(bt)
        Create a RNode instance from a BTree
    get_children()
        Get the children of the current RNode
    add_children(c)
        Add a children to the ones of the current RNode
    is_leaf()
        Indicates if the current RNode has no children, and then can be considered as a leaf
    is_node()
        Indicates if the current RNode has children, and then can be considered as a node
    get_value()
        Get the value of the current RNode
    set_value(v)
        Set a new value for the current RNode
    map(f)
        Applies a function to every values contained in the current instance
    reduce(f, g)
        Reduce the current instance into a single value using two operators
    uacc(f, g)
        Makes an upward accumulation of the values in a the current instance using two operators
    dacc(f, unit_f)
        Makes an downward accumulation of the values in a the current instance
    zip(rt)
        Zip the values contained in a second RTree with the ones in the current instance
    map2(rt, f)
        Zip the values contained in a second RTree with the ones in the current instance using a function
    racc(f, unit_f)
        Makes a rightward accumulation of the values in the current instance
    lacc(f, unit_f)
        Makes a leftward accumulation of the values in the current instance
    r2b()
        Get a BTree from the current instance
    """

    def __init__(self, value, ts=None):
        if isinstance(value, BTree):
            if value == Leaf(None):
                raise ConstructorError("A RTree cannot be constructed from a single Leaf that contains None")
            # Create a RTree from a BTree
            bt = value
            rt = RNode.b2r(bt)
            self.value = rt.get_value()
            self.children = rt.get_children()
        else:
            self.value = value
            if ts is None:
                self.children = SList([])
            else:
                self.children = SList(ts)

    @staticmethod
    def b2r(bt):
        """
        Create a RNode instance from a BTree
        """
        def aux(btree):
            if btree.is_leaf():
                val = btree.get_value()
                if val is None:
                    return SList()
                else:
                    return SList([RNode(val)])
            else:
                n = btree.get_value()
                left = btree.get_left()
                right = btree.get_right()
                res_l = aux(left)
                res_r = aux(right)
                res_head = RNode(n, res_l)
                res_r.insert(0, res_head)
                return res_r

        return aux(bt).head()

    def __str__(self):
        res = "rnode " + str(self.value) + "["
        ch = self.get_children()
        for i in range(0, self.get_children().length()):
            if i == ch.length() - 1:
                res = res + str(ch[i])
            else:
                res = res + str(ch[i]) + ", "
        return res + "]"

    def __eq__(self, other):
        if isinstance(other, RNode):
            ch1 = self.get_children()
            ch2 = other.get_children()
            if ch1.length() != ch2.length():
                return False
            for i in range(0, ch1.length()):
                if ch1[i] != ch2[i]:
                    return False
            return self.get_value() == other.get_value()
        return False

    def is_leaf(self):
        """Indicates if the current RNode has no children, and then can be considered as a leaf
        """
        return len(self.children) == 0

    def is_node(self):
        """Indicates if the current RNode has children, and then can be considered as a node
        """
        return len(self.children) != 0

    def get_children(self):
        """Get the children of the current RNode
        """
        return self.children

    def add_children(self, c):
        """Add a children to the ones of the current RNode

        Parameters
        ----------
        c
            The children to add
        """
        self.children.append(c)

    def get_value(self):
        """Get the value of the current RNode
        """
        return self.value

    def set_value(self, v):
        """Set a new value for the current RNode

        Parameters
        ----------
        v
            The new value to set
        """
        self.value = v

    def map(self, f):
        """Applies a function to every values contained in the current instance

        Parameters
        ----------
        f : callable
            The function to apply to every values of the current instance
        """
        v = f(self.get_value())
        # To each element of the list of children, we apply the RNode.map function
        ch = self.children.map(lambda x: x.map(f))
        return RNode(v, ch)

    def reduce(self, f, g):
        """Reduce the current instance into a single value using two operators

        Parameters
        ----------
        f : callable
            A binary operator to combine all sub reduction of the children of the current instance
            into an intermediate reduction
        g : callable
            A binary operator to combine the value of the current instance with the intermediate reduction
        """
        if self.children.empty():
            return self.get_value()
        # We calculate the reduction of each childen
        reductions = self.children.map(lambda x: x.reduce(f, g))
        # We combine every sub reductions using g
        red = reductions[0]
        for i in range(1, reductions.length()):
            red = g(red, reductions[i])
        # The final reduction is the result of the combination of sub reductions and the value of the current instance
        return f(self.get_value(), red)

    def uacc(self, f, g):
        """Makes an upward accumulation of the values in a the current instance using two operators

        Parameters
        ----------
        f : callable
            A binary operator to combine all top values from the accumulation within the children of the current
            instance into an intermediate accumulation
        g : callable
            A binary operator to combine the value of the current instance with the intermediate accumulation
        """
        v = self.reduce(f, g)
        ch = self.children.map(lambda x: x.uacc(f, g))
        return RNode(v, ch)

    def dacc(self, f, unit_f):
        """Makes an downward accumulation of the values in a the current instance

        Parameters
        ----------
        f : callable
            A function to accumulate the value of the current instance with the current accumulator
        unit_f
            A value such as, forall x, f(x, unit_f) = x
        """

        def dacc2(t, fct, c):
            # Auxiliary function to make an accumulation with an arbitrary accumulator
            return RNode(c, t.children.map(lambda x: dacc2(x, fct, fct(c, t.get_value()))))

        # Since the accumulator changes at each iteration, we need to use a changing parameter, not defined in dacc.
        # Use of an auxiliary function, with as a first accumulator, unit_f
        return dacc2(self, f, unit_f)

    def zip(self, rt):
        """Zip the values contained in a second RTree with the ones in the current instance

        Precondition
        -------------
        The lengths of self.children and rt.children should be equal

        Parameters
        ----------
        rt : :obj:`RTree`
            The RTree to zip with the current instance
        """
        ch1 = self.get_children()
        ch2 = rt.get_children()
        assert ch1.length() == ch2.length(), "The rose trees cannot be zipped (not the same shape)"
        ch = SList([])
        for i in range(0, ch1.length()):
            ch.append(ch1[i].zip(ch2))
        v = (self.get_value(), rt.get_value())
        return RNode(v, ch)

    def map2(self, rt, f):
        """Zip the values contained in a second RTree with the ones in the current instance using a function

        Precondition
        -------------
        The lengths of self.children and rt.children should be equal

        Parameters
        ----------
        rt : :obj:`RTree`
            The RTree to zip with the current instance
        f : callable
            A function to zip values
        """
        ch1 = self.get_children()
        ch2 = rt.get_children()
        assert ch1.length() == ch2.length(), "The rose trees cannot be zipped (not the same shape)"
        ch = SList([])
        for i in range(0, ch1.length()):
            ch.append(ch1[i].map2(ch2, f))
        v = f(self.get_value(), rt.get_value())
        return RNode(v, ch)

    def racc(self, f, unit_f):
        """Makes a rightward accumulation of the values in the current instance

        rAcc (+) (RNode a ts)
            = let rs = scanl (+) [root ts[i] | i in [1 .. #ts]]
            in  RNode unit_(+) [setroot (rAcc (+) ts[i]) r[i] | i in [1 .. #ts]]

        Parameters
        ----------
        f : callable
            A function to accumulate the value of the current instance with the current accumulator
        unit_f
            A value such as, forall x, f(x, unit_f) = x
        """

        rv = self.get_children().map(lambda x: x.get_value())
        rs = rv.scanl(f, unit_f)
        ch = SList()
        ch0 = self.get_children()
        for i in range(0, ch0.length()):
            c = ch0[i]
            cs = c.racc(f, unit_f)
            cs.set_value(rs[i])
            ch.append(cs)
        return RNode(unit_f, ch)

    def lacc(self, f, unit_f):
        """Makes a leftward accumulation of the values in the current instance

        lAcc (+) (RNode a ts)
            = let rs = scanp (+) [root ts[i] | i in [1 .. #ts]]
            in  RNode unit_(+) [setroot (lAcc (+) ts[i]) r[i] | i in [1 .. #ts]]

        Parameters
        ----------
        f : callable
            A function to accumulate the value of the current instance with the current accumulator
        unit_f
            A value such as, forall x, f(x, unit_f) = x
        """
        rv = self.get_children().map(lambda x: x.get_value())
        rs = rv.scanp(f, unit_f)
        ch = SList()
        ch0 = self.get_children()
        for i in range(0, ch0.length()):
            c = ch0[i]
            cs = c.lacc(f, unit_f)
            cs.set_value(rs[i])
            ch.append(cs)
        return RNode(unit_f, ch)

    def r2b(self):
        """Get a BTree from the current instance
        """
        def r2b1(t, ss):
            a = t.get_value()
            left = r2b2(t.get_children())
            right = r2b2(ss)
            return Node(a, left, right)

        def r2b2(ts):
            if ts.empty():
                return Leaf(None)
            else:
                h = ts.head()
                t = ts.tail()
                return r2b1(h, t)

        return r2b1(self, SList())
