
from langchain_ollama import ChatOllama


SYNTHESIS_PROMPT = """You are a senior tech lead reviewing code. You have received feedback from two specialized AI reviewers:

BUG REVIEWER FINDINGS:
{bug_feedback}

STYLE & SECURITY REVIEWER FINDINGS:
{style_feedback}

Your task is to combine these into a single, clean, actionable code review report.

Format the report as follows:
1. SUMMARY — A brief overview of the PR quality (1-2 sentences)
2. CRITICAL ISSUES — All CRITICAL severity items from both reviewers, combined
3. WARNINGS — All WARNING severity items
4. SUGGESTIONS — All INFO/suggestion items
5. OVERALL VERDICT — One of: APPROVE, REQUEST CHANGES, or COMMENT

Be concise. Remove duplicate findings. Prioritize actionable feedback over nitpicks.
"""


def synthesize_report(code_diff: str, bug_feedback: str, style_feedback: str) -> str:
    model = ChatOllama(model="llama3.1", temperature=0.1)
    response = model.invoke(
        SYNTHESIS_PROMPT.format(
            bug_feedback=bug_feedback,
            style_feedback=style_feedback
        )
    )
    return response.content
