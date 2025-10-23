import re

# Define common tech keywords and short descriptions
STACK_KEYWORDS = {
    "streamlit": "Streamlit app (Python web framework for data apps)",
    "fastapi": "FastAPI backend (Python API framework)",
    "flask": "Flask microservice",
    "react": "React frontend (JavaScript library)",
    "docker": "Docker containerized setup",
    "node": "Node.js environment",
    "express": "Express.js server",
    "python": "Python-based project",
    "r": "R statistical scripts",
    "sql": "Database (SQL based)",
    "mongodb": "MongoDB (NoSQL database)",
    "postgres": "PostgreSQL database",
    "aws": "AWS cloud components",
    "gcp": "Google Cloud Platform setup",
    "firebase": "Firebase backend services",
    "next": "Next.js frontend framework",
    "vue": "Vue.js frontend framework",
}

def detect_stack(description: str, run_instructions: str):
    text = f"{description.lower()} {run_instructions.lower()}"
    found = [k for k in STACK_KEYWORDS if re.search(rf"\\b{k}\\b", text)]
    if not found:
        return ["General project (no specific stack detected)"]
    return [STACK_KEYWORDS[k] for k in found]
