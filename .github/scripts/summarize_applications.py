import os
import csv
import re
from github import Github
from openpyxl import Workbook

# Setup GitHub token and repo from environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)

print("📥 Fetching GitHub issues...")
issues = list(repo.get_issues(state='open', labels=['ambassador']))
print(f"🔍 Total issues fetched: {len(issues)}")

# Markdown extractor
def extract(label, body):
    match = re.search(rf"{re.escape(label)}\s*\n\s*(.+?)(\n|$)", body)
    return match.group(1).strip() if match else ""

# Extracted field definitions
submissions = []
for issue in issues:
    body = issue.body or ""
    entry = {
        "Issue #": issue.number,
        "Nominee Name": extract("Nominee Name", body),
        "Nominee Email": extract("Nominee Email", body),
        "GitHub Handle": extract("Nominee's GitHub or GitLab Handle", body),
        "Organization": extract("(Optional) Organization / Affiliation", body),
        "Location": extract("City, State/Province, Country", body),
        "Nominator Name": extract("Your Name", body),
        "Nominator Email": extract("Your Email (Optional)", body),
        "Contribution Checkboxes": "; ".join(re.findall(r"- \[x\] (.+)", body, re.IGNORECASE)),
        "Ambassador Pitch": extract("🏆 How Would the Nominee Contribute as an Ambassador?", body),
        "Additional Info": extract("Any additional details you'd like to share?", body)
    }

    # Construct clean submission summary
    summary = f"""Contributions:\n{entry['Contribution Checkboxes']}

Ambassador Nomination Statement:\n{entry['Ambassador Pitch']}

GitHub Handle:\n{entry['GitHub Handle']}

Additional Info:\n{entry['Additional Info']}"""
    entry["Submission Summary"] = summary
    submissions.append(entry)

# Deduplicate by nominee email (fallback to name)
print("🧹 Deduplicating...")
latest = {}
for s in sorted(submissions, key=lambda x: x["Issue #"], reverse=True):
    key = (s["Nominee Email"] or s["Nominee Name"]).lower()
    if key not in latest:
        latest[key] = s
deduped = list(latest.values())
duplicates = [s for s in submissions if s not in deduped]

# Output folder
os.makedirs("ambassador", exist_ok=True)

# Save raw submissions
with open("ambassador/submissions_all_raw.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=submissions[0].keys())
    writer.writeheader()
    writer.writerows(submissions)

# Save deduplicated
with open("ambassador/submissions_deduplicated.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=deduped[0].keys())
    writer.writeheader()
    writer.writerows(deduped)

# Save duplicates to Excel
if duplicates:
    wb = Workbook()
    ws = wb.active
    ws.title = "Duplicates Removed"
    ws.append(list(duplicates[0].keys()))
    for row in duplicates:
        ws.append([row.get(k, "") for k in duplicates[0].keys()])
    wb.save("ambassador/submissions_duplicates_removed.xlsx")
    print("📄 Duplicates saved to ambassador/submissions_duplicates_removed.xlsx")

print("✅ Done: All submission data saved.")
