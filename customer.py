class Customer:
    """A Customer.

    This class represents a customer in the simulation. Each customer will
    enter the simulation at _entry_time, will wait at most _patience turns.
    The restaurant need _prepare_time turns to prepare this customer order,
    and will receive _profit if can serve this customer on time.
    
    Your main task is to implement the remaining methods.
    """

    # === Private Attributes ===
    # @:type _id: int
    #    a unique integer that identifies each customer
    # @:type _entry_time int
    #    the specific turn when customer has entered the simulation
    # @:type _patience: int
    #    Maximum amount of turns a customer will wait for their order
    # @:type _prepare_time: int
    #    The number of turns required to complete an order
    # @:type _profit: float
    #    Amount of profit received from the customer's order

    def __init__(self, definition):
        """
        Create a new Customer self, given a definition from a line
        from a scenario file.

        :param definition: The specific line in a file that carries information
        about a customer.
        :type definition: str
        :rtype: None

        """
        # definition refers to the specific line of code which is read from
        # the file. it looks a little bit like '1\t23215\t13\t4\t8'
        # we need to split this into a list by removing the tab.

        c_lst = definition.split()
        self._entry_time = int(c_lst[0])
        self._id = int(c_lst[1])
        self._profit = float(c_lst[2])
        self._prepare_time = int(c_lst[3])
        self._patience = int(c_lst[4])

    def id(self):
        """
        return the id value of the customer.

        :rtype: int

        >>> c = Customer('1\t23215\t13\t4\t8')
        >>> c.id()
        23215

        """
        return self._id

    def entry_turn(self):
        """
        return the entry turn of the customer.

        :rtype: int

        >>> c = Customer('1\t23215\t13\t4\t8')
        >>> c.entry_turn()
        1

        """
        return self._entry_time

    def patience(self):
        """
        return the patience (max amount of time the customer is willing to wait

        :rtype: int

        >>> c = Customer('1\t23215\t13\t4\t8')
        >>> c.patience()
        8

        """
        return self._patience

    def profit(self):
        """
        return the profit a customer will give from their order.

        :rtype: float

        >>> c = Customer('1\t23215\t13\t4\t8')
        >>> c.profit()
        13.0

        """
        return self._profit

    def prep(self):
        """
        return the amount of prepare time a customer will need to wait for their
        order.

        :rtype: int

        >>> c = Customer('1\t23215\t13\t4\t8')
        >>> c.prep()
        4

        """
        return self._prepare_time

    def __repr__(self):
        """
        Represent Customer(self) as a string that can
        be evaluated to produce an equivalent Customer.

        @rtype: str

        >>> c = Customer('1\t23215\t13\t4\t8')
        >>> c
        23215

        """
        return str(self._id)

    def __str__(self):
        """
        Return a user-friendly string representation of Customer self.

        @:rtype: str

        >>> c = Customer('1\t23215\t13\t4\t8')
        >>> print(c)
        Id: 23215, Entry: 1, Profit: 13.0, Prep: 4, Patience: 8
        """
        return 'Id: {}, Entry: {}, Profit: {}, Prep: {}, Patience: {}' \
            .format(self.id(), self._entry_time, self.profit(), self.prep(),
                    self._patience)

    def __eq__(self, other):
        """
        determine whether or not Customer self is equivalent to Other

        @:type other: Any
            Any object to compare with self
        @:rtype: bool

        >>> c1 = Customer('1\t23215\t13\t4\t8')
        >>> c2 = Customer('3\t22222\t11\t12\t13')
        >>> c3 = Customer('1\t23215\t13\t4\t8')
        >>> c1 == c2
        False
        >>> c1 == c3
        True

        """
        return (type(self) == type(other)) and \
               (self.id(), self.entry_turn(), self.profit(), self.prep(),
                self.patience()) == \
               (other.id(), other.entry_turn(), other.profit(), other.prep(),
                other.patience())


if __name__ == '__main__':
    import doctest
    doctest.testmod()
