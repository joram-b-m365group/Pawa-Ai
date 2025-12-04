"""Test Groq integration directly"""

import asyncio
import os
from groq import Groq

# Set API key
os.environ["GROQ_API_KEY"] = "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"

async def test_groq():
    print("Testing Groq API with Llama 3.1 70B...\n")

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Test question
    test_question = "What is biology?"

    print(f"Question: {test_question}\n")
    print("Waiting for Groq response...\n")

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Updated model!
            messages=[
                {
                    "role": "system",
                    "content": "You are Genius AI, a helpful and intelligent assistant."
                },
                {
                    "role": "user",
                    "content": test_question
                }
            ],
            temperature=0.7,
            max_tokens=2048,
        )

        response = completion.choices[0].message.content

        print("="*70)
        print("GROQ RESPONSE (70B PARAMETERS!):")
        print("="*70)
        print(response)
        print("="*70)
        print("\nSUCCESS! Groq is working!")
        print("You now have 70 BILLION parameter AI for FREE!")
        print("Intelligence level: 8.5/10 (near GPT-4!)")

    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_groq())
