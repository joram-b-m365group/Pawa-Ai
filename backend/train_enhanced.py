"""Enhanced training script with comprehensive dataset.

This version includes 50+ high-quality training examples covering:
- Python programming
- General knowledge
- Science and technology
- Business and entrepreneurship
- Problem solving
- How-to questions
"""

import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Training data - 50+ diverse examples
TRAINING_DATA = [
    # Python Programming (15 examples)
    {
        "prompt": "What is Python?",
        "response": "Python is a high-level, interpreted programming language known for its simplicity and readability. Created by Guido van Rossum in 1991, Python emphasizes code readability with significant whitespace. It supports multiple programming paradigms including procedural, object-oriented, and functional programming. Python is widely used for web development, data science, artificial intelligence, automation, and scientific computing."
    },
    {
        "prompt": "How do I define a function in Python?",
        "response": "To define a function in Python, use the 'def' keyword followed by the function name and parentheses. Example: def greet(name): return f'Hello, {name}!' Functions can accept parameters, have default values, and return results. You can also create lambda functions for simple operations: lambda x: x * 2."
    },
    {
        "prompt": "What are Python variables?",
        "response": "Variables in Python are containers for storing data values. Python is dynamically typed, so you don't need to declare variable types. Examples: name = 'Alice', age = 25, price = 19.99. Variables can be reassigned and their types can change during execution."
    },
    {
        "prompt": "How do Python lists work?",
        "response": "Lists in Python are ordered, mutable collections that can hold mixed data types. Create a list with square brackets: numbers = [1, 2, 3, 4]. Access elements by index: numbers[0] returns 1. Lists support methods like append(), remove(), sort(), and can be sliced: numbers[1:3]."
    },
    {
        "prompt": "What are Python dictionaries?",
        "response": "Dictionaries are unordered collections of key-value pairs. Create with curly braces: person = {'name': 'Bob', 'age': 30}. Access values using keys: person['name'] returns 'Bob'. Dictionaries are mutable and support methods like keys(), values(), items(), and get()."
    },
    {
        "prompt": "How do I use if statements in Python?",
        "response": "If statements control program flow based on conditions. Syntax: if condition: do_something elif other_condition: do_other_thing else: default_action. Python uses indentation to define code blocks. You can combine conditions with 'and', 'or', and 'not' operators."
    },
    {
        "prompt": "What are Python loops?",
        "response": "Python has two main loop types: 'for' and 'while'. For loops iterate over sequences: for item in list: print(item). While loops run until a condition is false: while x < 10: x += 1. Use 'break' to exit loops early and 'continue' to skip iterations."
    },
    {
        "prompt": "How do I handle errors in Python?",
        "response": "Use try-except blocks to handle errors gracefully. Syntax: try: risky_operation() except ValueError: handle_error() except Exception as e: handle_any_error(e) finally: cleanup(). This prevents program crashes and allows for error recovery."
    },
    {
        "prompt": "What are Python classes?",
        "response": "Classes are blueprints for creating objects. Define with 'class' keyword: class Dog: def __init__(self, name): self.name = name. Classes encapsulate data (attributes) and behavior (methods). Create instances: my_dog = Dog('Rex'). Supports inheritance and polymorphism."
    },
    {
        "prompt": "How do I read files in Python?",
        "response": "Use the open() function with 'with' statement for safe file handling: with open('file.txt', 'r') as f: content = f.read(). Modes include 'r' (read), 'w' (write), 'a' (append). The file closes automatically after the block."
    },
    {
        "prompt": "What are Python modules?",
        "response": "Modules are Python files containing functions, classes, and variables. Import with: import math or from math import sqrt. Create your own by saving code in .py files. Modules organize code and enable reusability across projects."
    },
    {
        "prompt": "How do I use Python strings?",
        "response": "Strings are sequences of characters enclosed in quotes. Create with single, double, or triple quotes for multi-line. Support methods like upper(), lower(), split(), replace(). Format with f-strings: f'Hello {name}' or .format() method."
    },
    {
        "prompt": "What are list comprehensions?",
        "response": "List comprehensions provide concise ways to create lists. Syntax: [expression for item in iterable if condition]. Example: squares = [x**2 for x in range(10)] creates a list of squares. More readable and faster than traditional loops."
    },
    {
        "prompt": "How do I install Python packages?",
        "response": "Use pip, Python's package manager. Command: pip install package_name. Install specific versions: pip install package==1.2.3. List installed packages: pip list. Upgrade packages: pip install --upgrade package_name. Use virtual environments to isolate dependencies."
    },
    {
        "prompt": "What is Python pandas?",
        "response": "Pandas is a powerful data analysis library. Provides DataFrame and Series structures for working with tabular data. Import with: import pandas as pd. Create DataFrame: df = pd.DataFrame(data). Offers functions for filtering, grouping, merging, and analyzing data efficiently."
    },

    # General Knowledge (10 examples)
    {
        "prompt": "What is artificial intelligence?",
        "response": "Artificial Intelligence (AI) is the simulation of human intelligence by machines. It includes machine learning, where systems learn from data, natural language processing for understanding text and speech, computer vision for analyzing images, and robotics. AI powers applications like virtual assistants, recommendation systems, autonomous vehicles, and medical diagnosis."
    },
    {
        "prompt": "How does the internet work?",
        "response": "The internet is a global network of interconnected computers. Data travels in packets through routers and switches using protocols like TCP/IP. DNS servers translate domain names to IP addresses. When you visit a website, your browser sends requests to servers, which respond with HTML, CSS, and JavaScript to display the page."
    },
    {
        "prompt": "What is machine learning?",
        "response": "Machine learning is a subset of AI where algorithms learn patterns from data without explicit programming. Types include supervised learning (labeled data), unsupervised learning (finding patterns), and reinforcement learning (learning through rewards). Used for predictions, classifications, clustering, and decision-making."
    },
    {
        "prompt": "What is cloud computing?",
        "response": "Cloud computing delivers computing services (servers, storage, databases, software) over the internet. Benefits include scalability, cost-efficiency, and accessibility. Main models: IaaS (Infrastructure), PaaS (Platform), SaaS (Software). Major providers include AWS, Azure, and Google Cloud."
    },
    {
        "prompt": "How do databases work?",
        "response": "Databases organize and store data for efficient retrieval. Relational databases (SQL) use tables with rows and columns, connected by relationships. NoSQL databases handle unstructured data. Databases support CRUD operations (Create, Read, Update, Delete) and use queries to access data."
    },
    {
        "prompt": "What is blockchain?",
        "response": "Blockchain is a distributed ledger technology that records transactions in blocks linked cryptographically. Each block contains data, a hash, and the previous block's hash. It's decentralized, immutable, and transparent. Used for cryptocurrencies, smart contracts, and supply chain tracking."
    },
    {
        "prompt": "What is cybersecurity?",
        "response": "Cybersecurity protects systems, networks, and data from digital attacks. Includes measures like firewalls, encryption, authentication, and intrusion detection. Key principles: confidentiality, integrity, availability. Common threats include malware, phishing, ransomware, and DDoS attacks."
    },
    {
        "prompt": "How do APIs work?",
        "response": "APIs (Application Programming Interfaces) allow different software systems to communicate. They define methods for requesting and exchanging data. REST APIs use HTTP methods (GET, POST, PUT, DELETE) and return JSON or XML. Enable integration between services and third-party applications."
    },
    {
        "prompt": "What is data science?",
        "response": "Data science extracts insights from data using statistics, machine learning, and programming. Process includes data collection, cleaning, exploration, modeling, and visualization. Data scientists use tools like Python, R, SQL, and frameworks like TensorFlow and scikit-learn for analysis and predictions."
    },
    {
        "prompt": "What is agile methodology?",
        "response": "Agile is an iterative approach to software development emphasizing flexibility, collaboration, and customer feedback. Uses short sprints (1-4 weeks), daily standups, and continuous improvement. Popular frameworks include Scrum and Kanban. Delivers working software incrementally rather than all at once."
    },

    # Business and Entrepreneurship (10 examples)
    {
        "prompt": "How do I start a business?",
        "response": "Starting a business involves: 1) Identify a problem to solve, 2) Validate demand through market research, 3) Create a business plan, 4) Choose a legal structure (LLC, corporation), 5) Register your business, 6) Set up finances and accounting, 7) Build your product/service, 8) Market to customers, 9) Launch and iterate based on feedback."
    },
    {
        "prompt": "What is a business model?",
        "response": "A business model describes how a company creates, delivers, and captures value. Key components include target customers, value proposition, revenue streams, cost structure, and key resources. Examples: subscription (Netflix), marketplace (Amazon), freemium (Spotify), advertising (Google)."
    },
    {
        "prompt": "How do I price my product?",
        "response": "Pricing strategies include: cost-plus (cost + markup), value-based (perceived value), competitive (market rates), and penetration (low initial price). Consider production costs, target market, positioning, and profit margins. Test different price points and adjust based on customer response and data."
    },
    {
        "prompt": "What is marketing?",
        "response": "Marketing promotes products/services to target audiences. Includes market research, branding, advertising, content creation, social media, email campaigns, and SEO. Focus on understanding customer needs, creating compelling messages, choosing right channels, and measuring ROI. Digital marketing is cost-effective for startups."
    },
    {
        "prompt": "How do I get customers?",
        "response": "Customer acquisition strategies: 1) Content marketing (blogs, videos), 2) Social media engagement, 3) SEO for organic traffic, 4) Paid advertising (Google Ads, Facebook), 5) Partnerships and affiliates, 6) Referral programs, 7) Direct outreach, 8) Events and networking. Track metrics like CAC (Customer Acquisition Cost) and LTV (Lifetime Value)."
    },
    {
        "prompt": "What is a SaaS business?",
        "response": "SaaS (Software as a Service) delivers software via the internet on a subscription basis. Benefits include recurring revenue, scalability, and automatic updates. Customers access software through browsers without installation. Examples: Salesforce, Slack, Zoom. Key metrics: MRR, churn rate, CAC payback period."
    },
    {
        "prompt": "How do I raise funding?",
        "response": "Funding options: 1) Bootstrapping (self-funding), 2) Friends and family, 3) Angel investors, 4) Venture capital, 5) Crowdfunding, 6) Bank loans, 7) Grants. Prepare a pitch deck showing problem, solution, market size, traction, team, and financials. Each option has tradeoffs in control, dilution, and requirements."
    },
    {
        "prompt": "What is product-market fit?",
        "response": "Product-market fit occurs when your product satisfies strong market demand. Signs include: organic growth, high retention, customers actively recommend you, willing to pay, and engagement metrics improving. Achieve by deeply understanding customer pain points, iterating based on feedback, and focusing on core value proposition."
    },
    {
        "prompt": "How do I scale a business?",
        "response": "Scaling strategies: 1) Automate repetitive tasks, 2) Build systems and processes, 3) Hire the right team, 4) Increase marketing while maintaining ROI, 5) Expand to new markets or products, 6) Improve unit economics, 7) Raise capital for growth. Focus on sustainable, profitable growth rather than growth at all costs."
    },
    {
        "prompt": "What is revenue model?",
        "response": "Revenue models define how a business makes money. Common types: subscription (recurring payments), transaction fees (percentage per sale), licensing (pay for usage rights), advertising (sell ad space), freemium (free basic + paid premium), affiliate (commissions), and consulting (hourly/project fees)."
    },

    # Problem Solving (8 examples)
    {
        "prompt": "How do I debug code?",
        "response": "Debugging process: 1) Reproduce the bug consistently, 2) Use print statements or debugger to inspect values, 3) Check error messages and stack traces, 4) Isolate the problem by testing sections, 5) Review recent changes, 6) Search for similar issues online, 7) Use debugging tools (breakpoints, watch variables), 8) Fix and test thoroughly."
    },
    {
        "prompt": "How do I learn programming?",
        "response": "Learning path: 1) Choose a beginner-friendly language (Python), 2) Learn basics (variables, loops, functions), 3) Build small projects, 4) Read others' code, 5) Practice on platforms like LeetCode, 6) Build real projects solving actual problems, 7) Join coding communities, 8) Stay consistent and patient. Focus on understanding concepts over memorization."
    },
    {
        "prompt": "How do I optimize code performance?",
        "response": "Performance optimization: 1) Profile code to find bottlenecks, 2) Use efficient data structures and algorithms, 3) Minimize database queries, 4) Cache frequently used data, 5) Use async/await for I/O operations, 6) Reduce nested loops, 7) Optimize database indices, 8) Consider parallel processing. Measure before and after optimizations."
    },
    {
        "prompt": "How do I solve algorithm problems?",
        "response": "Problem-solving approach: 1) Understand the problem fully, 2) Identify patterns and similar problems, 3) Consider multiple approaches, 4) Start with brute force, then optimize, 5) Use appropriate data structures, 6) Write pseudocode first, 7) Test with edge cases, 8) Analyze time and space complexity."
    },
    {
        "prompt": "How do I manage technical debt?",
        "response": "Managing technical debt: 1) Document debt as you create it, 2) Prioritize based on impact and effort, 3) Allocate time each sprint for refactoring, 4) Write tests before refactoring, 5) Refactor in small, safe increments, 6) Balance new features with code quality, 7) Prevent new debt through code reviews and standards."
    },
    {
        "prompt": "How do I choose a tech stack?",
        "response": "Tech stack selection criteria: 1) Project requirements and constraints, 2) Team expertise and learning curve, 3) Community support and documentation, 4) Scalability needs, 5) Performance requirements, 6) Available libraries and tools, 7) Hosting and deployment options, 8) Long-term maintenance. Popular stacks: MERN, MEAN, Django, Rails."
    },
    {
        "prompt": "How do I design system architecture?",
        "response": "Architecture design process: 1) Understand requirements (functional and non-functional), 2) Identify main components and responsibilities, 3) Define communication patterns, 4) Consider scalability and fault tolerance, 5) Choose appropriate databases, 6) Plan for security, 7) Document architecture diagrams, 8) Review with team. Use patterns like microservices, MVC, event-driven."
    },
    {
        "prompt": "How do I conduct code reviews?",
        "response": "Effective code reviews: 1) Check for correctness and logic errors, 2) Verify tests are included, 3) Ensure code follows style guidelines, 4) Look for security vulnerabilities, 5) Suggest performance improvements, 6) Provide constructive feedback, 7) Praise good solutions, 8) Keep reviews timely and focused. Be respectful and collaborative."
    },

    # Science and Technology (7 examples)
    {
        "prompt": "How does neural network work?",
        "response": "Neural networks are computing systems inspired by biological brains. They consist of layers of interconnected nodes (neurons). Each connection has a weight that adjusts during training. Input data flows through hidden layers, where mathematical transformations occur, to produce output. Backpropagation adjusts weights to minimize error. Used for pattern recognition, predictions, and classification."
    },
    {
        "prompt": "What is quantum computing?",
        "response": "Quantum computing uses quantum mechanics principles to process information. Unlike classical bits (0 or 1), qubits can exist in superposition (both states simultaneously). Quantum entanglement allows qubits to correlate. This enables parallel processing of vast possibilities. Potential applications: cryptography, drug discovery, optimization, and AI. Still in early development stages."
    },
    {
        "prompt": "How does encryption work?",
        "response": "Encryption converts readable data (plaintext) into scrambled format (ciphertext) using algorithms and keys. Symmetric encryption uses the same key for encryption and decryption (AES). Asymmetric uses public-private key pairs (RSA). Common uses: secure communications, data storage, authentication. Encryption strength depends on algorithm and key length."
    },
    {
        "prompt": "What is version control?",
        "response": "Version control tracks changes to files over time. Git is the most popular system. Benefits: collaboration, history tracking, branching for features, rollback to previous versions, and conflict resolution. Key concepts: commits (snapshots), branches (parallel development), merges (combining changes), and remote repositories (GitHub, GitLab)."
    },
    {
        "prompt": "How do containers work?",
        "response": "Containers package applications with dependencies into isolated units. Docker is the leading platform. Containers share the host OS kernel but have separate file systems and processes. Benefits: consistency across environments, faster deployment, resource efficiency, and scalability. Used with orchestration tools like Kubernetes for managing multiple containers."
    },
    {
        "prompt": "What is CI/CD?",
        "response": "CI/CD automates software delivery. Continuous Integration (CI) automatically builds and tests code changes. Continuous Deployment (CD) automatically releases to production. Benefits: faster releases, fewer bugs, rapid feedback. Popular tools: Jenkins, GitLab CI, GitHub Actions, CircleCI. Includes automated testing, building, and deployment pipelines."
    },
    {
        "prompt": "How does DNS work?",
        "response": "DNS (Domain Name System) translates domain names to IP addresses. When you visit a website: 1) Browser checks cache, 2) Queries DNS resolver, 3) Resolver queries root servers, 4) Directed to TLD servers, 5) Finally to authoritative nameserver, 6) IP address returned, 7) Browser connects to server. Acts as the internet's phonebook."
    }
]

