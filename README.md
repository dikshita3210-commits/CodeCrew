# 🤖 CodeCrew — Multi-Agent AI Code Reviewer

> **Smarter Code Reviews Through Multi-Agent Intelligence**

CodeCrew is an intelligent **multi-agent AI-powered code review system** that automatically analyzes code changes and GitHub Pull Requests for bugs, logic errors, security vulnerabilities, and code quality issues.

Instead of relying on a single AI model, CodeCrew uses **specialized AI agents** that independently analyze different aspects of the code. Their findings are then combined by a **Synthesizer Orchestrator** to generate a structured and actionable final code review report.

---

## 💡 About the Project

Manual code reviews can be time-consuming and may sometimes miss important bugs, security risks, or maintainability issues.

CodeCrew uses a **multi-agent architecture** to make code reviews more focused and structured. Each AI agent is assigned a specific responsibility, allowing different aspects of the code to be analyzed independently.

Users can review code by:

- 📝 Pasting a code diff directly
- 🔗 Providing a GitHub Pull Request URL

The system processes the code, sends it through specialized reviewer agents, and generates a unified final report.

---

## 🧠 AI Agents

### 🐛 Agent 1 — Bug Reviewer

Focuses on detecting:

- Logic errors
- Edge cases
- Runtime bugs
- Resource leaks
- Potential failures

### 🛡️ Agent 2 — Style & Security Reviewer

Focuses on detecting:

- Code style issues
- Maintainability problems
- Hardcoded secrets
- Unsafe coding patterns
- Basic security vulnerabilities

### 🧠 Synthesizer Orchestrator

The Synthesizer combines the outputs of both reviewer agents and:

- Merges their findings
- Removes duplicate issues
- Assigns severity levels
- Organizes the results
- Generates a final review verdict

---

## 🔄 How It Works

```text
        User Input
           │
           ▼
  ┌──────────────────┐
  │ Paste Code Diff  │
  │        OR        │
  │ GitHub PR URL    │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │  Fetch & Process │
  │    Code Diff     │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │    LangGraph     │
  │  Orchestration   │
  └────────┬─────────┘
           │
      ┌────┴────┐
      │         │
      ▼         ▼
 ┌──────────┐ ┌──────────────┐
 │   Bug    │ │    Style &   │
 │ Reviewer │ │   Security   │
 │  Agent   │ │    Agent     │
 └────┬─────┘ └──────┬───────┘
      │              │
      └──────┬───────┘
             │
             ▼
   ┌─────────────────┐
   │   Synthesizer   │
   │   Orchestrator  │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │  Final AI Code  │
   │  Review Report  │
   └─────────────────┘
```

---

## ✨ Key Features

- 🤖 Multi-agent AI code review pipeline
- 🐛 Bug and logic error detection
- 🔍 Edge case and runtime issue detection
- 🔐 Security vulnerability analysis
- 🔑 Hardcoded secret detection
- 🧹 Code style and maintainability review
- 🔗 GitHub Pull Request integration
- 📝 Direct code diff analysis
- 🧠 Multi-agent orchestration with LangGraph
- 🔄 Automatic merging and deduplication of findings
- 🚨 Issue severity classification
- ✅ Final code review verdict
- 📊 Interactive Streamlit interface
- 📄 Structured AI-generated review reports

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **LangGraph** | Multi-agent workflow orchestration |
| **LangChain** | Building and managing AI agents |
| **GPT-4o-mini** | AI model powering the reviewer agents |
| **PyGithub** | Fetching GitHub Pull Requests and code diffs |
| **Streamlit** | Interactive web application and UI |

---

## 🎯 Why Multi-Agent Architecture?

CodeCrew divides the code review process among specialized AI agents rather than asking a single agent to analyze everything at once.

This provides:

- **Specialization** — Each agent focuses on a specific category of issues.
- **Modularity** — Additional reviewer agents can be added in the future.
- **Separation of Concerns** — Bug detection and style/security analysis are handled independently.
- **Structured Orchestration** — LangGraph manages the multi-agent workflow.
- **Unified Results** — The Synthesizer combines multiple perspectives into one actionable report.

---

## 🔮 Future Enhancements

- Automated review comments directly on GitHub Pull Requests
- Support for private repositories
- Additional specialized reviewer agents
- Automated test case generation
- Performance optimization analysis
- Automatic code fix suggestions
- CI/CD integration for automated code reviews

---

## 👥 Team  Stochastic girls

CodeCrew was developed as an **Agentic AI Internship Project** by a team of five members.
| Team Members | 
|---|
| **Dikshita**  | 
| **Manshi Rawat** | 
| **Kanika Khati** | 
| **Namrata Yadav** | 
| **Kavya Pandey** | 

The project demonstrates how specialized AI agents can collaborate through orchestration to automate and improve real-world software development workflows.

---

### ⭐ CodeCrew — Smarter Code Reviews Through Multi-Agent Intelligence

Built with **LangGraph • LangChain • GPT-4o-mini • PyGithub • Streamlit*

