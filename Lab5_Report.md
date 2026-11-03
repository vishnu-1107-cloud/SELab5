# Lab 5: Static Code Analysis Report

**Student ID:** PES2UG24CS593  
**Assigned repository:** [L5_32_expense_tracker](https://github.com/SETAPESU26/L5_32_expense_tracker)  
**Student repository:** [SELab5](https://github.com/vishnu-1107-cloud/SELab5)  
**Analysis tools:** Pylint, Flake8, Bandit

## Objective

Run static-analysis tools against the assigned expense tracker, document the issues found, make corrective changes, and compare the results before and after cleanup.

## Work performed

The original program was analyzed with Pylint, Flake8, and Bandit. Initial findings included shell command construction with a file path, insecure temporary-file handling, a hard-coded temporary directory and password, broad exception handling, module-level mutable budget state, naming and documentation problems, and style violations.

The implementation was updated to:

- Open report files through Python's `webbrowser` module instead of constructing a shell command.
- Create temporary files securely with `tempfile.mkstemp` and use the system temporary directory.
- Read the optional bank-sync password from the environment and compare it with `secrets.compare_digest`.
- Keep expenses and the budget on an `ExpenseTracker` instance.
- Handle an empty expense list with `max(..., default=None)`.
- Apply Python naming, documentation, iteration, and formatting conventions.

## Final results

| Tool/check | Final result |
|---|---|
| Pylint | 10.00/10 |
| Flake8 | No issues found (exit code 0) |
| Bandit | No issues identified |
| Demo comparison | Before and after output matched |

The full before-and-after tool outputs and captured demo outputs are included in the accompanying `reports_before` and `reports_after` folders.

## Conclusion

The analysis identified security, correctness, maintainability, and formatting problems that were not apparent from the basic demonstration alone. After remediation, all three tools reported clean results, and the recorded demonstration output remained the same. Static analysis is useful as an early feedback step, while code review and behavioral checks remain necessary.

## Reflection

Bandit focused on potentially unsafe security patterns, Pylint on broader code quality, and Flake8 on style consistency. The most significant changes removed shell-based file opening and unsafe temporary-file handling, eliminated the embedded password, and isolated tracker state. In future work, these tools can be run during development and before commits; findings should still be reviewed in context because clean reports do not prove the absence of all defects.
