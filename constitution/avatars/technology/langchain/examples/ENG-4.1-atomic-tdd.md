---
law_id: ENG-4.1
avatar: langchain
---

# ENG-4.1: Atomic TDD Examples for LangChain

## COMPLIANT: Unit Testing LangChain Chains with Mocked LLM

```python
import pytest
from unittest.mock import Mock, patch, AsyncMock
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.llms.fake import FakeListLLM
from langchain_core.messages import AIMessage, HumanMessage
from chains.summarization import SummarizationChain
from chains.qa import QuestionAnsweringChain


class TestLLMChain:
    """Atomic tests for LLM chain functionality."""

    @pytest.fixture
    def mock_llm(self):
        """Provide a deterministic mock LLM."""
        return FakeListLLM(responses=[
            "This is a test response.",
            "Another deterministic response.",
            "Third response for testing."
        ])

    @pytest.fixture
    def simple_prompt(self):
        """Provide a simple prompt template."""
        return PromptTemplate(
            input_variables=["topic"],
            template="Write a brief summary about {topic}."
        )

    def test_chain_formats_prompt_correctly(self, mock_llm, simple_prompt):
        """Test that chain correctly formats the prompt template."""
        chain = LLMChain(llm=mock_llm, prompt=simple_prompt)

        # Access formatted prompt
        formatted = simple_prompt.format(topic="machine learning")

        assert "machine learning" in formatted
        assert "Write a brief summary about" in formatted

    def test_chain_returns_llm_response(self, mock_llm, simple_prompt):
        """Test that chain returns the LLM response."""
        chain = LLMChain(llm=mock_llm, prompt=simple_prompt)

        result = chain.invoke({"topic": "testing"})

        assert result["text"] == "This is a test response."

    def test_chain_passes_input_variables_to_prompt(self, mock_llm):
        """Test that input variables are passed to prompt template."""
        prompt = PromptTemplate(
            input_variables=["name", "role"],
            template="Describe {name} who works as a {role}."
        )
        chain = LLMChain(llm=mock_llm, prompt=prompt)

        result = chain.invoke({"name": "Alice", "role": "engineer"})

        # Chain should have processed inputs
        assert result is not None

    def test_chain_handles_empty_input_gracefully(self, mock_llm, simple_prompt):
        """Test chain behavior with empty input."""
        chain = LLMChain(llm=mock_llm, prompt=simple_prompt)

        result = chain.invoke({"topic": ""})

        # Should still return a response
        assert "text" in result


class TestSequentialChain:
    """Atomic tests for sequential chain execution."""

    @pytest.fixture
    def summarize_chain(self):
        """Provide summarization chain with mock LLM."""
        llm = FakeListLLM(responses=["Summarized: Key points extracted."])
        prompt = PromptTemplate(
            input_variables=["document"],
            template="Summarize this document: {document}"
        )
        return LLMChain(
            llm=llm,
            prompt=prompt,
            output_key="summary"
        )

    @pytest.fixture
    def analyze_chain(self):
        """Provide analysis chain with mock LLM."""
        llm = FakeListLLM(responses=["Analysis: Positive sentiment detected."])
        prompt = PromptTemplate(
            input_variables=["summary"],
            template="Analyze the sentiment of: {summary}"
        )
        return LLMChain(
            llm=llm,
            prompt=prompt,
            output_key="analysis"
        )

    def test_sequential_chain_passes_output_to_next_chain(
        self, summarize_chain, analyze_chain
    ):
        """Test that output from first chain feeds into second chain."""
        sequential = SequentialChain(
            chains=[summarize_chain, analyze_chain],
            input_variables=["document"],
            output_variables=["summary", "analysis"]
        )

        result = sequential.invoke({
            "document": "This is a long document about testing."
        })

        assert "summary" in result
        assert "analysis" in result

    def test_sequential_chain_preserves_intermediate_outputs(
        self, summarize_chain, analyze_chain
    ):
        """Test that intermediate outputs are preserved."""
        sequential = SequentialChain(
            chains=[summarize_chain, analyze_chain],
            input_variables=["document"],
            output_variables=["summary", "analysis"]
        )

        result = sequential.invoke({
            "document": "Test document content."
        })

        # Both outputs should be present
        assert result["summary"] == "Summarized: Key points extracted."
        assert result["analysis"] == "Analysis: Positive sentiment detected."


class TestQuestionAnsweringChain:
    """Atomic tests for QA chain functionality."""

    @pytest.fixture
    def mock_retriever(self):
        """Provide mock retriever with deterministic results."""
        from langchain_core.documents import Document

        mock = Mock()
        mock.get_relevant_documents.return_value = [
            Document(page_content="Python is a programming language."),
            Document(page_content="Python was created by Guido van Rossum.")
        ]
        return mock

    @pytest.fixture
    def qa_chain(self, mock_retriever):
        """Provide QA chain with mocked components."""
        llm = FakeListLLM(responses=[
            "Python is a programming language created by Guido van Rossum."
        ])

        return QuestionAnsweringChain(
            llm=llm,
            retriever=mock_retriever
        )

    def test_qa_chain_retrieves_relevant_documents(
        self, qa_chain, mock_retriever
    ):
        """Test that QA chain calls retriever with question."""
        qa_chain.invoke({"question": "What is Python?"})

        mock_retriever.get_relevant_documents.assert_called_once_with(
            "What is Python?"
        )

    def test_qa_chain_uses_retrieved_context_in_prompt(
        self, qa_chain, mock_retriever
    ):
        """Test that retrieved documents are used as context."""
        result = qa_chain.invoke({"question": "What is Python?"})

        # Should have answer based on retrieved context
        assert result is not None
        assert "answer" in result or "text" in result

    def test_qa_chain_handles_no_relevant_documents(self, mock_retriever):
        """Test QA chain when no documents are retrieved."""
        mock_retriever.get_relevant_documents.return_value = []

        llm = FakeListLLM(responses=["I don't have enough context to answer."])
        qa_chain = QuestionAnsweringChain(
            llm=llm,
            retriever=mock_retriever
        )

        result = qa_chain.invoke({"question": "Unknown topic?"})

        # Should handle gracefully
        assert result is not None
```

