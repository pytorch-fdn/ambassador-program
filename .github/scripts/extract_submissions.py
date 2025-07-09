import csv
import os
import random
from collections import defaultdict

# Define reviewer list
reviewers = [f"Reviewer {i}" for i in range(1, 8)]

# Define scoring rubric columns
scoring_fields = [
    "PyTorch Experience (1-5)",
    "Foundation Tools Familiarity (1-5)",
    "Code Contributions (1-5)",
    "Community Participation (1-5)",
    "Maintainer Role (Y/N)",
    "Technical Content (1-5)",
    "Academic Publications (Y/N)",
    "Event Leadership (1-5)",
    "Public Speaking (1-5)",
    "Mentorship (1-5)",
    "Online Presence (1-5)",
    "Community Metrics (1-5)",
    "Foundation Values Alignment (1-5)",
    "Motivation & Vision (1-5)",
    "Bonus: Cross-Ecosystem (Y/N)",
    "Bonus: Diversity (Y/N)",
    "Bonus: Innovation (Y/N)",
    "Community References (Y/N)",
    "Comments",
    "Total Score"
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

# Assign 2 reviewers per submission
assignments = []
reviewer_counts = defaultdict(int)

for submission in submissions:
    # Assign 2 reviewers with the least current load
    sorted_reviewers = sorted(reviewers, key=lambda r: reviewer_counts[r])
    assigned = random.sample(sorted_reviewers[:4], 2)  # Random from least-burdened 4
    for reviewer in assigned:
        reviewer_counts[reviewer] += 1
        assignments.append((submission, reviewer))

# Process each submission-reviewer pair
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

    # Add empty scoring fields
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
