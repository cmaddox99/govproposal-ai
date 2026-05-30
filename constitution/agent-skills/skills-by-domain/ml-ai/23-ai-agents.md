---
skill:
  id: skill-23-ai-agents
  name: AI Agents
  category: ai-development
  version: "2.0.0"

laws:
  implements:
    - id: BUS-1.1
      title: Priority Hierarchy Law
  references:
    - id: BUS-6.1
      title: Risk Assessment Law
    - id: ENG-6.7
      title: Audit Trail Law

triggers:
  phrases:
    - "Build AI agent"
    - "Autonomous workflow"
    - "Agent with tools"
    - "Multi-step reasoning"

followed_by:
  - skill-24-ai-safety
  - skill-21-prompt-engineering
---

# Skill: AI Agent Design

> **Purpose:** Design and implement AI agents that can autonomously plan, reason, and execute multi-step tasks using tools and memory.

---

## Purpose

AI Agent Design is the practice of building autonomous systems that use LLMs to reason, plan, and act. This skill ensures:

1. **Reliability** - Agents complete tasks consistently
2. **Safety** - Actions bounded and reversible where needed
3. **Transparency** - Reasoning visible and auditable
4. **Efficiency** - Minimal steps to achieve goals
5. **Controllability** - Human oversight maintained

**Key principle:** Agents amplify human capability, not replace human judgment.

---

## When to Invoke

Invoke this skill when:

- Building systems that take autonomous actions
- Implementing multi-step task automation
- Creating AI assistants with tool access
- Designing workflows requiring reasoning
- Building copilots for complex domains

**Trigger phrases:**
- "Can the AI take actions on its own?"
- "We need it to use multiple tools"
- "Build an agent that can..."
- "How do we make it more autonomous?"
- "It needs to plan and execute tasks"

---

## Constitutional Foundation

### Engineering Constitution
- **Article II, Section 2.1** - Simplicity: Agent architecture appropriate
- **Article IV, Section 4.1** - Test-First: Agent behaviors tested
- **Article VI, Section 6.1** - Observability: Agent actions logged

### Business Constitution
- **Article III, Section 3.3** - Audit Trail: All actions traceable
- **Article IV, Section 4.1** - Continuity: Graceful failure handling

### Product Constitution
- **Article V, Section 5.1** - User Experience: Clear agent status

---

## Agent Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                      AI AGENT                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    PLANNER                           │   │
│  │  - Goal decomposition                                │   │
│  │  - Task ordering                                     │   │
│  │  - Strategy selection                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   EXECUTOR                           │   │
│  │  - Tool selection                                    │   │
│  │  - Action execution                                  │   │
│  │  - Error handling                                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│              ┌────────────┼────────────┐                   │
│              ▼            ▼            ▼                   │
│         ┌────────┐   ┌────────┐   ┌────────┐              │
│         │ Tool 1 │   │ Tool 2 │   │ Tool N │              │
│         └────────┘   └────────┘   └────────┘              │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    MEMORY                            │   │
│  │  - Conversation history                              │   │
│  │  - Task state                                        │   │
│  │  - Learned patterns                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Tool System

### Tool Definition

```python
from dataclasses import dataclass
from typing import Callable, Any
from abc import ABC, abstractmethod

@dataclass
class ToolParameter:
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None

@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: list[ToolParameter]
    returns: str
    examples: list[dict] = None

class Tool(ABC):
    """Base class for agent tools."""

    @property
    @abstractmethod
    def definition(self) -> ToolDefinition:
        """Return tool definition for LLM."""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> dict:
        """Execute the tool with given parameters."""
        pass

    def to_openai_schema(self) -> dict:
        """Convert to OpenAI function calling format."""
        return {
            "type": "function",
            "function": {
                "name": self.definition.name,
                "description": self.definition.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        p.name: {
                            "type": p.type,
                            "description": p.description
                        }
                        for p in self.definition.parameters
                    },
                    "required": [
                        p.name for p in self.definition.parameters
                        if p.required
                    ]
                }
            }
        }
```

### Example Tools

