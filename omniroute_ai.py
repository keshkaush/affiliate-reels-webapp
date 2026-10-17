import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables

class OmnirouteAI:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro-vision') # For multimodal input

    def identify_products(self, content_text: str) -> list:
        """
        Simulates AI product identification.
        In a real scenario, this would analyze video/image content or text descriptions.
        For now, it's a simple keyword-based detection.
        """
        products = []
        # Simple keyword matching for demo purposes
        product_keywords = ["earbuds", "speaker", "charger", "watch", "bag", "shirt", "gadget", "accessory", "clothing", "smart home"]
        for keyword in product_keywords:
            if keyword in content_text.lower():
                products.append(keyword)
        return products

    def analyze_video(self, video_data: dict) -> dict:
        """
        Simulates AI analysis of a video for faceless content and product detection.
        Takes a dictionary containing 'title' and 'description' (or similar text fields).
        """
        title = video_data.get('title', '')
        description = video_data.get('description', '')
        content_text = f"{title} {description}"

        # Simulate faceless detection
        is_faceless = "face" not in content_text.lower() and "person" not in content_text.lower()

        # Simulate product identification
        products_found = self.identify_products(content_text)

        return {
            "is_faceless": is_faceless,
            "products_found": products_found
        }

    def generate_caption(self, product_name: str, affiliate_link: str, description: str = "") -> str:
        """Generates a social media caption with #ad disclosure."""
        prompt = f"Create a short, engaging social media caption for a reel promoting '{product_name}'. Include a call to action to click the link for more info, and ensure it contains '#ad' or '(affiliate link)' for disclosure. Here is a brief description of the product: '{description}'. The affiliate link is: {affiliate_link}"
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating caption: {e}")
            return f"Check out this amazing {product_name}! Get yours now: {affiliate_link} #ad"

    def detect_interest(self, comment_text: str) -> dict:
        """
        Detects purchase interest in a comment.
        """
        keywords = ["buy", "link", "price", "where to get", "shop", "want", "how much"]
        interest_found = any(kw in comment_text.lower() for kw in keywords)
        return {"confidence": 0.9 if interest_found else 0.1, "detected_products": self.identify_products(comment_text)}

    def extract_product_name(self, text: str) -> dict:
        """Extracts product name from text."""
        # Simple extraction for demo
        product_keywords = self.identify_products(text)
        return {"product_name": product_keywords[0]} if product_keywords else None
