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

Create the local feature branch using a name that follows the common _feature/issue-title_ pattern. After creating the local branch, push the change to the remote repository. An example using the branch name _feature/issue10-standardize-cdm_:

```
git branch -m feature/issue10-standardize-cdm
git push -u origin feature/issue10-standardize-cdm
```

## Commiting Code Changes to the Feature Branch

In order to add new files or modified files to the next commit, use the following command:

```
git add <file_name>
git -m "This is a short description of the changes"`
git push
```
