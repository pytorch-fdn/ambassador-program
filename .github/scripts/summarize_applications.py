import os
import csv
import re
from github import Github
from openpyxl import Workbook

# Load GitHub access credentials
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)

print("📥 Fetching open GitHub issues with 'ambassador' label...")
issues = repo.get_issues(state='open', labels=['ambassador'])

submissions = []

# Helper to extract plain-text responses
def extract(label, body):
    match = re.search(rf"{label}\s*\n\s*(.+)", body)
    return match.group(1).strip() if match else ""

# Helper to extract checkbox options
def extract_checkboxes(body):
    checkbox_section = re.findall(r"How has the nominee contributed to PyTorch\?\s*\n((?:- \[.\] .+\n?)+)", body)
    if not checkbox_section:
        return []
    return checkbox_section[0].strip().splitlines()

# Process each issue
for issue in issues:
    body = issue.body or ""

    name = extract("Nominee Name", body)
    email = extract("Nominee Email", body)
    github_handle = extract("Nominee's GitHub or GitLab Handle", body)
    ambassador_plan = extract("🏆 How Would the Nominee Contribute as an Ambassador?", body)
    additional_info = extract("Any additional details you'd like to share?", body)
    contributions = extract_checkboxes(body)

    # Format submission summary
    submission_summary = f"""**GitHub Handle:** {github_handle or 'Not Provided'}

**How Has the Nominee Contributed to PyTorch?**
{chr(10).join(contributions) if contributions else 'Not Provided'}

**Ambassador Contribution Plan**
{ambassador_plan or 'Not Provided'}

**Additional Information**
{additional_info or 'Not Provided'}
"""

    submissions.append({
        "Issue #": issue.number,
        "Nominee Name": name,
        "Nominee Email": email,
        "Submission Summary": submission_summary.strip()
    })

print(f"✅ Total submissions found: {len(submissions)}")

# Deduplicate by email (fallback to name)
latest_by_email = {}
for entry in sorted(submissions, key=lambda x: x["Issue #"], reverse=True):
    key = (entry["Nominee Email"] or entry["Nominee Name"]).lower()
    if key not in latest_by_email:
        latest_by_email[key] = entry

deduped = list(latest_by_email.values())
duplicates = [entry for entry in submissions if entry not in deduped]

# Ensure output directory
os.makedirs("ambassador", exist_ok=True)

# Save all submissions
with open("ambassador/submissions_all.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=submissions[0].keys())
    writer.writeheader()
    writer.writerows(submissions)

# Save deduplicated submissions
with open("ambassador/submissions_deduped.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=deduped[0].keys())
    writer.writeheader()
    writer.writerows(deduped)

# Save duplicates to Excel
if duplicates:
    wb = Workbook()
    ws = wb.active
    ws.title = "Duplicates"
    ws.append(duplicates[0].keys())
    for row in duplicates:
        ws.append([row[k] for k in duplicates[0].keys()])
    wb.save("ambassador/submissions_duplicates.xlsx")

print("📁 Files written: submissions_all.csv, submissions_deduped.csv, submissions_duplicates.xlsx")
