
from langchain_ollama import ChatOllama


BUG_REVIEWER_PROMPT = """You are an expert code reviewer specializing in detecting bugs, logic errors, and edge cases.

Your task is to review the code diff provided and identify:
1. Logic errors (off-by-one, incorrect conditions, wrong return values)
2. Runtime errors (null references, unhandled exceptions, type mismatches)
3. Edge cases (empty inputs, boundary values, race conditions)
4. Resource leaks (unclosed files, missing cleanup, memory issues)

For each issue found, provide:
- Severity (CRITICAL, WARNING, INFO)
- File and line reference
- A clear description of the bug
- A suggested fix

If no issues are found, state that clearly.

CODE DIFF:
{code_diff}
"""


def review_bugs(code_diff: str ) -> str:
    model = ChatOllama(model="llama3.1", temperature=0.2)
    response = model.invoke(BUG_REVIEWER_PROMPT.format(code_diff=code_diff))
    return response.content

