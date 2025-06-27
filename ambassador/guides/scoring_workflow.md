# 🧮 Scoring Workflow: PyTorch Ambassador Program

This document outlines the scoring and decision process used to evaluate nominations for the PyTorch Ambassador Program. It is intended for:

- ✅ Reviewers who provide scores and notes
- ✅ Program managers who finalize decisions and run GitHub workflows

---

## 📌 Overview

Nominations are reviewed using a **1–5 score system** captured in a shared scoring spreadsheet. After scores are reviewed, the Program Manager manually applies final decisions via GitHub comments and a workflow.

---

## 👥 Reviewer Responsibilities

### Step 1: Score the Nominee

Each reviewer should:

1. Open the relevant row in the **reviewer tracking sheet**
2. Add a score between **1 and 5**
3. Include a **brief explanation** in the notes column

### Scoring Guide:

| Score | Meaning                             |
|-------|-------------------------------------|
| 1     | Not ready for the program           |
| 2     | Below expectations                  |
| 3     | Meets expectations                  |
| 4     | Strong candidate                    |
| 5     | Exceptional — ideal ambassador      |

📝 Thoughtful comments are important — they help nominees understand the decision and provide transparency.

---

## 🛠 Program Manager Workflow

### Step 2: Review Scores & Post Final Decision

Once all reviewers have submitted their scores:

1. Review the nominee’s row in the spreadsheet
2. Post a comment on their GitHub issue with either:

   - `approved` — if they are ready for the next step
   - `rejected` — if they do not meet current criteria

Example:

approved
The nominee meets the scoring threshold and will move forward to the interview phase.


> Note: Comment is **not case sensitive** and no scores need to be posted on GitHub.

---

### Step 3: Trigger the Finalization Workflow (Manual)

Once decisions are posted:

- Trigger the `Finalize Reviewer Decisions` workflow in the GitHub Actions tab.

This will:

- ✅ Add the `approved` or `rejected` label
- ✅ Remove the `pending-review` label (if present)
- ✅ Close rejected issues automatically
- ✅ Post a confirmation comment on each issue
- ✅ Create and commit a CSV summary at `ambassador/decision_summary.csv`

---

## ✅ Example Comment Added by Workflow

For an approved issue:

✅ Thank you! This submission has been approved. We’ll contact you shortly with next steps.


For a rejected issue:

Thank you for your submission. After careful review, your application has been rejected.
We appreciate your interest and encourage you to stay involved with the PyTorch community: https://pytorch.org/community-hub/


---

## 🙋 Questions?

For any issues or help, please email [ambassadors@pytorch.org](mailto:ambassadors@pytorch.org) or tag the program manager in GitHub.
