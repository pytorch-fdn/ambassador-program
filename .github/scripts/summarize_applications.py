import os
import csv
import re
from github import Github
from openpyxl import Workbook

# Get GitHub token and repository name
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

# Authenticate
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)

print("📥 Fetching open GitHub issues with 'ambassador' label...")
issues = list(repo.get_issues(state='open', labels=['ambassador']))
print(f"✅ Total submissions found: {len(issues)}")

# Helper to extract text fields
def extract(label, body):
    pattern = rf"{re.escape(label)}\s*\n+(.+?)(\n\S|\Z)"
    match = re.search(pattern, body, re.DOTALL)
    return match.group(1).strip() if match else ""

# Extract all checkboxes
def extract_checkboxes(body):
    boxes = re.findall(r"- \[.?] .+", body)
    return "\n".join(boxes) if boxes else ""

# Build submissions list
submissions = []
for issue in issues:
    body = issue.body or ""

    contributions = extract_checkboxes(body)
    ambassador_plan = extract("How Would the Nominee Contribute as an Ambassador?", body)
    additional_info = extract("Any additional details you'd like to share?", body)

    summary = f"""Contributions:
{contributions}

How Would the Nominee Contribute as an Ambassador?
{ambassador_plan}

Additional Notes:
{additional_info}
"""

    entry = {
        "Issue #": issue.number,
        "Nominee Name": extract("Nominee Name", body),
        "Nominee Email": extract("Nominee Email", body),
        "GitHub Handle": extract("Nominee's GitHub or GitLab Handle", body),
        "Submission Summary": summary.strip()
    }
    submissions.append(entry)

# Deduplicate by email or name (most recent kept)
latest_submissions = {}
for entry in sorted(submissions, key=lambda x: x["Issue #"], reverse=True):
    key = (entry["Nominee Email"] or entry["Nominee Name"]).lower()
    if key not in latest_submissions:
        latest_submissions[key] = entry

deduped = list(latest_submissions.values())
duplicates = [s for s in submissions if s not in deduped]

# Save outputs
os.makedirs("ambassador", exist_ok=True)

with open("ambassador/submissions_all_raw.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=submissions[0].keys())
    writer.writeheader()
    writer.writerows(submissions)

with open("ambassador/submissions_deduplicated.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=deduped[0].keys())
    writer.writeheader()
    writer.writerows(deduped)

if duplicates:
    wb = Workbook()
    ws = wb.active
    ws.title = "Duplicates Removed"
    ws.append(list(duplicates[0].keys()))
    for row in duplicates:
        ws.append([row.get(k, "") for k in duplicates[0].keys()])
    wb.save("ambassador/submissions_duplicates_removed.xlsx")

print("✅ Done. Files generated in 'ambassador/' folder.")
