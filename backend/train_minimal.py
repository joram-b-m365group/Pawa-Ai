"""Minimal training script for low-resource systems (8GB RAM, no GPU).

This script uses the smallest viable model and minimal dependencies
to enable training on resource-constrained hardware.

Requirements:
- 8GB RAM minimum
- CPU only (no GPU needed)
- No cloud costs
"""

import json
import os
from pathlib import Path
from typing import Optional

# -*- coding: utf-8 -*-
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 70)
print("GENIUS AI - FREE MODEL TRAINING (Zero Dollar Setup)")
print("=" * 70)
print("\nLow-resource mode: Using minimal model for 8GB RAM")
print("This will work on your hardware without any cost!\n")


# ============================================================================
# STEP 1: Check and Install Minimal Dependencies
# ============================================================================

print("[1/6] Checking dependencies...")

def check_and_install_packages():
    """Check and install only essential packages."""
    import subprocess
    import sys

    essential_packages = [
        "torch",           # PyTorch (CPU version)
        "transformers",    # Hugging Face
        "datasets",        # For data handling
        "accelerate",      # For training
    ]

    print("\nInstalling essential packages (this may take a few minutes)...")
    print("Packages: torch (CPU), transformers, datasets, accelerate\n")

    for package in essential_packages:
        try:
            __import__(package)
            print(f"[OK] {package} already installed")
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package, "-q"
            ])
            print(f"[OK] {package} installed")

check_and_install_packages()

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
)
from datasets import Dataset

print(f"\n✓ PyTorch {torch.__version__} loaded (CPU mode)")
print(f"✓ All dependencies ready!\n")


# ============================================================================
# STEP 2: Minimal Training Data
# ============================================================================

print("[2/6] Preparing training data...")

# Minimal but effective training examples
# You can add more examples to improve quality
MINIMAL_TRAINING_DATA = [
    {
        "prompt": "What is Python?",
        "response": """Python is a high-level, interpreted programming language known for its simplicity and readability.

Key features:
- Easy to learn and read
- Versatile (web, data science, AI, automation)
- Large ecosystem of libraries
- Strong community support

Example:
```python
# Simple Python code
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))  # Output: Hello, World!
```"""
    },
    {
        "prompt": "How do I define a function in Python?",
        "response": """To define a function in Python, use the `def` keyword:

```python
def function_name(parameters):
    \"\"\"Docstring explaining the function.\"\"\"
    # Function body
    return result
```

Example:
```python
def add_numbers(a, b):
    \"\"\"Add two numbers and return the result.\"\"\"
    return a + b

result = add_numbers(5, 3)
print(result)  # Output: 8
```"""
    },
    {
        "prompt": "Explain variables in Python",
        "response": """Variables in Python store data values. Python is dynamically typed, so you don't need to declare variable types.

Assignment:
```python
x = 5           # Integer
name = "Alice"  # String
pi = 3.14       # Float
is_valid = True # Boolean
```

Multiple assignment:
```python
a, b, c = 1, 2, 3
x = y = z = 0
```

Variables are case-sensitive: `age` and `Age` are different variables."""
    },
    {
        "prompt": "What are lists in Python?",
        "response": """Lists are ordered, mutable collections that can hold items of different types.

Creating lists:
```python
numbers = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "orange"]
mixed = [1, "two", 3.0, True]
empty = []
```

Common operations:
```python
# Access
first = fruits[0]      # "apple"
last = fruits[-1]      # "orange"

# Modify
fruits[1] = "grape"    # Change item
fruits.append("mango") # Add to end
fruits.remove("apple") # Remove item

# Slice
subset = numbers[1:4]  # [2, 3, 4]
```"""
    },
    {
        "prompt": "How do I use if statements?",
        "response": """If statements control program flow based on conditions:

Basic syntax:
```python
if condition:
    # Code if true
elif another_condition:
    # Code if first is false, this is true
else:
    # Code if all are false
```

Example:
```python
age = 18

if age < 13:
    print("Child")
elif age < 20:
    print("Teenager")
else:
    print("Adult")

# Output: Teenager
```

Comparison operators: `==`, `!=`, `<`, `>`, `<=`, `>=`
Logical operators: `and`, `or`, `not`"""
    },
]

print(f"✓ Loaded {len(MINIMAL_TRAINING_DATA)} training examples")
print("  (You can add more examples to improve the model!)\n")


# ============================================================================
# STEP 3: Use Tiny Model (DistilGPT-2 - only 80MB!)
# ============================================================================

