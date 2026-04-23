# Workspace Layout

This reference defines the minimum reusable workspace shape for the learning-project-tutor skill.

## What Belongs In The Skill
- `SKILL.md`
- reusable references
- reusable scripts
- reusable templates

These files should be portable across users and vaults.

## What Belongs In The User Workspace
- `AGENTS.md`
- `memory/`
- `templates/learning/`
- `tools/`
- `topics/`

The user workspace is where learning runs happen. The skill should help create or maintain this structure, but the generated topic data should live outside the skill itself.

## Recommended Split

### Skill Layer
Stores stable teaching behavior:
- state machine rules
- source-aware course planning rules
- academic-paper handling rules
- response and diagnosis rules
- final-phase rules

### Workspace Layer
Stores run-time learning data:
- topic source files
- generated lessons
- user responses
- diagnoses
- final tasks
- QA logs
- topic-local memory
- global memory activation history

## Why This Split Matters
If you bundle your full repository as a skill, other users inherit your personal state, topic history, and path assumptions. That makes installation heavier and the skill less reusable.

If you package only the orchestration contract plus reusable assets, other users can install one folder and let Codex create the workspace in their own vault.

## Practical Packaging Rule
If a file answers "how should Codex teach?", it likely belongs in the skill.

If a file answers "what happened in this user's study run?", it likely belongs in the workspace.
