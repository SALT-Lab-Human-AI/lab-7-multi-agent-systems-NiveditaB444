[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/3WjIbrgM)
# 🤖 Multi-Agent Systems Lab: AutoGen vs. CrewAI

## Basics and Fundamentals (!!Read this first!!)
Before diving into the lab, please read through the [BASICS.md](BASICS.md) file to understand key concepts about multi-agent systems, architectures, and communication patterns. This foundational knowledge will help you grasp the implementations in this lab.

## 📚 Lab Overview

This lab introduces **multi-agent systems** - where multiple AI agents collaborate to solve complex problems. You'll work with two popular frameworks (**AutoGen** and **CrewAI**) to build, compare, and understand how intelligent agents can work together.

### What You'll Learn
- How to design agents with specific roles and responsibilities
- How agents communicate and collaborate
- Differences between conversational (AutoGen) vs. task-based (CrewAI) approaches
- When to use each framework for different problem types

---

## 🎯 What Are We Building?

### Part 1: AutoGen - Product Planning Workflow
**Scenario:** Build a product plan for an AI-powered interview platform

Four agents work together in sequence:
1. **ResearchAgent** - Analyzes market competitors
2. **AnalysisAgent** - Identifies key opportunities
3. **BlueprintAgent** - Creates product design
4. **ReviewerAgent** - Provides recommendations

**Communication Style:** Conversational (agents chat back and forth)

### Part 2: CrewAI - Travel Planning Workflow
**Scenario:** Plan a 5-day trip to Iceland

Four agents form a "crew":
1. **FlightAgent** - Researches flights
2. **HotelAgent** - Finds accommodations
3. **ItineraryAgent** - Creates daily plans
4. **BudgetAgent** - Calculates costs

**Communication Style:** Task-based (each agent completes assigned tasks)

---

## 🛠️ Technologies Used

### **AutoGen** (Microsoft)
- Framework for building multi-agent systems with LLMs
- Agents communicate conversationally
- Flexible workflow - agents can decide what to do next
- Great for iterative, chat-like problem solving

```python
from autogen import AssistantAgent, UserProxyAgent

assistant = AssistantAgent(name="assistant", llm_config={"config_list": [...]})
user_proxy = UserProxyAgent(name="user_proxy", human_input_mode="NEVER")
user_proxy.initiate_chat(assistant, message="Your task here")
```

### **CrewAI** (Crew Framework)
- High-level framework for orchestrating agent "crews"
- Task-based execution - clear inputs and outputs
- Built-in tools and structured workflows
- Great for sequential, goal-oriented tasks

```python
from crewai import Agent, Task, Crew

agent = Agent(role="...", goal="...", backstory="...")
task = Task(description="...", agent=agent)
crew = Crew(agents=[agent], tasks=[task])
result = crew.kickoff()
```

### **OpenAI API**
- Powers the language models both frameworks use
- GPT-4 or GPT-4-Turbo for intelligent reasoning

---

## 📖 Lab Manual

