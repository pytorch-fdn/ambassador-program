import os
from github import Github
import re

# Get token and repo name from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")  # Example: 'pytorch-fdn/foundation-programs'

# Authenticate with GitHub
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)

# Fetch issues with 'ambassador' label
issues = repo.get_issues(state='all', labels=['ambassador'])

# Prepare summary content
summary_lines = []
summary_lines.append("# PyTorch Ambassador Applications Summary\n\n")
summary_lines.append(f"**Total Applications**: {issues.totalCount}\n\n")
summary_lines.append("| Issue # | Nominee Name | Email | Organization | Location |\n")
summary_lines.append("|--------|--------------|------|--------------|----------|\n")

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

# Write summary to SUMMARY.md
output_file = "SUMMARY.md"
with open(output_file, "w") as f:
    f.writelines(summary_lines)

print(f"Summary written to {output_file}")
