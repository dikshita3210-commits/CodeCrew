# CodeCrew — Multi-Agent Code Review

An AI-powered code review system using LangGraph with 2 specialized agents and an orchestrator.

## Agents
- **Bug Reviewer**: Detects logic errors, edge cases, and runtime bugs
- **Style & Security Reviewer**: Checks code style, maintainability, and security issues
- **Orchestrator**: Combines both agent outputs into a single clean report

## Setup
1. Clone the repo
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with `OPENAI_API_KEY` and `GITHUB_TOKEN`
6. Run: `streamlit run app.py`

## Tech Stack
- LangGraph (orchestration)
- LangChain + GPT-4o-mini (agents)
- PyGithub (PR fetching)
- Streamlit (UI)
