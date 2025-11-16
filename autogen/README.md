# AutoGen Multi-Agent Workflow

## What is AutoGen?

**AutoGen** is Microsoft's open-source framework for building applications with multiple AI agents that can work together autonomously. In this project, we use AutoGen to orchestrate four specialized AI agents that collaborate to create comprehensive product plans.

Each agent is a conversable AI with a specific role and expertise, communicating through structured message passing to solve complex problems that require different perspectives.

---

## What Are We Doing?

We've built an **AI-powered product planning system** that automatically generates comprehensive product plans for new initiatives. The system uses four specialized AI agents working sequentially:

1. **Research Agent** - Analyzes the competitive landscape
2. **Analysis Agent** - Identifies market opportunities
3. **Blueprint Agent** - Designs the product with features and user journeys
4. **Review Agent** - Provides strategic recommendations and implementation roadmaps

### Use Case Example
For an "AI-powered interview platform for startups," the system:
- Researches competitors (HireVue, Pymetrics, Codility)
- Identifies market gaps and opportunities
- Designs core features and user experiences
- Recommends business models and implementation strategy

---

## Workflow Overview

The system follows a **sequential four-phase workflow** where each agent builds upon the work of previous agents:

```
PHASE 1: MARKET RESEARCH (1-2 min)
   ↓ ResearchAgent analyzes competitors and market trends
   ↓
PHASE 2: OPPORTUNITY ANALYSIS (1-2 min)
   ↓ AnalysisAgent identifies 3 key market opportunities
   ↓
PHASE 3: PRODUCT BLUEPRINT (1-2 min)
   ↓ BlueprintAgent defines 5-7 core features & user journeys
   ↓
PHASE 4: STRATEGIC REVIEW (1-2 min)
   ↓ ReviewerAgent provides feasibility and implementation roadmap
   ↓
OUTPUT: Full workflow analysis + executive summary
```

### Data Flow
```
Initial Product Concept
         ↓
    [ResearchAgent]
    Research Output
         ↓
    [AnalysisAgent] (receives research)
    Analysis Output
         ↓
    [BlueprintAgent] (receives research + analysis)
    Blueprint Output
         ↓
    [ReviewerAgent] (receives blueprint)
    Strategic Recommendations
         ↓
    Save to timestamped files
```

### Key Characteristics
- **Autonomous**: No human intervention needed between phases
- **Context-Aware**: Each agent receives all previous outputs
- **Sequential**: Agents work one after another, building on prior insights
- **Specialized**: Each agent has a distinct role and expertise level
- **Documented**: Full outputs saved with timestamps for reproducibility

---

## How Can It Help?

### For Product Teams
- **Rapid Market Analysis**: Generate competitive landscape in minutes
- **Data-Driven Insights**: Identify market opportunities with AI reasoning
- **Product Definition**: Get structured product blueprints with features and user journeys
- **Strategic Planning**: Receive implementation roadmaps and priority actions

### For Entrepreneurs
- **Startup Planning**: Quickly validate business ideas with market analysis
- **Feature Prioritization**: AI-generated feature sets and MVP definitions
- **Business Model Suggestions**: Automated business model recommendations
- **Resource Planning**: Implementation roadmaps with timeline and resource estimates

### For Educators
- **Learn Multi-Agent Systems**: Understand how to orchestrate AI agents
- **Study AI Collaboration**: See how specialized agents work together
- **Experiment with Prompts**: Modify agent behaviors by changing system messages
- **Explore AI Reasoning**: Observe how LLMs approach complex product problems

### For Developers
- **Architecture Reference**: See best practices for multi-agent systems
- **AutoGen Framework**: Learn the ConversableAgent API
- **Scalability Pattern**: Sequential agent pattern that scales to more agents
- **Integration Template**: Base for building similar workflows

---

## Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API key
- Internet connection

### Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Ensure .env is configured in parent directory (../env)
# The shared .env file is used across all multi-agent projects

# 3. Run the demo
python autogen_simple_demo.py          # Quick test (1-2 min)
python autogen_interview_platform.py   # Full workflow (3-5 min)
```

### Check Results
```bash
# View generated outputs
ls -la *.txt
cat workflow_outputs_*.txt
cat summary_*.txt
```

---

## Project Structure

```
autogen/
├── README.md                          # This file
├── config.py                          # Configuration and setup
├── autogen_simple_demo.py             # Lightweight demo (learning)
├── autogen_interview_platform.py      # Full workflow (production)
└── requirements.txt                   # Python dependencies

Shared configuration (from parent directory):
├── ../.env                            # Shared API credentials
└── ../shared_config.py                # Shared configuration

