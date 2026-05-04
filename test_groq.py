import os
import sys
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

if not GROQ_API_KEY or GROQ_API_KEY == "gsk_your_key_here":
    print("❌ GROQ_API_KEY is not set.")
    print("   1. Copy .env.example → .env")
    print("   2. Paste your real key from console.groq.com")
    sys.exit(1)

try:
    from groq import Groq
except ImportError:
    print("❌ groq package not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Reply in exactly one sentence."
            },
            {
                "role": "user",
                "content": "Confirm that the Groq API is working correctly."
            }
        ],
        temperature=0.3,
        max_tokens=60,
    )

    reply  = response.choices[0].message.content
    tokens = response.usage.total_tokens
    model  = response.model

    print("✅ Groq API is working!")
    print(f"   Model : {model}")
    print(f"   Reply : {reply}")
    print(f"   Tokens: {tokens}")

except Exception as e:
    print(f"❌ Groq API call failed: {e}")
    print("   Check your key at console.groq.com → API Keys")
    sys.exit(1)
