"""Interactive script to ask your custom trained model questions.

This allows you to chat with your model directly from the command line.
"""

import sys
import io
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 70)
print("GENIUS AI - Interactive Chat with Your Custom Model")
print("=" * 70)

# Load your trained model
print("\nLoading your custom trained model...")
model_path = "./tiny_genius_model"

tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float32,
)
model = model.to("cpu")
model.eval()

print("[OK] Model loaded and ready!")
print("\n" + "=" * 70)
print("Ask me anything about Python programming!")
print("Type 'quit' or 'exit' to end the conversation")
print("=" * 70 + "\n")

conversation_count = 0

while True:
    # Get user input
    try:
        question = input("\nYou: ")
    except EOFError:
        break
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        break

    # Check for exit
    if question.lower() in ['quit', 'exit', 'bye', 'goodbye']:
        print("\nAI: Goodbye! Thanks for chatting with me!")
        break

    if not question.strip():
        continue

    # Format prompt
    prompt = f"Q: {question}\nA:"

    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate response
    print("\nAI: ", end="", flush=True)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            top_k=50,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    # Decode response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Remove prompt from response
    if response.startswith(prompt):
        response = response[len(prompt):].strip()

    # Print response
    print(response)

    conversation_count += 1

    # Show statistics every 5 questions
    if conversation_count % 5 == 0:
        print(f"\n[Stats: {conversation_count} questions answered so far]")

print(f"\n\nSession ended. Total questions: {conversation_count}")
print("Your model is working great! Add more training data to improve quality.")
print("\n" + "=" * 70)
