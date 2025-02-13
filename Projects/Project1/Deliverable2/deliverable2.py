import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

class URLValidator:
    """
    A production-ready URL validation class that evaluates the credibility of a webpage
    using multiple factors: domain trust, content relevance, fact-checking, bias detection, citations, and security.
    """

    def __init__(self):
        # API Keys
        self.serpapi_key = SERPAPI_KEY
        self.google_safe_browsing_key = GOOGLE_SAFE_KEY

        # Load models once to avoid redundant API calls
        self.similarity_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        self.fake_news_classifier = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-fake-news-detection")
        self.sentiment_analyzer = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-sentiment")

    def fetch_page_content(self, url: str) -> str:
        """ Fetches and extracts text content from the given URL. """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            return " ".join([p.text for p in soup.find_all("p")])  # Extract paragraph text
        except requests.RequestException:
            return ""  # Fail gracefully by returning an empty string

    def get_domain_trust(self, url: str, content: str) -> int:
            """ Computes the domain trust score based on available data sources. """
            trust_scores = []

            # Hugging Face Fake News Detector
            if content:
                try:
                    trust_scores.append(self.get_domain_trust_huggingface(content))
                except:
                    pass

            # Compute final score (average of available scores)
            return int(sum(trust_scores) / len(trust_scores)) if trust_scores else 50

    def get_domain_trust_huggingface(self, content: str) -> int:
        """ Uses a Hugging Face fake news detection model to assess credibility. """
        if not content:
            return 50  # Default score if no content available
        result = self.fake_news_classifier(content[:512])[0]  # Process only first 512 characters
        return 100 if result["label"] == "REAL" else 30 if result["label"] == "FAKE" else 50

    def compute_similarity_score(self, user_query: str, content: str) -> int:
        """ Computes semantic similarity between user query and page content. """
        if not content:
            return 0
        return int(util.pytorch_cos_sim(self.similarity_model.encode(user_query), self.similarity_model.encode(content)).item() * 100)

    def check_facts(self, content: str) -> int:
        """ Cross-checks extracted content with Google Fact Check API. """
        if not content:
            return 50
        api_url = f"https://toolbox.google.com/factcheck/api/v1/claimsearch?query={content[:200]}"
        try:
            response = requests.get(api_url)
            data = response.json()
            return 80 if "claims" in data and data["claims"] else 40
        except:
            return 50  # Default uncertainty score

    def check_google_scholar(self, url: str) -> int:
        """ Checks Google Scholar citations using SerpAPI. """
        serpapi_key = self.serpapi_key
        params = {"q": url, "engine": "google_scholar", "api_key": serpapi_key}
        try:
            response = requests.get("https://serpapi.com/search", params=params)
            data = response.json()
            return min(len(data.get("organic_results", [])) * 10, 100)  # Normalize
        except:
            return 0  # Default to no citations

    def detect_bias(self, content: str) -> int:
        """ Uses NLP sentiment analysis to detect potential bias in content. """
        if not content:
            return 50
        sentiment_result = self.sentiment_analyzer(content[:512])[0]
        return 100 if sentiment_result["label"] == "POSITIVE" else 50 if sentiment_result["label"] == "NEUTRAL" else 30

    def get_star_rating(self, score: float) -> tuple:
        """ Converts a score (0-100) into a 1-5 star rating. """
        stars = max(1, min(5, round(score / 20)))  # Normalize 100-scale to 5-star scale
        return stars, "⭐" * stars

    def generate_explanation(self, domain_trust, similarity_score, fact_check_score, bias_score, citation_score, safe_browsing_score, final_score) -> str:
        """ Generates a human-readable explanation for the score. """
        reasons = []
        if domain_trust < 50:
            reasons.append("The source has low domain authority.")
        else:
            reasons.append("The source has high domain authority.")
        if similarity_score < 50:
            reasons.append("The content is not highly relevant to your query.")
        else:
            reasons.append("The content is highly relevant to your query.")
        if fact_check_score < 50:
            reasons.append("Limited fact-checking verification found.")
        else:
            reasons.append("High level of fact-checking verification found.")
        if bias_score < 50:
            reasons.append("Potential bias detected in the content.")
        else:
            reasons.append("No bias detected in the content.")
        if citation_score < 30:
            reasons.append("Few citations found for this content.")
        else:
            reasons.append("High level of citations found for this content.")
        if safe_browsing_score < 50:
            reasons.append("No malicious content detected.")
        else:
            reasons.append("Possible malicious content detected.")

        return " ".join(reasons) if reasons else "This source is highly credible and relevant."


    def check_google_safe_browsing(self, url: str) -> int:
        """
        Uses Google Safe Browsing API to check if a URL is malicious.
        Returns:
            - 100 if safe
            - 30 if flagged as potentially harmful
            - 10 if confirmed malicious
        """
        api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={self.google_safe_browsing_key}"
        payload = {
            "client": {
                "clientId": "your-app",
                "clientVersion": "1.0"
            },
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }

        try:
            response = requests.post(api_url, json=payload)
            data = response.json()
            if "matches" in data:
                return 10  # Malicious URL detected
            return 100  # Safe URL
        except:
            return 50  # Default score if API request fails

    def rate_url_validity(self, user_query: str, url: str) -> dict:
        """ Main function to evaluate the validity of a webpage. """
        content = self.fetch_page_content(url)

        domain_trust = self.get_domain_trust(url, content)
        similarity_score = self.compute_similarity_score(user_query, content)
        fact_check_score = self.check_facts(content)
        bias_score = self.detect_bias(content)
        citation_score = self.check_google_scholar(url)
        safe_browsing_score = self.check_google_safe_browsing(url)

        final_score = (
            (0.30 * domain_trust) +
            (0.30 * similarity_score) +
            (0.20 * fact_check_score) +
            (0.10 * bias_score) +
            (0.10 * citation_score) +
            (0.05 * safe_browsing_score)
        )

        stars, icon = self.get_star_rating(final_score)
        explanation = self.generate_explanation(domain_trust, similarity_score, fact_check_score, bias_score, citation_score, safe_browsing_score, final_score)

        return {
            "raw_score": {
                "Domain Trust": domain_trust,
                "Content Relevance": similarity_score,
                "Fact-Check Score": fact_check_score,
                "Bias Score": bias_score,
                "Citation Score": citation_score,
                "Safe Browsing Score": safe_browsing_score,
                "Final Validity Score": final_score
            },
            "stars": {
                "score": stars,
                "icon": icon
            },
            "explanation": explanation
        }
