# Git PR Workflow

## Purpose

Automate the standard Git workflow for this project.

Use this skill when the user asks to create a branch, commit changes, push them, and open a Pull Request.

## Workflow

Before making any Git changes:

1. Check the current branch.
2. Check for uncommitted changes.
3. Do not overwrite or discard existing user changes.
4. Pull the latest target branch when safe.

## Branch

Create a new branch using the branch name requested by the user.

If no branch name is provided, generate a clear branch name based on the task.

Example:

```bash
git checkout main
git pull
git checkout -b feature/example