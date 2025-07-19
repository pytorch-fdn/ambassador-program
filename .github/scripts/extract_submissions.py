import os
import re
import csv
import random
from collections import defaultdict
from github import Github
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

print("📥 Fetching GitHub issues...")

# Environment setup
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)

issues = list(repo.get_issues(state='all', labels=['ambassador']))
print(f"🔍 Found {len(issues)} total issues")

# Helper to extract field from issue body
def extract_field(label, body):
    match = re.search(rf"{label}\s*\n\s*(.+)", body)
    return match.group(1).strip() if match else ""

# Step 1: Parse issues
submissions_raw = []
for issue in issues:
    body = issue.body
    submission = {
        "Issue #": issue.number,
        "Nominee Name": extract_field("Nominee Name", body),
        "Nominee Email": extract_field("Nominee Email", body),
        "GitHub Handle": extract_field("GitHub or GitLab Handle", body),
        "Organization": extract_field("Organization / Affiliation", body),
        "Location": extract_field("City, State/Province, Country", body),
        "Contributions": extract_field("How has the nominee contributed to PyTorch?", body),
        "Ambassador Pitch": extract_field("How Would the Nominee Contribute as an Ambassador?", body),
        "Extra Notes": extract_field("Any additional details you'd like to share?", body),
    }
    submissions_raw.append(submission)

# Step 2: Deduplicate by GitHub handle (keep latest by Issue #)
submissions_by_handle = {}
duplicates = []
for s in sorted(submissions_raw, key=lambda x: x["Issue #"], reverse=True):
    handle = s.get("GitHub Handle", "").lower()
    if handle and handle not in submissions_by_handle:
        submissions_by_handle[handle] = s
    else:
        duplicates.append(s)

submissions = list(submissions_by_handle.values())
print(f"🧹 Deduplicated to {len(submissions)} unique submissions")

