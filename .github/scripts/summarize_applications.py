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
    match = re.search(rf"{label}\s*\n+(.+?)(\n\S|\Z)", body, re.DOTALL)
    return match.group(1).strip() if match else ""

# Helper to extract all checkbox lines
def extract_checkboxes(body):
    matches = re.findall(r"- \[x\] (.+)", body, flags=re.IGNORECASE)
    return "; ".join(matches) if matches else ""

# Build submissions list
submissions = []
for issue in issues:
    body = issue.body or ""

    entry = {
        "Issue #": issue.number,
        "Nominee Name": extract("Nominee Name", body),
        "Nominee Email": extract("Nominee Email", body),
        "GitHub Handle": extract("Nominee's GitHub or GitLab Handle", body),
        "Submission Summary": (
            f"🏆 Ambassador Contribution Plan:\n{extract('🏆 How Would the Nominee Contribute as an Ambassador?', body)}\n\n"
            f"🔗 Additional Information:\n{extract('Any additional details you\\'d like to share?', body)}\n\n"
            f"✅ Contribution Highlights:\n{extract_checkboxes(body)}"
        )
    }
    submissions.append(entry)

# Deduplication logic: prefer latest submission by email or name
latest_submissions = {}
for entry in sorted(submissions, key=lambda x: x["Issue #"], reverse=True):
    key = entry["Nominee Email"].lower() if entry["Nominee Email"] else entry["Nominee Name"].lower()
    if key not in latest_submissions:
        latest_submissions[key] = entry

deduped = list(latest_submissions.values())
duplicates = [s for s in submissions if s not in deduped]

# Ensure output folder
os.makedirs("ambassador", exist_ok=True)

# Write full submission CSV
with open("ambassador/submissions_all_raw.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=submissions[0].keys())
    writer.writeheader()
    writer.writerows(submissions)

# Write deduplicated CSV
with open("ambassador/submissions_deduplicated.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=deduped[0].keys())
    writer.writeheader()
    writer.writerows(deduped)

# Write duplicates to Excel
if duplicates:
    wb = Workbook()
    ws = wb.active
    ws.title = "Duplicates Removed"
    ws.append(list(duplicates[0].keys()))  # ✅ Fixed here
    for row in duplicates:
        ws.append([row.get(k, "") for k in duplicates[0].keys()])
    wb.save("ambassador/submissions_duplicates_removed.xlsx")
    print("🗂️ Duplicates written to ambassador/submissions_duplicates_removed.xlsx")

print("✅ Extraction and deduplication complete.")
