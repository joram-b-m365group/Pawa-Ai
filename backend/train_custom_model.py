"""Train a custom model that rivals OpenAI.

This script provides a complete workflow for creating your own intelligent model
by fine-tuning open-source models on your domain-specific data.

Usage:
    python train_custom_model.py

Requirements:
    - GPU with 16GB+ VRAM (or use CPU with longer training time)
    - Training data (provided examples or your own)
"""

import asyncio
import json
from pathlib import Path
from typing import Optional

from genius_ai.models.custom_model import (
    CustomIntelligentModel,
    CustomModelConfig,
)
from genius_ai.core.logger import logger


# ============================================================================
# STEP 1: Define Your Training Data
# ============================================================================

def get_sample_training_data() -> list[dict[str, str]]:
    """Get sample training data for demonstration.

    Replace this with your own domain-specific data!
    """
    return [
        # Programming & Coding
        {
            "prompt": "Write a Python function to check if a number is prime",
            "response": """Here's an efficient function to check if a number is prime:

```python
def is_prime(n: int) -> bool:
    \"\"\"Check if a number is prime.

    Args:
        n: Number to check

    Returns:
        True if prime, False otherwise
    \"\"\"
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Check odd divisors up to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2

    return True


# Test
print(is_prime(17))  # True
print(is_prime(18))  # False
```

This implementation is O(√n) time complexity."""
        },
        {
            "prompt": "Explain async/await in Python",
            "response": """async/await in Python enables asynchronous programming:

**Key Concepts:**
1. **async def**: Defines a coroutine function
2. **await**: Pauses execution until async operation completes
3. **asyncio**: Standard library for running async code

**Example:**
```python
import asyncio

async def fetch_data(url):
    \"\"\"Simulated async data fetch.\"\"\"
    await asyncio.sleep(1)  # Simulate I/O
    return f"Data from {url}"

async def main():
    # Run tasks concurrently
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3"),
    )
    print(results)

# Run
asyncio.run(main())
```

**Benefits:**
- Non-blocking I/O operations
- Better performance for I/O-bound tasks
- Cleaner than callbacks or threads"""
        },
        {
            "prompt": "How do I use FastAPI for REST APIs?",
            "response": """FastAPI makes building REST APIs simple and fast:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Data model
class Item(BaseModel):
    name: str
    price: float
    quantity: int

# In-memory storage
items = {}

# Create
@app.post("/items/")
async def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item
    return {"id": item_id, **item.dict()}

# Read
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

# Update
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return item

# Delete
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"message": "Item deleted"}
```

Run with: `uvicorn main:app --reload`
API docs at: http://localhost:8000/docs"""
        },

        # AI & Machine Learning
        {
            "prompt": "What is the difference between supervised and unsupervised learning?",
            "response": """**Supervised Learning:**
- Has labeled training data (input → output pairs)
- Goal: Learn to predict labels for new data
- Examples: Classification, Regression
- Algorithms: Linear Regression, Random Forest, Neural Networks
- Use case: Spam detection (emails labeled as spam/not spam)

**Unsupervised Learning:**
- No labeled data, only inputs
- Goal: Find hidden patterns or structure
- Examples: Clustering, Dimensionality Reduction
- Algorithms: K-Means, PCA, Autoencoders
- Use case: Customer segmentation (group similar customers)

**Key Difference:**
Supervised learning needs examples with correct answers to learn from, while unsupervised learning discovers patterns on its own.

**Example:**
```python
# Supervised: Predict house prices
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)  # Learn from labeled data
predictions = model.predict(X_test)

# Unsupervised: Group customers
from sklearn.cluster import KMeans
model = KMeans(n_clusters=3)
clusters = model.fit_predict(X)  # No labels needed
```"""
        },

        # Problem Solving
        {
            "prompt": "How do I debug a Python program?",
            "response": """**Debugging Strategies:**

**1. Print Debugging:**
```python
def calculate(x, y):
    print(f"Debug: x={x}, y={y}")  # Print values
    result = x / y
    print(f"Debug: result={result}")
    return result
```

**2. Using pdb Debugger:**
```python
import pdb

def buggy_function():
    x = 5
    pdb.set_trace()  # Breakpoint
    y = x * 2
    return y
```

**3. Logging:**
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def process_data(data):
    logger.debug(f"Processing {len(data)} items")
    # Your code
    logger.info("Processing complete")
```

**4. Exception Handling:**
```python
try:
    risky_operation()
except Exception as e:
    import traceback
    traceback.print_exc()  # Full stack trace
    logger.error(f"Error: {e}")
```

**5. IDE Debugger:**
- Set breakpoints in VS Code/PyCharm
- Step through code line by line
- Inspect variables

**Best Practice:** Start with print debugging, graduate to proper logging."""
        },

        # Explanations
        {
            "prompt": "Explain how neural networks work in simple terms",
            "response": """Neural networks are inspired by the human brain:

**Basic Concept:**
Imagine a network of connected nodes (neurons) that pass signals to each other. Each connection has a "weight" that determines how strong the signal is.

**How They Learn:**
1. **Input:** Feed data into the network (e.g., an image)
2. **Process:** Data flows through layers of neurons
3. **Output:** Network makes a prediction
4. **Compare:** Check if prediction is correct
5. **Adjust:** If wrong, adjust the weights slightly
6. **Repeat:** Do this millions of times until predictions improve

**Simple Example:**
```
Input: Photo of a cat
↓
Hidden Layer 1: Detects edges
↓
Hidden Layer 2: Detects shapes (ears, whiskers)
↓
Hidden Layer 3: Combines shapes into features
↓
Output: "This is a cat!" (95% confidence)
```

**Real-World Analogy:**
Like a child learning to recognize animals:
- First time: "Is that a dog?" (wrong)
- Parent corrects: "No, cats have pointier ears"
- Child adjusts understanding
- After many examples, can recognize cats accurately

**Key Components:**
- **Neurons:** Simple math functions
- **Weights:** Numbers that get adjusted during learning
- **Activation Functions:** Add non-linearity (like ReLU, Sigmoid)
- **Backpropagation:** How the network learns from mistakes

**Code Example:**
```python
import numpy as np

# Simple neuron
def neuron(inputs, weights, bias):
    return sum(inputs * weights) + bias

# Example
inputs = np.array([1.0, 2.0, 3.0])
weights = np.array([0.5, -0.2, 0.1])
bias = 0.5

output = neuron(inputs, weights, bias)
print(output)  # 0.8
```

Neural networks are just this repeated thousands of times across many layers!"""
        },

        # Add more examples across different topics
        {
            "prompt": "What are design patterns and why are they important?",
            "response": """Design patterns are reusable solutions to common programming problems.

**Why Important:**
1. **Proven Solutions:** Battle-tested approaches
2. **Communication:** Shared vocabulary among developers
3. **Maintainability:** Cleaner, more organized code
4. **Scalability:** Easier to extend and modify

**Common Patterns:**

**1. Singleton:**
Ensure only one instance exists
```python
class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Always same instance
db1 = Database()
db2 = Database()
assert db1 is db2  # True
```

**2. Factory:**
Create objects without specifying exact class
```python
class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
```

**3. Observer:**
Notify multiple objects when state changes
```python
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def notify(self, data):
        for observer in self._observers:
            observer.update(data)
```

**When to Use:**
- Don't force patterns where they don't fit
- Use when problem matches pattern's intent
- Keep code simple - patterns should simplify, not complicate"""
        },
    ]


