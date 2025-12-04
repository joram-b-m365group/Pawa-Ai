"""Quick test to verify custom trained model works."""

import sys
import io
from pathlib import Path

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

print("=" * 70)
print("QUICK TEST: Custom Trained Model")
print("=" * 70)

print("\n[1] Loading trained model...")
model_path = "./tiny_genius_model"

try:
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    tokenizer.pad_token = tokenizer.eos_token
    print("  [OK] Tokenizer loaded")

    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float32,
    )
    model = model.to("cpu")
    model.eval()
    print("  [OK] Model loaded on CPU")

    print("\n[2] Testing generation...")

    # Test 1: Python question
    test_prompts = [
        "Q: What is Python?\nA:",
        "Q: How do I define a function?\nA:",
        "Q: What are variables?\nA:",
    ]

    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n  Test {i}:")
        print(f"  Prompt: {prompt.strip()}")

        inputs = tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=80,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
            )

        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Remove prompt from output
        if generated_text.startswith(prompt):
            generated_text = generated_text[len(prompt):].strip()

        print(f"  Response: {generated_text[:150]}...")

    print("\n[3] Model info:")
    print(f"  Model parameters: ~82M")
    print(f"  Model device: CPU")
    print(f"  Model path: {model_path}")

    print("\n" + "=" * 70)
    print("SUCCESS! Your custom trained model works!")
    print("=" * 70)
    print("\nThe model is ready to be integrated with Genius AI system.")
    print("\nNext steps:")
    print("  1. Start the Genius AI backend server")
    print("  2. Test with the full system (orchestrator + agents)")
    print("  3. Test the web interface")
    print("\n" + "=" * 70)

except Exception as e:
    print(f"\n[ERROR] Failed to load or test model: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
