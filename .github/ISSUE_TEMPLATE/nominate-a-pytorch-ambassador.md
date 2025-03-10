---
name: Nominate a PyTorch Ambassador
about: Submit a nomination for the PyTorch Ambassador Program.
title: "[Nomination] <Nominee Name>"
labels: nomination, pending-review
assignees: reginankenchor

---

name: "Nominate a PyTorch Ambassador"
description: "Submit a nomination for the PyTorch Ambassador Program."
title: "[Nomination] <Nominee Name>"
labels: ["nomination", "pending-review"]
body:
  - type: markdown
    attributes:
      value: "## 🎖 PyTorch Ambassador Nomination Form\n\nThank you for nominating someone for the PyTorch Ambassador Program. Please provide the details below."

  - type: input
    id: nominee-name
    attributes:
      label: "Nominee Name"
      placeholder: "Enter full name"

  - type: input
    id: nominee-email
    attributes:
      label: "Nominee Email"
      placeholder: "Enter email address"

  - type: textarea
    id: reason
    attributes:
      label: "Why should they be an ambassador?"
      placeholder: "Describe their contributions to PyTorch and why they would be a great ambassador."
      render: markdown

  - type: textarea
    id: contributions
    attributes:
      label: "Nominee's Contributions to PyTorch"
      placeholder: "List any projects, talks, events, or tutorials they have created related to PyTorch."
      render: markdown

  - type: dropdown
    id: involvement
    attributes:
      label: "Nominee's Area of Involvement"
      multiple: true
      options:
        - "Community Advocate"
        - "Educator"
        - "Researcher"
        - "Developer"
        - "Speaker"
        - "Other"

  - type: input
    id: your-name
    attributes:
      label: "Your Name (If You're Nominating Someone Else)"
      placeholder: "Enter your name"

  - type: input
    id: your-email
    attributes:
      label: "Your Email (Optional)"
      placeholder: "Enter your email address"

  - type: textarea
    id: additional-info
    attributes:
      label: "Additional Information (Optional)"
      placeholder: "Any extra details you'd like to share about the nominee?"
      render: markdown
