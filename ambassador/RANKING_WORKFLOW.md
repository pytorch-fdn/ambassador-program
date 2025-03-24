
# ⚙️ Ranking Workflow: PyTorch Ambassador Program

This document explains how the **automated ranking system** works for evaluating nominations to the PyTorch Ambassador Program. It is intended for **maintainers, contributors, and workflow administrators** who want to understand or improve the scoring system.

---

## 📌 Purpose

The ranking workflow enables reviewers to **evaluate nominees using a 1–5 scale** via GitHub issue comments. The system then:
- Collects valid scores
- Calculates the average
- Automatically applies a final decision label (`approved` or `rejected`)
- Posts a summary comment for transparency

---

## 🧮 How It Works

### ✅ Step 1: Reviewers Comment Their Scores

Reviewers comment directly on a nomination issue using the format:

```
Score: X
```

Where `X` is an integer from 1 to 5. The comment is **not case-sensitive**.

Only **one score per reviewer** is counted. If a reviewer comments more than once, only their first valid score is used.

---

### 🧠 Step 2: Workflow Parses All Comments

When any comment is created, the GitHub Action:
1. Fetches all comments on the issue
2. Searches for those starting with `Score:`
3. Extracts the number and reviewer’s GitHub username
4. Skips duplicate users or invalid formats

---

### 📊 Step 3: Score Calculation & Decision Logic

- The system **adds all valid scores** and **divides by the number of reviewers**
- The average score is compared against a fixed threshold

| Average Score | Final Status |
|---------------|--------------|
| **≥ 3.0** | ✅ Approved |
| **< 3.0** | ❌ Rejected |

The workflow then:
- Removes any conflicting status labels (`approved`, `rejected`)
- Adds the correct label based on the result

---

### 💬 Step 4: Summary Comment

An automatic comment is posted to the issue with:
- The number of reviewers
- The average score (rounded to 2 decimals)
- The list of reviewer usernames
- The final decision (in bold)

---

## 🔧 Example Output

```
🧮 Average score from 3 reviewers: **3.67**
👥 Reviewed by: @alice, @bob, @carol
📌 Final decision: **APPROVED**
```

---

## 🧪 How to Test the Workflow

1. Create a test nomination
2. Leave multiple `Score: X` comments from different users
3. Confirm:
   - The correct label (`approved`/`rejected`) is applied
   - The score summary comment is posted
   - No duplicate outcome labels exist

---

## 🛠 Maintenance & Improvements

- Currently, the logic is in `.github/workflows/finalize-nomination-ranking.yml`
- Future improvements could include:
  - Ignoring comments on non-nomination issues
  - Supporting updates to scores
  - Custom weights per reviewer

---

## 🙋 Questions?

Contact a repo maintainer or open an issue in this repository if you need help understanding or adjusting the workflow.

