# CodeCrew — Multi-Agent Code Review

An AI-powered code review system using LangGraph with 2 specialized agents and an orchestrator.

# AGENTS
- **Bug Reviewer**
Agent 1
Logic errors, edge cases, runtime bugs, resource leaks
**Style & Security**
Agent 2
Code style, maintainability, hardcoded secrets, unsafe patterns
**Synthesizer**
*Orchestrator*
Merges both outputs, deduplicates, assigns severity, gives verdict



## Tech Stack
- LangGraph (orchestration)
- LangChain + GPT-4o-mini (agents)
- PyGithub (PR fetching)
- Streamlit (UI)
