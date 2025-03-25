# 🧑‍⚖️ Reviewer Guide: PyTorch Ambassador Program

Welcome, and thank you for helping review nominations for the PyTorch Ambassador Program! 🎉

This guide will walk you through everything you need to know to review nominations using our **delayed, score-based ranking system**.

---

## 📌 Overview

When someone is nominated to become a PyTorch Ambassador, we ask reviewers to evaluate their application and **submit a score from 1 to 5**. The system will acknowledge each reviewer's score and later calculate a final decision based on all inputs.

Final decisions are calculated and posted **automatically every 2 hours**, or once all reviewers have submitted.

---

## 📥 Step 1: Identify New Nominations

You can find open nominations under the Issues tab:  
👉 https://github.com/pytorch-fdn/foundation-initiative/issues

Each nomination issue will have the label:  
- `nomination`  
- `pending-review`  
- `ambassador`  

---

## 🔍 Step 2: Review the Nomination

Carefully read the information provided in the issue, including:  
- Nominee’s contributions to PyTorch  
- Plans for future engagement  
- Additional materials (GitHub profile, links, etc.)

---

## 🧮 Step 3: Submit Your Score

Comment directly on the issue with a line in this format:

```
Score: X
```

Where `X` is your score (from 1 to 5):

| Score | Meaning |
|-------|---------|
| 1 | Poor — nominee is not ready |
| 2 | Below average — needs more experience |
| 3 | Average — meets expectations |
| 4 | Good — strong candidate |
| 5 | Excellent — exceptional fit |

✅ **Only your first valid score will be counted** (multiple scores from the same reviewer are ignored)  
✅ **The score comment is not case-sensitive** (`Score: 4`, `SCORE: 4`, etc.)

After your score is submitted, the system will post a response like:

```
📝 Score received from @yourname: 4
⏳ Final decision will be calculated and posted after all reviewers have submitted their scores or in approximately 2 hours.
```

---

## 📊 Step 4: How the Final Decision Works

A scheduled workflow runs every 2 hours to process nominations. It will:

1. Collect all unique `Score: X` comments from reviewers
2. Calculate the **average score**
3. Automatically apply a final status label:

| Average Score | Final Status |
|---------------|--------------|
| ≥ 3.0 | ✅ Approved |
| < 3.0 | ❌ Rejected |

4. **Removes** the `pending-review` label if present
5. **Closes the issue automatically** if the nominee is rejected

The system then posts a summary comment with:
- The number of reviewers
- The average score
- The usernames of reviewers
- The final decision

---

## 🧼 Step 5: That’s It!

Once the final decision is made:
- If approved → The issue is labeled `approved` and onboarding begins
- If rejected → The issue is labeled `rejected` and is automatically closed

---

## 💡 Example Comments

**✅ Valid:**

```
Score: 4
Nominee has demonstrated strong community contributions and leadership.
```

**❌ Invalid (ignored):**

```
Rated 5 stars!
```

---

## 🙋 Need Help?

If you're unsure how to score a nominee, just leave a comment on the issue and tag the core team.  
Thanks again for supporting the growth of the PyTorch community! 🚀