Generated at runtime:
├── workflow_outputs_YYYYMMDD_HHMMSS.txt  # Full detailed outputs
└── summary_YYYYMMDD_HHMMSS.txt           # Executive summary
```

---

## Execution Modes

### Quick Demo (Learning & Testing)
```bash
python autogen_simple_demo.py
```
- **Duration**: 60-90 seconds
- **Tokens**: ~1,500-2,000
- **Cost**: ~$0.05
- **Best for**: Testing, learning, quick validation
- **Output**: Console display only

### Full Workflow (Production)
```bash
python autogen_interview_platform.py
```
- **Duration**: 180-300 seconds (3-5 minutes)
- **Tokens**: ~2,000-3,000
- **Cost**: ~$0.15-0.20
- **Best for**: Comprehensive analysis, documentation
- **Output**: Console display + timestamped files

---

## Agent Roles & Responsibilities

### 1. Research Agent
**Role**: Market Researcher

**Responsibilities**:
- Analyze 3-4 competitors in the market
- Identify key features and positioning strategies
- Research market trends and dynamics
- Highlight gaps and whitespace opportunities

**Sample Questions**:
- Who are the main competitors?
- What features do they offer?
- How is the market positioned?
- What are the market trends?

**Output**: 500-800 words of competitive landscape analysis

---

### 2. Analysis Agent
**Role**: Product Analyst

**Responsibilities**:
- Extract insights from research findings
- Identify 3 key market opportunities
- Assess competitive advantages
- Evaluate market viability

**Analysis Framework**:
- What is the market gap?
- Why does it matter?
- How can we address it?
- What's the potential market impact?

**Output**: 400-600 words of structured opportunity analysis

---

### 3. Blueprint Agent
**Role**: Product Designer

**Responsibilities**:
- Define 5-7 core MVP features
- Create user journey maps
- Identify target user personas
- Highlight competitive differentiation

**Design Elements**:
- Feature definitions with user benefits
- Journey mapping for key workflows
- Persona development (hiring managers, recruiters, candidates)
- Unique value proposition

**Output**: 600-900 words of detailed product blueprint

---

### 4. Review Agent
**Role**: Strategic Reviewer

**Responsibilities**:
- Assess feasibility of the product plan
- Suggest business models
- Create implementation roadmaps
- Prioritize key actions

**Review Aspects**:
- Technical feasibility
- Market fit assessment
- Business model viability
- Resource requirements
- Implementation timeline
- Top 5 priority actions

**Output**: 500-800 words of strategic recommendations

---

## Configuration

### Default Settings
```python
# Model and Performance
OPENAI_MODEL = "gpt-4-turbo-preview"
AGENT_TEMPERATURE = 0.7              # Balanced creativity
AGENT_MAX_TOKENS = 2000
AGENT_TIMEOUT = 300                  # 5 minutes

# Behavior
HUMAN_INPUT_MODE = "NEVER"           # Fully autonomous
VERBOSE = True                        # Show detailed logs
```

### Customize via Shared .env
Edit the shared `.env` file in the parent directory (`../.env`):
```
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview
AGENT_TEMPERATURE=0.7
AGENT_MAX_TOKENS=2000
VERBOSE=True
DEBUG=False
```

This `.env` file is shared across all multi-agent projects (autogen and crewai).

### Switching Models
Edit `config.py` or `.env`:
- Use `gpt-4` for best quality (higher cost)
- Use `gpt-3.5-turbo` for speed (lower cost)
- Use `gpt-4-turbo-preview` for balance

---

## Expected Output Examples

### Phase 1: Research Output
```
Competitors Identified:
- HireVue: Video interview platform, enterprise-focused
- Pymetrics: Neuroscience-based assessments
- Codility: Technical coding challenges

Market Gaps Found:
- Limited real-time interview intelligence
- Poor ATS integration
- Limited support for non-technical roles
- Weak candidate UX
```

### Phase 4: Strategic Recommendations
```
Feasibility: ✓ Highly feasible
Business Model: B2B SaaS with per-interview pricing
Implementation Timeline: 6 months to launch

Top 5 Priorities:
1. Validate market with customer interviews
2. Build technical prototype
3. Secure seed funding
4. Partner with ATS providers
5. Launch beta program

