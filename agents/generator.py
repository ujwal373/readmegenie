import os, textwrap, yaml
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
from agents.utils import detect_stack

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def load_style(style_name):
    with open("prompts/styles.yaml") as f:
        styles = yaml.safe_load(f)
    return styles.get(style_name.lower(), styles["professional"])

def generate_readme(project_title, author, description, run_instructions, github=None, linkedin=None, style="Professional"):
    style_cfg = load_style(style)
    stack_info = detect_stack(description, run_instructions)

    system_prompt = "You are ReadMeGenie, an expert in crafting beautiful README.md files for developers."

    user_prompt = textwrap.dedent(f"""
    Project Title: {project_title}
    Author: {author}
    Description: {description}
    How to Run: {run_instructions}
    GitHub: {github or "Not provided"}
    LinkedIn: {linkedin or "Not provided"}

    Detected Tech Stack:
    {', '.join(stack_info)}

    Tone: {style_cfg['tone']}
    Use Emojis: {style_cfg['emoji']}

    Please generate a README.md that:
    - Includes relevant setup or prerequisites based on the detected stack.
    - Matches the requested tone/style.
    - Contains sections: Overview, Features, Folder Structure, Installation, Usage, Author Info.
    - Is formatted in Markdown.
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