**Why compliant:** Each test verifies a single behavior of a LangChain component. Mock LLMs provide deterministic responses for reproducible tests. Retrievers are mocked to isolate chain logic from vector store. Tests focus on chain mechanics, not LLM output quality. Fixtures provide clean separation of test setup.

---

## VIOLATION: Testing Chains with Real LLM Calls

```python
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


def test_summarization_chain():
    """Test summarization with real LLM - not atomic."""
    # Real LLM call - non-deterministic
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)

    prompt = PromptTemplate(
        input_variables=["text"],
        template="Summarize: {text}"
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    # Long document - slow test
    result = chain.invoke({
        "text": "This is a very long document..." * 100
    })

    # Vague assertion - output varies
    assert len(result["text"]) > 0
    assert "summary" in result["text"].lower()  # May or may not contain "summary"


def test_full_rag_pipeline():
    """Test entire RAG pipeline - too many concerns."""
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import Chroma

    # Real embeddings - slow and costly
    embeddings = OpenAIEmbeddings()

    # Real vector store - external dependency
    vectorstore = Chroma.from_documents(
        documents=load_documents('data/docs'),  # External file dependency
        embedding=embeddings
    )

    # Real LLM
    llm = ChatOpenAI()

    # Full chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever()
    )

    result = qa_chain.invoke("What is the main topic?")

    # Assertions depend on document content and LLM behavior
    assert result["result"] is not None
```

**Why violates ENG-4.1:** Tests make real API calls which are slow, costly, and non-deterministic. External dependencies (files, vector stores) make tests unreliable. Output varies between runs, making assertions fragile. Multiple components are tested together, obscuring failure causes. Tests are not isolated or reproducible.

---

## COMPLIANT: Testing LangChain Agents with Tool Mocking

