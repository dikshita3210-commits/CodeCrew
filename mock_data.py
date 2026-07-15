

SAMPLE_REVIEWS = [
    {
        "repo": "user/auth-service",
        "pr_number": 142,
        "title": "Fix login issue and validate token",
        "author": "kanikakhati",
        "status": "Completed",
        "critical": 1,
        "warning": 2,
        "info": 5,
        "score": 82,
        "files_changed": 6,
        "time_ago": "2h ago",
    },
    {
        "repo": "payment/stripe-integration",
        "pr_number": 88,
        "title": "Add webhook signature verification",
        "author": "teammate-2",
        "status": "Completed",
        "critical": 0,
        "warning": 1,
        "info": 4,
        "score": 91,
        "files_changed": 3,
        "time_ago": "5h ago",
    },
    {
        "repo": "frontend/dashboard",
        "pr_number": 215,
        "title": "Refactor user dashboard components",
        "author": "teammate-3",
        "status": "In Progress",
        "critical": None,
        "warning": None,
        "info": None,
        "score": None,
        "files_changed": 9,
        "time_ago": "1d ago",
    },
    {
        "repo": "api/gateway",
        "pr_number": 67,
        "title": "Add rate limiting middleware",
        "author": "kanikakhati",
        "status": "Completed",
        "critical": 0,
        "warning": 1,
        "info": 3,
        "score": 88,
        "files_changed": 4,
        "time_ago": "3d ago",
    },
]

SAMPLE_PR_LIST = [
    {
        "repo": "user/auth-service",
        "pr_number": 142,
        "title": "Fix login issue and validate token",
        "author": "kanikakhati",
        "additions": 48,
        "deletions": 12,
        "files_changed": 6,
        "status": "Not reviewed",
    },
    {
        "repo": "payment/stripe-integration",
        "pr_number": 88,
        "title": "Add webhook signature verification",
        "author": "teammate-2",
        "additions": 120,
        "deletions": 4,
        "files_changed": 3,
        "status": "Not reviewed",
    },
    {
        "repo": "api/gateway",
        "pr_number": 67,
        "title": "Add rate limiting middleware",
        "author": "kanikakhati",
        "additions": 76,
        "deletions": 20,
        "files_changed": 4,
        "status": "Not reviewed",
    },
]

MOCK_DIFF = """def calculate_total(price, quantity):
-   return price * quantity
+   if quantity < 0:
+       raise ValueError("quantity cannot be negative")
+   return price * quantity"""