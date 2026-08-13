# Upload to GitHub

Recommended repository name: `aqarmind-backend`

## GitHub UI

1. Create a new repository named `aqarmind-backend`.
2. Set visibility to **Public**.
3. Do **not** add a README, .gitignore, or license during creation (this package already contains them).
4. Copy the remote repository URL.

## Local commands

From inside this folder:

```bash
git init
git branch -M main
git add .
git status
git commit -m "Initial public Aqarmind backend"
git remote add origin https://github.com/YOUR-USERNAME/aqarmind-backend.git
git push -u origin main
```

Before `git commit`, inspect `git status` and confirm `.env` is **not** listed.

## Extra GitHub security

After publishing:

- Keep GitHub secret scanning / push protection enabled where available.
- Never paste real credentials into Issues, Actions logs, README files, or commits.
- If a real secret is ever committed, rotate it immediately even if the commit is later deleted.
