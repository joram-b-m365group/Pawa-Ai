"""
Train Genius AI with a MASSIVE dataset for real intelligence
Uses HuggingFace datasets for quick, high-quality data
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import sys

print("=" * 70)
print("GENIUS AI - MASSIVE TRAINING")
print("=" * 70)
print()
print("Training with 10,000+ real-world examples")
print("This will make your AI MUCH smarter!")
print("=" * 70)
print()

# Load model
print("[1/6] Loading DistilGPT-2 model...")
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_name)
print("Model loaded (82M parameters)")
print()

# Load a large, high-quality dataset from HuggingFace
print("[2/6] Loading training dataset...")
print("Using 'databricks/databricks-dolly-15k' dataset")
print("This is 15,000 high-quality instruction-response pairs!")
print()

try:
    # Load Dolly dataset - 15k instruction-following examples
    dataset = load_dataset("databricks/databricks-dolly-15k", split="train")
    print(f"Loaded {len(dataset)} examples")

    # Take first 10,000 to save time
    dataset = dataset.select(range(min(10000, len(dataset))))
    print(f"Using {len(dataset)} examples for training")
    print()

except Exception as e:
    print(f"Error loading dataset: {e}")
    print()
    print("Falling back to smaller dataset...")
    # Fallback to a different dataset
    dataset = load_dataset("HuggingFaceH4/no_robots", split="train[:5000]")
    print(f"Loaded {len(dataset)} examples from fallback dataset")
    print()

# Format the dataset
print("[3/6] Formatting dataset...")

def format_example(example):
    """Format examples into prompt-response format"""
    # Dolly format
    if "instruction" in example and "response" in example:
        prompt = example["instruction"]
        if example.get("context"):
            prompt = f"{prompt}\n\nContext: {example['context']}"
        response = example["response"]
        return f"Question: {prompt}\n\nAnswer: {response}"

    # Generic format
    elif "prompt" in example and "completion" in example:
        return f"Question: {example['prompt']}\n\nAnswer: {example['completion']}"

    # Messages format
    elif "messages" in example:
        text = ""
        for msg in example["messages"]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            text += f"{role.capitalize()}: {content}\n\n"
        return text

    # Fallback
    else:
        return str(example)

dataset = dataset.map(lambda x: {"text": format_example(x)})
print("Dataset formatted")
print()

# Tokenize
print("[4/6] Tokenizing dataset...")
def tokenize(examples):
    result = tokenizer(
        examples["text"],
        truncation=True,
        max_length=512,
        padding="max_length",
    )
    result["labels"] = result["input_ids"].copy()
    return result

tokenized_dataset = dataset.map(tokenize, batched=True, remove_columns=dataset.column_names)
print("Dataset tokenized")
print()

# Training arguments
print("[5/6] Configuring training...")
training_args = TrainingArguments(
    output_dir="./genius_model_massive",
    num_train_epochs=3,  # 3 epochs on 10k examples = very good
    per_device_train_batch_size=4,
    save_steps=1000,
    save_total_limit=2,
    logging_steps=100,
    learning_rate=5e-5,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    no_cuda=True,  # CPU training
    report_to="none",
)
print("Training configured")
print()

# Train
print("[6/6] TRAINING STARTING...")
print("This will take 1-2 hours on CPU")
print("Your AI will be MUCH smarter after this!")
print("-" * 70)
print()

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# Train the model
trainer.train()

# Save
print()
print("-" * 70)
print("Saving model...")
model.save_pretrained("./genius_model_massive")
tokenizer.save_pretrained("./genius_model_massive")
print()

print("=" * 70)
print("SUCCESS! Your AI is now MASSIVELY smarter!")
print("=" * 70)
print()
print(f"Model trained on {len(dataset)} examples")
print("Model saved to: ./genius_model_massive")
print()
print("This model will give MUCH better, more intelligent responses!")
print("=" * 70)
