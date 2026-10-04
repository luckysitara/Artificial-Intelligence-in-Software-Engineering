# AI: SQL to ORM Refactoring and Security Analysis

### Task Description
This task demonstrates the use of AI as a refactoring and security reviewer. A
procedural user-management script that executes raw SQL through a
`mysql.connector` cursor was translated into a modern, object-oriented
SQLAlchemy ORM implementation, and the security and professional benefits of
the change were analysed.

### AI Tool Used
* **Claude (Claude Code)**

### Files & Resources
* [initial_code.py](./initial_code.py): The procedural starting point — hand-written SQL strings executed through a cursor, with connection, transaction and error handling left to the caller.
* [refactored_code.py](./refactored_code.py): The SQLAlchemy ORM version — a declarative `User` model, automatic table creation and Session-based CRUD with an automatic rollback scope.
* Screenshots of the prompt and of the AI's complete response are included in the submitted Google Doc.

### Prompt Used
```
You are a senior Python engineer. Refactor the procedural database script
below into a modern, robust, object-oriented version that uses the SQLAlchemy
ORM instead of raw SQL:

<paste of initial_code.py>

Requirements:
1. Define the User class as a SQLAlchemy declarative model that maps the
   users table (id, username, email) and keeps the schema in one place.
2. Show how to create the table from the model, how to add a new user and how
   to query that user back using an ORM Session, including how transactions
   are committed/rolled back and how the connection is managed.
3. Refactor every function of the original script: create_user,
   get_user_by_username, update_user_email, delete_user and list_users.
4. Explain in detail why the SQLAlchemy ORM version is a more professional and
   a more secure solution than executing raw SQL, especially SQL built with
   string formatting.
5. Keep credentials out of the source code, keep the code PEP8-clean and
   runnable, and point out any bugs the original script contains.

Format the answer as (a) the complete refactored code in one block and then
(b) the detailed security and professionalism analysis.
```

### Result & Verification
The refactored script runs end-to-end (create → query → update → list →
delete → list) with `DATABASE_URL=sqlite:// python3 refactored_code.py`; the
same model compiles to MySQL DDL unchanged, because the only environment
specific detail is the dialect prefix of the connection URL.

The refactor also fixes a real defect of the original script: none of the
procedural functions committed their transaction, so every write depended on
the caller remembering `connection.commit()`. With the ORM, the
`session_scope()` helper commits on success and rolls back automatically when
an exception is raised.

### Security & Professional Analysis
* **Injection safety by construction.** The ORM binds values as parameters
  for every statement it generates. The original script happened to be
  parameterized, but its pattern — building SQL text and passing it to
  `execute()` — is the same pattern where f-strings and `%` formatting creep
  in later; an ORM makes that class of mistake structurally impossible for
  values, and it quotes identifiers (columns, tables) that raw SQL cannot
  parameterize at all.
* **Transaction and resource management.** Sessions give one atomic unit of
  work per operation: commit on success, rollback on failure, connections
  returned to the pool. The procedural version leaks that responsibility to
  every caller.
* **Single source of truth for the schema.** Column names, types and
  constraints are declared once on the model. A rename is a single edit that
  tooling can follow, instead of a search-and-replace across SQL strings.
* **Portability.** Swapping `mysql+mysqlconnector` for another dialect runs
  the same code on PostgreSQL or SQLite — invaluable for unit tests, which
  can run against an in-memory database.
* **Readability and type safety.** `User(username=..., email=...)` states its
  intent in Python; attribute errors and type mismatches are caught by the
  interpreter, by linters and by IDEs long before the SQL reaches the server.
* **Credentials stay out of the code.** The connection URL is read from the
  environment instead of being hard-coded.

### Analysis & Reflection
Mapping a table to a Python class turns the database into ordinary objects
with attributes, so the compiler, the linter and the IDE understand the code
the same way they understand any other Python program. When the schema lives
in the model there is exactly one place where a column name, a type or a
constraint can be wrong, and a rename propagates by editing that single
declaration instead of hunting through SQL strings scattered across the
codebase. The ORM also removes whole categories of hand-written boilerplate —
opening connections, remembering `commit()`, mapping rows to tuples by
position — which are precisely the places where procedural scripts quietly
break, as the original `create_user` did by leaving the transaction
uncommitted.

Maintainability improves for the same reason: a new developer reads a
declarative model and a handful of short, intention-revealing methods instead
of reconstructing the database contract from string literals. Sessions give
every operation a uniform transaction boundary, so error handling and
rollback logic are written once rather than in each function, and because the
engine is chosen by a single URL the same data layer can be exercised in
tests against SQLite and deployed on MySQL without touching the code. In
short, the ORM trades a small amount of indirection for a large reduction in
the surface where mistakes can hide.
