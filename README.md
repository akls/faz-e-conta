# faz-e-conta



# Contributing Code

In short, contributing code involves the following three steps that are outlined in detail below:

1. Creating a feature branch
2. Commiting code to the feature branch
3. Create a pull request (PR) from feature branch to `dev` followed by code review
5. Merge the PR to `dev`

## 1. Creating a Feature Branch

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

## 2. Commiting Code Changes to the Feature Branch

In order to add new files or modified files to the next commit, use the following command:

```
git add <file_name>
git -m "This is a short description of the changes"`
git push
```

## 3. Create a pull request (PR) to merge the feature branch into `dev`

Pull requests (PRs) from the feature branches should be created for the `dev` branch and merged only after completed code review. That is, feature branches should not be merged directly to the `main` branch.

To create a PR for a feature branch, go to the section _Pull Requests_ on the Github website and select _New pull request_. Choose the feature branch and `dev` branch and click `Create pull request`.

## 4. Code review

## 5. Merge the PR to `dev`

# First-time Django Installation

1. `pip install django`
2. `python -m django startproject faz_e_conta`
3. `python manage.py startapp data_hub`

After doing changes to the (data) model:

4. `python manage.py makemigrations`
5. `python manage.py migrate`

To run the server:

6. `python manage.py runserver`
