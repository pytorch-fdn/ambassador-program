# 🧮 Scoring Workflow: PyTorch Ambassador Program

This document outlines the **scoring system** used to evaluate nominations for the PyTorch Ambassador Program. It is intended for **reviewers, maintainers, and workflow administrators** who participate in or manage the review process.

---

## 📌 Purpose

The scoring workflow enables reviewers to evaluate nominee submissions using a **1–5 scale** recorded in an internal scoring sheet. It supports a structured review process by:

- Collecting reviewer input consistently  
- Encouraging transparent explanations for scores  
- Supporting program managers in making informed decisions  
- Logging final decisions back to GitHub for recordkeeping  
- Closing rejected issues and preparing approved ones for next steps

---

## 🔁 Overview of the Scoring Flow

| Phase                   | Labels Used                     |
|-------------------------|----------------------------------|
| Nomination submitted    | `pending-review`                |
| Review begins (manual)  | `under-review`, `scoring-in-progress` |
| Review finalized        | `approved` / `rejected`, `scoring-complete` |

---

## 🧾 Step 1: Scoring in the Reviewer Sheet

Each reviewer enters their score in the **shared reviewer spreadsheet** under the relevant column (Reviewer 1–6). Scores must be integers between **1 and 5**.

### 🔢 Score Guide

| Score | Description                            |
|-------|----------------------------------------|
| 1     | Not ready for the program              |
| 2     | Below expectations                     |
| 3     | Meets expectations                     |
| 4     | Strong candidate                       |
| 5     | Exceptional — ideal ambassador         |

✅ Reviewers must include a brief explanation in the “Notes” column.  
This explanation helps ensure nominees receive constructive, thoughtful feedback.

---

## ✅ Step 2: Manual Review & Decision

Once all reviewers have scored:

1. The **Program Manager** (or ED) reviews the total input  
2. They determine whether the nominee should be `approved` or `rejected`  
3. The final decision is typed as a comment on the GitHub issue:
   - `approved` → nominee progresses to the next stage
   - `rejected` → issue is closed, with a thank-you message and link to community hub

💬 Example decision comment:
approved
Great work — nominee will proceed to the interview and onboarding process.

---

## 🛠 Step 3: Run the Manual Workflow

A GitHub workflow is **manually triggered** to process all open nominations that have been commented on with `approved` or `rejected`.

The workflow will:
- Apply the appropriate label (`approved` or `rejected`)
- Remove temporary labels (`pending-review`, `under-review`, etc.)
- Close the issue if it is rejected
- Add a summary comment to the issue
- Generate a CSV (`ambassador/decision_summary.csv`) with issue numbers, decisions, and reviewers
- Commit the summary CSV to the repo

---

## ✅ Example Summary Comment Posted by Bot

🧮 Final decision: APPROVED
🔎 Reviewer notes are available in the internal scoring sheet.
📩 Next steps will be shared with the nominee by the program team.

---

## 🧪 How to Use the Workflow

1. Ensure all scores are filled in the reviewer sheet  
2. Comment `approved` or `rejected` on each nomination issue  
3. Trigger the **Finalize Decisions** workflow in the GitHub Actions tab  
4. Verify:
   - Issues are updated and/or closed
   - Comments are posted
   - CSV is committed to `/ambassador/`

---

## 🚧 Future Enhancements

- Reviewer dashboard (UI)
- Auto-reminders for pending reviews
- Notification alerts for nominees
- Bulk export to onboarding pipeline

---

## 🙋 Questions?

If you need help using or maintaining these workflows, contact the program team or email