Resource Estimate: 3-5 engineers, 6 months, $500K-1M
```

---

## Features & Capabilities

### Multi-Agent Orchestration
- Sequential workflow with context passing
- Each agent has specialized system prompts
- Autonomous operation without human intervention
- Full message history retained throughout workflow

### Configuration Management
- Centralized .env file for API keys
- Environment variable loading
- Configuration validation before execution
- Easy model switching and customization

### Output Management
- Timestamped files prevent overwriting
- Full workflow outputs with phase separation
- Executive summaries for quick review
- Structured, readable format

### Error Handling
- API key validation
- Configuration verification
- Graceful error messages
- Troubleshooting guidance

---

## Performance Metrics

| Metric | Quick Demo | Full Workflow |
|--------|-----------|---------------|
| Duration | 60-90 sec | 3-5 min |
| API Calls | 4 | 4 |
| Tokens Used | 1,500-2,000 | 2,000-3,000 |
| Estimated Cost | $0.05 | $0.15-0.20 |
| Output | Console | Files + Console |

### Resource Requirements
- **Memory**: 500 MB - 1 GB
- **Network**: Internet required (API calls)
- **Storage**: ~10 KB per run
- **CPU**: Minimal (mostly I/O bound)

---

## Troubleshooting

### Issue: "API key not found"
**Solution**:
```bash
# Ensure the shared .env file is configured in the parent directory:
# /Users/pranavhharish/Desktop/IS-492/multi-agent/.env
# Should contain: OPENAI_API_KEY=sk-your-key
```

### Issue: "Module not found"
**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: "Timeout or slow responses"
**Solution**:
- Reduce AGENT_MAX_TOKENS in config.py
- Switch to gpt-3.5-turbo for faster responses
- Check internet connection

### Issue: "High API costs"
**Solution**:
- Use `autogen_simple_demo.py` for testing
- Switch to gpt-3.5-turbo model
- Reduce AGENT_MAX_TOKENS in config.py

---

## Customization

### Change Product Topic
Edit the initial prompt in the main script:
```python
# Instead of "AI interview platform"
research_output = workflow.initiate_research_phase(
    "E-learning platform for enterprise training"
)
```

### Modify Agent Roles
Edit system messages in `autogen_interview_platform.py`:
```python
# Find the agent creation code and change the system_message
researcher_system_msg = "Your custom role description..."
```

### Add a New Phase
```python
def conduct_new_phase(self, previous_output):
    # Create new agent
    # Initiate conversation
    # Return output
```

---

## Integration with Broader Project

This project is part of a larger multi-agent systems exploration:

```
multi-agent/
├── autogen/                 # This project (uses parent .env)
├── crewai/                  # Alternative framework (CrewAI, uses parent .env)
├── shared_config.py         # Shared configuration across frameworks
└── .env                     # Shared API credentials for all projects
```

Both `autogen` and `crewai` use the same `.env` file at the parent level for unified API key and configuration management. There are no local .env files in each directory.

---

## Use Cases

### 1. Product Planning
Generate comprehensive product plans in minutes instead of weeks
```bash
python autogen_interview_platform.py
```

### 2. Market Research
Quick competitive analysis and opportunity identification
```bash
python autogen_simple_demo.py
```

### 3. Learning & Teaching
Understand multi-agent systems and AI collaboration patterns
- Study the code and run examples
- Modify prompts and observe agent behavior
- Extend with new phases

### 4. Rapid Prototyping
Validate startup ideas with AI-driven analysis
- Quick market validation
- Feature ideation
- Business model suggestions

### 5. Model Comparison
Test different LLM models and compare outputs
- Switch models in config.py
- Compare quality, speed, and cost
- Find optimal model for your use case

---

## Technical Stack

- **Framework**: Microsoft AutoGen (>=0.2.0)
- **LLM**: OpenAI GPT-4 Turbo (switchable)
- **Language**: Python 3.9+
- **API Management**: python-dotenv
- **Validation**: Pydantic (>=2.0.0)
- **HTTP Client**: requests (>=2.31.0)

---

## Next Steps

1. **Run the Demo**: Execute `autogen_simple_demo.py` to see it in action
2. **Review Outputs**: Check generated output files for insights
3. **Customize**: Modify the product topic and run again
4. **Experiment**: Change agent prompts and observe behavior changes
5. **Extend**: Add new phases or agents to the workflow

---

## Learning Resources

### AutoGen Documentation
- Official AutoGen GitHub: https://github.com/microsoft/autogen
- ConversableAgent API: Core agent abstraction used in this project

### AI Product Planning
- Lean Product Development approaches
- Jobs to be Done framework
- Design Thinking for product definition

### Multi-Agent Systems
- Agent-based modeling
- Collaborative AI systems
- Sequential decision making

---

## Summary

The **AutoGen Multi-Agent Workflow** demonstrates how to orchestrate multiple specialized AI agents to solve complex product planning problems. Through sequential collaboration where each agent builds upon previous insights, the system generates comprehensive, well-reasoned product plans in minutes.

**Key Strengths**:
- Fully autonomous - no human intervention needed
- Context-aware - agents build on previous analysis
- Specialized - each agent contributes unique expertise
- Fast - complete analysis in 1-5 minutes
- Educational - excellent for learning multi-agent patterns
- Extensible - easy to add new agents or phases

**Perfect For**: Product teams, entrepreneurs, educators, and developers interested in AI-powered automation and multi-agent systems.
