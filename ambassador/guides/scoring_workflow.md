# 🧮 Scoring Workflow: PyTorch Ambassador Program

This document outlines the **scoring system** used to evaluate nominations for the PyTorch Ambassador Program. It is intended for **reviewers, maintainers, and workflow administrators** who participate in or manage the review process.

---

## 📌 Purpose

The scoring workflow enables reviewers to evaluate nominee submissions using a **1–5 scale** via GitHub issue comments. It supports a structured review process by:

- Acknowledging valid scores immediately
- Accepting only one score per reviewer
- Allowing a review coordination phase
- Calculating average scores
- Applying a final decision (`approved` or `rejected`)
- Closing rejected issues
- Adding a `scoring-complete` label for tracking

---

## 🔁 Overview of the Scoring Flow

| Phase | Labels Used |
|-------|-------------|
| Nomination submitted | `pending-review` |
| Review begins (manual trigger) | `under-review`, `scoring-in-progress` |
| Review finalized | `approved` / `rejected`, `scoring-complete` |

---

## 🧾 Step 1: Submitting a Score

Reviewers comment directly on a nomination issue using this format:

Score: X

Where `X` is an integer from **1 to 5**. The comment is **not case-sensitive**.

✅ Only the **first valid score per reviewer** is counted.  
⚠️ A warning will appear if additional scores are submitted by the same user.

---

## ✅ Step 2: Acknowledgement Comment

When a valid score is submitted, the bot responds with:

📝 Score received from @reviewer: X
⏳ Final decision will be calculated and posted after all reviewers have submitted or in approximately 2 hours.
🚨 Only your first score is counted. Please discuss with other reviewers before submitting.


This encourages team coordination **before** scoring and reinforces the single-score policy.

---

## 🧮 Step 3: Finalizing the Score

The finalization step is **manually triggered** by a reviewer or maintainer. It:

1. Gathers all valid `Score: X` comments
2. Filters out duplicate scores (only first per user)
3. Calculates the **average score**
4. Applies the final label:

| Average Score | Outcome |
|---------------|---------|
| ≥ 3.0         | ✅ `approved` |
| < 3.0         | ❌ `rejected` |

5. Adds the `scoring-complete` label  
6. Removes temporary labels: `pending-review`, `under-review`, `scoring-in-progress`  
7. Closes the issue if it is rejected

---

### 💬 Example Summary Comment

🧮 Final average score from 3 reviewer(s): 4.33
👥 Reviewed by: @alice, @bob, @carol
📌 Final decision: APPROVED

---

## 🛠 Workflow Files Involved

- `.github/workflows/acknowledge-score.yml`  
  Acknowledges and limits reviewer scores

- `.github/workflows/finalize-scoring.yml`  
  Calculates score average and applies final decision

- `.github/workflows/mark-under-review.yml`  
  Manually removes `pending-review` and adds `under-review`, `scoring-in-progress`

---

## 🧪 How to Test the Workflow

1. Create a test nomination issue with the `nomination` label
2. Trigger the manual **under-review** workflow
3. Submit `Score: X` comments from different users
4. Trigger **Finalize Scoring** manually
5. Confirm:
   - Decision label (`approved`/`rejected`) is added
   - `scoring-complete` label is added
   - Summary comment is posted
   - Temporary review labels are removed
   - Rejected issues are closed

---

## 🚧 Future Enhancements

- Per-issue review deadlines
- Reviewer coordination UI
- Score override logic with audit trail
- Discord or email alerts when scoring is finalized

---

## 🙋 Questions?

If you need help using or maintaining these workflows, contact a maintainer or open an issue in this repository.