def get_validation_data() -> list[dict[str, str]]:
    """Get validation data for evaluating model performance."""
    return [
        {
            "prompt": "Write a function to calculate factorial",
            "response": """Here's a factorial function with recursion:

```python
def factorial(n: int) -> int:
    \"\"\"Calculate factorial of n.\"\"\"
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Or iterative:
def factorial_iterative(n: int) -> int:
    \"\"\"Calculate factorial iteratively.\"\"\"
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```"""
        },
        {
            "prompt": "Explain what REST API is",
            "response": """REST (Representational State Transfer) is an architectural style for web APIs:

**Key Principles:**
1. **Stateless:** Each request contains all needed information
2. **Client-Server:** Separation of concerns
3. **Uniform Interface:** Consistent way to interact with resources
4. **Cacheable:** Responses can be cached

**HTTP Methods:**
- **GET:** Retrieve data
- **POST:** Create new resource
- **PUT:** Update existing resource
- **DELETE:** Remove resource

**Example:**
```
GET /api/users/123      → Get user 123
POST /api/users         → Create new user
PUT /api/users/123      → Update user 123
DELETE /api/users/123   → Delete user 123
```"""
        },
    ]


# ============================================================================
# STEP 2: Load Custom Training Data (Optional)
# ============================================================================

def load_custom_data(file_path: str) -> list[dict[str, str]]:
    """Load training data from JSON file.

    Args:
        file_path: Path to JSON file with format:
            [{"prompt": "...", "response": "..."}, ...]

    Returns:
        List of training examples
    """
    path = Path(file_path)
    if not path.exists():
        logger.warning(f"File not found: {file_path}")
        return []

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    logger.info(f"Loaded {len(data)} examples from {file_path}")
    return data


# ============================================================================
# STEP 3: Training Function
# ============================================================================

