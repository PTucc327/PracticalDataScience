'''
take in input of string
convert string to url
generate score based on rules
return json object including score and explanation of the score
'''
import json
from urllib.parse import quote

def eval_url(url) :
    ''' takes in a url and 
    '''
    new_url = quote(url)
    json_output = '{"Score: " 0, "Explanation: " "This is why"}'


    return json_output


var1 = input("Enter a URL:" )

print(eval_url(var1))
