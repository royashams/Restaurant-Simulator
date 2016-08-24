from customer import Customer

class Restaurant(object):
    """A Restaurant.

    This class represents a restaurant in the simulation. This is the base
    class for different restaurant approaches. The main purpose of this
    class to define common interfaces for different approaches. If there
    are common tasks for all approaches that did not depend on a specific
    management style, they should be implemented here. Otherwise, they should
    be implemented in the subclasses.

    This class is abstract; subclasses must implement add_customer and
    process_turn functions.

    You may, if you wish, change the API of this class to add
    extra public methods or attributes. Make sure that anything
    you add makes sense for ALL approaches, and not just a particular
    approach.

    """

    # === Private Attributes ===
    # :type _p_queue: list[Customer]
    #   is a customized priority queue based on each approach.
    # :type _total: int
    #   describes the total number of customers served
    # :type _r_profit: float
    #   describes total profit the restaurant makes.
    # :type _next_action: int
    #   describes the next turn where a new customer's order is chosen.

    def __init__(self):
        """Initialize a restaurant.
        @:rtype: None
        """
        self._p_queue = []
        self._total = 0
        self._r_profit = 0.0
        self._next_action = 1

    # There are some aspects of the doctest that call on _p_queue, however
    # it is not good convention to access a private attribute. Instead, we can
    # make a getter, a setter, and convert it into a property, and call on the
    # property in the doctest examples.

    def _get_p_queue(self):
        # """
        # Return the _p_queue attribute of self.
        #
        # :rtype: int
        #
        # >>> pat = PatApproach()
        # >>> pat._get_p_queue()
        # []
        # """
        return self._p_queue

    def _set_p_queue(self, obj):
        # """
        # Set _p_queue of Restaurant self to obj.
        #
        # :type obj: Object
        # :rtype: None
        #
        # >>> pat = PatApproach()
        # >>> pat._set_p_queue(['obj'])
        # >>> pat._get_p_queue()
        # ['obj']
        # """
        self._p_queue = obj

    p_queue = property(_get_p_queue, _set_p_queue)

    def add_customer(self, new_customer):
        """Add a new entering customer to the restaurant.

        :type new_customer: Customer
            The new customer that is entering the restaurant
        :rtype: None
        """
        raise NotImplementedError(" Must de defined in approach subclasses!")

    def sort_customers(self):
        """
        This helper function makes sure the customers are in proper order in
        the queue every time this function is called.

        :rtype: None

        # Note: writing docstring examples for this particular method becomes
        # tricky, as the simulator file is also required for a practical test
        # case. However, after extraneous and careful testing, I assure that
        #this method is correct.
        """
        temp = [c for c in self._p_queue]
        self._p_queue = []
        # clears the queue and adds every customer to a temporary list
        if len(temp) != 0:
            for t in temp:
                self.add_customer(t)

    def process_turn(self, current_turn):
        """Process the current_turn.

        This function will process the current turn. If the restaurant is not
        serving any customer now, and there are waiting customers, it should
        select one of them to serve.

        You can assume that all customers who entered the restaurant before or
        during this turn were already passed to the restaurant by simulator via
        calling the AddCustomer function.

        :type self: Restaurant
        :type current_turn: int
            The number of current turn
        :rtype: None

        >>> mat = MatApproach()
        >>> c1 = Customer('1\t11111\t10\t11\t12')
        >>> mat.add_customer(c1)
        >>> mat.process_turn(1)
        >>> mat.p_queue
        []
        >>> c2 = Customer('3\t22222\t10\t11\t1')
        >>> mat.add_customer(c2)
        >>> mat.process_turn(3)
        >>> mat.p_queue
        [22222]
        >>> mat.process_turn(4)
        >>> mat.p_queue
        [22222]
        >>> mat.process_turn(5)
        >>> mat.p_queue
        []

        """
        for c in self._p_queue:
            if c.patience() + c.entry_turn() <= current_turn:
                self._p_queue.remove(c)
                # now must reorder all remaining customers
                self.sort_customers()
                self.process_turn(current_turn)
        # this removes any customer who has reached their maximum patience when
        # their order has not been chosen yet, and processes the turn again
        # in case there are multiple people running out of patience, or if
        # someone must be served on this turn.

        if current_turn >= self._next_action:
            if len(self._p_queue) != 0:
                current_customer = self._p_queue.pop(0)
                # makes sure the queue is not empty
                self._r_profit += current_customer.profit()
                self._total += 1
                self._next_action = current_customer.prep() + current_turn
                # add the customer's prep time in order to choose a customer on
                # the turn after their order is finished.

                # Now, we have successfully served a customer
                # now must reorder all remaining customers
                self.sort_customers()

        else:
            pass

    def write_report(self, report_file):
        """Write the final report of this restaurant approach in the report_file.

        :type self: Restaurant
        :type report_file: File
            This is an open file that this restaurant will write the report into
        :rtype: None
        """

        names = {'PatApproach()': 'Pat', 'MaxApproach()': 'Max',
                 'MatApproach()': 'Mat', 'PacApproach()': 'Pac'}

        s = "Results for the serving approach using {}'s suggestion:\n".\
            format(names[str(self)])
        s += 'Total profit: ${}\n'.format(self._r_profit)
        s += 'Customer served: {}\n'.format(self._total)

        report_file.write(s)

    def __repr__(self):
        """
        Represent Restaurant self as a string that can be evaluated to produce
        an equivalent Restaurant.
        @rtype: str

        """
        raise NotImplementedError(" Must de defined in approach subclasses!")