print("[3/6] Loading minimal model...")
print("  Using DistilGPT-2 (82M parameters, ~300MB)")
print("  This is perfect for 8GB RAM and learning!\n")

MODEL_NAME = "distilgpt2"  # Tiny but functional!

# Load tokenizer
print("  Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

print("  Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,  # CPU doesn't support float16
)

print(f"✓ Model loaded successfully!")
print(f"  Parameters: ~82 million")
print(f"  Memory: ~300MB\n")


# ============================================================================
# STEP 4: Prepare Dataset
# ============================================================================

print("[4/6] Preparing dataset...")

def format_example(example):
    """Format training example."""
    return {
        "text": f"Question: {example['prompt']}\nAnswer: {example['response']}\n"
    }

# Format and create dataset
formatted_data = [format_example(ex) for ex in MINIMAL_TRAINING_DATA]
dataset = Dataset.from_list(formatted_data)

# Tokenize
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=512,  # Keep it short for RAM
        padding="max_length",
    )

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=dataset.column_names,
)

print(f"✓ Dataset prepared: {len(tokenized_dataset)} examples\n")


# ============================================================================
# STEP 5: Train!
# ============================================================================

print("[5/6] Starting training...")
print("  This will take 5-15 minutes on CPU")
print("  Settings optimized for 8GB RAM\n")

output_dir = Path("./genius_ai_tiny_model")
output_dir.mkdir(exist_ok=True)

# Minimal training args for low RAM
training_args = TrainingArguments(
    output_dir=str(output_dir),
    num_train_epochs=3,
    per_device_train_batch_size=1,  # Minimal batch size for RAM
    gradient_accumulation_steps=2,
    learning_rate=5e-5,
    warmup_steps=10,
    logging_steps=1,
    save_steps=100,
    save_total_limit=1,
    no_cuda=True,  # Force CPU
    fp16=False,    # CPU doesn't support fp16
    report_to="none",  # No external reporting
)

# Test before training
print("Testing BASE model (before training):")
print("-" * 70)
test_prompt = "Question: What is Python?\nAnswer:"
inputs = tokenizer(test_prompt, return_tensors="pt")
before_output = model.generate(**inputs, max_new_tokens=50, do_sample=False)
before_text = tokenizer.decode(before_output[0], skip_special_tokens=True)
print(before_text)
print("-" * 70 + "\n")

# Create trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# Train!
print("Training started...\n")
train_result = trainer.train()

print("\n✓ Training complete!")
print(f"  Final loss: {train_result.training_loss:.4f}\n")

# Save model
print("Saving model...")
model.save_pretrained(str(output_dir))
tokenizer.save_pretrained(str(output_dir))
print(f"✓ Model saved to: {output_dir}\n")


# ============================================================================
# STEP 6: Test Trained Model
# ============================================================================

print("[6/6] Testing TRAINED model (after training):")
print("-" * 70)

# Reload the fine-tuned model
trained_model = AutoModelForCausalLM.from_pretrained(str(output_dir))
trained_model.eval()

# Test
inputs = tokenizer(test_prompt, return_tensors="pt")
after_output = trained_model.generate(**inputs, max_new_tokens=50, do_sample=False)
after_text = tokenizer.decode(after_output[0], skip_special_tokens=True)
print(after_text)
print("-" * 70 + "\n")

print("=" * 70)
print("SUCCESS! Your model is trained!")
print("=" * 70)
print(f"""
✅ Training Complete!

Your model is saved at: {output_dir}

What you've achieved:
  • Trained your own AI model (zero cost!)
  • Works on 8GB RAM, no GPU needed
  • Based on DistilGPT-2 (82M parameters)
  • Fine-tuned on Python knowledge

Next steps:
  1. Add more training examples (50-500+)
  2. Train for more epochs (try 5-10)
  3. Test with different questions
  4. Integrate with Genius AI system

To use your model:
  from transformers import AutoModelForCausalLM, AutoTokenizer

  model = AutoModelForCausalLM.from_pretrained("{output_dir}")
  tokenizer = AutoTokenizer.from_pretrained("{output_dir}")

  # Generate
  inputs = tokenizer("Question: What is Python?\\nAnswer:", return_tensors="pt")
  outputs = model.generate(**inputs, max_new_tokens=100)
  print(tokenizer.decode(outputs[0]))

💡 Tips to improve:
  • Add more training data (current: {len(MINIMAL_TRAINING_DATA)} examples)
  • Use a larger model when you have more RAM
  • Train for longer (more epochs)
  • Use a GPU if available (much faster!)

Total cost: $0.00 ✨
""")
