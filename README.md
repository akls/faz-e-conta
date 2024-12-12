# faz-e-conta



# Contributing Code

## Creating a Feature Branch

Step 1: Clone the repository

`git clone https://github.com/akls/faz-e-conta`

Step 2: Switch to the `dev` branch

`git switch dev`

You can confirm the current local branch with `git status`. The output should be something like

```
On branch dev
Your branch is up to date with 'origin/dev'.

nothing to commit, working tree clean
```

Step 3: Create a feature branch

Create the local feature branch using a name that follows the common _feature/issue-title_ pattern. An example is:

`git branch -m feature/issue10-standardize-cdm`

and push it to the remote repository with

`git push -u origin feature/issue10-standardize-cdm`

