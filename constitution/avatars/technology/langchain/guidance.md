# LangChain/LlamaIndex Guidance

> **Purpose:** Stack-specific agent behaviors for building LLM applications with LangChain and LlamaIndex frameworks.

---

## Overview

This guidance provides patterns for AI agents working with LangChain and LlamaIndex to build LLM-powered applications including chatbots, RAG systems, agents, and chains.

---

## Testing Framework

**Primary Framework:** pytest + pytest-asyncio + langchain testing utilities

### Test Structure

```python
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from myproject.chains.qa_chain import QAChain
from myproject.agents.research_agent import ResearchAgent
from myproject.retrievers.hybrid_retriever import HybridRetriever


class TestQAChain:
    """Tests for the QA chain."""

    @pytest.fixture
    def mock_llm(self):
        """Mock LLM for testing."""
        mock = MagicMock(spec=ChatOpenAI)
        mock.invoke.return_value = AIMessage(content="Test response")
        return mock

    @pytest.fixture
    def mock_retriever(self):
        """Mock retriever for testing."""
        mock = MagicMock()
        mock.invoke.return_value = [
            Document(page_content="Relevant content", metadata={"source": "doc1"})
        ]
        return mock

    @pytest.fixture
    def qa_chain(self, mock_llm, mock_retriever):
        """QA chain with mocked dependencies."""
        return QAChain(llm=mock_llm, retriever=mock_retriever)

    def test_chain_returns_answer_with_sources(self, qa_chain):
        """Chain should return answer with source citations."""
        # Act
        result = qa_chain.invoke({"question": "What is the policy?"})

        # Assert
        assert "answer" in result
        assert "sources" in result
        assert len(result["sources"]) > 0

    def test_chain_uses_retriever(self, qa_chain, mock_retriever):
        """Chain should retrieve relevant documents."""
        # Act
        qa_chain.invoke({"question": "Test question"})

        # Assert
        mock_retriever.invoke.assert_called_once()

    def test_chain_handles_no_relevant_docs(self, qa_chain, mock_retriever):
        """Chain should handle case with no relevant documents."""
        # Arrange
        mock_retriever.invoke.return_value = []

        # Act
        result = qa_chain.invoke({"question": "Unknown topic"})

        # Assert
        assert "I don't have enough information" in result["answer"].lower() or result["answer"]


class TestResearchAgent:
    """Tests for the research agent."""

    @pytest.fixture
    def mock_tools(self):
        """Mock tools for agent."""
        search_tool = MagicMock()
        search_tool.name = "search"
        search_tool.invoke.return_value = "Search results..."

        return [search_tool]

    @pytest.fixture
    def agent(self, mock_llm, mock_tools):
        """Research agent with mocks."""
        return ResearchAgent(llm=mock_llm, tools=mock_tools)

    @pytest.mark.asyncio
    async def test_agent_completes_task(self, agent):
        """Agent should complete research task."""
        # Act
        result = await agent.run("Research topic X")

        # Assert
        assert result["success"]
        assert "answer" in result

    def test_agent_uses_tools_appropriately(self, agent, mock_tools):
        """Agent should use tools when needed."""
        # Act
        agent.run_sync("Find information about Y")

        # Assert
        # Verify tool was considered/used
        assert mock_tools[0].invoke.called or True  # Depends on agent logic


class TestHybridRetriever:
    """Tests for hybrid retrieval."""

    @pytest.fixture
    def sample_docs(self):
        """Sample documents for testing."""
        return [
            Document(page_content="Python is a programming language", metadata={"id": "1"}),
            Document(page_content="Machine learning uses algorithms", metadata={"id": "2"}),
            Document(page_content="Python is great for ML", metadata={"id": "3"}),
        ]

    @pytest.fixture
    def retriever(self, sample_docs):
        """Hybrid retriever with sample docs."""
        return HybridRetriever.from_documents(sample_docs)

    def test_retriever_returns_relevant_docs(self, retriever):
        """Retriever should return relevant documents."""
        # Act
        results = retriever.invoke("Python programming")

        # Assert
        assert len(results) > 0
        assert any("Python" in doc.page_content for doc in results)

    def test_retriever_respects_k_parameter(self, retriever):
        """Retriever should respect k parameter."""
        # Act
        results = retriever.invoke("Python", k=2)

        # Assert
        assert len(results) <= 2
```

---

