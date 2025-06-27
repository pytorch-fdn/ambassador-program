# 👥 Reviewer Guide: PyTorch Ambassador Program

Welcome — and thank you for supporting the review process for the **PyTorch Ambassador Program**! 🎉  
This guide walks you through how to evaluate nominations and help nominees receive thoughtful, consistent feedback.

---

## 📌 Your Role as a Reviewer

As a reviewer, your job is to:

1. Identify active nominations  
2. Review the nominee’s contributions and readiness  
3. Leave a comment with either **`approved`** or **`rejected`** and an optional explanation  
4. Once all reviews are in, the program manager runs a workflow to finalize decisions

---

## 🔍 Step 1: Find Nominations

Visit the GitHub issues page:  
👉 [View all nominations](https://github.com/pytorch-fdn/ambassador-program/issues)

Look for issues labeled:

- `ambassador`
- `pending-review`

These are ready for you to review.

---

## 📝 Step 2: Evaluate the Nominee

Carefully read the nomination issue. Consider:

- The nominee’s contributions to PyTorch or its ecosystem  
- Community engagement (e.g., events, mentorship, education)  
- Future goals and plans as an ambassador  
- Any linked profiles or supporting materials

---

## ✅ Step 3: Submit Your Recommendation

Comment directly on the issue using one of the two decisions:

- `approved` — if you support the nominee  
- `rejected` — if you believe the nominee is not a fit at this time

Optionally, add a short explanation to support your choice.

### ✅ Example: Approval

approved
The nominee has hosted two workshops, contributed to tutorials, and is active in the community forums. Strong candidate.

shell
Copy
Edit

### ❌ Example: Rejection

rejected
While the nominee is enthusiastic, there’s limited contribution history. Would suggest reapplying after 6 months of deeper involvement.

yaml
Copy
Edit

---

### 🚫 What Not to Do

- Don’t use scores like `score: 4` — those are no longer valid  
- Don’t leave vague comments like “+1”  
- Don’t submit both approved and rejected — pick one

---

## ⚙️ Step 4: What Happens After Reviews

After reviewers have submitted their decisions, a **manual GitHub Action** is run to process them:

1. The system checks for the most recent decision comment from each issue  
2. If any comment includes **`approved`** or **`rejected`** (case-insensitive), it is processed  
3. It:
   - Adds the `approved` or `rejected` label  
   - Removes the `pending-review` label  
   - Comments on the issue with the outcome  
   - Closes the issue if rejected  
   - Adds a row in `decision_summary.csv` for tracking

---

## 📨 What Nominees See

Each nominee will receive a comment like:

- ✅ **Approved:**

  > 🎉 Congratulations! Your application has been **approved**. We’ll follow up with next steps shortly via email or GitHub.

- ❌ **Rejected:**

  > Thank you for your submission. After careful review, your application has been **rejected**. We encourage you to stay involved: [pytorch.org/community-hub](https://pytorch.org/community-hub)

---

## 🙋 Frequently Asked Questions

### 🔁 What if someone submits twice?

The program manager will detect and remove duplicates. Only review the **latest** version.

### 👤 Can I review anonymously?

No. Reviews must be posted from your GitHub account so we can track accountability and prevent duplicates.

### 🤝 Can I coordinate with other reviewers?

Yes — coordination is encouraged.  
Feel free to discuss nominees on Slack, GitHub, or privately before commenting.

---

## 🧠 Reviewer Tips

- Use the **reviewer tracking sheet** to manage who’s reviewing what  
- Focus on **impact**, **fit**, and **readiness**  
- Keep your comments constructive — even when rejecting

---

## 📫 Need Help?

For questions, reach out to:  
📧 **[ambassadors@pytorch.org](mailto:ambassadors@pytorch.org)**

Thanks again for supporting a fair and inspiring review process! 🚀
