import os
import csv
import re
from github import Github

# Load token and repo name from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")  # e.g., 'pytorch-fdn/ambassador-program'
LABEL_FILTER = "ambassador"

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)

# Fetch issues with the given label
issues = repo.get_issues(state="all", labels=[LABEL_FILTER])

# Ensure the 'ambassador' directory exists
os.makedirs("ambassador", exist_ok=True)

# Define base headers (excluding reviewer/duplicate fields)
headers = [
    "Issue #", "Nominee Name", "Nominee Email", "GitHub Handle", "Location", "Organization",
    "Nominator Name", "Nominator Email", "Contributions", "Ambassador Pitch", "Extra Notes",
    "Issue URL"
]

# Helper function to extract field content by label
def extract_field(text, label):
    pattern = rf"{label}\n(.+?)(\n\n|\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

# Collect rows of data
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

# Deduplicate by nominee email (keep last)
email_to_last_index = {}
for i, row in enumerate(rows):
    email = row[2].strip().lower()
    email_to_last_index[email] = i  # Last occurrence

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

# Create reviewer tracking sheet
reviewer_file = "ambassador/ambassador_reviewer_sheet.csv"
reviewer_headers = ["Issue #", "First Name", "Last Name", "Issue Link",
                    "Reviewer 1", "Reviewer 2", "Reviewer 3", "Reviewer 4", "Reviewer 5", "Reviewer 6"]

reviewer_rows = []
for row in unique_rows:
    issue_number = row[0]
    full_name = row[1].strip()
    name_parts = full_name.split()
    first_name = name_parts[0] if len(name_parts) > 0 else ""
    last_name = name_parts[-1] if len(name_parts) > 1 else ""
    issue_url = row[-1]  # "Issue URL" is the last column in the deduped row
    issue_link = f"[View Issue]({issue_url})"
    reviewer_row = [issue_number, first_name, last_name, issue_link] + [""] * 6
    reviewer_rows.append(reviewer_row)

with open(reviewer_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(reviewer_headers)
    writer.writerows(reviewer_rows)

print(f"✅ Deduplicated submissions → {deduped_file}")
print(f"✅ Removed duplicates → {duplicates_file}")
print(f"✅ Reviewer tracking sheet → {reviewer_file}")
