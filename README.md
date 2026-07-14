# CodeCrew — Multi-Agent Code Review

An AI-powered code review system using LangGraph with 2 specialized agents and an orchestrator.

## Agents
- **Bug Reviewer**: Detects logic errors, edge cases, and runtime bugs
- **Style & Security Reviewer**: Checks code style, maintainability, and security issues
- **Orchestrator**: Combines both agent outputs into a single clean report


## Tech Stack
- LangGraph (orchestration)
- LangChain + GPT-4o-mini (agents)
- PyGithub (PR fetching)
- Streamlit (UI)
