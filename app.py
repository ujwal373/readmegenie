import streamlit as st
from agents.generator import generate_readme

st.set_page_config(page_title="ReadMeGenie 🧞‍♂️", layout="wide")

st.title("🧞‍♂️ ReadMeGenie – Your AI README Maker")
st.write("Generate beautiful README.md files instantly — built by developers, for developers.")

with st.sidebar:
    st.header("🧠 Enter Your Project Details")
    title = st.text_input("📘 Project Title")
    author = st.text_input("👤 Your Name")
    description = st.text_area("📝 Project Description", height=180)
    run = st.text_area("⚙️ How to Run the Project", height=100)
    github = st.text_input("🔗 GitHub URL (optional)")
    linkedin = st.text_input("💼 LinkedIn URL (optional)")
    style = st.selectbox("🎨 Style", ["Professional", "Minimal", "Fancy", "Emoji"])
    generate = st.button("✨ Generate README")

if generate:
    if not all([title, author, description, run]):
        st.warning("Please fill in all required fields (Title, Name, Description, How to Run).")
    else:
        with st.spinner("🪄 Crafting your README..."):
            readme_text = generate_readme(title, author, description, run, github, linkedin, style)
            st.success("✅ README Generated Successfully!")
            st.markdown(readme_text)

            st.download_button(
                label="💾 Download README.md",
                data=readme_text,
                file_name="README.md",
                mime="text/markdown"
            )

st.markdown("---")
st.caption("Built with ❤️ using Streamlit + OpenAI | © 2025 ReadMeGenie")
