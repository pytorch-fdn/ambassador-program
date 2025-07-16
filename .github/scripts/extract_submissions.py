from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

# Reviewer scoring structure
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
    ("Motiviation and Vision", "Vision", "Clear articulation of why they want to be an Ambassador and what they hope to accomplish?"),
    ("Motiviation and Vision", "Vision", "Proposed goals or initiatives that align with the mission of the PyTorch Foundation?"),
    ("Additional Bonus Criteria", "Cross-Community Collaboration", "Contributions or bridges to other relevant ecosystems (e.g., HuggingFace?)"),
    ("Additional Bonus Criteria", "Cross-Community Collaboration", "Integration work across tools or libraries within the AI/ML infrastructure landscape?"),
    ("Additional Bonus Criteria", "Geographic and Demographic Diversity", "Representation from underrepresented regions or groups to foster inclusivity and global outreach?"),
    ("Additional Bonus Criteria", "Innovation and Pioneering Work", "Early adoption or novel application of PyTorch or its ecosystem tools in industry, research, or startups?"),
    ("Credibility", "Community References", "References from other known community members?")
]

# Output folder
excel_output_folder = "ambassador/reviewer_sheets_excel"
os.makedirs(excel_output_folder, exist_ok=True)

# Group assignments per reviewer (same as before)
reviewer_data = defaultdict(list)
reviewer_counts = defaultdict(int)
assignments = []

for submission in submissions:
    sorted_reviewers = sorted(reviewers, key=lambda r: reviewer_counts[r])
    assigned = random.sample(sorted_reviewers[:4], 2)
    for reviewer in assigned:
        reviewer_counts[reviewer] += 1
        assignments.append((submission, reviewer))

for reviewer in reviewers:
    wb = Workbook()
    ws = wb.active
    ws.title = "Review Sheet"

    row_idx = 1
    ws.append([
        "Submission ID", "First Name", "Last Name", "Submission Summary",
        "Reviewer's Comment", "Category", "Subcategory", "Question", "Score"
    ])
    ws.row_dimensions[row_idx].font = Font(bold=True)
    row_idx += 1

    for submission, assigned_reviewer in assignments:
        if assigned_reviewer != reviewer:
            continue

        issue_id = submission["Issue #"]
        nominee_name = submission["Nominee Name"]
        name_parts = nominee_name.split()
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[-1] if len(name_parts) > 1 else ""
        summary = f"""Contributions:
{submission.get("Contributions", "").strip()}

Ambassador Pitch:
{submission.get("Ambassador Pitch", "").strip()}

Additional Notes:
{submission.get("Extra Notes", "").strip()}"""

        start_row = row_idx

        for category, subcat, question in rubric:
            ws.append([
                issue_id, first_name, last_name, summary,
                "", category, subcat, question, ""
            ])
            row_idx += 1

        end_row = row_idx - 1

        # Merge cells for ID, name, summary across rubric block
        for col in [1, 2, 3, 4]:  # A, B, C, D
            ws.merge_cells(start_row=start_row, end_row=end_row, start_column=col, end_column=col)
            cell = ws.cell(row=start_row, column=col)
            cell.alignment = Alignment(vertical="top", wrap_text=True)

        # Add summary section
        category_groups = defaultdict(list)
        for idx, (cat, _, _) in enumerate(rubric):
            category_groups[cat].append(start_row + idx)

        for cat, rows in category_groups.items():
            formula = f'=SUMPRODUCT((I{rows[0]}:I{rows[-1]}="Yes")*1)'
            ws.append([issue_id, first_name, last_name, "", "", cat, "Total Yes", f"{len(rows)} questions", formula])
            row_idx += 1

        total_formula = f'=SUMPRODUCT((I{start_row}:I{end_row}="Yes")*1)'
        ws.append([issue_id, first_name, last_name, "", "", "Final Score", "", f"{end_row - start_row + 1} questions", total_formula])
        row_idx += 2

    # Autofit column width
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            if cell.value:
                max_len = max(max_len, len(str(cell.value)))
        ws.column_dimensions[col_letter].width = min(max_len + 4, 50)

    # Save file
    filename = f"{reviewer.replace(' ', '_').lower()}_sheet.xlsx"
    wb.save(os.path.join(excel_output_folder, filename))

print("✅ Reviewer Excel sheets generated in 'ambassador/reviewer_sheets_excel/'")

