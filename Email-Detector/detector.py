# Email Detector - Phishing Analysis Tool
from transformers import pipeline
import re

class EmailAnalyzer:
    def __init__(self):
        self.model = pipeline("text-classification", model="distilbert-base-uncased")
        self.scam_patterns = [
            r"urgent action required",
            r"click (?:here|this link)",
            r"account (?:verification|suspended)",
            r"password (?:expired|update)"
        ]

    def analyze_email(self, text):
        """Detects phishing attempts in email content"""
        # AI analysis
        ai_result = self.model(text[:1024])[0]  # Trim long emails
        
        # Pattern matching
        red_flags = [patt for patt in self.scam_patterns 
                    if re.search(patt, text, re.IGNORECASE)]
        
        if ai_result['label'] == 'LABEL_1' or red_flags:
            return f"🚨 PHISHING ({len(red_flags)} red flags detected)"
        return "✅ Legitimate email"

if __name__ == "__main__":
    print("📧 AI Email Detector")
    analyzer = EmailAnalyzer()
    
    test_email = """Dear user, your account will be suspended unless 
    you verify your details immediately: http://fake-bank.com/login"""
    
    print("Sample analysis:")
    print(analyzer.analyze_email(test_email))