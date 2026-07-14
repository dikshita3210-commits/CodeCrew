from langchain_ollama import ChatOllama


STYLE_REVIEWER_PROMPT = """You are an expert code reviewer specializing in code style, maintainability, and basic security.

Your task is to review the code diff provided and identify:
1. Code style issues (naming conventions, inconsistent formatting, overly complex functions)
2. Maintainability concerns (hardcoded values, missing documentation, duplicate logic)
3. Basic security issues (hardcoded credentials, SQL injection patterns, unsafe eval/exec usage, exposed secrets)
4. Best practice violations (missing error handling, improper imports, inefficient algorithms)

For each issue found, provide:
- Severity (CRITICAL, WARNING, INFO)
- File and line reference
- A clear description of the issue
- A suggested improvement

If no issues are found, state that clearly.

CODE DIFF:
{code_diff}
"""

def review_style(code_diff: str) -> str:
    model = ChatOllama(model="llama3.1", temperature=0.2)
    response = model.invoke(STYLE_REVIEWER_PROMPT.format(code_diff=code_diff))
    return response.content
