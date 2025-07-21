import os
import csv
import re
from github import Github
from openpyxl import Workbook

# Get GitHub token and repository name
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)

print("📥 Fetching open GitHub issues labeled 'ambassador'...")
issues = list(repo.get_issues(state='open', labels=['ambassador']))
print(f"🔍 Total open issues fetched: {len(issues)}")

# Helper to extract a field from the issue body
def extract(label, body):
    match = re.search(rf"{re.escape(label)}\s*\n\s*(.+)", body)
    return match.group(1).strip() if match else ""

# Extract structured data from each issue
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
        "Your Name": extract("Your Name", body),
        "Your Email": extract("Your Email (Optional)", body),
        "Submission Summary": "\n\n".join([
            f"Nominee Self/Nominated: {extract('Select one:', body)}",
            f"Requirements Acknowledged: {extract('Please confirm that the nominee meets the following requirements:', body)}",
            f"Contributions: {extract('How has the nominee contributed to PyTorch?', body)}",
            f"Ambassador Pitch: {extract('🏆 How Would the Nominee Contribute as an Ambassador?', body)}",
            f"Additional Info: {extract('Any additional details you\'d like to share?', body)}"
        ])
    }
    submissions.append(entry)

print("🧹 Deduplicating by email or name...")

# Deduplication logic: keep latest (by issue #), use email if available
latest_submissions = {}
for entry in sorted(submissions, key=lambda x: x["Issue #"], reverse=True):
    key = entry["Nominee Email"].lower() if entry["Nominee Email"] else entry["Nominee Name"].lower()
    if key and key not in latest_submissions:
        latest_submissions[key] = entry

deduped = list(latest_submissions.values())
duplicates = [s for s in submissions if s not in deduped]

# Ensure output folder
os.makedirs("ambassador", exist_ok=True)

# Write raw submissions
with open("ambassador/submissions_all_raw.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=submissions[0].keys())
    writer.writeheader()
    writer.writerows(submissions)

# Write deduplicated submissions
with open("ambassador/submissions_deduplicated.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=deduped[0].keys())
    writer.writeheader()
    writer.writerows(deduped)

# Write duplicates to Excel if any
if duplicates:
    wb = Workbook()
    ws = wb.active
    ws.title = "Duplicates Removed"
    ws.append(list(duplicates[0].keys()))
    for d in duplicates:
        ws.append([d.get(k, "") for k in ws[1]])
    wb.save("ambassador/submissions_duplicates_removed.xlsx")
    print("🗂️ Duplicates written to ambassador/submissions_duplicates_removed.xlsx")
else:
    print("✅ No duplicates found.")

print("🎉 Done: Data extracted and files saved.")
