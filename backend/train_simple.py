"""Simple training script for zero-cost AI model training.

Works with 8GB RAM, no GPU needed, completely free.
"""

import json
import sys
from pathlib import Path

print("=" * 70)
print("GENIUS AI - FREE MODEL TRAINING")
print("=" * 70)
print("\nUsing minimal resources: 8GB RAM, CPU only, $0 cost")
print("This may take 10-20 minutes...\n")

# Install dependencies
print("[1/6] Installing dependencies...")
import subprocess

packages = ["torch", "transformers", "datasets", "accelerate"]
for pkg in packages:
    try:
        __import__(pkg)
        print(f"  {pkg}: already installed")
    except ImportError:
        print(f"  {pkg}: installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from datasets import Dataset

print(f"\nPyTorch {torch.__version__} ready (CPU mode)\n")

# Training data
print("[2/6] Loading training data...")
TRAINING_DATA = [
    {
        "prompt": "What is Python?",
        "response": "Python is a high-level programming language. Example:\n\ndef greet(name):\n    return f'Hello, {name}!'"
    },
    {
        "prompt": "How do I define a function?",
        "response": "Use the def keyword:\n\ndef function_name(parameters):\n    return result"
    },
    {
        "prompt": "What are variables?",
        "response": "Variables store data:\n\nx = 5\nname = 'Alice'\npi = 3.14"
    },
    {
        "prompt": "What are lists?",
        "response": "Lists are ordered collections:\n\nfruits = ['apple', 'banana']\nfirst = fruits[0]"
    },
    {
        "prompt": "How do I use if statements?",
        "response": "If statements control flow:\n\nif condition:\n    # code\nelif:\n    # code\nelse:\n    # code"
    },
]

print(f"Loaded {len(TRAINING_DATA)} examples\n")

# Load tiny model
print("[3/6] Loading model (DistilGPT-2, 82M parameters)...")
MODEL_NAME = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float32)
print("Model loaded (300MB)\n")

# Prepare dataset
print("[4/6] Preparing dataset...")
formatted = [{"text": f"Q: {ex['prompt']}\nA: {ex['response']}\n"} for ex in TRAINING_DATA]
dataset = Dataset.from_list(formatted)

def tokenize(examples):
    result = tokenizer(examples["text"], truncation=True, max_length=512, padding="max_length")
    # Add labels (same as input_ids for causal language modeling)
    result["labels"] = result["input_ids"].copy()
    return result

tokenized = dataset.map(tokenize, batched=True, remove_columns=dataset.column_names)
print(f"Dataset ready ({len(tokenized)} examples)\n")

# Test before training
print("[5/6] Testing BASE model (before training):")
print("-" * 70)
test_input = "Q: What is Python?\nA:"
inputs = tokenizer(test_input, return_tensors="pt")
before = model.generate(**inputs, max_new_tokens=30, do_sample=False)
print(tokenizer.decode(before[0], skip_special_tokens=True))
print("-" * 70 + "\n")

# Train
output_dir = Path("./tiny_genius_model")
output_dir.mkdir(exist_ok=True)

print("Training started (this takes 10-15 minutes on CPU)...")
training_args = TrainingArguments(
    output_dir=str(output_dir),
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=2,
    learning_rate=5e-5,
    warmup_steps=5,
    logging_steps=1,
    save_steps=50,
    save_total_limit=1,
    no_cuda=True,
    fp16=False,
    report_to="none",
)

trainer = Trainer(model=model, args=training_args, train_dataset=tokenized)
result = trainer.train()

print(f"\nTraining complete! Loss: {result.training_loss:.4f}")
model.save_pretrained(str(output_dir))
tokenizer.save_pretrained(str(output_dir))
print(f"Model saved to: {output_dir}\n")

# Test after training
print("[6/6] Testing TRAINED model (after training):")
print("-" * 70)
trained = AutoModelForCausalLM.from_pretrained(str(output_dir))
trained.eval()
after = trained.generate(**inputs, max_new_tokens=30, do_sample=False)
print(tokenizer.decode(after[0], skip_special_tokens=True))
print("-" * 70 + "\n")

print("=" * 70)
print("SUCCESS! Your AI model is trained!")
print("=" * 70)
print(f"""
Model saved at: {output_dir}
Training examples: {len(TRAINING_DATA)}
Total cost: $0.00

Next steps:
1. Add more training data (try 50-500 examples)
2. Train for more epochs (try 5-10)
3. Test with different questions
4. Use a larger model when you have more RAM

To use your model:
  from transformers import AutoModelForCausalLM, AutoTokenizer
  model = AutoModelForCausalLM.from_pretrained("{output_dir}")
  tokenizer = AutoTokenizer.from_pretrained("{output_dir}")

You just trained your own AI model for FREE!
""")
