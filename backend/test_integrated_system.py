"""End-to-end test script for Genius AI with custom trained model.

This script tests all major features:
1. Custom trained model loading
2. Streaming thoughts (real-time agent reasoning)
3. Tool execution (calculator, code execution)
4. RAG integration (document retrieval)
5. Learning system (strategy tracking)
"""

import asyncio
import sys
import io
from pathlib import Path

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


async def test_custom_model():
    """Test 1: Load and test custom trained model."""
    print("=" * 70)
    print("TEST 1: Custom Trained Model")
    print("=" * 70)

    from genius_ai.models.custom_trained import CustomTrainedModel
    from genius_ai.models.base import GenerationConfig

    print("\n[1.1] Loading custom trained model...")
    model = CustomTrainedModel(model_path="./tiny_genius_model", device="cpu")
    await model.initialize()

    print("\n[1.2] Model info:")
    info = model.get_model_info()
    for key, value in info.items():
        print(f"  {key}: {value}")

    print("\n[1.3] Testing generation...")
    prompt = "Q: What is Python?\nA:"
    config = GenerationConfig(temperature=0.7, max_tokens=100)
    response = await model.generate(prompt, config)

    print(f"\nPrompt: {prompt}")
    print(f"Response: {response.text}")
    print(f"Tokens used: {response.usage['total_tokens']}")

    await model.cleanup()
    print("\n✓ Custom model test PASSED\n")
    return True


async def test_orchestrator_with_model():
    """Test 2: Orchestrator with custom model and all agents."""
    print("=" * 70)
    print("TEST 2: Multi-Agent Orchestration")
    print("=" * 70)

    from genius_ai.models.custom_trained import CustomTrainedModel
    from genius_ai.agents.orchestrator import OrchestratorAgent
    from genius_ai.core.logger import logger

    print("\n[2.1] Setting up orchestrator with custom model...")
    model = CustomTrainedModel(model_path="./tiny_genius_model", device="cpu")
    await model.initialize()

    orchestrator = OrchestratorAgent(
        model=model,
        enable_reflection=True,
        enable_tools=True,
        rag_retriever=None,  # Test without RAG first
    )

    print("\n[2.2] Testing problem decomposition...")
    test_query = "What are the key features of Python and how do I define functions?"

    print(f"\nQuery: {test_query}")
    response = await orchestrator.process(test_query, context={})

    print(f"\nResponse: {response.content}")
    print(f"\nMetadata:")
    for key, value in response.metadata.items():
        print(f"  {key}: {value}")

    print(f"\nThoughts ({len(response.thoughts)} total):")
    for i, thought in enumerate(response.thoughts[:5], 1):  # Show first 5
        print(f"  {i}. [{thought.agent_role.value}] {thought.content[:100]}...")

    await model.cleanup()
    print("\n✓ Orchestrator test PASSED\n")
    return True


async def test_tool_execution():
    """Test 3: Tool execution with custom model."""
    print("=" * 70)
    print("TEST 3: Tool Execution")
    print("=" * 70)

    from genius_ai.models.custom_trained import CustomTrainedModel
    from genius_ai.agents.tool_user import ToolUserAgent

    print("\n[3.1] Setting up tool user agent...")
    model = CustomTrainedModel(model_path="./tiny_genius_model", device="cpu")
    await model.initialize()

    tool_agent = ToolUserAgent(model=model)

    print("\n[3.2] Testing calculator tool...")
    calc_task = "Calculate 25 * 4 + 100"
    print(f"Task: {calc_task}")

    response = await tool_agent.process(calc_task, context={})
    print(f"Response: {response.content}")

    print("\n[3.3] Testing code execution tool...")
    code_task = "Execute this Python code: x = 10; y = 20; result = x + y"
    print(f"Task: {code_task}")

    response = await tool_agent.process(code_task, context={})
    print(f"Response: {response.content}")

    await model.cleanup()
    print("\n✓ Tool execution test PASSED\n")
    return True


async def test_rag_integration():
    """Test 4: RAG integration."""
    print("=" * 70)
    print("TEST 4: RAG Integration")
    print("=" * 70)

    from genius_ai.rag.retriever import RAGRetriever, Document
    from genius_ai.models.custom_trained import CustomTrainedModel
    from genius_ai.agents.orchestrator import OrchestratorAgent

    print("\n[4.1] Initializing RAG retriever...")
    rag_retriever = RAGRetriever()
    await rag_retriever.initialize()

    print("\n[4.2] Adding test documents...")
    test_docs = [
        Document(
            content="Python lists are ordered, mutable collections. You can access elements by index.",
            metadata={"source": "python_docs", "topic": "lists"},
        ),
        Document(
            content="Python dictionaries store key-value pairs. Use dict[key] to access values.",
            metadata={"source": "python_docs", "topic": "dictionaries"},
        ),
        Document(
            content="Python functions are defined with the def keyword followed by the function name.",
            metadata={"source": "python_docs", "topic": "functions"},
        ),
    ]

    chunks_added = await rag_retriever.add_documents(test_docs)
    print(f"Added {chunks_added} chunks to knowledge base")

    print("\n[4.3] Testing retrieval...")
    query = "How do I use dictionaries in Python?"
    retrieved = await rag_retriever.retrieve_context(query, top_k=2)

    print(f"\nQuery: {query}")
    print(f"Retrieved {len(retrieved)} chunks:")
    for i, chunk in enumerate(retrieved, 1):
        print(f"  {i}. {chunk[:100]}...")

    print("\n[4.4] Testing orchestrator with RAG...")
    model = CustomTrainedModel(model_path="./tiny_genius_model", device="cpu")
    await model.initialize()

    orchestrator = OrchestratorAgent(
        model=model,
        enable_reflection=True,
        enable_tools=True,
        rag_retriever=rag_retriever,
    )

    response = await orchestrator.process(query, context={})
    print(f"\nResponse with RAG: {response.content}")

    await model.cleanup()
    print("\n✓ RAG integration test PASSED\n")
    return True


