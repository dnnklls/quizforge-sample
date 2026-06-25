# QuizForge Sample Roadmap

## Current sample

- Static GitHub Pages site.
- Opens with a simple quiz flow.
- Pulls 30 random questions from a larger JSON question pool.
- Immediate practice feedback: wrong answers show the correct answer and explanation.
- Results page with score, missed questions, and topic breakdown.
- Mobile-first layout with a compact progress strip and large question focus.

## Question pool workflow without a database

For now, the question bank is stored as static files:

- `data/questions.json` — readable source format.
- `data/questions.js` — browser-loaded version used by the site.

Update flow:

1. Collect source material: PDFs, screenshots, images, text notes, or spreadsheets.
2. Extract questions and answers.
3. Clean wording, dedupe overlaps, and assign categories/difficulty.
4. Generate multiple-choice options.
5. Update `data/questions.json` and `data/questions.js`.
6. Commit and push to GitHub Pages.

Important limitation: browser-side edits are temporary unless saved back into the repo. Without a backend/database, normal users cannot permanently edit the question bank from the website.

## Near-term improvements

### 1. Simple landing page

Keep it minimal:

- One headline.
- One sentence explaining the quiz.
- Primary button: `Start quiz`.
- Secondary button/link: `Question bank` or `Settings`.
- Tiny stats row: question count, random 30, practice mode.

No long product explanation on the landing page. The user should reach the quiz immediately.

### 2. Better quiz screen

- Keep the main question as the visual focus.
- Use a thin progress bar instead of a large progress panel.
- Show compact metadata: `Question 4/30 · 03:12 · Meal Service`.
- Keep answer choices large and mobile-friendly.
- Show immediate feedback in practice mode:
  - selected wrong answer = red
  - correct answer = green
  - short explanation below
- Add exam mode later:
  - no immediate answer reveal
  - full review only after submission

### 3. Question bank tools

- Add a separate question-bank/settings tab or modal.
- Show total questions by category.
- Validate missing fields, duplicate questions, and missing correct answers.
- Add import helpers for JSON/CSV.
- Keep admin/editing out of the main quiz flow.

## Upgrade paths for editable question pools

### Option A — Static JSON only

Best for the current sample.

Pros:

- Fastest.
- No hosting complexity.
- No login or database.
- Works on GitHub Pages.

Cons:

- Question edits require a repo update and redeploy.
- Browser edits are not permanent.

### Option B — Google Sheet as question bank

Best lightweight admin option.

Pros:

- Easy for non-technical editing.
- Can use a spreadsheet as the source of truth.
- No full custom admin panel needed.

Cons:

- Needs a publish/API integration.
- Must handle formatting and validation carefully.

### Option C — Airtable or Notion CMS

Best if the question bank needs a nicer content-management layer.

Pros:

- Easier filtering, tagging, and editing.
- Better than raw JSON for admins.
- Can support richer metadata.

Cons:

- External service dependency.
- API/auth setup required.

### Option D — Real database + admin panel

Best long-term production direction.

Pros:

- Proper login and roles.
- Permanent edits from the website.
- Saved attempts, analytics, leaderboards, and user progress.
- Cleaner import/export pipeline.

Cons:

- More build time.
- More maintenance.
- Requires backend hosting and database setup.

## Future features

- Practice mode and exam mode toggle.
- Category-specific quizzes.
- Weak-topic recommendations.
- Saved attempts and progress history.
- Admin CSV/JSON import.
- Question validation dashboard.
- Search/filter question bank.
- Leaderboards with anti-cheat controls.
- Shareable result links.
- Premium question packs or private question sets.
- User accounts and role-based admin access.

## Recommended next step

Keep the sample static for now, but structure the question bank cleanly so it can later move to Google Sheets, Airtable, Notion, or a real database without rewriting the quiz UI.
