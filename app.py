import streamlit as st
from agents.generator import generate_readme
from agents.github_analyzer import analyze_repo
from agents.badge_agent import generate_badge_block
from agents.commit_agent import commit_readme
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# ===========================
# Helper: Language Chart
# ===========================
def language_chart(languages):
    if not languages:
        return ""
    fig, ax = plt.subplots()
    ax.pie(languages.values(), labels=languages.keys(), autopct="%1.1f%%")
    ax.set_title("Language Breakdown")
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return f"![Language Chart](data:image/png;base64,{b64})\n\n"


# ===========================
# Page Config
# ===========================
st.set_page_config(page_title="ReadMeGenie 🧞‍♂️", page_icon="🧞‍♂️", layout="wide")

# ===========================
# Load Custom CSS
# ===========================
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===========================
# Sidebar Input
# ===========================
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

st.sidebar.subheader("🔗 Optional: GitHub Repository URL")
repo_url = st.sidebar.text_input("Paste your GitHub repo link (optional)")
auto_analyze = st.sidebar.button("🧠 Auto-Analyze Repo")

# ===========================
# Header
# ===========================
st.markdown("<h1 style='text-align:center;'>🧞‍♂️ ReadMeGenie</h1>", unsafe_allow_html=True)
st.caption("Generate elegant, developer-friendly README.md files instantly.")

# ===========================
# GitHub Analyzer Section
# ===========================
meta = None
badge_block = ""
chart_md = ""

if auto_analyze and repo_url:
    with st.spinner("🔍 Analyzing GitHub repository..."):
        try:
            auto_summary, meta = analyze_repo(repo_url)
            if meta:
                st.success("✅ Repository analyzed successfully!")

                # --- Generate badges and chart ---
                badge_block = generate_badge_block(
                    meta["owner"], meta["repo"], meta["language_breakdown"]
                )
                chart_md = language_chart(meta["language_breakdown"])

                # --- Display results ---
                st.markdown(badge_block, unsafe_allow_html=True)
                st.markdown(chart_md, unsafe_allow_html=True)
                st.text_area("📄 Auto Summary (editable)",
                             value=auto_summary, height=200, key="auto_summary")

                # Pre-fill project description with summary
                description = auto_summary
            else:
                st.warning("⚠️ Could not retrieve full metadata.")
        except Exception as e:
            st.error(f"❌ GitHub analysis failed: {e}")

# ===========================
# Generate README
# ===========================
if generate:
    if not all([title, author, description, run]):
        st.warning("Please fill in all required fields (Title, Name, Description, How to Run).")
    else:
        with st.spinner("🪄 Crafting your README..."):
            readme_text = generate_readme(title, author, description, run, github, linkedin, style)

            # --- Prepend badges and chart (if available) ---
            if badge_block or chart_md:
                readme_text = badge_block + chart_md + readme_text

            st.success("✅ README Generated Successfully!")

            preview_tab, raw_tab = st.tabs(["📄 Preview", "💻 Raw Markdown"])
            with preview_tab:
                st.markdown(readme_text)

            with raw_tab:
                st.code(readme_text, language="markdown")
                st.download_button("💾 Download README.md", data=readme_text,
                                   file_name="README.md", mime="text/markdown")

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

# ===========================
# Commit to GitHub Section
# ===========================
if meta and "readme_text" in locals():
    st.divider()
    st.subheader("📤 Publish to GitHub")
    st.caption(
        "Paste your **GitHub Personal Access Token (PAT)** below "
        "to automatically create a new branch and upload this README.md to your repository."
    )

    github_token = st.text_input("🔑 GitHub Personal Access Token", type="password")
    branch_name = st.text_input("🌿 Branch name", value="readmegenie-update")
    commit_btn = st.button("🚀 Commit to GitHub")

    if commit_btn and github_token:
        with st.spinner("Pushing README to GitHub..."):
            try:
                commit_url = commit_readme(
                    meta["owner"], meta["repo"], github_token, readme_text, branch_name
                )
                st.success(f"✅ README pushed successfully! [View branch on GitHub]({commit_url})")
            except Exception as e:
                st.error(f"❌ Commit failed: {e}")

# ===========================
# Footer
# ===========================
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
