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

print("📥 Fetching GitHub issues...")
issues = list(repo.get_issues(state='all', labels=['ambassador']))

print(f"🔍 Total issues fetched: {len(issues)}")

# Helper to extract a label's value from issue body
def extract(label, body):
    match = re.search(rf"{label}\s*\n\s*(.+)", body)
    return match.group(1).strip() if match else ""

# Extract all relevant data
submissions = []
for issue in issues:
    body = issue.body or ""
    entry = {
        "Issue #": issue.number,
        "Nominee Name": extract("Nominee Name", body),
        "Nominee Email": extract("Nominee Email", body),
        "Organization": extract("Organization / Affiliation", body),
        "Location": extract("City, State/Province, Country", body),
        "Contributions": extract("Relevant Contributions and Links", body),
        "Ambassador Pitch": extract("Why do you want to be a PyTorch Ambassador?", body),
        "Extra Notes": extract("Additional Notes or Comments", body),
        "Nominate Others": extract("I would like to nominate contributors", body),
        "Additional Info": extract("Any other information", body)
    }
    submissions.append(entry)

print("🧹 Deduplicating...")

# Deduplication logic: use email if present, fallback to name
latest_submissions = {}
for entry in sorted(submissions, key=lambda x: x["Issue #"], reverse=True):
    key = entry["Nominee Email"].lower() if entry["Nominee Email"] else entry["Nominee Name"].lower()
    if key not in latest_submissions:
        latest_submissions[key] = entry

deduped = list(latest_submissions.values())
duplicates = [s for s in submissions if s not in deduped]

# Ensure output folder
os.makedirs("ambassador", exist_ok=True)

# Save full submission CSV
with open("ambassador/ambassador_submissions_full.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=submissions[0].keys())
    writer.writeheader()
    writer.writerows(submissions)

# Save deduplicated CSV
with open("ambassador/ambassador_submissions_deduped.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=deduped[0].keys())
    writer.writeheader()
    writer.writerows(deduped)

# Save duplicates to Excel
if duplicates:
    wb = Workbook()
    ws = wb.active
    ws.title = "Duplicates Removed"
    ws.append(list(duplicates[0].keys()))
    for d in duplicates:
        ws.append([d.get(k, "") for k in ws[1]])
    wb.save("ambassador/duplicates_removed.xlsx")
    print(f"🗂️ Duplicates written to ambassador/duplicates_removed.xlsx")

print("✅ Step 1 complete: Extraction + Deduplication done.")
