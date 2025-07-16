import os
import csv
import random
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

# Load submissions
with open("ambassador/ambassador_submissions_deduped.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    submissions = list(reader)

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
    ("Motivation and Vision", "Vision", "Proposed goals or initiatives that align with the mission of the PyTorch Foundation?"),
    ("Additional Bonus Criteria", "Cross-Community Collaboration", "Contributions or bridges to other relevant ecosystems (e.g., HuggingFace?)"),
    ("Additional Bonus Criteria", "Cross-Community Collaboration", "Integration work across tools or libraries within the AI/ML infrastructure landscape?"),
    ("Additional Bonus Criteria", "Geographic and Demographic Diversity", "Representation from underrepresented regions or groups to foster inclusivity and global outreach?"),
    ("Additional Bonus Criteria", "Innovation and Pioneering Work", "Early adoption or novel application of PyTorch or its ecosystem tools in industry, research, or startups?"),
    ("Credibility", "Community References", "References from other known community members?")
]

output_folder = "ambassador/reviewer_sheets_excel"
os.makedirs(output_folder, exist_ok=True)

# Randomly assign 2 reviewers to each submission
assignments = []
reviewer_counts = defaultdict(int)
for submission in submissions:
    sorted_reviewers = sorted(reviewers, key=lambda r: reviewer_counts[r])
    assigned = random.sample(sorted_reviewers[:4], 2)
    for reviewer in assigned:
        reviewer_counts[reviewer] += 1
        assignments.append((submission, reviewer))

# Create sheets for each reviewer
for reviewer in reviewers:
    wb = Workbook()
    ws = wb.active
    ws.title = "Review Sheet"

    summary_ws = wb.create_sheet(title="Score Summary")
    summary_ws.append(["Submission ID", "First Name", "Last Name"] + list({cat for cat, _, _ in rubric}) + ["Final Score"])
    for cell in summary_ws[1]: cell.font = Font(bold=True)

    # Add dropdown
    dv = DataValidation(type="list", formula1='"Yes,No,N/A"', allow_blank=True)
    ws.add_data_validation(dv)

    headers = ["Submission ID", "First Name", "Last Name", "Submission Summary", "Reviewer's Comment", "Category", "Subcategory", "Question", "Score"]
    ws.append(headers)
    for cell in ws[1]: cell.font = Font(bold=True)

    row_idx = 2
    for submission, assigned_reviewer in assignments:
        if assigned_reviewer != reviewer:
            continue

        sid = submission["Issue #"]
        name_parts = submission["Nominee Name"].split()
        fname = name_parts[0] if name_parts else ""
        lname = name_parts[-1] if len(name_parts) > 1 else ""
        summary = f"""Contributions:\n{submission.get("Contributions", "").strip()}

Ambassador Pitch:\n{submission.get("Ambassador Pitch", "").strip()}

Additional Notes:\n{submission.get("Extra Notes", "").strip()}"""

        rubric_rows = []
        category_row_map = defaultdict(list)
        for cat, subcat, q in rubric:
            ws.append([sid, fname, lname, summary, "", cat, subcat, q, ""])
            rubric_rows.append(row_idx)
            category_row_map[cat].append(row_idx)
            for col in [1,2,3,4]:  # Merge ID, name, summary
                ws.merge_cells(start_row=row_idx, end_row=row_idx, start_column=col, end_column=col)
                ws.cell(row=row_idx, column=col).alignment = Alignment(vertical="top", wrap_text=True)
            dv.add(ws[f"I{row_idx}"])
            row_idx += 1

        # Build score summary formulas
        col_offset = 4
        summary_row = [sid, fname, lname]
        for cat in sorted(category_row_map.keys()):
            rows = category_row_map[cat]
            formula = f"=SUMPRODUCT(--('Review Sheet'!I{rows[0]}:I{rows[-1]}=\"Yes\"))"
            summary_row.append(formula)
        total_formula = f"=SUM({get_column_letter(4)}{summary_ws.max_row + 1}:{get_column_letter(3 + len(category_row_map))}{summary_ws.max_row + 1})"
        summary_row.append(total_formula)
        summary_ws.append(summary_row)

    # Autofit
    for ws_target in [ws, summary_ws]:
        for col in ws_target.columns:
            max_len = max(len(str(cell.value)) if cell.value else 0 for cell in col)
            ws_target.column_dimensions[get_column_letter(col[0].column)].width = min(max_len + 4, 50)

    # Save
    wb.save(os.path.join(output_folder, f"{reviewer.replace(' ', '_').lower()}_sheet.xlsx"))

print("✅ Reviewer Excel sheets with working formulas and summary sheet created.")
