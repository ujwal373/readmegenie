# 🧞‍♂️ ReadMeGenie — AI-Powered README Generator

ReadMeGenie is an **AI documentation companion** for developers who want elegant, complete, and visually engaging `README.md` files without the hassle.  
Just enter your project details — or paste a GitHub repo link — and let the Genie craft a perfect README with badges, visuals, and even direct GitHub publishing.

---

## ✨ Features

- **🧠 AI-Generated READMEs** — Uses OpenAI GPT models to create professional, Markdown-formatted documentation.
- **🔗 GitHub Auto-Analyzer** — Fetches repo details, files, and languages directly from GitHub.
- **🏷️ Badge & Chart Generator** — Adds GitHub stars, forks, issues, and language charts using Shields.io and Matplotlib.
- **✍️ Smart Editor Mode** — Allows selective AI rewriting of README sections (improve tone, shorten, add emojis, etc.).
- **📤 GitHub Commit Agent** — Pushes the generated README to your repository with a new branch and commit.
- **🧩 Modular Multi-Agent Design** — Each feature (generation, analysis, badges, editing, commit) runs as an independent agent.
- **🌈 Beautiful Streamlit UI** — Intuitive sidebar controls, live preview, and markdown download.

---

## 🏗️ Architecture Overview

```
User Input / GitHub URL
        ↓
🧠 GitHub Analyzer Agent
        ↓
🏷️ Badge & Chart Agent
        ↓
✨ Generator Agent (OpenAI)
        ↓
✍️ Editor Agent (optional)
        ↓
📤 Commit Agent (GitHub API)
        ↓
README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/ujwalmojidra/readmegenie.git
cd readmegenie
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set up environment variables
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

> 💡 When deploying on Streamlit Cloud, add your key to **Secrets** instead of a `.env` file.

### 4️⃣ Run the app
```bash
streamlit run app.py
```

### 5️⃣ (Optional) Deploy on Streamlit Cloud
- Push this repo to GitHub.  
- Create a new app on [Streamlit Cloud](https://streamlit.io/cloud).  
- Set secrets and environment variables under **Settings → Secrets**.  

---

## ⚙️ Folder Structure

```
ReadMeGenie/
├── app.py                        # Main Streamlit app (orchestrator)
├── agents/
│   ├── generator.py              # README generation logic (OpenAI)
│   ├── github_analyzer.py        # GitHub API analyzer
│   ├── badge_agent.py            # Badge and chart generator
│   ├── commit_agent.py           # GitHub commit handler
│   └── utils.py                  # Stack detection helpers
├── assets/
│   ├── logo.png                  # App logo
│   └── style.css                 # Custom UI styles
├── prompts/
│   └── styles.yaml               # Predefined tone/style templates
├── requirements.txt
└── .env (local)
```

---

## 🧩 Agents Overview

| Agent | Description |
|--------|--------------|
| 🧠 **Generator Agent** | Creates full README from title, description, and run instructions using OpenAI. |
| 🔍 **GitHub Analyzer** | Extracts repo info, languages, and content for better context. |
| 🏷️ **Badge Agent** | Generates live Shields.io badges and Matplotlib language pie charts. |
| ✍️ **Editor Agent** | Rewrites specific sections of the README on demand. |
| 📤 **Commit Agent** | Pushes the generated README.md to GitHub via API. |

---

## 🪪 Example Output

```markdown
# MyApp 🚀

A Python-based FastAPI application that analyzes DeFi wallet risk on Solana.
...

![GitHub stars](https://img.shields.io/github/stars/ujwalmojidra/myapp?style=social)
![GitHub forks](https://img.shields.io/github/forks/ujwalmojidra/myapp?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/ujwalmojidra/myapp)
```

---

## 💡 Tech Stack

- **Frontend:** Streamlit  
- **Backend:** OpenAI GPT-4o-mini  
- **Data Visualization:** Matplotlib  
- **Version Control:** GitHub REST API v3  
- **Environment:** Python 3.10+  

---

## 🧰 Requirements

```bash
streamlit
openai
requests
python-dotenv
matplotlib
PyYAML
```

---

## 📤 Commit to GitHub (optional)

Paste your **Personal Access Token** with `repo` permissions in the app sidebar and click **Commit to GitHub** —  
ReadMeGenie will create a new branch (`readmegenie-update`) and push your freshly generated README.

---

## ❤️ Credits

Built by [**Ujwal Mojidra**](https://github.com/ujwalmojidra)  
Supercharged with **OpenAI GPT** + **Streamlit**

---

## 🧭 License
This project is licensed under the **MIT License** — feel free to use, modify, and share.
