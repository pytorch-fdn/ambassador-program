import os
import csv
import re
import random
from collections import defaultdict
from github import Github

# Load token and repo name from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
LABEL_FILTER = "ambassador"

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)

# Fetch issues with the given label
issues = repo.get_issues(state="all", labels=[LABEL_FILTER])

# Ensure the 'ambassador' directory exists
os.makedirs("ambassador", exist_ok=True)

# Define base headers
headers = [
    "Issue #", "Nominee Name", "Nominee Email", "GitHub Handle", "Location", "Organization",
    "Nominator Name", "Nominator Email", "Contributions", "Ambassador Pitch", "Extra Notes",
    "Issue URL"
]

def extract_field(text, label):
    pattern = rf"{label}\n(.+?)(\n\n|\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

rows = []
for issue in issues:
    body = issue.body or ""

    nominee_name = extract_field(body, "Nominee Name")
    nominee_email = extract_field(body, "Nominee Email")
    github_handle = extract_field(body, "Nominee's GitHub or GitLab Handle")
    location = extract_field(body, "City, State/Province, Country")
    organization = extract_field(body, "Organization / Affiliation")
    nominator_name = extract_field(body, "Your Name")
    nominator_email = extract_field(body, "Your Email")
    contributions = extract_field(body, "How has the nominee contributed to PyTorch\\?")
    pitch = extract_field(body, "\\ud83c\\udfc6 How Would the Nominee Contribute as an Ambassador\\?")
    notes = extract_field(body, "Any additional details you'd like to share\\?")

    row = [
        issue.number, nominee_name, nominee_email, github_handle, location, organization,
        nominator_name, nominator_email, contributions, pitch, notes,
        issue.html_url
    ]
    rows.append(row)

# Deduplicate by nominee email
email_to_last_index = {}
for i, row in enumerate(rows):
    email = row[2].strip().lower()
    email_to_last_index[email] = i

unique_rows = []
duplicates_only = []

for i, row in enumerate(rows):
    email = row[2].strip().lower()
    if email_to_last_index[email] == i:
        unique_rows.append(row)
    else:
        duplicates_only.append(row)

# Save deduplicated entries
deduped_file = "ambassador/ambassador_submissions_deduped.csv"
with open(deduped_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(unique_rows)

# Save removed duplicates
duplicates_file = "ambassador/ambassador_duplicates_removed.csv"
with open(duplicates_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(duplicates_only)

print(f"✅ Deduplicated submissions → {deduped_file}")
print(f"✅ Removed duplicates → {duplicates_file}")

# === START Reviewer Sheet Generation ===

# Define reviewer list
reviewers = [f"Reviewer {i}" for i in range(1, 8)]

# Define scoring rubric columns
scoring_fields = [
    "Technical Expertise (1–5)",
    "Community Engagement and Evangelism (1–5)",
    "Online Influence and Reach (1–5)",
    "Alignment and Values (1–5)",
    "Additional Bonus Criteria (1–5)",
    "Credibility (1–5)",
    "Final Score (1–5)",         # Reviewer must manually enter this
    "Reviewer Comments"          # Open text field for qualitative feedback
]

# Output folder
output_folder = "ambassador/reviewer_sheets"
os.makedirs(output_folder, exist_ok=True)

# Load deduplicated submissions
with open("ambassador/ambassador_submissions_deduped.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    submissions = list(reader)

# Prepare expanded data per reviewer
reviewer_data = defaultdict(list)
assignments = []
reviewer_counts = defaultdict(int)

for submission in submissions:
    sorted_reviewers = sorted(reviewers, key=lambda r: reviewer_counts[r])
    assigned = random.sample(sorted_reviewers[:4], 2)
    for reviewer in assigned:
        reviewer_counts[reviewer] += 1
        assignments.append((submission, reviewer))

for submission, reviewer in assignments:
    name_parts = submission["Nominee Name"].split()
    first_name = name_parts[0] if len(name_parts) > 0 else ""
    last_name = name_parts[-1] if len(name_parts) > 1 else ""
    summary = f"""Contributions:
{submission.get("Contributions", "").strip()}

Ambassador Pitch:
{submission.get("Ambassador Pitch", "").strip()}

Additional Notes:
{submission.get("Extra Notes", "").strip()}"""

    row = {
        "Submission ID": submission["Issue #"],
        "First Name": first_name,
        "Last Name": last_name,
        "Reviewer": reviewer,
        "Submission Summary": summary
    }

    for field in scoring_fields:
        row[field] = ""

    reviewer_data[reviewer].append(row)

# Write each reviewer's sheet
for reviewer, rows in reviewer_data.items():
    file_path = os.path.join(output_folder, f"{reviewer.replace(' ', '_').lower()}_sheet.csv")
    with open(file_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

print("✅ Reviewer sheets generated in 'ambassador/reviewer_sheets/'")
