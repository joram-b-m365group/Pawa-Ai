"""
Model Fine-Tuning Pipeline
Fine-tune models on custom data to make them smarter in specific domains
"""

import json
from typing import List, Dict, Any
from pathlib import Path


class FineTuner:
    """
    Fine-tune AI models on custom data

    This system allows you to:
    1. Prepare training data
    2. Fine-tune models using Ollama's modelfile system
    3. Create specialized expert models
    """

    def __init__(self, base_model: str = "llama3.2"):
        self.base_model = base_model
        self.training_data_dir = Path("data/training")
        self.training_data_dir.mkdir(parents=True, exist_ok=True)

    def prepare_training_data(
        self,
        examples: List[Dict[str, str]],
        dataset_name: str
    ) -> str:
        """
        Prepare training data in the correct format

        Args:
            examples: List of {"prompt": ..., "response": ...} dicts
            dataset_name: Name for this dataset

        Returns:
            Path to saved training data
        """
        # Convert to training format
        training_data = []
        for example in examples:
            training_data.append({
                "prompt": example["prompt"],
                "response": example["response"]
            })

        # Save to file
        output_file = self.training_data_dir / f"{dataset_name}.jsonl"
        with open(output_file, 'w') as f:
            for item in training_data:
                f.write(json.dumps(item) + '\n')

        return str(output_file)

    def create_modelfile(
        self,
        model_name: str,
        system_prompt: str,
        temperature: float = 0.8,
        training_data_path: Optional[str] = None
    ) -> str:
        """
        Create a Modelfile for custom model

        Args:
            model_name: Name for the new model
            system_prompt: System instructions for the model
            temperature: Default temperature
            training_data_path: Optional path to training data

        Returns:
            Path to Modelfile
        """
        modelfile_content = f"""FROM {self.base_model}

# System prompt that defines the model's personality and expertise
SYSTEM \"\"\"
{system_prompt}
\"\"\"

# Parameters
PARAMETER temperature {temperature}
PARAMETER top_p 0.9
PARAMETER top_k 40
"""

        # Save Modelfile
        modelfile_path = self.training_data_dir / f"Modelfile.{model_name}"
        with open(modelfile_path, 'w') as f:
            f.write(modelfile_content)

        return str(modelfile_path)

    def create_medical_expert(self) -> Dict[str, str]:
        """
        Example: Create a medical expert model

        Returns:
            Instructions to create the model
        """
        system_prompt = """You are a medical expert AI with deep knowledge of:
- Human anatomy and physiology
- Diseases and conditions
- Medical treatments and procedures
- Pharmacology and drug interactions
- Medical research and evidence-based medicine

Provide accurate, helpful medical information while reminding users to consult healthcare professionals for personal medical advice.
Use clear, accessible language while maintaining medical accuracy."""

        modelfile_path = self.create_modelfile(
            model_name="medical-expert",
            system_prompt=system_prompt,
            temperature=0.7  # Lower for medical accuracy
        )

        return {
            "model_name": "medical-expert",
            "modelfile_path": modelfile_path,
            "ollama_command": f"ollama create medical-expert -f {modelfile_path}",
            "usage": "ollama run medical-expert"
        }

    def create_coding_expert(self, languages: List[str] = None) -> Dict[str, str]:
        """
        Example: Create a coding expert model

        Args:
            languages: Programming languages to specialize in

        Returns:
            Instructions to create the model
        """
        langs = languages or ["Python", "JavaScript", "Java", "C++"]
        lang_list = ", ".join(langs)

        system_prompt = f"""You are an expert software engineer specializing in {lang_list}.

You provide:
- Clean, production-quality code
- Best practices and design patterns
- Performance optimizations
- Security considerations
- Detailed explanations

You write code that is:
- Readable and well-documented
- Efficient and optimized
- Secure and robust
- Following industry standards"""

        modelfile_path = self.create_modelfile(
            model_name="code-expert",
            system_prompt=system_prompt,
            temperature=0.4  # Lower for code precision
        )

        return {
            "model_name": "code-expert",
            "modelfile_path": modelfile_path,
            "ollama_command": f"ollama create code-expert -f {modelfile_path}",
            "usage": "ollama run code-expert"
        }

    def create_creative_writer(self) -> Dict[str, str]:
        """
        Example: Create a creative writing expert

        Returns:
            Instructions to create the model
        """
        system_prompt = """You are a masterful creative writer and storyteller.

You excel at:
- Crafting compelling narratives
- Creating vivid characters
- Writing beautiful prose and poetry
- Developing engaging plots
- Using literary devices effectively

Your writing is:
- Emotionally resonant
- Imaginative and original
- Well-structured
- Engaging and memorable"""

        modelfile_path = self.create_modelfile(
            model_name="creative-writer",
            system_prompt=system_prompt,
            temperature=0.95  # Higher for creativity
        )

        return {
            "model_name": "creative-writer",
            "modelfile_path": modelfile_path,
            "ollama_command": f"ollama create creative-writer -f {modelfile_path}",
            "usage": "ollama run creative-writer"
        }

    def create_custom_expert(
        self,
        name: str,
        expertise: str,
        qualities: List[str],
        temperature: float = 0.8
    ) -> Dict[str, str]:
        """
        Create a custom expert model

        Args:
            name: Model name (lowercase, hyphens for spaces)
            expertise: What the model is expert in
            qualities: List of qualities/characteristics
            temperature: Creativity level

        Returns:
            Instructions to create the model
        """
        qualities_text = "\n- ".join(qualities)

        system_prompt = f"""You are an expert in {expertise}.

Your key qualities:
- {qualities_text}

Provide expert-level assistance in your domain while being clear, helpful, and accurate."""

        modelfile_path = self.create_modelfile(
            model_name=name,
            system_prompt=system_prompt,
            temperature=temperature
        )

        return {
            "model_name": name,
            "modelfile_path": modelfile_path,
            "ollama_command": f"ollama create {name} -f {modelfile_path}",
            "usage": f"ollama run {name}"
        }

    def get_fine_tuning_guide(self) -> str:
        """
        Get comprehensive guide for fine-tuning models

        Returns:
            Markdown guide
        """
        return """# Fine-Tuning Guide

## Quick Start

### 1. Create a Custom Model (Easy Way)

```bash
# Create a medical expert
ollama create medical-expert -f path/to/Modelfile.medical-expert

# Create a coding expert
ollama create code-expert -f path/to/Modelfile.code-expert

# Use your custom model
ollama run medical-expert
```

### 2. Advanced: Fine-Tune on Your Data

#### Step 1: Prepare Training Data

Create a file `training_data.jsonl` with your examples:

```json
{"prompt": "What is photosynthesis?", "response": "Photosynthesis is the process..."}
{"prompt": "Explain quantum entanglement", "response": "Quantum entanglement is..."}
```

#### Step 2: Create a Modelfile

```dockerfile
FROM llama3.2

# Your custom system prompt
SYSTEM "You are an expert in biology..."

# Optional: Add training examples as context
```

#### Step 3: Create the Model

```bash
ollama create my-expert -f Modelfile
```

### 3. Tips for Best Results

**System Prompts:**
- Be specific about expertise
- Define personality and style
- Set clear guidelines
- Include examples of good responses

**Temperature Settings:**
- 0.3-0.4: Factual, precise (medical, legal, code)
- 0.7-0.8: Balanced (general use)
- 0.9-1.0: Creative (writing, brainstorming)

**Training Data:**
- Quality > Quantity
- Diverse examples
- Consistent format
- Representative of use cases

### 4. Testing Your Model

```bash
# Test interactively
ollama run my-expert

# Test with API
curl http://localhost:11434/api/generate -d '{
  "model": "my-expert",
  "prompt": "your test question"
}'
```

## Pre-Built Expert Models

Use the FineTuner class to create expert models:

```python
from ultimate_ai.training import FineTuner

tuner = FineTuner()

# Create experts
medical = tuner.create_medical_expert()
coding = tuner.create_coding_expert(["Python", "JavaScript"])
writer = tuner.create_creative_writer()

# Or create your own
custom = tuner.create_custom_expert(
    name="physics-tutor",
    expertise="physics education",
    qualities=[
        "Patient and encouraging",
        "Uses clear explanations",
        "Provides step-by-step solutions",
        "Makes physics fun and accessible"
    ],
    temperature=0.7
)

# Then run the command it gives you
print(custom["ollama_command"])
```

## Advanced: Multi-Step Fine-Tuning

For truly specialized models:

1. Start with base model (llama3.2)
2. Fine-tune on domain data
3. Further specialize with examples
4. Iterate and improve

This creates models that are MORE intelligent than ChatGPT in your specific domain!
"""


from typing import Optional


# Make it easy to use
if __name__ == "__main__":
    tuner = FineTuner()

    # Create example experts
    print("Creating Expert Models...\n")

    medical = tuner.create_medical_expert()
    print(f"Medical Expert: {medical['ollama_command']}\n")

    coding = tuner.create_coding_expert()
    print(f"Coding Expert: {coding['ollama_command']}\n")

    writer = tuner.create_creative_writer()
    print(f"Creative Writer: {writer['ollama_command']}\n")

    print("\nRun these commands to create your expert models!")
    print("\nFor the full guide, see:")
    print(tuner.get_fine_tuning_guide())
