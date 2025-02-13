
import requests
import time
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import hashlib
import hmac
import base64
# Replace with your Moz API credentials
MOZ_ACCESS_ID = "Enter Moz access ID here"
MOZ_SECRET_KEY ="Enter Moz secret key here"


def eval_url(url: str, user_query: str) -> dict :
    ''' 
        takes in a url and user query
        calculate a score based on domain trust, similarity, fact checking, bias, citation count
        returns a dictionary object with the score and explanation

        Args:
        url: string input
        user_query: string input

        Returns:
        dict: representing score and explanation
    '''
    try:
      response = requests.get(url)
      response.raise_for_status()
      html_text = response.text
    #Extract information from url
      soup = BeautifulSoup(html_text, "html.parser")
      page_text = " ".join([p.text for p in soup.find_all("p")])
    except:
      return {"Error": "Invalid URL"}
    
    #get domain trust score
    domain_trust = calculate_moz_trust_score(url)

    #get similarity score
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    similarity_score = util.pytorch_cos_sim(model.encode(user_query), model.encode(page_text)).item()*100

    #get fact_check_score
    fact_check_score = check_facts(page_text)

    #get bias score
    sentiment_pipeline = pipeline("text-classification", model= "cardiffnlp/twitter-roberta-base-sentiment")
    sentiment_result =sentiment_pipeline(page_text[:512])[0]
    bias_score = 100 if sentiment_result['label'] == 'Positive' else 50 if sentiment_result['label'] == 'Neutral' else 30

    #get citation score
    citation_count = check_google_scholar(url)
    citation_score = min(citation_count*10,100)

    #Calculate final score
    final_score = ((0.3*domain_trust) +
     (0.3*similarity_score) +
      (0.2*fact_check_score) +
       (0.1*bias_score) +
        (0.1*citation_score))

    #create the explanation
    explanation = ''


    if(final_score >=90):
      explanation= 'This website answers your query'
    elif(final_score>=60 and final_score<90):
      explanation = 'This website might answer your query'
    elif(final_score>=30 and final_score<60):
      explanation = 'This website might not answer your query'
    else:
      explanation = 'This website does not answer your query'

    output = {"Score": float(final_score), "Explanation": explanation}

    return output


def get_moz_metrics(url : str) :
    """Fetch Moz Domain Authority, Page Authority, and Spam Score"""
    expires = int(time.time()) + 300
    string_to_sign = f"{MOZ_ACCESS_ID}\n{expires}"
    signature = base64.b64encode(hmac.new(MOZ_SECRET_KEY.encode(), string_to_sign.encode(), hashlib.sha1).digest()).decode()

    api_url = "https://lsapi.seomoz.com/v2/url_metrics"
    headers = {"Authorization": f"Basic {base64.b64encode(f'{MOZ_ACCESS_ID}:{signature}'.encode()).decode()}"}
    data = {"targets": [url], "metrics": ["domain_authority", "page_authority", "spam_score"]}

    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("results", [{}])[0]
    return {}


def calculate_moz_trust_score(url: str)-> float:
    """Calculate a trust score (0-100) using Moz metrics
    Args: 
    url(str): URL to calculate trust score

    Returns:
    float: Trust score (0-100)
    """
    moz_data = get_moz_metrics(url)
    da = moz_data.get("domain_authority", 50)
    pa = moz_data.get("page_authority", 50)
    spam_score = moz_data.get("spam_score", 100)  # If missing, assume worst case

    # Trust Score Formula (Weighted)
    trust_score = (
        (da * 0.5) +               # Domain Authority (50%)
        (pa * 0.3) +               # Page Authority (30%)
        ((100 - spam_score) * 0.2) # Inverted Spam Score (20%)
    )

    return round(min(trust_score, 100), 2)


def check_facts(text :str) -> int:
  '''
  Takes a string input and utilizes google toolbox api to check facts
  Returns a score between 0-100 indicating factual reliability

  Args:
   text: string input

  Returns:
   int: representing score
  '''
  api_url = f"https://toolbox.google.com/factcheck/api/v1/claimssearch?query={text[:200]}"
  try:
    response =requests.get(api_url)
    data= response.json()
    if "claims" in data and data["claims"]:
      return 80
    return 40
  except:
    return 50


def check_google_scholar(url :str) -> int:
'''
Takes a string input of the url and
uses serp api along with google scholar to check citation count

Args:
  url: string input


Returns 
  int : represting score
'''

  serpapi_key = "SERPAPI_KEY_HERE"
  params = {"q":url, "engine":"google_scholar","api_key":serpapi_key}
  try:
    response = requests.get("https://serpapi.com/search", params= params)
    data= response.json()
    return len(data.get('organic_results',[]))
  except:
    return 0



var1 = "I just unlocked volt prime what mods should I equip"
var2 = "https://overframe.gg/items/arsenal/61/volt-prime/"

print(eval_url(url = var2, user_query=var1))