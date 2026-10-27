# Static analysis findings

**Student ID:** PES2UG24CS593  
**Assigned repository:** [L5_32_expense_tracker](https://github.com/SETAPESU26/L5_32_expense_tracker)  
**Line numbers:** The line numbers below refer to the original `expense_tracker.py` before cleanup.

| Issue | Type | Line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Shell command injection risk (Bandit B605) | High security | 61 | `os.system("xdg-open " + path)` passed a path through a shell, so shell metacharacters could be interpreted as commands. | Convert the path to a file URI and pass it to `webbrowser.open`, without constructing a shell command. |
| Hard-coded temporary directory (Bandit B108) | Medium security | 8 | `/tmp/expense_reports` was OS-specific and assumed the directory existed. | Derive the report directory from `tempfile.gettempdir()` and create it with `Path.mkdir`. |
| Insecure temporary filename (Bandit B306) | Medium security | 55 | `tempfile.mktemp` returned a name without creating the file, leaving a race window. | Use `tempfile.mkstemp`, which creates a unique file atomically, and close its descriptor. |
| Broad exception handler (Pylint W0718) | Correctness | 38-42 | `except Exception` concealed unrelated programming errors while handling an empty expense list. | Use `max(..., default=None)` to express the empty-list case directly. |
| Global budget mutation (Pylint W0603) | Maintainability | 28-30 | `setBudget` changed module state with `global`, making separate trackers share one budget. | Put expenses and budget on an `ExpenseTracker` instance. |
| Hard-coded password (Bandit B105) | Low security | 5 | A demo password was embedded in source and could be mistaken for a usable secret. | Read `BANK_SYNC_PASSWORD` from the environment and compare it with `secrets.compare_digest`; the demo remains unauthenticated when no secret is configured. |
| Non-standard function and variable names (Pylint C0103) | Naming | 7, 11, 20, 28, 28, 33, 38, 44, 49, 53, 55, 59 | CamelCase names and a lowercase module-level budget did not follow Python naming conventions. | Use snake_case methods and a clearly named uppercase default-budget constant. |
| Missing documentation strings (Pylint C0114/C0116) | Documentation | 1, 11, 20, 28, 33, 38, 44, 49, 53, 59, 64 | The module and public functions had no documentation strings. | Add concise module, class, and method documentation strings. |
| Index-based ledger loop (Pylint C0200) | Readability | 45-46 | `range(len(expenses))` indexed the list unnecessarily. | Iterate with `enumerate(..., start=1)`. |
| Whitespace before colon (Flake8 E203) | Formatting | 15 | The dictionary literal included a space before a colon. | Reformat the entry with standard spacing; the refactor stores expenses in a dataclass. |
| Missing blank line before function (Flake8 E302) | Formatting | 44 | `printLedger` was separated from the preceding function by only one blank line. | Keep standard top-level spacing between definitions. |
| Inline comment spacing (Flake8 E261) | Formatting | 74 | The inline comment did not have two spaces before `#`. | Remove the redundant inline comment from the demonstration. |
| Line too long (Flake8 E501) | Formatting | 77 | The summary print statement exceeded the configured 79-character limit. | Split the output call across multiple lines. |

## Results

The cleaned program preserves the demonstration output. Bandit reports no findings, Flake8 reports no formatting issues, and Pylint scores the final file at **10.00/10**. See the `reports_before` and `reports_after` folders for the complete tool output and demo output.