class PatApproach(Restaurant):
    """A Restaurant with Pat management style.

    This class represents a restaurant that uses the Pat management style,
    in which customers are served based on their earliest arrival time.
    This class is a subclass of Restaurant and implements two functions:
    add_customer and __repr__.

    """

    def add_customer(self, new_customer):
        """Add a new entering customer to the restaurant according to Pat's
        priority, which is based on the earliest arrival time.

        Overrides Restaurant.add_customer

        :type new_customer: Customer
            The new customer that is entering the restaurant
        :rtype: None

        >>> pat = PatApproach()
        >>> c1 = Customer('1\t11111\t10\t11\t12')
        >>> pat.add_customer(c1)
        >>> pat.p_queue
        [11111]
        >>> c2 = Customer('3\t22222\t11\t12\t13')
        >>> pat.add_customer(c2)
        >>> pat.p_queue
        [11111, 22222]
        >>> c3 = Customer('2\t33333\t12\t13\t14')
        >>> pat.add_customer(c3)
        >>> pat.p_queue
        [11111, 33333, 22222]

        """

        lst = [x.entry_turn() for x in self._p_queue]
        # add all entry turns from all existing customers to a list.
        new_et = new_customer.entry_turn()
        lst.sort()
        if new_et in lst:
            # find last occurrence of the new_et value and insert after that
            # occurrence.
            back = lst[::-1]
            last = back.index(new_et)
            target = len(lst) - last
        else:
            lst.append(new_et)
            lst.sort()
            target = lst.index(new_et)

        self._p_queue.insert(target, new_customer)

    def __repr__(self):
        """
        Represent PatApproach(self) as a string that can
        be evaluated to produce an equivalent PatApproach.

        Overrides Restaurant.__repr__

        @rtype: str

        >>> p = PatApproach()
        >>> p
        PatApproach()

        """
        return 'PatApproach()'


class MatApproach(Restaurant):
    """A Restaurant with Mat management style.

    This class represents a restaurant that uses the Mat management style,
    in which customers are served based on their latest entry time. This class
    is a subclass of Restaurant and implements two functions: add_customer and
    __repr__.

    """

    def add_customer(self, new_customer):
        """Add a new entering customer to the restaurant according to Mat's
        priority, which is based on the most recent arrival time.

        Overrides Restaurant.add_customer

        :type new_customer: Customer
            The new customer that is entering the restaurant
        :rtype: None

        >>> mat = MatApproach()
        >>> c1 = Customer('1\t11111\t10\t11\t12')
        >>> mat.add_customer(c1)
        >>> mat.p_queue
        [11111]
        >>> c2 = Customer('3\t22222\t11\t12\t13')
        >>> mat.add_customer(c2)
        >>> mat.p_queue
        [22222, 11111]
        >>> c3 = Customer('2\t33333\t12\t13\t14')
        >>> mat.add_customer(c3)
        >>> mat.p_queue
        [22222, 33333, 11111]
        """
        lst = [x.entry_turn() for x in self._p_queue]
        # add all entry turns from all existing customers to a list.
        new_et = new_customer.entry_turn()
        lst.append(new_et)
        lst.sort()
        lst1 = lst[::-1]
        # reverse the list to order it from high (latest) entry time to low
        target = lst1.index(new_et)
        # find the placement of the entry turn of the new customer in comparison
        # to all of the other entry turns
        self._p_queue.insert(target, new_customer)

    def __repr__(self):
        """
        Represent MatApproach(self) as a string that can
        be evaluated to produce an equivalent MatApproach.

        Overrides Restaurant.__repr__

        @rtype: str

        >>> m = MatApproach()
        >>> m
        MatApproach()

        """
        return 'MatApproach()'


