# 📄 ReadMeGenie

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-orange.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)

---

## Overview
Welcome to **ReadMeGenie**! This Streamlit application is designed to streamline the creation of professional `README.md` files. With the help of an AI agent, you can generate comprehensive content based on your project details entered through user-friendly form inputs. 

The app provides a live Markdown preview and allows you to download your generated README file directly, all within the intuitive Streamlit framework—no separate backend required!

## Features
✨ **AI-Powered Content Generation**: Utilize OpenAI's API to create well-structured README files effortlessly.  
🔍 **Live Markdown Preview**: See your README update in real-time as you input information.  
⬇️ **Downloadable Output**: Save your generated README as a Markdown file with just one click.  
🛠️ **Simple Setup**: Minimal installation requirements make it easy to get started.  

## Folder Structure
```
readmegenie/
├── app.py                  # Main application file
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (API keys)
└── .envexample             # Example .env file
```

## Installation
To get started with ReadMeGenie, follow these steps:

1. **Download all the files** from the repository.
2. **Edit the `.env` file**: Add your OpenAI API key. You can use `.envexample` as a reference to format your own `.env`.
3. **Install the required packages** by running the following command in your terminal:
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the application**:
    ```bash
    streamlit run app.py
    ```

## Usage
Once the application is running, navigate to the provided local URL (usually `http://localhost:8501`) in your web browser. Fill out the form with your project details, and watch as ReadMeGenie crafts your README.md file. When you are satisfied, download it directly to your device!

## Author Info
👤 **Ujwal Mojidra**  
[LinkedIn](https://www.linkedin.com/in/ujwal-mojidra-28098723a/)  
[GitHub](https://github.com/ujwal373/readmegenie)  

---

Thank you for using ReadMeGenie! If you have any questions or feedback, feel free to reach out. Happy coding! 🚀