print("=" * 70)
print("GENIUS AI - ENHANCED MODEL TRAINING")
print("=" * 70)
print(f"\nDataset: {len(TRAINING_DATA)} high-quality examples")
print("Topics: Python, AI, Business, Problem Solving, Technology")
print("\nThis training will make your model MUCH smarter!")
print("=" * 70)

# Continue with existing training code
print("\n[1/6] Installing dependencies...")

try:
    import torch
    print("  torch: OK")
except ImportError:
    print("  torch: installing...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "torch"], check=True)
    import torch

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
    print("  transformers: OK")
except ImportError:
    print("  transformers: installing...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "transformers"], check=True)
    from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments

try:
    from datasets import Dataset
    print("  datasets: OK")
except ImportError:
    print("  datasets: installing...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "datasets"], check=True)
    from datasets import Dataset

print(f"\nPyTorch {torch.__version__} ready (CPU mode)")

print(f"\n[2/6] Loading training data...")
print(f"Loaded {len(TRAINING_DATA)} examples")

# Format data for training
formatted_data = []
for item in TRAINING_DATA:
    text = f"Q: {item['prompt']}\nA: {item['response']}"
    formatted_data.append({"text": text})

print("\n[3/6] Loading model (DistilGPT-2, 82M parameters)...")
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name)
print("Model loaded (300MB)")

print("\n[4/6] Preparing dataset...")
dataset = Dataset.from_list(formatted_data)

def tokenize(examples):
    result = tokenizer(
        examples["text"],
        truncation=True,
        max_length=512,
        padding="max_length"
    )
    result["labels"] = result["input_ids"].copy()
    return result

tokenized_dataset = dataset.map(tokenize, batched=True, remove_columns=["text"])
print(f"Dataset ready ({len(tokenized_dataset)} examples)")

print("\n[5/6] Testing BASE model (before training):")
print("-" * 70)
test_prompt = "Q: What is Python?\nA:"
inputs = tokenizer(test_prompt, return_tensors="pt")
with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=50, pad_token_id=tokenizer.eos_token_id)
generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"Q: What is Python?")
print(f"A: {generated[len(test_prompt):].strip()}")
print("-" * 70)

