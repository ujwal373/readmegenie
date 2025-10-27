import requests, base64

def commit_readme(owner, repo, token, readme_text, branch="readmegenie-update"):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # 1️⃣ Get default branch & latest SHA
    repo_info = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=headers).json()
    base_branch = repo_info.get("default_branch", "main")
    sha_latest = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{base_branch}",
        headers=headers
    ).json()["object"]["sha"]

    # 2️⃣ Create new branch
    branch_data = {"ref": f"refs/heads/{branch}", "sha": sha_latest}
    requests.post(f"https://api.github.com/repos/{owner}/{repo}/git/refs", headers=headers, json=branch_data)

    # 3️⃣ Encode README content
    content_b64 = base64.b64encode(readme_text.encode()).decode()

    # 4️⃣ Create or update README.md
    commit_data = {
        "message": "docs: update README via ReadMeGenie 🤖",
        "content": content_b64,
        "branch": branch
    }
    r = requests.put(f"https://api.github.com/repos/{owner}/{repo}/contents/README.md",
                     headers=headers, json=commit_data)

    if r.status_code in [200, 201]:
        return f"https://github.com/{owner}/{repo}/tree/{branch}"
    else:
        raise Exception(f"Commit failed: {r.text}")
