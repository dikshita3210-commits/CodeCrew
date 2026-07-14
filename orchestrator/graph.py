from typing import TypedDict, Optional, Annotated
from langgraph.graph import StateGraph, END
from agents.bug_reviewer import review_bugs
from agents.style_reviewer import review_style
from orchestrator.synthesis import synthesize_report


class AgentState(TypedDict):
    code_diff: str
    bug_feedback: Optional[str]
    style_feedback: Optional[str]
    final_report: Optional[str]
    iterations: int


def bug_reviewer_node(state: AgentState) -> AgentState:
    """Agent 1: Reviews for bugs and logic errors."""
    feedback = review_bugs(state["code_diff"])
    return {"bug_feedback": feedback, "iterations": state["iterations"] + 1}


def style_reviewer_node(state: AgentState) -> AgentState:
    """Agent 2: Reviews for style and security."""
    feedback = review_style(state["code_diff"])
    return {"style_feedback": feedback, "iterations": state["iterations"] + 1}


def synthesize_node(state: AgentState) -> AgentState:
    """Orchestrator: Combines both agent outputs into one report."""
    report = synthesize_report(
        code_diff=state["code_diff"],
        bug_feedback=state["bug_feedback"],
        style_feedback=state["style_feedback"]
    )
    return {"final_report": report}


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("bug_reviewer", bug_reviewer_node)
    workflow.add_node("style_reviewer", style_reviewer_node)
    workflow.add_node("synthesizer", synthesize_node)

    # Start from bug_reviewer, then go to style_reviewer
    workflow.add_edge("bug_reviewer", "style_reviewer")
    # Then synthesize
    workflow.add_edge("style_reviewer", "synthesizer")
    workflow.add_edge("synthesizer", END)

    # Set entry point
    workflow.set_entry_point("bug_reviewer")

    graph = workflow.compile()
    return graph
