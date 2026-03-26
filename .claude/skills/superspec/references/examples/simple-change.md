# Example: Simple Change

## User Prompt

“Adjust the submit button state and helper text on the existing payment form. The rest of the page should stay the same.”

## Expected Route

Light path:

```txt
Classify -> Mini Align -> Propose -> Apply -> Verify
```

## Align Outcome

- confirm when the button is disabled
- confirm the new copy
- confirm whether loading and error text also change

## Artifact Shape

- `proposal.md`: one existing page, explicit UX tweak, note affected states
- `design.md`: update button state logic and helper text rendering path
- `tasks.md`: split copy update, interaction logic update, verification
