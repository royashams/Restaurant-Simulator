# Restaurant-Simulator
A program that simulates a restaurant given a file listing various customers, including their Id, Profit, Prepare time, and Patience.
According to these attributes, there are four different approaches which prioritize one attribute at a time.  

Pat's Approach prioritizes earliest arrival time.
Mat's Approach prioritizes latest arrival time.
Max's Approach prioritizes the customer with the largest profit
Pac's Approach prioritizes customers with less patience.

The program is given a scenario file as input, as a list of multiple customers, and generates an output file listing each approach with 
the number of customers served, and the profit generated.

This was completed as a class assignment in June 2016, where I was required to write API and implement customer.py and restaurant.py.
However, simulator.py was provided as starter code.