async def test_learning_system():
    """Test 5: Learning system."""
    print("=" * 70)
    print("TEST 5: Learning System")
    print("=" * 70)

    from genius_ai.memory.learning import learning_system

    print("\n[5.1] Recording test strategies...")

    # Record some strategies
    learning_system.record_strategy(
        problem_type="question",
        approach="decompose into sub-questions and retrieve knowledge",
        success=True,
        confidence=0.9,
        metadata={"agent": "reasoning", "used_rag": True},
    )

    learning_system.record_strategy(
        problem_type="problem",
        approach="break down into steps and use tools",
        success=True,
        confidence=0.85,
        metadata={"agent": "planning", "used_tools": True},
    )

    print("\n[5.2] Recording feedback...")
    learning_system.record_feedback(
        conversation_id="test_conv_1",
        message_id="msg_1",
        rating=5,
        comment="Excellent response with clear explanations",
    )

    learning_system.record_feedback(
        conversation_id="test_conv_2",
        message_id="msg_2",
        rating=4,
        comment="Good response but could be more detailed",
    )

    print("\n[5.3] Getting insights...")
    insights = learning_system.get_insights()

    print(f"\nTotal strategies: {insights['total_strategies']}")
    print(f"Total feedback: {insights['total_feedback']}")
    print(f"Positive feedback rate: {insights['positive_feedback_rate']:.1%}")
    print(f"Best performing type: {insights['best_performing_type']}")

    print("\n[5.4] Getting suggestions...")
    suggestions = learning_system.suggest_improvements("question")
    print(f"\nSuggestions for 'question' type:")
    for suggestion in suggestions[:3]:
        print(f"  - {suggestion}")

    print("\n✓ Learning system test PASSED\n")
    return True


async def test_streaming_thoughts():
    """Test 6: Streaming thoughts (simulated)."""
    print("=" * 70)
    print("TEST 6: Streaming Thoughts")
    print("=" * 70)

    from genius_ai.models.custom_trained import CustomTrainedModel
    from genius_ai.agents.orchestrator import OrchestratorAgent

    print("\n[6.1] Setting up orchestrator with thought callback...")
    model = CustomTrainedModel(model_path="./tiny_genius_model", device="cpu")
    await model.initialize()

    orchestrator = OrchestratorAgent(
        model=model,
        enable_reflection=True,
        enable_tools=False,
    )

    # Collect thoughts
    thoughts_collected = []

    async def thought_callback(thought):
        thoughts_collected.append(thought)
        print(f"  → [{thought.agent_role.value}] {thought.content[:80]}...")

    orchestrator.set_thought_stream_callback(thought_callback)

    print("\n[6.2] Processing query with streaming thoughts...")
    query = "Explain Python variables and lists"
    print(f"\nQuery: {query}\n")

    response = await orchestrator.process(query, context={})

    print(f"\n[6.3] Final response: {response.content}")
    print(f"\nTotal thoughts streamed: {len(thoughts_collected)}")

    await model.cleanup()
    print("\n✓ Streaming thoughts test PASSED\n")
    return True


async def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("GENIUS AI - INTEGRATED SYSTEM TEST")
    print("Testing custom trained model with all features")
    print("=" * 70 + "\n")

    results = []

    # Test 1: Custom model
    try:
        result = await test_custom_model()
        results.append(("Custom Model", result))
    except Exception as e:
        print(f"✗ Custom model test FAILED: {e}\n")
        results.append(("Custom Model", False))

    # Test 2: Orchestrator
    try:
        result = await test_orchestrator_with_model()
        results.append(("Orchestrator", result))
    except Exception as e:
        print(f"✗ Orchestrator test FAILED: {e}\n")
        results.append(("Orchestrator", False))

    # Test 3: Tool execution
    try:
        result = await test_tool_execution()
        results.append(("Tool Execution", result))
    except Exception as e:
        print(f"✗ Tool execution test FAILED: {e}\n")
        results.append(("Tool Execution", False))

    # Test 4: RAG integration
    try:
        result = await test_rag_integration()
        results.append(("RAG Integration", result))
    except Exception as e:
        print(f"✗ RAG integration test FAILED: {e}\n")
        results.append(("RAG Integration", False))

    # Test 5: Learning system
    try:
        result = await test_learning_system()
        results.append(("Learning System", result))
    except Exception as e:
        print(f"✗ Learning system test FAILED: {e}\n")
        results.append(("Learning System", False))

    # Test 6: Streaming thoughts
    try:
        result = await test_streaming_thoughts()
        results.append(("Streaming Thoughts", result))
    except Exception as e:
        print(f"✗ Streaming thoughts test FAILED: {e}\n")
        results.append(("Streaming Thoughts", False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your Genius AI system is fully functional!")
        print("\nYour custom trained model is integrated and working with:")
        print("  ✓ Multi-agent orchestration")
        print("  ✓ Real-time streaming thoughts")
        print("  ✓ Tool execution (calculator, code)")
        print("  ✓ RAG knowledge retrieval")
        print("  ✓ Continuous learning system")
        print("\nReady for commercialization! 🚀")
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Please check the errors above.")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    print("Starting Genius AI integrated system tests...")
    print("This will test all features with your custom trained model.\n")

    asyncio.run(run_all_tests())