```python
class SearchTool(Tool):
    """Search the web for information."""

    def __init__(self, search_api_key: str):
        self.api_key = search_api_key

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="search",
            description="Search the web for current information. Use for facts, news, or data you don't know.",
            parameters=[
                ToolParameter(
                    name="query",
                    type="string",
                    description="The search query"
                ),
                ToolParameter(
                    name="num_results",
                    type="integer",
                    description="Number of results to return",
                    required=False,
                    default=5
                )
            ],
            returns="List of search results with titles, snippets, and URLs"
        )

    async def execute(self, query: str, num_results: int = 5) -> dict:
        # Implementation
        results = await self._search(query, num_results)
        return {"results": results, "query": query}


class DatabaseQueryTool(Tool):
    """Query a database with natural language."""

    def __init__(self, db_connection, schema: dict):
        self.db = db_connection
        self.schema = schema

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="query_database",
            description=f"Query the database. Available tables: {list(self.schema.keys())}",
            parameters=[
                ToolParameter(
                    name="sql",
                    type="string",
                    description="SQL query to execute (SELECT only)"
                )
            ],
            returns="Query results as a list of dictionaries"
        )

    async def execute(self, sql: str) -> dict:
        # Validate query is SELECT only
        if not sql.strip().upper().startswith("SELECT"):
            return {"error": "Only SELECT queries are allowed"}

        try:
            results = await self.db.execute(sql)
            return {"results": results, "row_count": len(results)}
        except Exception as e:
            return {"error": str(e)}


class CodeExecutionTool(Tool):
    """Execute Python code in a sandboxed environment."""

    def __init__(self, sandbox_config: dict):
        self.config = sandbox_config

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="execute_code",
            description="Execute Python code. Use for calculations, data processing, or testing logic.",
            parameters=[
                ToolParameter(
                    name="code",
                    type="string",
                    description="Python code to execute"
                ),
                ToolParameter(
                    name="timeout_seconds",
                    type="integer",
                    description="Maximum execution time",
                    required=False,
                    default=30
                )
            ],
            returns="Execution output including stdout, stderr, and return value"
        )

    async def execute(self, code: str, timeout_seconds: int = 30) -> dict:
        # Execute in sandbox with timeout
        result = await self._sandbox_execute(code, timeout_seconds)
        return result
```

---

## Agent Loop

### ReAct Agent