# Step 3: Write deduplicated CSV
os.makedirs("ambassador", exist_ok=True)
with open("ambassador/ambassador_submissions_deduped.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=submissions[0].keys())
    writer.writeheader()
    writer.writerows(submissions)

# Step 4: Save duplicates separately
if duplicates:
    dup_wb = Workbook()
    ws = dup_wb.active
    ws.title = "Duplicates Removed"
    ws.append(list(duplicates[0].keys()))
    for d in duplicates:
        ws.append([d.get(k, "") for k in ws[1]])
    dup_wb.save("ambassador/duplicates_removed.xlsx")
    print("⚠️ Duplicates saved to ambassador/duplicates_removed.xlsx")

# Step 5: Generate Reviewer Sheets
print("📊 Generating reviewer sheets...")

reviewers = [f"Reviewer {i}" for i in range(1, 8)]

rubric = [
    ("Technical Expertise", "Proficiency with the PyTorch Ecosystem", "Demonstrated knowledge and practical experience with PyTorch, including model building, traininga and deployment?"),
    ("Technical Expertise", "Proficiency with the PyTorch Ecosystem", "Familiarity with foundation-hosted projects, vLLM, DeepSpeed?"),
    ("Open Source Contributions", "Community Contributions", "Made commits, PRs, issues filed, and code reviews across PyTorch and its ecosystem repositories?"),
    ("Open Source Contributions", "Community Contributions", "Evidence of active participation in community discussions, RFCs, and GitHub projects?"),
    ("Open Source Contributions", "Community Contributions", "Maintenance or leadership of related open source projects or libraries?"),
    ("Thought Leadership and Technical Writing", "Publishing", "Authored technical blog posts, whitepapers, tutorials, or case studies on PyTorch or its ecosystem?"),
    ("Thought Leadership and Technical Writing", "Publishing", "Published academic research papers or publications in relevant scientific journals or conferences?"),
    ("Community Engagement and Evangelism", "Event Organization and Involvement", "Experience organizing or leading community events such as meetups, conferences, study groups, or hackathons?"),
    ("Community Engagement and Evangelism", "Event Organization and Involvement", "Participation in significant developer or ML community events (e.g., NeurIPS, PyTorch Conference, ICML, CVPR,...)"),
    ("Community Engagement and Evangelism", "Public Speaking and Presentation Skills", "Record of delivering talks, webinars, or workshops on PyTorch-related topics?"),
    ("Community Engagement and Evangelism", "Public Speaking and Presentation Skills", "Ability to communicate complex concepts clearly to both technical and non-technical audiences?"),
    ("Community Engagement and Evangelism", "Public Speaking and Presentation Skills", "Sample video recordings or links to previous talks?"),
    ("Community Engagement and Evangelism", "Mentorship and Education", "Experience mentoring students, junior developers, or researchers?"),
    ("Community Engagement and Evangelism", "Mentorship and Education", "Development or teaching of curricula or courses related to machine learning, deep learning, or distributed systems?"),
    ("Online Influence and Reach", "Social Media and Content Creation", "Active presence on platforms like Twitter, LinkedIn, YouTube, Medium, or personal blogs with a focus on machine learning, AI, or software development?"),
    ("Online Influence and Reach", "Social Media and Content Creation", "Consistency and quality of content promoting PyTorch and associated tools?"),
    ("Online Influence and Reach", "Community Impact Metrics", "High number of followers, subscribers, or consistent engagement levels with online content (>10,000 followers/>100,000 subs)?"),
    ("Online Influence and Reach", "Community Impact Metrics", "Demonstrated ability to spark discussion, share knowledge, and grow community awareness?"),
    ("Alignment and Values", "Alignment with PyTorch Foundation Values", "Commitment to open source principles, community-first development, and inclusive collaboration?"),
    ("Alignment and Values", "Alignment with PyTorch Foundation Values", "Advocacy for responsible AI development and ethical machine learning practices?"),
    ("Motivation and Vision", "Vision", "Clear articulation of why they want to be an Ambassador and what they hope to accomplish?"),
    ("Motivation and Vision", "Vision", "Proposed goals or initiatives that align with the mission of the PyTorch Foundation?")
]

summary_categories = list({cat for cat, _, _ in rubric})
assignments = []
reviewer_counts = defaultdict(int)
for submission in submissions:
    assigned = random.sample(sorted(reviewers, key=lambda r: reviewer_counts[r])[:4], 2)
    for reviewer in assigned:
        reviewer_counts[reviewer] += 1
        assignments.append((submission, reviewer))

output_folder = "ambassador/reviewer_sheets_excel"
os.makedirs(output_folder, exist_ok=True)

for reviewer in reviewers:
    wb = Workbook()
    ws = wb.active
    ws.title = "Review Sheet"
    summary_ws = wb.create_sheet("Score Summary")

    # Headers
    headers = ["Submission ID", "First Name", "Last Name", "Submission Summary",
               "Reviewer's Comment", "Category", "Subcategory", "Question", "Score"]
    ws.append(headers)
    for col in range(1, len(headers)+1):
        ws.cell(row=1, column=col).font = Font(bold=True)

    dv = DataValidation(type="list", formula1='"Yes,No,N/A"', allow_blank=True)
    ws.add_data_validation(dv)

    row_idx = 2
    candidate_ranges = []

    for submission, assigned_reviewer in assignments:
        if assigned_reviewer != reviewer:
            continue

        sid = submission["Issue #"]
        name = submission["Nominee Name"].split()
        fname = name[0]
        lname = name[-1] if len(name) > 1 else ""
        summary = f"""Contributions:\n{submission.get("Contributions", "")}

Ambassador Pitch:\n{submission.get("Ambassador Pitch", "")}

Additional Notes:\n{submission.get("Extra Notes", "")}"""

        start = row_idx
        for cat, subcat, question in rubric:
            ws.append([sid, fname, lname, summary, "", cat, subcat, question, ""])
            row_idx += 1
        end = row_idx - 1
        candidate_ranges.append((sid, fname, lname, start, end))

        for col in [1, 2, 3, 4]:
            ws.merge_cells(start_row=start, end_row=end, start_column=col, end_column=col)
            ws.cell(row=start, column=col).alignment = Alignment(vertical="top", wrap_text=True)

        for r in range(start, end + 1):
            dv.add(ws[f"I{r}"])

    # Score summary tab
    summary_ws.append(["Submission ID", "First Name", "Last Name"] + summary_categories + ["Final Score"])
    for col in range(1, summary_ws.max_column + 1):
        summary_ws.cell(row=1, column=col).font = Font(bold=True)

    for sid, fname, lname, start, end in candidate_ranges:
        cat_rows = defaultdict(list)
        for r in range(start, end + 1):
            cat = ws.cell(row=r, column=6).value
            cat_rows[cat].append(r)

        row_num = summary_ws.max_row + 1
        formulas = []
        for cat in summary_categories:
            if cat in cat_rows:
                rows = cat_rows[cat]
                formulas.append(f'=SUMPRODUCT(--(\'Review Sheet\'!I{rows[0]}:I{rows[-1]}="Yes"))')
            else:
                formulas.append("0")
        total_formula = f"=SUM({','.join([f'{get_column_letter(i+4)}{row_num}' for i in range(len(formulas))])})"
        summary_ws.append([sid, fname, lname] + formulas + [total_formula])

    wb.save(os.path.join(output_folder, f"{reviewer.replace(' ', '_').lower()}_sheet.xlsx"))

print("✅ All reviewer sheets and summaries generated.")
