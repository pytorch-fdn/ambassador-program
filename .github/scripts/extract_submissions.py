import os
import csv
import random
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

# Load deduplicated submissions
with open("ambassador/ambassador_submissions_deduped.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    submissions = list(reader)

# Define reviewers
reviewers = [f"Reviewer {i}" for i in range(1, 8)]

# Define the rubric
rubric = [
    ("Technical Expertise", "Proficiency", "Demonstrated knowledge of PyTorch?"),
    ("Technical Expertise", "Proficiency", "Familiarity with vLLM and DeepSpeed?"),
    ("Open Source", "Contributions", "Made PRs, issues, and reviews across PyTorch?"),
    ("Open Source", "Contributions", "Participated in GitHub discussions or RFCs?"),
    ("Motivation and Vision", "Vision", "Why do they want to be an ambassador?")
]

# Output folder
excel_output_folder = "ambassador/reviewer_sheets_excel"
os.makedirs(excel_output_folder, exist_ok=True)

# Assign reviewers randomly and evenly
assignments = []
reviewer_counts = defaultdict(int)
for submission in submissions:
    sorted_reviewers = sorted(reviewers, key=lambda r: reviewer_counts[r])
    assigned = random.sample(sorted_reviewers[:4], 2)
    for reviewer in assigned:
        reviewer_counts[reviewer] += 1
        assignments.append((submission, reviewer))

# Generate reviewer sheets
for reviewer in reviewers:
    wb = Workbook()
    ws = wb.active
    ws.title = "Review Sheet"

    # Header
    headers = [
        "Submission ID", "First Name", "Last Name", "Submission Summary",
        "Reviewer's Comment", "Category", "Subcategory", "Question", "Score", "Category Total / Final Score"
    ]
    ws.append(headers)
    for col_num, col in enumerate(headers, 1):
        ws.cell(row=1, column=col_num).font = Font(bold=True)

    # Add dropdown for score values
    dv = DataValidation(type="list", formula1='"Yes,No,N/A"', allow_blank=True)
    ws.add_data_validation(dv)

    row_idx = 2
    for submission, assigned_reviewer in assignments:
        if assigned_reviewer != reviewer:
            continue

        issue_id = submission["Issue #"]
        nominee_name = submission["Nominee Name"]
        name_parts = nominee_name.split()
        first_name = name_parts[0] if name_parts else ""
        last_name = name_parts[-1] if len(name_parts) > 1 else ""
        summary = f"""Contributions:\n{submission.get("Contributions", "").strip()}

Ambassador Pitch:\n{submission.get("Ambassador Pitch", "").strip()}

Additional Notes:\n{submission.get("Extra Notes", "").strip()}"""

        start_row = row_idx
        category_rows = defaultdict(list)

        for category, subcat, question in rubric:
            ws.append([
                issue_id, first_name, last_name, summary,
                "", category, subcat, question, "", ""
            ])
            row_idx += 1
            category_rows[category].append(row_idx - 1)

        # Insert category total rows
        for cat, rows in category_rows.items():
            score_range = f"I{rows[0]}:I{rows[-1]}"
            formula = f'=SUMPRODUCT(--({score_range}="Yes"))'
            ws.append(["", "", "", "", "", cat, "", "Category Total", "", formula])
            row_idx += 1

        # Insert final score row
        total_range = f"I{start_row}:{get_column_letter(9)}{row_idx - 1}"
        formula = f'=SUMPRODUCT(--(I{start_row}:I{row_idx - 1}="Yes"))'
        ws.append(["", "", "", "", "", "Final Score", "", "Overall Total", "", formula])
        row_idx += 1

        # Merge Submission Info columns
        for col in [1, 2, 3, 4]:  # Columns A-D
            ws.merge_cells(start_row=start_row, end_row=row_idx - 1, start_column=col, end_column=col)
            cell = ws.cell(row=start_row, column=col)
            cell.alignment = Alignment(vertical="top", wrap_text=True)

    # Apply dropdown to Score column (column 9)
    for row in range(2, row_idx):
        dv.add(ws[f"I{row}"])

    # Autofit columns
    for col in ws.columns:
        max_length = max((len(str(cell.value)) if cell.value else 0) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = min(max_length + 4, 50)

    # Save file
    file_path = os.path.join(excel_output_folder, f"{reviewer.replace(' ', '_').lower()}_sheet.xlsx")
    wb.save(file_path)

print("✅ Final reviewer sheets generated with dropdowns and formulas.")