```python
from enum import Enum
from dataclasses import dataclass

class AgentState(Enum):
    THINKING = "thinking"
    ACTING = "acting"
    OBSERVING = "observing"
    FINISHED = "finished"
    ERROR = "error"

@dataclass
class AgentStep:
    state: AgentState
    thought: str = None
    action: str = None
    action_input: dict = None
    observation: str = None

class ReActAgent:
    """Agent using ReAct (Reasoning + Acting) pattern."""

    def __init__(
        self,
        llm_client,
        tools: list[Tool],
        max_steps: int = 10,
        system_prompt: str = None
    ):
        self.llm = llm_client
        self.tools = {t.definition.name: t for t in tools}
        self.max_steps = max_steps
        self.system_prompt = system_prompt or self._default_system_prompt()

    def _default_system_prompt(self) -> str:
        tool_descriptions = "\n".join([
            f"- {name}: {tool.definition.description}"
            for name, tool in self.tools.items()
        ])

        return f"""You are an AI assistant that can use tools to help users.

Available tools:
{tool_descriptions}

To use a tool, respond with:
Thought: [Your reasoning about what to do]
Action: [tool_name]
Action Input: [JSON input for the tool]

After receiving an observation, continue reasoning:
Thought: [Your reasoning about the observation]
... (continue with more actions if needed)

When you have the final answer:
Thought: I have enough information to answer
Final Answer: [Your response to the user]

Always think step by step. Be thorough but efficient."""

    async def run(self, task: str) -> dict:
        """Run the agent on a task."""

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": task}
        ]

        steps = []

        for step_num in range(self.max_steps):
            # Get LLM response
            response = await self.llm.chat(messages)

            # Parse response
            step = self._parse_response(response)
            steps.append(step)

            if step.state == AgentState.FINISHED:
                return {
                    "success": True,
                    "answer": step.thought,
                    "steps": steps
                }

            if step.state == AgentState.ACTING:
                # Execute tool
                tool = self.tools.get(step.action)
                if not tool:
                    observation = f"Error: Unknown tool '{step.action}'"
                else:
                    try:
                        result = await tool.execute(**step.action_input)
                        observation = str(result)
                    except Exception as e:
                        observation = f"Error executing tool: {e}"

                # Add to messages
                messages.append({"role": "assistant", "content": response})
                messages.append({"role": "user", "content": f"Observation: {observation}"})

                step.observation = observation

        return {
            "success": False,
            "error": "Max steps reached",
            "steps": steps
        }

    def _parse_response(self, response: str) -> AgentStep:
        """Parse LLM response into structured step."""

        if "Final Answer:" in response:
            answer = response.split("Final Answer:")[-1].strip()
            return AgentStep(
                state=AgentState.FINISHED,
                thought=answer
            )

        thought = None
        action = None
        action_input = None

        if "Thought:" in response:
            thought_section = response.split("Thought:")[-1]
            if "Action:" in thought_section:
                thought = thought_section.split("Action:")[0].strip()
            else:
                thought = thought_section.strip()

        if "Action:" in response:
            action_section = response.split("Action:")[-1]
            if "Action Input:" in action_section:
                action = action_section.split("Action Input:")[0].strip()
            else:
                action = action_section.split("\n")[0].strip()

        if "Action Input:" in response:
            input_section = response.split("Action Input:")[-1].strip()
            try:
                action_input = json.loads(input_section)
            except:
                action_input = {"raw": input_section}

        if action:
            return AgentStep(
                state=AgentState.ACTING,
                thought=thought,
                action=action,
                action_input=action_input
            )

        return AgentStep(
            state=AgentState.THINKING,
            thought=thought or response
        )
```

### Planning Agent

```python
@dataclass
class Plan:
    goal: str
    steps: list[str]
    current_step: int = 0
    completed_steps: list[dict] = None

class PlanningAgent:
    """Agent that creates and executes plans."""

    def __init__(self, llm_client, tools: list[Tool], max_replans: int = 3):
        self.llm = llm_client
        self.tools = {t.definition.name: t for t in tools}
        self.max_replans = max_replans
        self.executor = ReActAgent(llm_client, tools, max_steps=5)

    async def run(self, goal: str) -> dict:
        """Create and execute a plan."""

        # Create initial plan
        plan = await self._create_plan(goal)
        replans = 0

        while plan.current_step < len(plan.steps):
            step = plan.steps[plan.current_step]

            # Execute step
            result = await self.executor.run(step)

            if result["success"]:
                plan.completed_steps.append({
                    "step": step,
                    "result": result["answer"]
                })
                plan.current_step += 1
            else:
                # Replan if step failed
                if replans < self.max_replans:
                    plan = await self._replan(plan, result["error"])
                    replans += 1
                else:
                    return {
                        "success": False,
                        "error": "Max replans exceeded",
                        "plan": plan
                    }

        # Synthesize final answer
        answer = await self._synthesize_answer(goal, plan)

        return {
            "success": True,
            "answer": answer,
            "plan": plan
        }

    async def _create_plan(self, goal: str) -> Plan:
        """Create a plan to achieve the goal."""

        prompt = f"""Create a step-by-step plan to achieve this goal:

Goal: {goal}

Available tools: {list(self.tools.keys())}

Create 3-7 concrete steps. Each step should be actionable with the available tools.

Return as a numbered list:
1. [First step]
2. [Second step]
..."""

        response = await self.llm.complete(prompt)
        steps = self._parse_plan(response)

        return Plan(goal=goal, steps=steps, completed_steps=[])

    async def _replan(self, current_plan: Plan, error: str) -> Plan:
        """Replan after a step failure."""

        prompt = f"""The plan encountered an error. Create a new plan.

Original goal: {current_plan.goal}
Completed steps: {current_plan.completed_steps}
Failed step: {current_plan.steps[current_plan.current_step]}
Error: {error}

Create a revised plan that accounts for the completed work and avoids the error.

Return as a numbered list:"""

        response = await self.llm.complete(prompt)
        steps = self._parse_plan(response)

        return Plan(
            goal=current_plan.goal,
            steps=steps,
            completed_steps=current_plan.completed_steps
        )
```

