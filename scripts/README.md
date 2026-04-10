Run the renaming script to standardize Markdown basenames to UPPERCASE.

From the repository root (PowerShell):

```powershell
& .\scripts\rename_md_basenames_uppercase.ps1
```

The script uppercases each file's basename (e.g., `readme.md` -> `README.md`) and preserves the original extension.

Notes:
- The script uses a two-step Move to ensure case-only renames succeed on Windows filesystems.
- Review changes with `git status` before committing.