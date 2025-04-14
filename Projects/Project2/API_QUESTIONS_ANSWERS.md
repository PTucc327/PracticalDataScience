# API Questions and Answers 4/14/25


1. What is an API call (answer in your own words)?

An API call utilizes a URL to gain access and perform an action.


2. What is an example we discussed to create an API call locally?

Use Fast API, create and activate a virtual environment, pip install fast api, create main.py script and add code from the fast api website, then from the terminal execute fastapi dev main.py, fast api is then run locally meaning it is only on the device that has executed the code not accessible for everyone. Then you can curl the local URL from the terminal while it is active and get the content. 


3. What is an example we discussed to create an API call on the cloud? 

Use AWS, create a lambda function, the lambda handler method is equivalent to the __main__ method. Must make sure code is deployed before testing. Add triggers create new api REST API to create an API Gateway, go to the api gateway, the api created before is there and can be tested. Testing on the api gateway section is different in format from testing done earlier. Deploy API, go to post find the invoke URL and that's how you make calls to the API. resources it says api required is false, create api key, create usage plan for the api key, rate 10 burst 20, requests 1000 per month, associate the key with the api stage dev, add the api key to the project, make sure the api key is required, deploy , anyone can use now if they have api key


4. What is the difference between FastAPI and creating API from AWS Gateway?

With FastAPI it is local meaning that you cannot access the api from any other location other than your pc. With AWS anyone with the api key can be allowed to access the api or even people without the api key depending on the AWS API settings.


5. In your own words after watching the video, what are the main steps to create an API call on AWS Gateway?

Create the backend(lambda function) for the project, then create a new API (REST API), Deploy the API and define the methods you want(ie get, post, put) and find the invoke URL. If you want an api key to be required then you create an API key, go to create a usge plan for the API key selecting the resources for that key. Then associate the key with the project, from there you make sure it says the api key is required and then deploy and now only people with the api key can access.


6. Professionally in the industry, how does developers ship product from one team to another? What's the usage of API here?

They utilize API’s to access different products between teams. One team can create the code that another team needs to access and that other team can utilize its api to access the code created by the first team.