---

## Memory Systems

### Conversation Memory

```python
from collections import deque

class ConversationMemory:
    """Manage conversation history for agents."""

    def __init__(
        self,
        max_messages: int = 50,
        max_tokens: int = 4000
    ):
        self.messages = deque(maxlen=max_messages)
        self.max_tokens = max_tokens

    def add(self, role: str, content: str):
        """Add a message to memory."""
        self.messages.append({"role": role, "content": content})

    def get_context(self) -> list[dict]:
        """Get conversation context within token budget."""
        context = []
        token_count = 0

        # Add messages from most recent
        for msg in reversed(self.messages):
            msg_tokens = len(msg["content"]) // 4  # Rough estimate
            if token_count + msg_tokens > self.max_tokens:
                break
            context.insert(0, msg)
            token_count += msg_tokens

        return context

    def summarize(self, llm_client) -> str:
        """Summarize conversation for long-term storage."""
        all_content = "\n".join([
            f"{m['role']}: {m['content']}"
            for m in self.messages
        ])

        prompt = f"""Summarize this conversation concisely, preserving key facts and decisions:

{all_content}

Summary:"""

        return llm_client.complete(prompt)
```

### Working Memory

```python
@dataclass
class MemoryItem:
    key: str
    value: Any
    importance: float  # 0-1
    timestamp: datetime
    access_count: int = 0

class WorkingMemory:
    """Short-term memory for task execution."""

    def __init__(self, capacity: int = 20):
        self.capacity = capacity
        self.items: dict[str, MemoryItem] = {}

    def store(self, key: str, value: Any, importance: float = 0.5):
        """Store an item in working memory."""
        self.items[key] = MemoryItem(
            key=key,
            value=value,
            importance=importance,
            timestamp=datetime.utcnow()
        )

        # Evict if over capacity
        if len(self.items) > self.capacity:
            self._evict()

    def retrieve(self, key: str) -> Any:
        """Retrieve an item from memory."""
        if key in self.items:
            self.items[key].access_count += 1
            return self.items[key].value
        return None

    def search(self, query: str, llm_client) -> list[MemoryItem]:
        """Semantic search over memory items."""
        # Use LLM to find relevant items
        items_str = "\n".join([
            f"- {key}: {str(item.value)[:100]}"
            for key, item in self.items.items()
        ])

        prompt = f"""Which of these memory items are relevant to: "{query}"?

Items:
{items_str}

Return the relevant keys, comma-separated:"""

        response = llm_client.complete(prompt)
        keys = [k.strip() for k in response.split(",")]

        return [self.items[k] for k in keys if k in self.items]

    def _evict(self):
        """Remove least important/used items."""
        # Score = importance * recency * access_count
        def score(item):
            age_hours = (datetime.utcnow() - item.timestamp).total_seconds() / 3600
            recency = 1 / (1 + age_hours)
            return item.importance * recency * (1 + item.access_count * 0.1)

        scored = sorted(self.items.items(), key=lambda x: score(x[1]))

        # Remove lowest scoring
        while len(self.items) > self.capacity:
            key, _ = scored.pop(0)
            del self.items[key]
```

---

## Multi-Agent Systems

### Agent Orchestration

