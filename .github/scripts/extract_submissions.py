import os
import csv
import re
from github import Github

# Load token and repo name from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")  # e.g., 'pytorch-fdn/ambassador-program'
LABEL_FILTER = "ambassador"  # Label used to filter ambassador submissions

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)

# Fetch issues with the given label
issues = repo.get_issues(state="all", labels=[LABEL_FILTER])

# Ensure the 'ambassador' directory exists
os.makedirs("ambassador", exist_ok=True)
output_file = "ambassador/ambassador_submissions.csv"

# Define CSV headers
headers = [
    "Issue #", "Nominee Name", "Nominee Email", "GitHub Handle", "Location", "Organization",
    "Nominator Name", "Nominator Email", "Contributions", "Ambassador Pitch", "Extra Notes",
    "Issue URL", "Reviewer Score", "Reviewer Notes", "Duplicate"
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
        issue.html_url, "", "", ""  # placeholders for Reviewer Score, Notes, and Duplicate
    ]
    rows.append(row)

# Detect duplicates by nominee email
email_index = {}
duplicates = set()

for i, row in enumerate(rows):
    email = row[2].strip().lower()  # Nominee Email
    if email in email_index:
        duplicates.add(i)
        duplicates.add(email_index[email])
    else:
        email_index[email] = i

# Mark duplicates in the last column
for i, row in enumerate(rows):
    row[-1] = "Yes" if i in duplicates else "No"

# Write to CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"✅ CSV exported with {len(rows)} submissions → {output_file}")
