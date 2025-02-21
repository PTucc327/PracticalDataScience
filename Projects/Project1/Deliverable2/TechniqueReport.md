Questions:

What is a class object?

A class object is an instance of a class with its own attributes and methods. In the case of our URLValidator project, when we create the class object for the URLValidator we are able to then utilize the various methods within the class such as rate_url_validity to take a url and a query and evaluate it to see if the url will help answer the query provided.


What is a docstring?

A docstring is used to write documentation of a section of code. To do this you use 3 single quotes to start and 3 single quotes to close in between those quotes a person can write information regarding the section of code such as purpose, arguments the code takes in as well as the output if applicable.


How do you define  init of a class object?

 ‘def __init__(self):’


What is a method?

A method is a function associated with a class that is created to complete a certain task. In our project we have various methods such as check_facts(), and get_domain_trust() that are used to complete their own respective tasks to evaluate a url and provide a score.


How do you let functions fail gracefully?

To let functions fail gracefully a person should use a try-catch statement. The reason to do this is so when you run the code if there is no problem then the code will run all the way through the try block and no errors return however if there is an error then the code will stop running through the try block move into the catch and return a more meaningful response detailing the error that occurred.


What’s a standard practice of a return statement?

Standard practice for a return statement is to use them at the end of methods to send a value back to the point in which the method was called. In the case  of our project there are return statements at the end of each method to send the appropriate value back to where it was called. The methods that help to give values towards the score of the url return integer values where as the return from rate_url_validity returns a json object which outlines the various scores given to the url and explanation.