```python
@dataclass
class AgentConfig:
    name: str
    role: str
    tools: list[Tool]
    system_prompt: str

class MultiAgentSystem:
    """Orchestrate multiple specialized agents."""

    def __init__(self, agents: list[AgentConfig], llm_client):
        self.agents = {
            config.name: ReActAgent(
                llm_client,
                config.tools,
                system_prompt=config.system_prompt
            )
            for config in agents
        }
        self.agent_configs = {c.name: c for c in agents}
        self.llm = llm_client

    async def run(self, task: str) -> dict:
        """Run task using appropriate agent(s)."""

        # Determine which agent(s) to use
        routing = await self._route_task(task)

        results = []

        for agent_name in routing["agents"]:
            subtask = routing["subtasks"].get(agent_name, task)
            agent = self.agents[agent_name]

            result = await agent.run(subtask)
            results.append({
                "agent": agent_name,
                "task": subtask,
                "result": result
            })

        # Synthesize if multiple agents
        if len(results) > 1:
            final = await self._synthesize_results(task, results)
        else:
            final = results[0]["result"]["answer"]

        return {
            "answer": final,
            "agent_results": results
        }

    async def _route_task(self, task: str) -> dict:
        """Route task to appropriate agent(s)."""

        agent_descriptions = "\n".join([
            f"- {name}: {config.role}"
            for name, config in self.agent_configs.items()
        ])

        prompt = f"""Given this task, determine which agent(s) should handle it.

Task: {task}

Available agents:
{agent_descriptions}

If the task needs multiple agents, break it into subtasks.

Return JSON:
{{
    "agents": ["agent_name"],
    "subtasks": {{"agent_name": "subtask description"}}
}}"""

        response = await self.llm.complete(prompt)
        return json.loads(response)
```

---

## Good Examples

### Example 1: Research Agent

```python
research_agent = ReActAgent(
    llm_client=openai_client,
    tools=[
        SearchTool(api_key=SEARCH_API_KEY),
        WebScraperTool(),
        SummarizerTool(llm_client=openai_client),
        NoteTool()  # For storing findings
    ],
    system_prompt="""You are a research assistant. When given a topic:
1. Search for relevant sources
2. Read and extract key information
3. Synthesize findings
4. Provide a well-sourced summary

Always cite your sources."""
)
```

### Example 2: Data Analysis Agent

```python
data_agent = ReActAgent(
    llm_client=openai_client,
    tools=[
        DatabaseQueryTool(db_conn, schema),
        CodeExecutionTool(sandbox_config),
        VisualizationTool(),
        ExportTool()
    ],
    system_prompt="""You are a data analyst. When given a question:
1. Understand what data is needed
2. Query the database
3. Analyze and visualize results
4. Provide insights

Always explain your methodology."""
)
```

---

## Bad Examples (Anti-Patterns)

### Anti-Pattern 1: Unbounded Agents

```python
# BAD - No limits, no oversight
agent = Agent(
    tools=[FileTool(), ShellTool(), NetworkTool()],
    max_steps=float('inf')  # Runs forever
    # No human approval for dangerous actions
)
```

**Correct approach:** Bounded steps, action approval for sensitive operations.

---

### Anti-Pattern 2: No Error Handling

```python
# BAD - Crashes on tool errors
async def run(self, task):
    while True:
        action = self.plan_action()
        result = self.tools[action.name].execute(**action.input)  # May throw
        # No error handling, no recovery
```

**Correct approach:** Graceful error handling with recovery strategies.

---

## Quality Checklist

Before deploying an agent:

### Safety
- [ ] Actions bounded (max steps, timeouts)
- [ ] Sensitive actions require approval
- [ ] Dangerous tools properly sandboxed
- [ ] Failure modes graceful

### Reliability
- [ ] Tool errors handled
- [ ] Replanning on failure
- [ ] Clear termination conditions
- [ ] State recovery possible

### Observability
- [ ] All actions logged
- [ ] Reasoning visible
- [ ] Metrics tracked
- [ ] Debugging possible

### User Experience
- [ ] Progress visible
- [ ] Interruption possible
- [ ] Results verifiable
- [ ] Sources cited

---

## Skill Interactions

### Preceded By
- **21-Prompt Engineering** - Agent prompts
- **22-RAG Architecture** - RAG as agent tool

### Followed By
- **24-AI Safety** - Safe agent design

### Related Skills
- **13-Observability** - Agent monitoring
- **11-Incident Response** - Agent failures
