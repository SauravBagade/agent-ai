# 📌 What **Strands Agents** Is (High-Level)

Strands Agents is an **open-source SDK** (by AWS) for building intelligent AI agents that combine:

✅ A **language model** (e.g., Claude, LLaMA, Bedrock providers)
✅ **Tools** that give the agent real capabilities (e.g., API calls, calculators)
✅ A **reasoning loop** where the agent decides when to use tools and how to act ([Amazon Web Services, Inc.][2])

The SDK is **code-first**, lightweight, and supports **multi-agent systems and workflows**. ([strandsagents.com][3])

---

## 🧠 Strands Agent Architecture — Diagram (Text)

Below is a simplified **architecture diagram** showing the core components and how they interact:

```
 +---------------------------+
 |      User / App Layer     |
 |  (Query / Prompt Input)   |
 +-------------+-------------+
               |
               v
       +------------------+
       |   Strands Agent  |
       |   (Core Loop)    |
       +--------+---------+
                |
                |                                                     
                v
 +------------------------------+
 | Language Model (LLM Engine)  |
 | e.g., Claude, LLaMA, etc.    |
 +--------------+---------------+
                |
                |
                v
       +-------------------+
       |   Tools & APIs    |
       | (Calculator, HTTP |
       |  file read, etc.) |
       +-------------------+

```

### Component Roles

**1. Input (User/App)**
User text or structured input triggers the agent. It can be queries like:

> “Extract the summary from this document.” ([YouTube][1])

**2. Strands Agent Core Loop**

* Receives the input
* Decides whether to ask the model for reasoning
* May invoke tools based on model recommendations
* Continues until a final answer is ready

This core cycle is sometimes called the **Agentic Loop**:
👩‍💻 *User → Agent → LLM → (if needed) Tools → Integrate → Response* ([LinkedIn][4])

**3. Language Model (LLM)**
Handles natural-language reasoning, planning, and tool signal decisions.

**4. Tools & APIs**
Pre-built or custom actions that expand what the agent can do—e.g., calculators, HTTP requests, file operations. ([strandsagents.com][5])

---

## 🧩 Multi-Agent Systems (Advanced)

Strands supports **multi-agent workflows**, where outputs from one agent feed into another. This can be organized as:

```
Research Agent  ──>  Analysis Agent  ──>  Report Agent
      |                    |                     |
   (LLM + Tools)       (LLM + Tools)        (LLM + Tools)
```

This kind of diagram is used where tasks are **chained or orchestrated**. ([strandsagents.com][6])

---

## 🔧 How a Simple Agent Is Built (Concept)

A minimal agent typically includes:

✔ LLM model
✔ A small set of tools
✔ Optional session or state management

Example (Python conceptual):

```python
from strands import Agent
from strands_tools import calculator

agent = Agent(tools=[calculator])
response = agent("What is 42 × 7?")
print(response)
```


## 🧠 Key Concepts You Should Know

| Term              | Meaning                                                                    |
| ----------------- | -------------------------------------------------------------------------- |
| **Agent Loop**    | The cycle of reasoning → tool use → response. ([LinkedIn][4])              |
| **Tools**         | Functional capabilities (e.g., calculator, HTTP). ([strandsagents.com][5]) |
| **Session/State** | Maintains context across multiple messages. ([strandsagents.com][7])       |
| **Multi-Agent**   | Orchestrated agents collaborating on a task. ([strandsagents.com][8])      |

---

## 📌 TL;DR Diagram (ASCII)

```
+------------------+
|   User Query     |
+--------+---------+
         |
         v
+-------------------------+
|   Strands Agent Core    |
|  (decides actions)      |
+----------+--------------+
           |
           v
+-------------------------+
|       LLM Model         |
+-----------+-------------+
            |
            v
+-------------------------+
|       Tools/Actions     |
+-------------------------+
```
---

# Pre-requirements

# --- AI Core / Hybrid ---
strands-agent
strands-agents-tool
strands-agents-ollama
anthropic
boto3

# --- Utilities & Parsing ---
python-dotenv
pyyaml
requests
tabulate
rich
click

# --- DevOps Tool Helpers ---
paramiko            # SSH (optional)
docker              # Docker Python SDK
kubernetes          # K8s Python client
gitpython           # Git
pygithub            # GitHub API
prometheus-api-client
grafana-api-client

# --- Logs / Monitoring ---
elasticsearch       # (ELK)
loki-logger         # (optional)
opentelemetry-sdk   # (optional tracing)

# --- Web/API/CLI Interface ---
fastapi
uvicorn
typer               # Better CLI tool

# --- Testing ---
pytest
pytest-asyncio

# --- Optional Local LLM ---
ollama

# --- Optional Visualization ---
pydantic
networkx
----

--

--