### Prerequisites
- Python 3.8+
- OpenAI API key (get from https://platform.openai.com/api-keys)
- `pip` package manager

### Quick Setup

**1. Configure API Key:**
```bash
# Copy template
cp .env.example .env

# Add your OpenAI API key
# Edit .env and add:
OPENAI_API_KEY=sk-your-api-key-here
```

**2. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**3. Verify Configuration:**
```bash
python shared_config.py
```

### Running the Demos

**AutoGen Demo:**
```bash
python autogen/autogen_simple_demo.py
```

**CrewAI Demo:**
```bash
python crewai/crewai_demo.py
```

---

## 📁 Project Structure

```
multi-agent/
├── README.md                          ← You are here (complete lab guide)
├── requirements.txt                   ← Install ALL dependencies from here
├── .env.example                       ← Copy to .env (don't commit!)
├── .env                               ← Your configuration (add API key here)
├── shared_config.py                   ← Unified config for both frameworks
│
├── autogen/
│   ├── config.py                      ← AutoGen configuration (uses shared_config)
│   ├── autogen_simple_demo.py         ← RUN THIS: Simple demo
│   └── autogen_interview_platform.py  ← Full implementation
│
└── crewai/
    └── crewai_demo.py                 ← RUN THIS: Travel planning demo
```

---

## 🚀 Getting Started (5 Minutes)

### Step 1: Setup Environment
```bash
# Create .env file with your API key
cp .env.example .env
nano .env  # Add your OPENAI_API_KEY
```

### Step 2: Install Packages
```bash
pip install -r requirements.txt
```

### Step 3: Test Configuration
```bash
python shared_config.py
# Should show: ✅ Configuration validation passed!
```

### Step 4: Run First Demo
```bash
# Try AutoGen
python autogen/autogen_simple_demo.py

# OR try CrewAI
python crewai/crewai_demo.py
```

---

## 🔍 Understanding Multi-Agent Systems

### Key Concepts

**Agent:** An AI entity with a specific role, goal, and reasoning ability
```python
Agent(
    role="Flight Specialist",
    goal="Find the best flights for the trip",
    backstory="You have booked thousands of flights..."
)
```

**Task:** Work to be completed by an agent
```python
Task(
    description="Research flights from NYC to Reykjavik",
    agent=flight_agent,
    expected_output="List of flight options with prices"
)
```

**Workflow:** How agents interact and pass information
- **Conversational** (AutoGen): Agents chat, debate, iterate
- **Sequential** (CrewAI): Each agent completes task, passes output to next
- **Parallel:** Multiple agents work simultaneously (advanced)

### Why Use Multiple Agents?
- **Specialization:** Each agent is expert in one area
- **Modularity:** Easy to add/remove agents
- **Scalability:** Handle complex problems by breaking them down
- **Transparency:** Understand reasoning at each step

---

## 📊 Comparison: AutoGen vs. CrewAI

| Aspect | AutoGen | CrewAI |
|--------|---------|--------|
| **Communication** | Conversational | Task-based |
| **Workflow** | Flexible, agent-decided | Structured, sequential |
| **Setup** | More code, more control | Less code, simpler |
| **Best For** | Iterative problem-solving | Clear workflows |
| **Agent Autonomy** | High (agents decide next steps) | Lower (follows task structure) |
| **Output Structure** | Unstructured conversation | Structured task outputs |
| **Learning Curve** | Steeper | Gentler |

### Choose AutoGen If:
- ✓ Problem requires iteration and refinement
- ✓ Agents need to debate/discuss solutions
- ✓ Output structure is uncertain upfront
- ✓ You need fine-grained control

### Choose CrewAI If:
- ✓ Workflow is well-defined and sequential
- ✓ Each agent has clear inputs/outputs
- ✓ You want faster setup with less code
- ✓ Tasks are independent and composable

---

## 🎓 Lab Exercises

### Exercise 1: Run and Understand
1. Run `autogen/autogen_simple_demo.py`
2. Read the output - understand how agents interact
3. Run `crewai/crewai_demo.py`
4. Compare the communication styles

### Exercise 2: Modify Agent Roles
**AutoGen:** Edit agent backstories in `autogen/config.py`
```python
RESEARCH_AGENT = {
    "role": "Market Researcher",  # ← Modify this
    "temperature": 0.7,
}
```

**CrewAI:** Edit agent definitions in `crewai/crewai_demo.py`
```python
Agent(
    role="Flight Specialist",  # ← Modify this
    goal="...",
    backstory="..."  # ← Add more detail here
)
```

### Exercise 3: Add a New Task
**For AutoGen:** Add a new agent to the workflow
**For CrewAI:** Add a new task to the crew

### Exercise 4: Custom Problem
Try these scenarios with either framework:
- Plan a 3-day conference agenda
- Design a marketing strategy for a product
- Create a research paper outline
- Plan a software architecture

---

## 🔧 Troubleshooting

### "OPENAI_API_KEY is not configured"
```bash
# Make sure .env file exists and has your key
cat .env

# If missing, create it:
cp .env.example .env
# Then edit and add your key
nano .env
```

### "ModuleNotFoundError: No module named 'shared_config'"
```bash
# Run from project root, not from subdirectories
cd /Users/pranavhharish/Desktop/IS-492/multi-agent
python crewai/crewai_demo.py
```

### "Invalid API key" Error
```bash
# Check your key is valid at:
# https://platform.openai.com/account/api-keys

# Make sure it's in .env without quotes:
OPENAI_API_KEY=sk-proj-xxxxx  # ✓ Correct
# OPENAI_API_KEY="sk-proj-xxxxx"  # ✗ Wrong (don't use quotes)
```

### "Rate limit exceeded"
- Wait a few minutes and try again
- Check your API usage: https://platform.openai.com/account/usage

---

## 📚 Additional Resources

### Documentation
- **[AutoGen Docs](https://microsoft.github.io/autogen/)** - Official AutoGen documentation
- **[CrewAI Docs](https://docs.crewai.com/)** - Official CrewAI documentation
- **[OpenAI API](https://platform.openai.com/docs/)** - API reference and guides

### Learning
- **[LLM Agent Systems](https://lilianweng.github.io/posts/2023-06-23-agent/)** - Deep dive into agent theory
- **[ReAct Prompting](https://arxiv.org/abs/2210.03629)** - How agents think and act
- **[Multi-Agent Collaboration](https://arxiv.org/abs/2306.03589)** - Research on agent cooperation

### Community
- **AutoGen:** GitHub discussions at microsoft/autogen
- **CrewAI:** GitHub issues at joaomdmoura/crewai

