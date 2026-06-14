❯ provide me claude code prompt togenerate such a well crafted detail .md file in future projects                                                      

⏺ Here's a reusable prompt you can paste into Claude Code for any future project:

  ---

  Generate a comprehensive PROJECT_DOCS.md file for this project and save it in the project root folder.

  The file must include all of the following sections:

  1. **What the App Does** — A clear summary of the app's purpose and a bullet list of all features currently built.

  2. **Tech Stack Overview** — A table listing every technology/library used, which layer it belongs to (backend, frontend, database, etc.), and its
  specific role in the project.

  3. **Starting the Project in VS Code (From Scratch)** — Step-by-step instructions for someone setting up the project for the first time: creating the
   folder, opening VS Code, setting up a virtual environment, selecting the Python interpreter, installing dependencies, creating the folder structure,
   and running the app.

  4. **Step-by-Step Build Guide** — For each feature or module that was built, explain: the goal, what files were created or modified, what logic was
  implemented, and any important decisions made.

  5. **Project Structure** — An annotated folder/file tree showing every file and a one-line description of what it does.

  6. **File-by-File Explanation** — A deep-dive section for every significant file. For each file explain: what it does, key functions/classes/routes
  inside it, what libraries it uses and why, and how it connects to other files.

  7. **Database Schema** — ASCII table diagrams for every table showing column names, types, constraints, and relationships (foreign keys, cascades).

  8. **Architecture Diagram** — A full ASCII diagram showing how all layers of the app connect: browser → backend → database → templates → static
  files.

  9. **Request–Response Flow** — A numbered step-by-step walkthrough (using a concrete example like "user submits a form") tracing the full journey
  from browser click → route → validation → database → redirect → rendered page.
  10. **Authentication Flow** — Separate flow diagrams for Register, Login, Logout, and the protected route guard — showing every branch (success path
  and all error paths).
  
  11. **Route Map** — A table of every route in the app: HTTP method, URL pattern, whether auth is required, and a description of what it does.
  
  12. **How Each Module Powers the App** — A visual ASCII diagram showing the dependency chain between all files/modules and how data flows between
  them at runtime.
  
  13. **Quick Reference** — The exact commands needed to activate the environment, install packages, seed the database, and start the server. Include
  any sample login credentials from seed data. 
  
  Use ASCII diagrams for all architecture and flow visuals (no external image links).
  Format everything in clean GitHub-flavored Markdown with tables, code blocks, and headers.
  The tone should be educational — suitable for a student or new developer reading it for the first time.

  ---
  Tips for best results

  ┌────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────────────────┐
  │                          Tip                           │                                   Why                                   │
  ├────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ Run it after the project is fully built                │ Claude will have all the code in context and generate accurate diagrams │
  ├────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ Add for a [Flask/Django/React/etc.] project            │ Tailors the stack-specific details                                      │
  ├────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ Add targeted at beginners or for a senior dev audience │ Adjusts the tone and depth                                              │
  ├────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ Add also include a Troubleshooting section             │ Useful for common setup errors                                          │
  ├────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
  │ Add include a TODO / Roadmap section                   │ Documents what's left to build                                          │
  └────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────────────────┘
