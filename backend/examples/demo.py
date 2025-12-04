"""
Genius AI - Demo Script

This script demonstrates the core features of Genius AI.
Run this after starting the backend server.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from genius_ai.agents.orchestrator import OrchestratorAgent
from genius_ai.core.config import settings
from genius_ai.core.logger import logger
from genius_ai.memory.conversation import ConversationMemory, MessageRole
from genius_ai.models.base import ModelFactory, ModelType
from genius_ai.rag.retriever import RAGRetriever, Document


async def demo_basic_chat():
    """Demo: Basic chat with the model"""
    print("\n" + "=" * 60)
    print("DEMO 1: Basic Chat")
    print("=" * 60 + "\n")

    # Initialize model
    logger.info("Loading model...")
    model = ModelFactory.create(
        model_type=ModelType.MISTRAL,
        model_name=settings.base_model_name,
        device=settings.device,
    )
    await model.initialize()

    # Create orchestrator
    orchestrator = OrchestratorAgent(model=model, enable_reflection=True)

    # Ask a question
    question = "Explain the concept of machine learning in simple terms."
    print(f"User: {question}\n")

    response = await orchestrator.process(question)

    print(f"Assistant: {response.content}\n")
    print(f"Confidence: {response.confidence}")
    print(f"Thoughts: {len(response.thoughts)} agent thoughts")
    print(f"Metadata: {response.metadata}")

    # Cleanup
    await model.cleanup()


async def demo_multi_agent():
    """Demo: Multi-agent reasoning"""
    print("\n" + "=" * 60)
    print("DEMO 2: Multi-Agent Reasoning")
    print("=" * 60 + "\n")

    # Initialize model
    model = ModelFactory.create(
        model_type=ModelType.MISTRAL,
        model_name=settings.base_model_name,
        device=settings.device,
    )
    await model.initialize()

    orchestrator = OrchestratorAgent(model=model, enable_reflection=True)

    # Complex task
    task = (
        "I need to build a web application for task management. "
        "Help me analyze the requirements and create a development plan."
    )
    print(f"User: {task}\n")

    response = await orchestrator.process(task)

    print(f"Assistant Response:\n{response.content}\n")

    # Show agent thoughts
    print("\n--- Agent Thought Process ---")
    for i, thought in enumerate(response.thoughts, 1):
        print(f"{i}. [{thought.agent_role.value}] {thought.content}")

    # Cleanup
    await model.cleanup()


async def demo_rag_system():
    """Demo: RAG (Retrieval-Augmented Generation)"""
    print("\n" + "=" * 60)
    print("DEMO 3: RAG System (Knowledge Base)")
    print("=" * 60 + "\n")

    # Initialize RAG
    rag = RAGRetriever()
    await rag.initialize()

    # Add some documents
    documents = [
        Document(
            content="Python is a high-level, interpreted programming language known for its simplicity and readability. It was created by Guido van Rossum and first released in 1991.",
            metadata={"source": "python_docs", "category": "programming"},
        ),
        Document(
            content="Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.",
            metadata={"source": "ml_docs", "category": "AI"},
        ),
        Document(
            content="FastAPI is a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.",
            metadata={"source": "fastapi_docs", "category": "web"},
        ),
    ]

    print("Adding documents to knowledge base...")
    chunks_added = await rag.add_documents(documents)
    print(f"Added {chunks_added} document chunks\n")

    # Query the knowledge base
    query = "What is Python?"
    print(f"Query: {query}\n")

    results = await rag.retrieve(query, top_k=2)

    print("Retrieved Documents:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['document']}")
        print(f"   Relevance: {1 - result['distance']:.2%}")

    # Get formatted context
    context = await rag.retrieve_context(query, top_k=2)
    print(f"\n--- Formatted Context for Prompt ---\n{context}\n")


async def demo_memory_system():
    """Demo: Conversation memory"""
    print("\n" + "=" * 60)
    print("DEMO 4: Conversation Memory")
    print("=" * 60 + "\n")

    # Create conversation memory
    memory = ConversationMemory(
        max_messages=10,
        system_prompt="You are a helpful assistant specialized in explaining technical concepts.",
    )

    # Simulate a conversation
    conversations = [
        ("user", "What is Python?"),
        ("assistant", "Python is a high-level programming language..."),
        ("user", "What are its main features?"),
        ("assistant", "Python has several key features: simplicity, readability..."),
        ("user", "Can you give an example?"),
    ]

    for role, content in conversations:
        if role == "user":
            memory.add_user_message(content)
        else:
            memory.add_assistant_message(content)

    # Get formatted history
    history = memory.get_formatted_history()

    print("Conversation History:")
    for msg in history:
        print(f"\n{msg['role'].upper()}: {msg['content']}")

    # Get statistics
    stats = memory.get_stats()
    print(f"\n--- Memory Statistics ---")
    print(f"Total messages: {stats['total_messages']}")
    print(f"User messages: {stats['user_messages']}")
    print(f"Assistant messages: {stats['assistant_messages']}")


async def demo_streaming():
    """Demo: Streaming responses"""
    print("\n" + "=" * 60)
    print("DEMO 5: Streaming Responses")
    print("=" * 60 + "\n")

    # Initialize model
    model = ModelFactory.create(
        model_type=ModelType.MISTRAL,
        model_name=settings.base_model_name,
        device=settings.device,
    )
    await model.initialize()

    # Create a prompt
    prompt = "Write a short poem about artificial intelligence."
    print(f"Prompt: {prompt}\n")
    print("Response (streaming): ", end="", flush=True)

    # Stream response
    async for chunk in model.generate_stream(prompt):
        print(chunk, end="", flush=True)

    print("\n")

    # Cleanup
    await model.cleanup()


async def demo_complete_workflow():
    """Demo: Complete workflow with all features"""
    print("\n" + "=" * 60)
    print("DEMO 6: Complete Workflow")
    print("=" * 60 + "\n")

    # Initialize components
    model = ModelFactory.create(
        model_type=ModelType.MISTRAL,
        model_name=settings.base_model_name,
        device=settings.device,
    )
    await model.initialize()

    orchestrator = OrchestratorAgent(model=model, enable_reflection=True)
    memory = ConversationMemory()
    rag = RAGRetriever()
    await rag.initialize()

    # Add knowledge
    print("1. Adding knowledge to RAG system...")
    knowledge = Document(
        content="Genius AI is an advanced conversational AI system with multi-agent reasoning, RAG, and advanced memory systems.",
        metadata={"source": "system_docs"},
    )
    await rag.add_documents([knowledge])

    # User asks a question
    user_message = "Tell me about Genius AI and how it uses multiple agents."
    print(f"\n2. User asks: {user_message}")

    memory.add_user_message(user_message)

    # Retrieve relevant knowledge
    print("\n3. Retrieving relevant knowledge from RAG...")
    context = await rag.retrieve_context(user_message)

    # Process with orchestrator
    print("\n4. Processing with multi-agent orchestrator...")
    response = await orchestrator.process(
        user_message, context={"knowledge": context, "history": memory.get_formatted_history()}
    )

    # Add response to memory
    memory.add_assistant_message(response.content)

    # Display results
    print(f"\n5. Response:\n{response.content}")

    print(f"\n6. Metadata:")
    print(f"   - Confidence: {response.confidence}")
    print(f"   - Agents involved: {len(response.thoughts)}")
    print(f"   - Memory size: {len(memory.get_messages())} messages")

    # Cleanup
    await model.cleanup()


async def main():
    """Run all demos"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 16 + "GENIUS AI - DEMO" + " " * 26 + "║")
    print("║" + " " * 10 + "Advanced Conversational AI System" + " " * 15 + "║")
    print("╚" + "═" * 58 + "╝")

    demos = [
        ("Basic Chat", demo_basic_chat),
        ("Multi-Agent Reasoning", demo_multi_agent),
        ("RAG System", demo_rag_system),
        ("Memory System", demo_memory_system),
        ("Streaming", demo_streaming),
        ("Complete Workflow", demo_complete_workflow),
    ]

    print("\nAvailable Demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"{i}. {name}")
    print(f"{len(demos) + 1}. Run all demos")

    try:
        choice = input("\nSelect demo (1-7): ").strip()

        if choice == str(len(demos) + 1):
            # Run all demos
            for name, demo_func in demos:
                try:
                    await demo_func()
                    input("\nPress Enter to continue to next demo...")
                except Exception as e:
                    logger.error(f"Error in {name}: {e}")
                    print(f"\nError in {name}: {e}")
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            # Run selected demo
            name, demo_func = demos[int(choice) - 1]
            await demo_func()
        else:
            print("Invalid choice")

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        logger.error(f"Demo error: {e}")
        print(f"\nError: {e}")

    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
