import os
import csv
from github import Github
import re

# Get token and repo name from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")  # Example: 'pytorch-fdn/ambassador-program'

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)

# Fetch issues with 'ambassador' label
issues = list(repo.get_issues(state='all', labels=['ambassador']))

# Prepare summary content
summary_lines = []
summary_lines.append("# PyTorch Ambassador Applications Summary\n\n")
summary_lines.append(f"**Total Applications**: {len(issues)}\n\n")
summary_lines.append("| Issue # | Nominee Name | Email | Organization | Location |\n")
summary_lines.append("|--------|--------------|------|--------------|----------|\n")

csv_rows = []

for issue in issues:
    body = issue.body

    # Helper to extract values
    def extract(label):
        match = re.search(rf"{label}\s*\n\s*(.+)", body)
        return match.group(1).strip() if match else "Not Provided"

    name = extract("Nominee Name")
    email = extract("Nominee Email")
    org = extract("Organization / Affiliation")
    location = extract("City, State/Province, Country")

    summary_lines.append(f"| {issue.number} | {name} | {email} | {org} | {location} |\n")

    csv_rows.append([issue.number, name, email, org, location])

# Ensure ambassador directory exists
os.makedirs("ambassador", exist_ok=True)

# Write to Markdown in ambassador folder
with open("ambassador/SUMMARY.md", "w") as f:
    f.writelines(summary_lines)

print("Summary written to ambassador/SUMMARY.md")

# Write to CSV in ambassador folder
with open("ambassador/SUMMARY.csv", "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Issue #", "Nominee Name", "Email", "Organization", "Location"])
    writer.writerows(csv_rows)

print("Summary written to ambassador/SUMMARY.csv")
