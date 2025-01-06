# Git Cheat Sheet

## Setup

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email
git config --global user.email "you@example.com"

# Verify configuration
git config --list
```

## Starting a Project

```bash
# Create a new Git repository
git init

# Clone an existing repository
git clone <repository-url>
```

## Basic Commands

```bash
# Check the status of your repository
git status

# Add changes to the staging area
git add <file>          # Add a specific file
git add .               # Add all changes

# Commit changes
git commit -m "Commit message"
```

## Branching

```bash
# List branches
git branch

# Create a new branch
git branch <branch-name>

# Switch to a branch
git checkout <branch-name>

# Create and switch to a new branch
git checkout -b <branch-name>
```

## Merging

```bash
# Merge a branch into the current branch
git merge <branch-name>
```

## Viewing Changes

```bash
# Show changes (in the working directory)
git diff

# Show changes (staged for commit)
git diff --cached

# View commit history
git log
```

## Remote Repositories

```bash
# Add a remote repository
git remote add origin <repository-url>

# Fetch changes from a remote repository
git fetch

# Push changes to a remote repository
git push origin <branch-name>

# Pull changes from a remote repository
git pull origin <branch-name>
```

## Push and Pull Operations

```bash
# Push the current branch to the remote repository
git push

# Push all branches to the remote repository
git push --all

# Pull the latest changes from the remote repository
git pull

# Fetch and merge changes in one command
git pull origin <branch-name>
```

## Undoing Changes

```bash
# Unstage a file
git reset <file>

# Discard changes in a file
git checkout -- <file>

# Revert to the last commit
git reset --hard HEAD
```

## Tags

```bash
# Create a new tag
git tag <tag-name>

# List tags
git tag

# Push tags to remote
git push origin <tag-name>
```

## Stashing

```bash
# Stash changes
git stash

# List stashes
git stash list

# Apply the most recent stash
git stash apply

# Drop a stash
git stash drop
```

## Helpful Aliases

```bash
# Set up some helpful aliases
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
```