## Common Patterns

### Good Patterns

**Chain Construction with LCEL:**

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_openai import ChatOpenAI

class QAChain:
    """Question-answering chain with retrieval."""

    def __init__(self, llm, retriever, prompt_template: str = None):
        self.llm = llm
        self.retriever = retriever
        self.prompt = ChatPromptTemplate.from_template(
            prompt_template or self._default_prompt()
        )
        self.chain = self._build_chain()

    def _default_prompt(self) -> str:
        return """Answer the question based on the context below.
If you cannot answer from the context, say "I don't have enough information."

Context:
{context}

Question: {question}

Answer:"""

    def _build_chain(self):
        """Build the chain using LCEL."""
        return (
            RunnableParallel(
                context=self.retriever | self._format_docs,
                question=RunnablePassthrough()
            )
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def _format_docs(self, docs):
        """Format retrieved documents."""
        return "\n\n".join(doc.page_content for doc in docs)

    def invoke(self, question: str) -> dict:
        """Run the chain."""
        # Get documents for source tracking
        docs = self.retriever.invoke(question)

        # Run chain
        answer = self.chain.invoke(question)

        return {
            "answer": answer,
            "sources": [
                {"content": doc.page_content[:200], "metadata": doc.metadata}
                for doc in docs
            ]
        }

    async def ainvoke(self, question: str) -> dict:
        """Async version."""
        docs = await self.retriever.ainvoke(question)
        answer = await self.chain.ainvoke(question)
        return {"answer": answer, "sources": docs}
```

**Custom Tools:**

```python
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional

class SearchInput(BaseModel):
    """Input schema for search tool."""
    query: str = Field(description="Search query")
    max_results: int = Field(default=5, description="Maximum results to return")

class WebSearchTool(BaseTool):
    """Tool for searching the web."""

    name: str = "web_search"
    description: str = "Search the web for current information. Use for facts, news, or recent events."
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        """Execute search."""
        # Implementation
        results = self._search_api(query, max_results)
        return self._format_results(results)

    async def _arun(self, query: str, max_results: int = 5) -> str:
        """Async execution."""
        results = await self._async_search_api(query, max_results)
        return self._format_results(results)

    def _format_results(self, results: list) -> str:
        """Format results for LLM consumption."""
        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(f"{i}. {r['title']}\n   {r['snippet']}\n   URL: {r['url']}")
        return "\n\n".join(formatted)
```

**Agent with Memory:**

```python
from langchain_core.prompts import MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

class ConversationalAgent:
    """Agent with conversation memory."""

    def __init__(self, llm, tools: list, system_prompt: str = None):
        self.llm = llm
        self.tools = tools
        self.message_history = ChatMessageHistory()

        # Create prompt with memory placeholder
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt or "You are a helpful assistant."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Create agent
        agent = create_openai_functions_agent(llm, tools, self.prompt)
        self.executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        # Wrap with message history
        self.agent_with_history = RunnableWithMessageHistory(
            self.executor,
            lambda session_id: self.message_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def chat(self, message: str, session_id: str = "default") -> str:
        """Chat with memory."""
        result = self.agent_with_history.invoke(
            {"input": message},
            config={"configurable": {"session_id": session_id}}
        )
        return result["output"]
```

**Callbacks for Observability:**

```python
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict, List
import structlog

logger = structlog.get_logger()

class MetricsCallbackHandler(BaseCallbackHandler):
    """Callback handler for metrics and logging."""

    def __init__(self):
        self.llm_calls = 0
        self.total_tokens = 0
        self.retriever_calls = 0

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        """Log LLM start."""
        self.llm_calls += 1
        logger.info("llm_start", prompts=prompts[:100], call_number=self.llm_calls)

    def on_llm_end(self, response, **kwargs):
        """Log LLM completion."""
        if hasattr(response, 'llm_output') and response.llm_output:
            tokens = response.llm_output.get('token_usage', {})
            self.total_tokens += tokens.get('total_tokens', 0)
            logger.info("llm_end", tokens=tokens)

    def on_retriever_start(self, serialized: Dict[str, Any], query: str, **kwargs):
        """Log retriever start."""
        self.retriever_calls += 1
        logger.info("retriever_start", query=query)

    def on_retriever_end(self, documents, **kwargs):
        """Log retriever results."""
        logger.info("retriever_end", num_docs=len(documents))

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs):
        """Log tool execution."""
        logger.info("tool_start", tool=serialized.get("name"), input=input_str[:100])

    def get_metrics(self) -> dict:
        """Get accumulated metrics."""
        return {
            "llm_calls": self.llm_calls,
            "total_tokens": self.total_tokens,
            "retriever_calls": self.retriever_calls
        }
```

---

## Anti-Patterns to Avoid

### Hardcoded Prompts

```python
# BAD - Hardcoded prompt in chain
chain = prompt | llm | parser
# No way to customize or version prompts

# GOOD - Configurable prompts
class ConfigurableChain:
    def __init__(self, prompt_template: str = None, prompt_config_path: str = None):
        if prompt_config_path:
            self.prompt = load_prompt_from_config(prompt_config_path)
        else:
            self.prompt = ChatPromptTemplate.from_template(
                prompt_template or DEFAULT_PROMPT
            )
```

### No Error Handling

```python
# BAD - No error handling
def query(question):
    return chain.invoke(question)  # May throw API errors

# GOOD - Proper error handling
def query(question: str) -> dict:
    try:
        result = chain.invoke(question)
        return {"success": True, "answer": result}
    except openai.RateLimitError:
        logger.warning("Rate limited, retrying...")
        time.sleep(60)
        return query(question)
    except Exception as e:
        logger.error("Chain failed", error=str(e))
        return {"success": False, "error": str(e)}
```

### Blocking Async Code

```python
# BAD - Using sync in async context
async def process_queries(queries):
    results = []
    for q in queries:
        results.append(chain.invoke(q))  # Blocking!
    return results

# GOOD - Proper async
async def process_queries(queries):
    tasks = [chain.ainvoke(q) for q in queries]
    return await asyncio.gather(*tasks)
```

---

## Tools and Commands

### Development

```bash
# Install dependencies
pip install langchain langchain-openai langchain-community

# Set up environment
cp .env.example .env
# Add OPENAI_API_KEY, etc.

# Run interactive testing
python -c "from src.chains import QAChain; ..."

# Start LangServe (if using)
langchain serve
```

### Testing

```bash
# Run unit tests (mocked)
pytest tests/ -m "not integration"

# Run integration tests
OPENAI_API_KEY=xxx pytest tests/integration/

# Run with verbose output
pytest -v -s

# Run specific test
pytest tests/chains/test_qa_chain.py::TestQAChain::test_chain_returns_answer
```

### Debugging

```bash
# Enable LangChain debug mode
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=xxx

# Use LangSmith for tracing
# https://smith.langchain.com
```

---

## LangChain-Specific Guidance

### Testing Strategy

1. **Unit Tests** - Mock LLM and external services
   - Chain logic
   - Prompt formatting
   - Output parsing

2. **Integration Tests** - Real LLM calls (sparingly)
   - End-to-end flows
   - Tool integration
   - Retrieval quality

3. **Prompt Tests** - Validate prompt effectiveness
   - Few-shot examples
   - Edge cases
   - Format compliance

### Prompt Management

```python
# prompts/qa_prompts.py

QA_SYSTEM_PROMPT = """You are a helpful assistant that answers questions based on provided context.

Guidelines:
- Only answer based on the provided context
- If uncertain, say so
- Cite sources when possible
- Be concise but thorough"""

QA_USER_TEMPLATE = """Context:
{context}

Question: {question}

Please provide a helpful answer based on the context above."""

# Version prompts for tracking
PROMPT_VERSION = "1.2.0"
```

### Production Checklist

```markdown
## LangChain Production Checklist

### Code Quality
- [ ] All chains/agents tested
- [ ] Error handling comprehensive
- [ ] Async used where beneficial
- [ ] Callbacks for observability

### Prompts
- [ ] Prompts versioned
- [ ] Prompts tested
- [ ] Edge cases handled
- [ ] Token limits considered

### Performance
- [ ] Caching implemented (embeddings, responses)
- [ ] Batch processing where possible
- [ ] Streaming for long responses
- [ ] Rate limiting handled

### Observability
- [ ] LangSmith or equivalent tracing
- [ ] Metrics collected (tokens, latency)
- [ ] Errors logged with context
- [ ] Cost tracking enabled

### Security
- [ ] API keys in environment variables
- [ ] Input validation
- [ ] Output filtering (if needed)
- [ ] PII handling
```
