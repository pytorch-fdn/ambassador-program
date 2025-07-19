import os
import csv
import re
from github import Github

# Step 0: Setup environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

# Step 1: Authenticate GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)

print("📥 Fetching GitHub issues...")
issues = list(repo.get_issues(state='all', labels=['ambassador']))
print(f"🔍 Total issues fetched: {len(issues)}")

# Helper: Extract value from GitHub issue template body
def extract(label, body):
    match = re.search(rf"{label}\s*\n\s*(.+)", body)
    return match.group(1).strip() if match else ""

# Step 2: Extract submission data
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

# Step 3: Deduplicate — keep latest per email/name
latest_submissions = {}
seen_keys = set()

for entry in sorted(submissions, key=lambda x: x["Issue #"], reverse=True):
    key = entry["Nominee Email"].lower() if entry["Nominee Email"] else entry["Nominee Name"].lower()
    if key not in latest_submissions:
        latest_submissions[key] = entry
        seen_keys.add(key)

deduped = list(latest_submissions.values())

# Step 4: Track duplicates
duplicates = []
seen_keys_copy = seen_keys.copy()  # prevent modifying original while checking
for entry in submissions:
    key = entry["Nominee Email"].lower() if entry["Nominee Email"] else entry["Nominee Name"].lower()
    if key in seen_keys_copy:
        seen_keys_copy.remove(key)  # keep only the first seen (i.e., latest)
    else:
        duplicates.append(entry)

# Step 5: Ensure output directory exists
output_dir = "ambassador/output_step1"
os.makedirs(output_dir, exist_ok=True)

# Step 6: Write full submissions
with open(os.path.join(output_dir, "ambassador_submissions_full.csv"), "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=submissions[0].keys())
    writer.writeheader()
    writer.writerows(submissions)

# Step 7: Write deduplicated submissions
with open(os.path.join(output_dir, "ambassador_submissions_deduped.csv"), "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=deduped[0].keys())
    writer.writeheader()
    writer.writerows(deduped)

# Step 8: Write duplicates removed
if duplicates:
    with open(os.path.join(output_dir, "duplicates_removed.csv"), "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=duplicates[0].keys())
        writer.writeheader()
        writer.writerows(duplicates)
    print(f"🗂️ Duplicates written to {output_dir}/duplicates_removed.csv")
else:
    print("✅ No duplicates found.")

print("✅ Step 1 complete: Extraction + Deduplication done.")