print("\nTraining started (this takes 5-10 minutes on CPU)...")
print("With 50+ examples, your model will be MUCH smarter!\n")

training_args = TrainingArguments(
    output_dir="./genius_model_enhanced",
    num_train_epochs=5,  # More epochs for better learning
    per_device_train_batch_size=1,
    save_strategy="epoch",
    logging_steps=5,
    no_cuda=True,  # CPU mode
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

result = trainer.train()
print(f"\nTraining complete! Final loss: {result.training_loss:.4f}")

# Save the model
output_dir = "./genius_model_enhanced"
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
print(f"Model saved to: {output_dir}")

print(f"\n[6/6] Testing ENHANCED model (after training):")
print("-" * 70)

# Test multiple questions
test_questions = [
    "What is Python?",
    "How do I start a business?",
    "What is machine learning?",
    "How do I debug code?"
]

for question in test_questions:
    test_prompt = f"Q: {question}\nA:"
    inputs = tokenizer(test_prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = generated[len(test_prompt):].strip()
    print(f"Q: {question}")
    print(f"A: {response}\n")

print("-" * 70)

print("\n" + "=" * 70)
print("SUCCESS! Your ENHANCED AI model is trained!")
print("=" * 70)
print(f"\nTraining Summary:")
print(f"  Dataset: {len(TRAINING_DATA)} diverse examples")
print(f"  Final Loss: {result.training_loss:.4f}")
print(f"  Epochs: 5")
print(f"  Model Size: ~313MB")
print(f"  Topics: Python, AI, Business, Tech, Problem-solving")
print(f"  Location: {output_dir}/")
print(f"\nYour model is now MUCH smarter and can answer questions about:")
print("  - Python programming")
print("  - AI and machine learning")
print("  - Business and entrepreneurship")
print("  - Problem solving")
print("  - Science and technology")
print("\nTo use your enhanced model:")
print("  python backend/ask_model.py")
print("\n" + "=" * 70)
