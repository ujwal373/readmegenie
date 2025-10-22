import streamlit as st
from agents.generator import generate_readme
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="ReadMeGenie 🧞‍♂️", page_icon="🧞‍♂️", layout="wide")

# --- LOAD CSS ---
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.image("assets/logo.png", width=120)
st.sidebar.title("🧞‍♂️ ReadMeGenie")
st.sidebar.markdown("Craft the perfect README — powered by OpenAI & Streamlit.")

st.sidebar.divider()
title = st.sidebar.text_input("📘 Project Title")
author = st.sidebar.text_input("👤 Your Name")
description = st.sidebar.text_area("📝 Project Description", height=150)
run = st.sidebar.text_area("⚙️ How to Run the Project", height=100)
github = st.sidebar.text_input("🔗 GitHub URL (optional)")
linkedin = st.sidebar.text_input("💼 LinkedIn URL (optional)")
style = st.sidebar.selectbox("🎨 Style", ["Professional", "Minimal", "Fancy", "Emoji"])
generate = st.sidebar.button("✨ Generate README")

# --- HEADER ---
st.markdown("<h1 style='text-align:center;'>🧞‍♂️ ReadMeGenie</h1>", unsafe_allow_html=True)
st.caption("Generate elegant, developer-friendly README.md files instantly.")

# --- MAIN SECTION ---
if generate:
    if not all([title, author, description, run]):
        st.warning("Please fill in all required fields (Title, Name, Description, How to Run).")
    else:
        with st.spinner("🪄 Crafting your README..."):
            readme_text = generate_readme(title, author, description, run, github, linkedin, style)
            st.success("✅ README Generated Successfully!")

            preview_tab, raw_tab = st.tabs(["📄 Preview", "💻 Raw Markdown"])

            with preview_tab:
                st.markdown(readme_text)

            with raw_tab:
                st.code(readme_text, language="markdown")
                st.download_button("💾 Download README.md", data=readme_text, file_name="README.md", mime="text/markdown")

                # Copy to Clipboard button (client-side JS trick)
                copy_js = f"""
                <script>
                function copyToClipboard(text) {{
                    navigator.clipboard.writeText(text);
                    alert("✅ Copied to clipboard!");
                }}
                </script>
                <button onclick="copyToClipboard(`{readme_text}`)">📋 Copy Markdown</button>
                """
                st.components.v1.html(copy_js, height=40)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align:center;'>
        Built with ❤️ by <a href='https://github.com/ujwalmojidra' target='_blank'>Ujwal Mojidra</a> • 
        Powered by <b>OpenAI</b> + <b>Streamlit</b>
    </div>
    """,
    unsafe_allow_html=True
)
