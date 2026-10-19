from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SmsRequest(BaseModel):
    sender: str
    message: str

@app.post("/api/v1/analyze-sms")
async def analyze_sms(data: SmsRequest):
    text = data.message.lower()
    
    # Simple keyword-based scam scoring logic
    scam_keywords = ["won", "prize", "congratulations", "click here", "recharge", "free", "offer", "lottery", "urgent", "verify"]
    score = 0.0
    
    matches = sum(1 for word in scam_keywords if word in text)
    if matches > 0:
        score = min(0.4 + (matches * 0.2), 0.99) # Higher score if more scam keywords match
        
    risk_label = "Safe"
    if score > 0.7:
        risk_label = "High Risk"
    elif score > 0.3:
        risk_label = "Suspicious"
    else:
        risk_label = "Unverified"
        
    return {
        "scam_probability": score,
        "risk_label": risk_label
    }
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)