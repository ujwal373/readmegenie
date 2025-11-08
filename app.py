import streamlit as st
from agents.generator import generate_readme
from agents.github_analyzer import analyze_repo
from agents.badge_agent import generate_badge_block
from agents.commit_agent import commit_readme
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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
# Initialize Session State
# ===========================
if "page" not in st.session_state:
    st.session_state.page = "input"
if "meta" not in st.session_state:
    st.session_state.meta = None
if "readme_text" not in st.session_state:
    st.session_state.readme_text = ""

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
# PAGE 1: Input Details
# ===========================
if st.session_state.page == "input":
    st.title("🧞‍♂️ ReadMeGenie")
    st.caption("Step 1 of 2 — Fill in your project details")

    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("📘 Project Title")
        author = st.text_input("👤 Your Name")
        github = st.text_input("🔗 GitHub URL (optional)")
        linkedin = st.text_input("💼 LinkedIn URL (optional)")

    with col2:
        description = st.text_area("📝 Project Description", height=150)
        run = st.text_area("⚙️ How to Run the Project", height=100)
        style = st.selectbox("🎨 Style", ["Professional", "Minimal", "Fancy", "Emoji"])

    st.divider()
    if st.button("🧠 Auto-Analyze from GitHub"):
        if github:
            with st.spinner("Analyzing repository..."):
                try:
                    summary, meta = analyze_repo(github)
                    st.session_state.meta = meta
                    st.success("✅ Repo analyzed successfully!")
                    st.text_area("📄 Auto Summary (editable)",
                                 value=summary, height=200, key="auto_summary")
                    description = summary
                except Exception as e:
                    st.error(f"❌ Analysis failed: {e}")
        else:
            st.warning("Please enter a GitHub repo URL first.")

    st.divider()
    if st.button("➡️ Continue to Generate"):
        if not all([title, author, description, run]):
            st.warning("Please fill in all required fields before continuing.")
        else:
            st.session_state.project_data = {
                "title": title,
                "author": author,
                "description": description,
                "run": run,
                "github": github,
                "linkedin": linkedin,
                "style": style,
            }
            st.session_state.page = "generate"
            st.rerun()

# ===========================
# PAGE 2: Generate README
# ===========================
elif st.session_state.page == "generate":
    st.title("🧞‍♂️ ReadMeGenie")
    st.caption("Step 2 of 2 — Review, Generate, and Publish your README")

    proj = st.session_state.project_data
    meta = st.session_state.meta

    badge_block = ""
    chart_md = ""
    if meta:
        badge_block = generate_badge_block(meta["owner"], meta["repo"], meta["language_breakdown"])
        chart_md = language_chart(meta["language_breakdown"])
        st.markdown(badge_block, unsafe_allow_html=True)
        st.markdown(chart_md, unsafe_allow_html=True)

    if st.button("✨ Generate README"):
        with st.spinner("Crafting your README..."):
            readme_text = generate_readme(
                proj["title"], proj["author"], proj["description"],
                proj["run"], proj["github"], proj["linkedin"], proj["style"]
            )
            if badge_block or chart_md:
                readme_text = badge_block + chart_md + readme_text

            st.session_state.readme_text = readme_text
            st.success("✅ README Generated Successfully!")

    if st.session_state.readme_text:
        preview_tab, raw_tab = st.tabs(["📄 Preview", "💻 Raw Markdown"])
        with preview_tab:
            st.markdown(st.session_state.readme_text)
        with raw_tab:
            st.code(st.session_state.readme_text, language="markdown")
            st.download_button("💾 Download README.md",
                               data=st.session_state.readme_text,
                               file_name="README.md",
                               mime="text/markdown")

    st.divider()
    if st.button("⬅️ Back to Input"):
        st.session_state.page = "input"
        st.rerun()

    st.subheader("📤 Publish to GitHub")
    token = st.text_input("🔑 GitHub Personal Access Token", type="password")
    branch = st.text_input("🌿 Branch name", value="readmegenie-update")
    if st.button("🚀 Commit to GitHub"):
        if meta and token:
            with st.spinner("Pushing README to GitHub..."):
                try:
                    url = commit_readme(meta["owner"], meta["repo"], token, st.session_state.readme_text, branch)
                    st.success(f"✅ README pushed successfully! [View on GitHub]({url})")
                except Exception as e:
                    st.error(f"❌ Commit failed: {e}")
        else:
            st.warning("Missing GitHub repo or token.")