class MaxApproach(Restaurant):
    """A Restaurant with Max management style.

    This class represents a restaurant that uses the Max management style,
    in which customers are served based on their maximum profit. This class
    is a subclass of Restaurant and implements two functions: add_customer and
    __repr__.

    """
    def add_customer(self, new_customer):
        """Add a new entering customer to the front of the restaurant queue
         according to Max's priority, which is based on the maximum profit
         of the customer.

        Overrides Restaurant.add_customer

        :type new_customer: Customer
            The new customer that is entering the restaurant
        :rtype: None

        >>> mx = MaxApproach()
        >>> c1 = Customer('1\t44444\t10\t11\t12')
        >>> mx.add_customer(c1)
        >>> mx.p_queue
        [44444]
        >>> c2 = Customer('2\t55555\t11\t12\t13')
        >>> mx.add_customer(c2)
        >>> mx.p_queue
        [55555, 44444]
        >>> c3 = Customer('3\t66666\t9\t13\t14')
        >>> mx.add_customer(c3)
        >>> mx.p_queue
        [55555, 44444, 66666]
        """

        # for all of the customers, it needs to look through all of the
        # profits and add to the queue where the
        # highest profit is most prioritized.

        lst = [x.profit() for x in self._p_queue]
        # add all profits from all existing customers to a list.
        new_et = new_customer.profit()
        # separate the new customer's profit value.
        lst.append(new_et)
        lst.sort()
        lst1 = lst[::-1]
        # Reverse the list so that it displays from highest to lowest
        target = lst1.index(new_et)
        # find the placement of the profit of the new customer in comparison
        # to all of the other profits
        self._p_queue.insert(target, new_customer)

    def __repr__(self):
        """
        Represent MaxApproach(self) as a string that can
        be evaluated to produce an equivalent MaxApproach.
        @rtype: str

        Overrides Restaurant.__repr__

        >>> m = MaxApproach()
        >>> m
        MaxApproach()

        """
        return 'MaxApproach()'


class PacApproach(Restaurant):
    """A Restaurant with Pac management style.

    This class represents a restaurant that uses the Pac management style,
    in which customers are served based on their order's preparation time. This
    class is a subclass of Restaurant and implements two functions: add_customer
    and __repr__.

    """
    def add_customer(self, new_customer):
        """Add a new entering customer to the front of the restaurant queue
         according to Pac's priority, which is based on the shortest order prep
         time of the customer.

        Overrides Restaurant.add_customer

        :type new_customer: Customer
            The new customer that is entering the restaurant
        :rtype: None

        >>> pc = PacApproach()
        >>> c1 = Customer('1\t77777\t10\t3\t12')
        >>> pc.add_customer(c1)
        >>> pc.p_queue
        [77777]
        >>> c2 = Customer('2\t88888\t11\t2\t13')
        >>> pc.add_customer(c2)
        >>> pc.p_queue
        [88888, 77777]
        >>> c3 = Customer('3\t99999\t9\t4\t14')
        >>> pc.add_customer(c3)
        >>> pc.p_queue
        [88888, 77777, 99999]
        """

        # for all of the customers, it needs to look through all of the
        # prepare times and add to the queue where the least/shortest order
        # prepare time is most prioritized.

        lst = [x.prep() for x in self._p_queue]
        # add all prep times from all existing customers to a list.
        new_et = new_customer.prep()
        lst.sort()
        if new_et in lst:
            # find last occurrence of the new_et value and insert after that
            # occurrence.
            back = lst[::-1]
            last = back.index(new_et)
            target = len(lst) - last
        else:
            lst.append(new_et)
            lst.sort()
            target = lst.index(new_et)

        self._p_queue.insert(target, new_customer)

    def __repr__(self):
        """
        Represent PacApproach(self) as a string that can
        be evaluated to produce an equivalent PacApproach.

        Overrides Restaurant.__repr__

        @rtype: str

        >>> p = PacApproach()
        >>> p
        PacApproach()

        """
        return 'PacApproach()'

if __name__ == '__main__':
    import doctest
    doctest.testmod()
