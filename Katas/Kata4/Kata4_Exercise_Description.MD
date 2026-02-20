# Kata 4 — Data Transformation Pipeline
Foundation 2, Sprint Week 2

Python Focus: File Handling + SQLite Integration
Git Focus: Rebasing
The Exercise:

# Create a pipeline script that:

* Reads raw data from CSV files (simulating API bulk downloads)
* Transforms the data (cleaning, type conversion, calculated fields)
* Loads the transformed data into SQLite tables
* Generates a summary report (counts, basic statistics) written to a markdown file

# Requirements:

* Separate concerns: distinct functions for extract, transform, load, report
* Use generators for memory-efficient processing of large files
* Include data validation (reject/log malformed records)
* Make the pipeline idempotent (running twice produces same result)

# Git Tasks:

* Develop on a feature branch with multiple commits
* Before merging, rebase your branch onto main: git rebase main
* Squash fixup commits if you have any: identify commits that are just fixes to previous commits
* Complete the merge with a clean, linear history

# Stretch:

* Add a --dry-run flag that reports what would happen without writing to the database