```python
import pytest
from unittest.mock import Mock, patch
from langchain.agents import AgentExecutor, create_react_agent
from langchain.llms.fake import FakeListLLM
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate


class TestAgentToolSelection:
    """Atomic tests for agent tool selection logic."""

    @pytest.fixture
    def mock_tools(self):
        """Provide mock tools with predictable behavior."""
        calculator = Tool(
            name="calculator",
            description="Performs mathematical calculations",
            func=lambda x: str(eval(x))  # Simplified for testing
        )

        search = Tool(
            name="search",
            description="Searches for current information",
            func=Mock(return_value="Search result: Found relevant info")
        )

        return [calculator, search]

    @pytest.fixture
    def agent_llm(self):
        """Provide LLM with scripted agent responses."""
        # Responses follow ReAct format
        return FakeListLLM(responses=[
            "Thought: I need to calculate this.\nAction: calculator\nAction Input: 2 + 2",
            "Thought: I now have the answer.\nFinal Answer: The result is 4"
        ])

    def test_agent_selects_calculator_for_math_question(
        self, mock_tools, agent_llm
    ):
        """Test that agent selects calculator tool for math."""
        prompt = PromptTemplate.from_template(
            """Answer the question using tools.

            Tools: {tools}
            Tool Names: {tool_names}

            Question: {input}
            {agent_scratchpad}"""
        )

        agent = create_react_agent(agent_llm, mock_tools, prompt)
        executor = AgentExecutor(agent=agent, tools=mock_tools)

        result = executor.invoke({"input": "What is 2 + 2?"})

        assert "4" in result["output"]

    def test_agent_uses_tool_description_for_selection(self, mock_tools):
        """Test that tool descriptions influence selection."""
        calculator = mock_tools[0]
        search = mock_tools[1]

        # Verify tool descriptions are accessible
        assert "mathematical" in calculator.description.lower()
        assert "search" in search.description.lower()

    def test_agent_handles_tool_execution_error(self, mock_tools, agent_llm):
        """Test agent behavior when tool raises error."""
        # Create tool that raises error
        error_tool = Tool(
            name="error_tool",
            description="A tool that fails",
            func=Mock(side_effect=ValueError("Tool execution failed"))
        )

        prompt = PromptTemplate.from_template(
            """Answer using tools.

            Tools: {tools}
            Tool Names: {tool_names}

            Question: {input}
            {agent_scratchpad}"""
        )

        # Agent should handle error gracefully
        llm = FakeListLLM(responses=[
            "Thought: I'll try the tool.\nAction: error_tool\nAction Input: test",
            "Thought: The tool failed. I'll provide a direct answer.\nFinal Answer: Unable to process."
        ])

        agent = create_react_agent(llm, [error_tool], prompt)
        executor = AgentExecutor(
            agent=agent,
            tools=[error_tool],
            handle_parsing_errors=True
        )

        result = executor.invoke({"input": "Use the tool"})

        assert result is not None


class TestAgentMemory:
    """Atomic tests for agent memory functionality."""

    @pytest.fixture
    def memory(self):
        """Provide conversation memory."""
        from langchain.memory import ConversationBufferMemory
        return ConversationBufferMemory(return_messages=True)

    def test_memory_stores_conversation_history(self, memory):
        """Test that memory stores messages."""
        from langchain_core.messages import HumanMessage, AIMessage

        memory.chat_memory.add_user_message("Hello")
        memory.chat_memory.add_ai_message("Hi there!")

        history = memory.load_memory_variables({})

        assert len(history["history"]) == 2
        assert isinstance(history["history"][0], HumanMessage)
        assert isinstance(history["history"][1], AIMessage)

    def test_memory_provides_context_to_agent(self, memory):
        """Test that memory context is available to agent."""
        memory.chat_memory.add_user_message("My name is Alice")
        memory.chat_memory.add_ai_message("Nice to meet you, Alice!")

        context = memory.load_memory_variables({})

        # Context should contain previous conversation
        messages = context["history"]
        assert any("Alice" in str(m.content) for m in messages)

    def test_memory_clear_removes_history(self, memory):
        """Test that clearing memory removes all messages."""
        memory.chat_memory.add_user_message("Test message")
        memory.clear()

        history = memory.load_memory_variables({})

        assert len(history["history"]) == 0
```

**Why compliant:** Each test focuses on a single agent behavior (tool selection, memory, error handling). Mock LLMs provide scripted responses for deterministic testing. Tools are mocked to isolate agent logic from external services. Tests verify specific mechanics rather than LLM output quality.

---

## VIOLATION: Testing Agent with Multiple Concerns

```python
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import DuckDuckGoSearchRun


def test_complete_agent():
    """Test agent with real components - not atomic."""
    # Real LLM
    llm = ChatOpenAI(temperature=0)

    # Real search tool - external dependency
    search = DuckDuckGoSearchRun()

    # Real web browsing - network dependent
    from langchain_community.tools import WebBrowsingTool
    browser = WebBrowsingTool()

    agent = initialize_agent(
        tools=[search, browser],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )

    # Complex query requiring multiple tool calls
    result = agent.invoke(
        "Find the current stock price of Apple and summarize recent news"
    )

    # Vague assertions
    assert result["output"] is not None
    assert len(result["output"]) > 50
```

**Why violates ENG-4.1:** Real LLM and tools make test slow and non-deterministic. Network-dependent tools (search, browser) can fail unpredictably. Multiple tool interactions in single test. Assertions are vague and don't verify specific behavior. Test outcome depends on current web content.

---

## TDD Cycle Commands

```bash
# RED: Run specific test, see it fail
pytest tests/chains/test_summarization.py::test_chain_returns_summary -v

# GREEN: Write code, run test again
pytest tests/chains/test_summarization.py::test_chain_returns_summary -v

# REFACTOR: Run all unit tests
pytest tests/ -m "not integration"

# VERIFY: Check coverage and constitutional compliance
pytest --cov=src --cov-fail-under=80
constitution-lint .

# Commit when green and compliant
git add -A && git commit -m "Add summarization chain"
```
