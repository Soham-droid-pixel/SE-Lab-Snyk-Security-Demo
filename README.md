# Snyk Security Demonstration Lab

Welcome to the **Snyk Security Demo**, a repository designed to illustrate common software vulnerabilities mapped to the OWASP Top 10. This project demonstrates how insecure coding practices can expose applications to attacks, how **Snyk** identifies these vulnerabilities in real-time as a SAST (Static Application Security Testing) tool, and how to successfully remediate them.

## 🎯 Purpose

This lab provides side-by-side comparisons of vulnerable code and its secure counterpart. By using the Snyk IDE extension (or Snyk CLI), developers can scan the vulnerable files, see the exact traces of the critical severity bugs, and apply industry-standard fixes.

---

## 🪲 Vulnerabilities & Remediation Comparisons

### 1. Command Injection
**Files:** `vuln_command.py` ➡️ `fixed_command.py`

*   **The Flaw (`vuln_command.py`):** User input (`target_ip`) is taken straight from a web query and injected directly into an OS-level shell using `os.system()`. An attacker could pass a payload like `127.0.0.1; cat /etc/passwd` to execute arbitrary commands.
*   **How Snyk helps:** Snyk Code flags the `os.system()` sink as a **High/Critical Command Injection**, tracing from the Flask request source to the OS execution sink.
*   **The Fix (`fixed_command.py`):**
    *   Replaced `os.system()` with `subprocess.run()`, disabling shell execution logic.
    *   Passed arguments securely as an array: `["ping", "-c", "1", target_ip]`.
    *   Implemented strict **Input Validation** using a Regex pattern to ensure only a valid IPv4 address is accepted. 

### 2. Insecure Deserialization & Cross-Site Scripting (XSS)
**Files:** `vuln_sdlc_logic.py` ➡️ `fixed_sdlc_logic.py`

*   **The Flaw (`vuln_sdlc_logic.py`):** The application reads a Base64 encoded cookie and deserializes it natively via Python's `pickle.loads()`. Pickle does not just store data; it stores program logic. Handcrafted pickles can execute malicious Python code upon load. Furthermore, trusting data directly onto an HTML-rendered response opens an XSS vulnerability.
*   **How Snyk helps:** Snyk highlights `pickle.loads` as a **Critical Insecure Deserialization** flaw, advising immediate transition to safer data formats.
*   **The Fix (`fixed_sdlc_logic.py`):**
    *   Switched exclusively to `json.loads()`, which parses strictly data (dictionaries/lists) and ignores executable logic.
    *   Added `escape()` from Flask's `markupsafe` library to sanitize output strings, preventing XSS injection when reflecting the loaded `name` key.

### 3. SQL Injection (SQLi)
**Files:** `vuln_sql.py` ➡️ `fixed_sql.py`

*   **The Flaw (`vuln_sql.py`):** Raw username and password parameters are string-concatenated directly into an SQLite `SELECT` query. An attacker can circumvent the entire authentication logic by supplying `' OR '1'='1` as a username.
*   **How Snyk helps:** Identifies the unsanitized concatenation traversing into `cursor.execute()` as a **High-severity SQL Injection**.
*   **The Fix (`fixed_sql.py`):**
    *   Refactored the query to use **Parameterized Queries**. 
    *   Using the `?` placeholder allows the SQLite driver to treat user input purely as literal data boundaries rather than executable SQL syntax, completely neutralizing SQLi techniques.

---

## 🛡️ How Snyk is Utilized in this Project

1.  **Shift-Left Security:** By utilizing Snyk Code directly in the IDE (VS Code), vulnerabilities in `vuln_*.py` files are underlined immediately upon saving. Developers get real-time feedback before code is even committed.
2.  **Data Flow Analysis:** Snyk maps the *Source* (e.g., `request.args.get`) to the *Sink* (e.g., `cursor.execute`) displaying exactly how tainted data flows through the application.
3.  **Remediation Advice:** Snyk not only reports the issue but offers actionable fix examples (like suggesting parameterization for SQLi or `subprocess` for command execution), greatly reducing resolution time.
4.  **Dependency Scanning (SCA):** If any outdated packages are present in `requirements.txt`, Snyk Open Source can scan and offer upgrade paths to secure versions, shielding against known CVEs.

## 🚀 Running the Lab
You can verify the fixes by setting up a local virtual environment:
```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/Scripts/activate # On Windows

# 2. Install dependencies (Flask, etc)
pip install -r requirements.txt

# 3. Run Snyk test (if Snyk CLI is installed)
snyk code test
``` 
You will notice Snyk successfully catches the issues in `vuln_*.py` while verifying the security integrity of `fixed_*.py`.