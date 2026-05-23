import re
import tkinter as tk
from urllib.parse import urlparse

# --- Detection Logic ---

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "update", "secure", "account",
    "bank", "password", "confirm", "signin"
]

TRUSTED_DOMAINS = [
    "google.com", "paypal.com", "amazon.com", "microsoft.com"
]

def is_ip_address(url):
    return re.match(r"http[s]?://\d+\.\d+\.\d+\.\d+", url)

def has_suspicious_keywords(url):
    return any(word in url.lower() for word in SUSPICIOUS_KEYWORDS)

def has_long_url(url):
    return len(url) > 75

def has_at_symbol(url):
    return "@" in url

def has_multiple_subdomains(domain):
    return domain.count('.') > 2

def is_trusted_domain(domain):
    return any(domain.endswith(trusted) for trusted in TRUSTED_DOMAINS)

def analyze_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc

    score = 0

    if is_ip_address(url):
        score += 2
    if has_suspicious_keywords(url):
        score += 2
    if has_long_url(url):
        score += 1
    if has_at_symbol(url):
        score += 2
    if has_multiple_subdomains(domain):
        score += 1
    if not is_trusted_domain(domain):
        score += 1

    if score >= 5:
        verdict = "⚠️ Likely Phishing URL"
    elif score >= 3:
        verdict = "⚠️ Suspicious URL"
    else:
        verdict = "✅ Likely Safe"

    return score, verdict


# --- GUI Setup ---

def check_url():
    url = entry.get()
    if not url:
        result_label.config(text="Please enter a URL", fg="orange")
        return

    score, verdict = analyze_url(url)
    result_label.config(text=f"Score: {score} | {verdict}", fg="black")


app = tk.Tk()
app.title("Phishing URL Detector")
app.geometry("400x200")

# Title
title_label = tk.Label(app, text="Phishing URL Detector", font=("Arial", 16))
title_label.pack(pady=10)

# Input field
entry = tk.Entry(app, width=50)
entry.pack(pady=5)

# Button
check_button = tk.Button(app, text="Check URL", command=check_url)
check_button.pack(pady=10)

# Result
result_label = tk.Label(app, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Run app
app.mainloop()