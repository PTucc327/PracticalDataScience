'''
take in input of string
convert string to url
generate score based on rules
return json object including score and explanation of the score
'''
import json
import requests
from bs4 import BeautifulSoup

def eval_url(url) :
    ''' takes in a url and 
    '''
    response = requests.get(url)
    #Check if the url is valid or not
    if response.status_code == 200:
        html_content = response.content
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
    #Extract information from url
    soup = BeautifulSoup(html_content, "html.parser")
    paragraphs = soup.find_all("p", class_="article-text")
    for paragraph in paragraphs:
        print(paragraph.text)
    
    #Create JSON object to output
    json_output = '{"Score: " 0, "Explanation: " "This is why"}'
    

    return json_output


var1 = input("Enter a URL: " )

print(eval_url(var1))
