# Reflection

**Student ID:** PES2UG24CS593

The supplied three-page handout asks for four reflection answers but does not include the questions themselves. The responses below cover four reflection themes grounded in the stated learning outcomes.

## 1. What did static analysis reveal about the original program?

The program's demo worked, but the source still had risks that the demo did not exercise. Bandit identified a shell command that incorporated a file path, an insecure temporary-file pattern, a hard-coded temporary directory, and a password literal. Pylint also found broad exception handling and shared global budget state. Flake8 exposed inconsistent spacing and long lines.

## 2. How did the three tools differ?

Bandit focused on risky security patterns, including shell execution and temporary files. Pylint checked broader code quality, such as exception handling, global state, naming, and documentation. Flake8 focused on style rules that make Python code consistent and easier to scan. Their findings overlapped in purpose but covered different kinds of risk.

## 3. Which changes mattered most, and how was behavior checked?

The shell command was replaced with a file-URI open through Python's `webbrowser` module. Temporary report files now use `mkstemp` in a directory derived from the system temporary directory. The hard-coded password was removed; password checks use an environment-provided value and a constant-time comparison. I also moved expenses and the budget into an `ExpenseTracker` instance and replaced the broad exception with `max(..., default=None)`. The before and after demo output matched, and the final static-analysis runs reported zero Bandit findings, zero Flake8 findings, and a Pylint score of 10.00/10.

## 4. How will static analysis help in future work?

I would run the tools during development and before committing changes. That catches style problems and suspicious patterns while the relevant code is still easy to change. I would still review each finding in context, because a clean tool report cannot prove that program behavior or every security property is correct.
