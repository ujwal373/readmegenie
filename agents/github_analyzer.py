import requests, os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def parse_github_url(url: str):
    parts = url.strip("/").split("/")
    if len(parts) < 2:
        return None, None
    return parts[-2], parts[-1]

def analyze_repo(github_url: str):
    owner, repo = parse_github_url(github_url)
    if not owner or not repo:
        return "Invalid GitHub URL."

    base = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}

    info = requests.get(base, headers=headers).json()
    contents = requests.get(f"{base}/contents", headers=headers).json()
    languages = requests.get(f"{base}/languages", headers=headers).json()

    # Extract high-level metadata
    summary = {
        "name": info.get("name"),
        "description": info.get("description", "No description."),
        "stars": info.get("stargazers_count", 0),
        "language": ", ".join(languages.keys()) or "Unknown",
        "files": [f["name"] for f in contents if isinstance(f, dict) and f.get("type") == "file"],
    }

    # Fetch small text files for extra context
    extra_context = ""
    for filename in ["requirements.txt", "package.json", "README.md"]:
        file = next((f for f in contents if f["name"].lower() == filename), None)
        if file:
            r = requests.get(file["download_url"])
            if r.ok and len(r.text) < 8000:
                extra_context += f"\n### {filename}\n{r.text}\n"

    # Summarize repo using OpenAI
    prompt = f"""
    You are an expert summarizer.
    Analyze the following GitHub repository information and provide a concise technical summary.

    Repo Name: {summary['name']}
    Description: {summary['description']}
    Languages: {summary['language']}
    Stars: {summary['stars']}
    Files: {', '.join(summary['files'][:10])}
    {extra_context}

    Summarize its purpose, tech stack, and how to run it in 5-8 lines.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    summary_text = response.choices[0].message.content.strip()
    return summary_text
