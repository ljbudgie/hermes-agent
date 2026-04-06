---
name: coding-agent-review
description: >
  Human-impact review for code changes. Before finalizing work, the agent checks
  whether changes touch areas that deserve human attention — accessibility,
  privacy, personal data handling, user-facing language, pricing/billing logic,
  automated decision-making, or deployment configuration. Based on the Burgess
  Principle: "Was a human member of the team able to personally review the
  specific facts of my situation?"
version: 1.0.0
author: ljbudgie
license: MIT
category: advocacy
metadata:
  hermes:
    tags: [advocacy, human-review, safety, accessibility, privacy, burgess-principle]
    category: advocacy
    source: https://github.com/ljbudgie/burgess-principle
---

# Coding Agent Review — Burgess Principle

Before finalizing any code changes, apply the Burgess Principle human-impact check. The core question is:

> "Was a human member of the team able to personally review the specific implications of this change for the people it affects?"

## When to Use

- Before completing a task that involved code changes
- When the user asks for a review of what you've done
- When you detect that your changes touch one of the human-impact areas below

## Human-Impact Areas

Flag changes for human review when they touch ANY of these areas:

1. **Accessibility** — UI changes, ARIA attributes, color contrast, screen reader support, keyboard navigation, motion/animation, text sizing, alt text, form labels
2. **Privacy & Personal Data** — Collection, storage, processing, or sharing of personal data; cookie/tracking changes; consent flows; data retention; analytics
3. **Security** — Authentication, authorization, credential handling, encryption, input validation, CORS, CSP headers, dependency updates with security implications
4. **User-Facing Language** — Error messages, notifications, onboarding text, terms of service references, marketing copy, anything a real person reads
5. **Pricing & Billing** — Payment flows, subscription logic, trial periods, pricing display, currency handling, refund logic, invoice generation
6. **Automated Decisions** — Algorithms that score, rank, filter, recommend, approve, or deny things for real people — credit checks, content moderation, hiring filters, risk assessment
7. **Deployment & Infrastructure** — Production environment changes, feature flags, rollout percentages, database migrations, service dependencies, monitoring/alerting thresholds

## Procedure

After completing code changes, before presenting the final summary:

1. **Scan** — Review all files you modified or created. List which human-impact areas (if any) were touched.
2. **Flag** — For each impacted area, write one sentence explaining what changed and why a human should look at it.
3. **Recommend** — State clearly whether this change should be reviewed by a human before shipping, and who (e.g., "a designer should check the new error messages", "a security engineer should review the auth flow changes").

### Output Format

If human-impact areas were touched, include a section like this in your response:

```
## 🔍 Human-Impact Review (Burgess Principle)

The following changes affect real people and should be reviewed by a human before shipping:

- **[Area]**: [What changed and why it matters]
- **[Area]**: [What changed and why it matters]

**Recommendation**: [Who should review, and what to look for]
```

If no human-impact areas were touched, state briefly:

```
## 🔍 Human-Impact Review (Burgess Principle)

No human-impact areas were affected by these changes. ✅
```

## Verification

- Every completed task includes a Human-Impact Review section
- Each flagged area has a specific, actionable description (not generic)
- The recommendation names a role or person type, not just "someone"
- The review is honest — if you're unsure whether an area was affected, flag it rather than skip it

## Attribution

Based on the [Burgess Principle](https://github.com/ljbudgie/burgess-principle) by Lewis James Burgess.
UK Certification Mark: UK00004343685. Free for personal use under MIT licence.