async def train_model(
    model_name: str = "genius-ai-custom",
    base_model: str = "mistralai/Mistral-7B-Instruct-v0.2",
    custom_data_path: Optional[str] = None,
    num_epochs: int = 3,
):
    """Train a custom model.

    Args:
        model_name: Name for your custom model
        base_model: Base model to fine-tune
        custom_data_path: Optional path to your custom training data JSON
        num_epochs: Number of training epochs
    """
    logger.info("=" * 60)
    logger.info("TRAINING CUSTOM MODEL TO RIVAL OPENAI")
    logger.info("=" * 60)

    # Load training data
    if custom_data_path:
        logger.info(f"Loading custom data from: {custom_data_path}")
        training_data = load_custom_data(custom_data_path)
        if not training_data:
            logger.error("No custom data loaded, using sample data instead")
            training_data = get_sample_training_data()
    else:
        logger.info("Using sample training data")
        training_data = get_sample_training_data()

    validation_data = get_validation_data()

    logger.info(f"Training examples: {len(training_data)}")
    logger.info(f"Validation examples: {len(validation_data)}")

    # Configure model
    config = CustomModelConfig(
        base_model=base_model,
        use_lora=True,  # Efficient fine-tuning
        use_4bit=True,  # Memory efficient
        num_epochs=num_epochs,
        batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        output_dir=f"./custom_models/{model_name}",
    )

    logger.info(f"\nModel Configuration:")
    logger.info(f"  Base Model: {config.base_model}")
    logger.info(f"  LoRA: {config.use_lora}")
    logger.info(f"  4-bit Quantization: {config.use_4bit}")
    logger.info(f"  Epochs: {config.num_epochs}")
    logger.info(f"  Batch Size: {config.batch_size}")
    logger.info(f"  Learning Rate: {config.learning_rate}")

    # Initialize model
    logger.info("\n" + "=" * 60)
    logger.info("STEP 1: Initializing Model")
    logger.info("=" * 60)

    model = CustomIntelligentModel(
        model_name=model_name,
        config=config,
    )

    await model.initialize()

    # Test base model before training
    logger.info("\n" + "=" * 60)
    logger.info("STEP 2: Testing BASE Model (Before Training)")
    logger.info("=" * 60)

    test_prompt = "Write a Python function to reverse a list"
    logger.info(f"\nPrompt: {test_prompt}")
    logger.info("\nBase Model Response:")
    logger.info("-" * 60)

    base_response = await model.generate(test_prompt)
    print(base_response.text)

    logger.info("\n" + "=" * 60)
    logger.info("STEP 3: Training Model on Custom Data")
    logger.info("=" * 60)
    logger.info("\nThis may take 30 minutes to several hours depending on:")
    logger.info("  - Number of training examples")
    logger.info("  - Model size")
    logger.info("  - Hardware (GPU vs CPU)")
    logger.info("\nTraining started...\n")

    # Train!
    metrics = await model.train_on_custom_data(
        training_data=training_data,
        validation_data=validation_data,
    )

    logger.info("\n" + "=" * 60)
    logger.info("STEP 4: Training Complete!")
    logger.info("=" * 60)
    logger.info(f"\nTraining Metrics:")
    logger.info(f"  Final Loss: {metrics['training_loss']:.4f}")
    logger.info(f"  Epochs: {metrics['epochs_completed']}")
    logger.info(f"  Examples: {metrics['examples_trained']}")
    logger.info(f"  Saved to: {metrics['model_saved_to']}")

    # Test fine-tuned model
    logger.info("\n" + "=" * 60)
    logger.info("STEP 5: Testing FINE-TUNED Model (After Training)")
    logger.info("=" * 60)

    logger.info(f"\nPrompt: {test_prompt}")
    logger.info("\nFine-Tuned Model Response:")
    logger.info("-" * 60)

    finetuned_response = await model.generate(test_prompt)
    print(finetuned_response.text)

    logger.info("\n" + "=" * 60)
    logger.info("SUCCESS! Your Custom Model is Ready")
    logger.info("=" * 60)
    logger.info("\nWhat's Next:")
    logger.info("  1. Test your model with different prompts")
    logger.info("  2. Add more training data to improve further")
    logger.info("  3. Integrate with Genius AI (replace default model in server.py)")
    logger.info("  4. Deploy to production!")
    logger.info(f"\nYour model is saved at: {metrics['model_saved_to']}")
    logger.info("\nTo use it, initialize with:")
    logger.info(f'  model = CustomIntelligentModel(model_name="{model_name}")')
    logger.info("  await model.initialize()")

    # Cleanup
    await model.cleanup()


# ============================================================================
# STEP 4: Main Entry Point
# ============================================================================

async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Train a custom model to rival OpenAI"
    )
    parser.add_argument(
        "--name",
        default="genius-ai-custom",
        help="Name for your custom model",
    )
    parser.add_argument(
        "--base-model",
        default="mistralai/Mistral-7B-Instruct-v0.2",
        help="Base model to fine-tune",
    )
    parser.add_argument(
        "--data",
        help="Path to custom training data JSON file",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=3,
        help="Number of training epochs",
    )

    args = parser.parse_args()

    await train_model(
        model_name=args.name,
        base_model=args.base_model,
        custom_data_path=args.data,
        num_epochs=args.epochs,
    )


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    GENIUS AI - CUSTOM MODEL TRAINING                         ║
║    Build Your Own Model to Rival OpenAI                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    asyncio.run(main())
