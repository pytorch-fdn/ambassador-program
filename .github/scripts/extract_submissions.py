from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
import os
import csv
import random
from collections import defaultdict

# === Load data ===
with open("ambassador/ambassador_submissions_deduped.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    submissions = list(reader)

reviewers = [f"Reviewer {i}" for i in range(1, 8)]

# Define rubric
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

# Define category mapping
categories = ["Technical Expertise", "Open Source Contributions", "Thought Leadership and Technical Writing",
              "Community Engagement and Evangelism", "Online Influence and Reach", "Alignment and Values",
              "Motivation and Vision"]

# Build a lookup for rubric indexes
category_map = defaultdict(list)
for i, (cat, _, _) in enumerate(rubric):
    category_map[cat].append(i)

# Random reviewer assignment
assignments = []
reviewer_counts = defaultdict(int)
for submission in submissions:
    sorted_reviewers = sorted(reviewers, key=lambda r: reviewer_counts[r])
    assigned = random.sample(sorted_reviewers[:4], 2)
    for reviewer in assigned:
        reviewer_counts[reviewer] += 1
        assignments.append((submission, reviewer))

# Output directory
output_dir = "ambassador/reviewer_sheets_excel"
os.makedirs(output_dir, exist_ok=True)

# Generate Excel with 2 sheets per reviewer
for reviewer in reviewers:
    wb = Workbook()
    ws = wb.active
    ws.title = "Review Sheet"

    # Summary worksheet
    summary_ws = wb.create_sheet(title="Score Summary")
    summary_headers = ["Submission ID", "First Name", "Last Name"] + categories + ["Final Score"]
    summary_ws.append(summary_headers)
    for col in summary_ws[1]:
        col.font = Font(bold=True)

    row_idx = 2
    summary_row = 2

    for submission, assigned_reviewer in assignments:
        if assigned_reviewer != reviewer:
            continue

        issue_id = submission["Issue #"]
        name_parts = submission["Nominee Name"].split()
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[-1] if len(name_parts) > 1 else ""

        category_rows = defaultdict(list)
        start_row = row_idx

        for cat, subcat, question in rubric:
            ws.append([
                issue_id, first_name, last_name, "", "", cat, subcat, question, ""
            ])
            category_rows[cat].append(row_idx)
            row_idx += 1

        # Write summary formulas
        formulas = []
        for cat in categories:
            if cat in category_rows:
                rng = category_rows[cat]
                formula = f"=SUMPRODUCT(--('{ws.title}'!I{rng[0]}:I{rng[-1]}=\"Yes\"))"
                formulas.append(formula)
            else:
                formulas.append("")

        total_formula = f"=SUM({','.join([chr(68+i) + str(summary_row) for i in range(3, 3+len(categories))])})"

        summary_ws.append([issue_id, first_name, last_name] + formulas + [total_formula])
        summary_row += 1

    # Save file
    reviewer_file = os.path.join(output_dir, f"{reviewer.replace(' ', '_').lower()}_sheet.xlsx")
    wb.save(reviewer_file)

print("✅ All reviewer sheets generated with corrected formulas and aligned categories.")
