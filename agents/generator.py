import os, textwrap
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

# Load .env locally, fallback to Streamlit secrets on deployment
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))

def generate_readme(project_title, author, description, run_instructions, github=None, linkedin=None, style="Professional"):
    client = OpenAI(api_key=api_key)
    
    system_prompt = "You are ReadMeGenie, an expert in writing beautiful, developer-friendly README.md files."
    
    user_prompt = textwrap.dedent(f"""
    Project Title: {project_title}
    Author: {author}
    Description: {description}
    How to Run: {run_instructions}
    GitHub: {github or "Not provided"}
    LinkedIn: {linkedin or "Not provided"}
    Style: {style}

    Write a clean, detailed README.md with:
    1. Title with emojis/badges
    2. Overview & Features
    3. Folder Structure (code block)
    4. Installation + Run Steps
    5. Author Links (GitHub + LinkedIn)
    Use Markdown formatting.
    """)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
