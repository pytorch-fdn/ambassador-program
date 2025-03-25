
# ⚙️ Ranking Workflow: PyTorch Ambassador Program

This document explains how the **automated ranking system** works for evaluating nominations to the PyTorch Ambassador Program. It is intended for **maintainers, contributors, and workflow administrators** who want to understand or improve the scoring system.

---

## 📌 Purpose

The ranking workflow enables reviewers to **evaluate nominees using a 1–5 scale** via GitHub issue comments. The system:
- Acknowledges each score when submitted
- Collects valid, unique reviewer scores
- Waits for a review window (2 hours)
- Calculates the average
- Applies a final decision label (`approved` or `rejected`)
- Posts a summary comment for transparency

---

## 🧮 How It Works

### ✅ Step 1: Reviewers Comment Their Scores

Reviewers comment directly on a nomination issue using the format:

```
Score: X
```

Where `X` is an integer from 1 to 5. The comment is **not case-sensitive**.

Only **one score per reviewer** is counted. If a reviewer comments more than once, only their **first valid score** is used.

---

### 🧠 Step 2: Acknowledgement Comment

As soon as a valid score is submitted, the system responds with:

```
📝 Score received from @reviewer: X
⏳ Final decision will be calculated and posted after all reviewers have submitted or in approximately 2 hours.
```

This ensures transparency and avoids premature decisions.

---

### ⏲️ Step 3: Scheduled Finalization

A scheduled GitHub Action runs **every 2 hours** (or can be manually triggered). It:

1. Collects all valid `Score: X` comments
2. Filters for unique reviewers
3. Calculates the **average score**
4. Applies the final label based on threshold

| Average Score | Final Status |
|---------------|--------------|
| **≥ 3.0** | ✅ Approved |
| **< 3.0** | ❌ Rejected |

The workflow:
- Removes conflicting labels (if any)
- Adds the correct final decision label
- Posts a summary comment

---

### 💬 Step 4: Summary Comment Example

```
🧮 Final average score from 3 reviewers: **3.67**
👥 Reviewed by: @alice, @bob, @carol
📌 Final decision: **APPROVED**
```

---

## 🧪 How to Test the Workflow

1. Submit a test nomination
2. Leave `Score: X` comments from different GitHub users
3. Wait for the scheduled action to run (or trigger manually)
4. Confirm:
   - The correct label (`approved`/`rejected`) is applied
   - The summary comment is posted
   - Conflicting labels are removed

---

## 🛠 Maintenance & Future Improvements

- Core logic lives in:
  - `.github/workflows/acknowledge-score-workflow.yml`
  - `.github/workflows/finalize-ranking-scheduled.yml`
- Ideas for improvement:
  - Restrict to nomination issues only
  - Allow score updates (override previous ones)
  - Set scoring deadlines per nomination

---

## 🙋 Questions?

If you need help updating or maintaining the workflow, contact a repo maintainer or open an issue in this repository.
