import requests, os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

# --- LOAD API KEY ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# --- HELPER: PARSE OWNER & REPO FROM URL ---
def parse_github_url(url: str):
    parts = url.strip("/").split("/")
    if len(parts) < 2:
        return None, None
    return parts[-2], parts[-1]


# --- MAIN FUNCTION ---
def analyze_repo(github_url: str):
    owner, repo = parse_github_url(github_url)
    if not owner or not repo:
        return "Invalid GitHub URL.", None

    base = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}

    info = requests.get(base, headers=headers).json()
    contents = requests.get(f"{base}/contents", headers=headers).json()
    languages = requests.get(f"{base}/languages", headers=headers).json()

    # --- EXTRACT HIGH-LEVEL METADATA ---
    summary = {
        "owner": owner,
        "repo": repo,
        "name": info.get("name"),
        "description": info.get("description", "No description."),
        "stars": info.get("stargazers_count", 0),
        "forks": info.get("forks_count", 0),
        "open_issues": info.get("open_issues_count", 0),
        "language_breakdown": languages,
        "language": ", ".join(languages.keys()) or "Unknown",
        "files": [
            f["name"] for f in contents
            if isinstance(f, dict) and f.get("type") == "file"
        ],
    }

    # --- FETCH SMALL TEXT FILES FOR CONTEXT ---
    extra_context = ""
    for filename in ["requirements.txt", "package.json", "pyproject.toml", "README.md"]:
        file = next((f for f in contents if f["name"].lower() == filename), None)
        if file:
            r = requests.get(file["download_url"])
            if r.ok and len(r.text) < 8000:
                extra_context += f"\n### {filename}\n{r.text}\n"

    # --- SUMMARIZE REPO USING OPENAI ---
    prompt = f"""
    You are an expert summarizer.
    Analyze the following GitHub repository and produce a concise 5-8 line technical summary.

    Repo Name: {summary['name']}
    Description: {summary['description']}
    Languages: {summary['language']}
    Stars: {summary['stars']}
    Forks: {summary['forks']}
    Files: {', '.join(summary['files'][:10])}

    {extra_context}

    Summarize its purpose, core technologies, and how to run it.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        summary_text = response.choices[0].message.content.strip()
    except Exception as e:
        summary_text = f"Error summarizing repo: {e}"

    # --- RETURN BOTH TEXT + METADATA ---
    return summary_text, summary
