import os
import csv
import re
from github import Github

# Load secrets
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)

print("🔍 Fetching ambassador issues (open only)...")
issues = repo.get_issues(state="open", labels=["ambassador"])

submissions = []

def extract_value(label, body):
    match = re.search(rf"{label}\s*\n\s*(.+?)(?:\n|$)", body)
    return match.group(1).strip() if match else ""

def extract_checkboxes(body):
    boxes = re.findall(r"- \[x\] (.+)", body, re.IGNORECASE)
    return "\n".join(f"- {b.strip()}" for b in boxes)

for issue in issues:
    body = issue.body or ""

    nominee_name = extract_value("Nominee Name", body)
    nominee_email = extract_value("Nominee Email", body)
    github_handle = extract_value("Nominee's GitHub or GitLab Handle", body)
    organization = extract_value("Organization / Affiliation", body)
    location = extract_value("City, State/Province, Country", body)
    nominator_name = extract_value("Your Name", body)
    nominator_email = extract_value("Your Email", body)
    ambassador_pitch = extract_value("🏆 How Would the Nominee Contribute as an Ambassador?", body)
    additional_info = extract_value("Any additional details you'd like to share?", body)
    contributions = extract_checkboxes(body)

    # Compose the Submission Summary
    summary_parts = []
    if github_handle:
        summary_parts.append(f"GitHub Handle: {github_handle}")
    if contributions:
        summary_parts.append(f"Contributions:\n{contributions}")
    if ambassador_pitch:
        summary_parts.append(f"Ambassador Pitch:\n{ambassador_pitch}")
    if additional_info:
        summary_parts.append(f"Additional Info:\n{additional_info}")

    submission_summary = "\n\n".join(summary_parts)

    submissions.append({
        "Issue #": issue.number,
        "Nominee Name": nominee_name,
        "Nominee Email": nominee_email,
        "Organization": organization,
        "Location": location,
        "Nominator Name": nominator_name,
        "Nominator Email": nominator_email,
        "Submission Summary": submission_summary
    })

print(f"📄 Total submissions found: {len(submissions)}")
print("🧹 Deduplicating...")

# Deduplicate by email, fallback to name
deduped = {}
for entry in sorted(submissions, key=lambda x: x["Issue #"], reverse=True):
    key = entry["Nominee Email"].lower() if entry["Nominee Email"] else entry["Nominee Name"].lower()
    if key not in deduped:
        deduped[key] = entry

deduped_list = list(deduped.values())
duplicates = [s for s in submissions if s not in deduped_list]

# Save results
os.makedirs("ambassador", exist_ok=True)

with open("ambassador/submissions_all.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=submissions[0].keys())
    writer.writeheader()
    writer.writerows(submissions)

with open("ambassador/submissions_deduped.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=deduped_list[0].keys())
    writer.writeheader()
    writer.writerows(deduped_list)

if duplicates:
    with open("ambassador/submissions_duplicates.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=duplicates[0].keys())
        writer.writeheader()
        writer.writerows(duplicates)

print("✅ Extraction and deduplication complete.")
print("📁 Files created in ambassador/:")
print("  - submissions_all.csv")
print("  - submissions_deduped.csv")
if duplicates:
    print("  - submissions_duplicates.csv")
