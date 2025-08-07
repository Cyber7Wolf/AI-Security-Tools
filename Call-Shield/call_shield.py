# call_shield.py
import warnings
from transformers import pipeline
import sounddevice as sd
import numpy as np
from datetime import datetime
import os

warnings.filterwarnings("ignore")

class CallShield:
    def __init__(self):
        self.model = pipeline("text-classification", 
                            model="distilbert-base-uncased")
        self.recording_dir = "recordings"
        os.makedirs(self.recording_dir, exist_ok=True)

    def analyze_audio(self, text):
        """Detects scam patterns in transcribed call audio"""
        result = self.model(text[:1000])[0]  # Trim long texts
        scam_keywords = ["urgent", "payment", "verify", 
                       "account", "suspended", "prize"]
        hits = [kw for kw in scam_keywords if kw in text.lower()]
        
        if result['label'] == 'LABEL_1' or hits:
            return f"🚨 SCAM DETECTED ({len(hits)} red flags)"
        return "✅ Legitimate call"

    def record_call(self, duration=30):
        """Records suspicious calls"""
        fs = 44100  # Sample rate
        print(f"🔴 Recording {duration} seconds...")
        recording = sd.rec(int(duration * fs), 
                         samplerate=fs, 
                         channels=1)
        sd.wait()
        filename = f"{self.recording_dir}/call_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        np.save(filename, recording)
        return filename

if __name__ == "__main__":
    print("📞 Call Shield - AI Scam Detection System")
    shield = CallShield()
    
    # Example usage
    test_transcript = "Your bank account has been compromised. Please verify your details immediately."
    print("Testing with sample scam call:")
    print(f"Transcript: {test_transcript}")
    print("Result:", shield.analyze_audio(test_transcript))