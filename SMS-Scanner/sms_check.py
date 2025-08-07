# SMS Fraud Detection System
from transformers import pipeline

class SMSScanner:
    def __init__(self):
        self.model = pipeline("text-classification", model="finiteautomata/bertweet-base-sentiment-analysis")
        self.scam_keywords = {
            "won prize": 2, 
            "free gift": 2,
            "account alert": 3,
            "click link": 3,
            "verify now": 2
        }

    def scan_message(self, text):
        """Analyzes SMS for scam patterns"""
        # AI sentiment analysis
        ai_result = self.model(text[:512])[0]
        
        # Keyword scoring
        risk_score = sum(
            score for kw, score in self.scam_keywords.items() 
            if kw in text.lower()
        )
        
        if ai_result['label'] == 'NEGATIVE' or risk_score >= 3:
            return f"🚨 SCAM ALERT (Risk score: {risk_score}/10)"
        return f"✅ Safe (Risk score: {risk_score}/10)"

if __name__ == "__main__":
    print("📱 SMS Scam Detector")
    scanner = SMSScanner()
    
    test_sms = "You've won a $1000 Walmart gift card! Claim now: bit.ly/free-gift"
    print(f"Testing message: '{test_sms}'")
    print("Result:", scanner.scan_message(test_sms))