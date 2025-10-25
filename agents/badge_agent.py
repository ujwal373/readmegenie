import requests, urllib.parse

def make_badge(label, message, color="blue", logo=None):
    base = "https://img.shields.io/badge/"
    msg = urllib.parse.quote(message)
    lbl = urllib.parse.quote(label)
    logo_part = f"?logo={urllib.parse.quote(logo)}" if logo else ""
    return f"![{label}](https://img.shields.io/badge/{lbl}-{msg}-{color}{logo_part})"

def github_badges(owner, repo):
    badges = []
    badges.append(f"![GitHub Repo stars](https://img.shields.io/github/stars/{owner}/{repo}?style=social)")
    badges.append(f"![GitHub forks](https://img.shields.io/github/forks/{owner}/{repo}?style=social)")
    badges.append(f"![GitHub issues](https://img.shields.io/github/issues/{owner}/{repo})")
    badges.append(f"![GitHub last commit](https://img.shields.io/github/last-commit/{owner}/{repo})")
    return badges

def language_badges(languages_dict):
    return [make_badge(lang, str(int(pct)) + "%", "brightgreen") for lang, pct in languages_dict.items()]

def generate_badge_block(owner, repo, languages):
    badges = github_badges(owner, repo)
    if languages:
        lang_badges = language_badges(languages)
        badges.extend(lang_badges)
    markdown = " ".join(badges)
    return f"{markdown}\n\n"
