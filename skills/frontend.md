# Frontend Skill

## Purpose

Use this playbook for the local web app, UX, accessibility, and structured output rendering.

## Practices

- Preserve the product's safety positioning in the UI.
- Render structured fields clearly: risk, referral, red flags, basis, limitations.
- Make loading, empty, and error states explicit.
- Design for desktop and mobile.
- Avoid implying diagnosis certainty through visual language.
- Keep components small when reuse is clear; avoid premature abstraction.

## Anti-Patterns

- Hiding safety notices.
- Presenting model output as a clinical decision.
- Creating generic dashboard UI with no SUS context.
- Adding analytics or external scripts without ADR.
- Memoizing by default without measured need.

## Checklist

- [ ] UI labels are Brazilian Portuguese or intentionally bilingual.
- [ ] Red flags are visually prominent.
- [ ] Safety notice is visible.
- [ ] Mobile layout works.
- [ ] Error states include next steps.
