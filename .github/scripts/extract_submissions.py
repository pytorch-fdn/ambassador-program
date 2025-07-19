import os
import re
import random
import requests
from collections import defaultdict
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

# Set your GitHub repo details
REPO = "pytorch-fdn/ambassador-program"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
API_URL = f"https://api.github.com/repos/{REPO}/issues?state=all&labels=closed&per_page=100"

# Output directories
os.makedirs("ambassador/reviewer_sheets_excel", exist_ok=True)

# Helper to extract structured data from the issue body
def extract_submission(issue):
    body = issue["body"]
    def extract(label):  # Flexible line extractor
        pattern = rf"\*\*{re.escape(label)}\*\*\s*\n([\s\S]*?)(?:\n\*\*|$)"
        match = re.search(pattern, body, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    return {
        "Issue #": str(issue["number"]),
        "Nominee Name": extract("Nominee Name"),
        "Nominee Email": extract("Nominee Email"),
        "GitHub Handle": extract("Nominee's GitHub or GitLab Handle"),
        "Organization": extract("Organization / Affiliation"),
        "Location": extract("City, State/Province, Country"),
        "Nominator Name": extract("Your Name"),
        "Nominator Email": extract("Your Email"),
        "Contributions": extract("How has the nominee contributed to PyTorch?"),
        "Ambassador Pitch": extract("How Would the Nominee Contribute as an Ambassador?"),
        "Extra Notes": extract("Any additional details you'd like to share?"),
        "Created At": issue["created_at"]
    }

# Step 1: Fetch and parse issues
print("📥 Fetching GitHub issues...")
all_issues = []
page = 1
while True:
    response = requests.get(f"{API_URL}&page={page}", headers=HEADERS)
    data = response.json()
    if not data or "message" in data:
        break
    all_issues.extend(data)
    page += 1

submissions_raw = [extract_submission(issue) for issue in all_issues if "Nominee Name" in issue["body"]]

# Step 2: Deduplicate by nominee name, keeping latest
print("🧹 Deduplicating...")
deduped, duplicates = {}, []
for sub in submissions_raw:
    key = sub["Nominee Name"].strip().lower()
    dt = datetime.strptime(sub["Created At"], "%Y-%m-%dT%H:%M:%SZ")
    if key not in deduped or dt > datetime.strptime(deduped[key]["Created At"], "%Y-%m-%dT%H:%M:%SZ"):
        if key in deduped:
            duplicates.append(deduped[key])
        deduped[key] = sub
    else:
        duplicates.append(sub)

submissions = list(deduped.values())

# Step 3: Reviewer logic
reviewers = [f"Reviewer {i}" for i in range(1, 8)]

# Updated rubric including all categories from the latest file
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
    ("Motivation and Vision", "Vision", "Proposed goals or initiatives that align with the mission of the PyTorch Foundation?"),
    ("Additional Bonus Criteria", "Cross-Community Collaboration", "Contributions or bridges to other relevant ecosystems (e.g., HuggingFace?)"),
    ("Additional Bonus Criteria", "Cross-Community Collaboration", "Integration work across tools or libraries within the AI/ML infrastructure landscape?"),
    ("Additional Bonus Criteria", "Geographic and Demographic Diversity", "Representation from underrepresented regions or groups to foster inclusivity and global outreach?"),
    ("Additional Bonus Criteria", "Innovation and Pioneering Work", "Early adoption or novel application of PyTorch or its ecosystem tools in industry, research, or startups?"),
    ("Credibility", "Community References", "References from other known community members?")
]

summary_categories = []
for cat, _, _ in rubric:
    if cat not in summary_categories:
        summary_categories.append(cat)

assignments = []
reviewer_counts = defaultdict(int)
for sub in submissions:
    assigned = random.sample(sorted(reviewers, key=lambda r: reviewer_counts[r])[:4], 2)
    for r in assigned:
        reviewer_counts[r] += 1
        assignments.append((sub, r))

# Step 4: Generate reviewer sheets
for reviewer in reviewers:
    wb = Workbook()
    ws = wb.active
    ws.title = "Review Sheet"
    summary_ws = wb.create_sheet("Score Summary")

    headers = [
        "Submission ID", "First Name", "Last Name", "Submission Summary",
        "Reviewer's Comment", "Category", "Subcategory", "Question", "Score"
    ]
    ws.append(headers)
    for c in range(1, len(headers)+1):
        ws.cell(row=1, column=c).font = Font(bold=True)

    dv = DataValidation(type="list", formula1='"Yes,No,N/A"', allow_blank=True)
    ws.add_data_validation(dv)

    row_idx = 2
    ranges = []

    for sub, r in assignments:
        if r != reviewer:
            continue
        sid = sub["Issue #"]
        name_parts = sub["Nominee Name"].split()
        fname = name_parts[0]
        lname = name_parts[-1] if len(name_parts) > 1 else ""
        summary = f"""
GitHub: {sub.get("GitHub Handle", "")}
Org: {sub.get("Organization", "")}
Location: {sub.get("Location", "")}

Contributions:
{sub.get("Contributions", "")}

Ambassador Pitch:
{sub.get("Ambassador Pitch", "")}

Additional Info:
{sub.get("Extra Notes", "")}
""".strip()

        start = row_idx
        for cat, subcat, question in rubric:
            ws.append([sid, fname, lname, summary, "", cat, subcat, question, ""])
            row_idx += 1
        end = row_idx - 1
        ranges.append((sid, fname, lname, start, end))

        for col in [1, 2, 3, 4, 5]:  # Merge key fields
            ws.merge_cells(start_row=start, end_row=end, start_column=col, end_column=col)
            ws.cell(row=start, column=col).alignment = Alignment(vertical="top", wrap_text=True)
        for r in range(start, end+1):
            dv.add(ws[f"I{r}"])

    # Autofit columns
    for col in ws.columns:
        max_len = max((len(str(c.value)) if c.value else 0) for c in col)
        ws.column_dimensions[get_column_letter(col[0].column)].width = min(max_len + 5, 60)

    # Score Summary
    summary_ws.append(["Submission ID", "First Name", "Last Name"] + summary_categories + ["Final Score"])
    for col in range(1, summary_ws.max_column + 1):
        summary_ws.cell(row=1, column=col).font = Font(bold=True)

    for sid, fname, lname, start, end in ranges:
        cat_rows = defaultdict(list)
        for r in range(start, end + 1):
            cat = ws.cell(row=r, column=6).value
            cat_rows[cat].append(r)

        formulas = []
        for cat in summary_categories:
            if cat in cat_rows:
                rows = cat_rows[cat]
                formulas.append(f'=SUMPRODUCT(--(\'Review Sheet\'!I{rows[0]}:I{rows[-1]}="Yes"))')
            else:
                formulas.append("0")
        row_number = summary_ws.max_row + 1
        final_formula = f"=SUM({','.join([f'{get_column_letter(i+4)}{row_number}' for i in range(len(formulas))])})"
        summary_ws.append([sid, fname, lname] + formulas + [final_formula])

    wb.save(f"ambassador/reviewer_sheets_excel/{reviewer.replace(' ', '_').lower()}_sheet.xlsx")

# Step 5: Save duplicates separately
dup_wb = Workbook()
ws = dup_wb.active
ws.title = "Duplicates Removed"

if duplicates:
    ws.append(list(duplicates[0].keys()))
    for d in duplicates:
        ws.append([d.get(k, "") for k in ws[1]])
else:
    ws.append(["No duplicates found"])

dup_wb.save("ambassador/duplicates_removed.xlsx")

print("✅ All reviewer sheets and duplicates file generated.")
