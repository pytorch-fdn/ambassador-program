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

# Define helper function to extract field content by label
def extract(label, body):
    pattern = rf"{re.escape(label)}\s*\n+(.+?)(\n\S|\Z)"
    match = re.search(pattern, body, re.DOTALL)
    return match.group(1).strip() if match else ""

# Create output list
output_rows = []

for issue in issues:
    body = issue.body or ""
    output_rows.append({
        "Submission ID": issue.number,
        "How Would the Nominee Contribute as an Ambassador?": extract("🏆 How Would the Nominee Contribute as an Ambassador?", body),
        "Any Additional Details": extract("Any additional details you'd like to share?", body)
    })

# Write to CSV
os.makedirs("ambassador", exist_ok=True)
with open("ambassador/contribution_details.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=output_rows[0].keys())
    writer.writeheader()
    writer.writerows(output_rows)

print("📄 File written to ambassador/contribution_details.csv")
