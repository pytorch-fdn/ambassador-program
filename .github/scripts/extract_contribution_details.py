import os
import csv
import re
from github import Github

# Load GitHub credentials
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)

print("🔍 Fetching open GitHub issues with 'ambassador' label...")
issues = list(repo.get_issues(state="open", labels=["ambassador"]))
print(f"✅ Found {len(issues)} issues")

# Extract plain text response by label
def extract(label, body):
    pattern = rf"{re.escape(label)}\s*\n+(.+?)(\n\S|\Z)"
    match = re.search(pattern, body, re.DOTALL)
    return match.group(1).strip() if match else ""

# Extract checked checkbox lines
def extract_checkboxes(body):
    matches = re.findall(r"- \[x\] (.+)", body, re.IGNORECASE)
    return "\n".join(f"- [x] {m.strip()}" for m in matches)

# Build rows
output_rows = []
for issue in issues:
    body = issue.body or ""
    output_rows.append({
        "Submission ID": issue.number,
        "Contributions": extract_checkboxes(body),
        "How Would the Nominee Contribute as an Ambassador?": extract("🏆 How Would the Nominee Contribute as an Ambassador?", body),
        "Any Additional Details": extract("Any additional details you'd like to share?", body)
    })

# Write to CSV
os.makedirs("ambassador", exist_ok=True)
output_path = "ambassador/contribution_details.csv"

with open(output_path, "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=output_rows[0].keys())
    writer.writeheader()
    writer.writerows(output_rows)

print(f"📄 File written to {output_path}")
