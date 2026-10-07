# Tough Talk — Difficult Conversation Simulator

**Live demo:** https://tough-talk-frontend.onrender.com
(hosted on Render's free tier — spins down after inactivity, so the first
load can take up to ~50 seconds; it's quick after that)

A one-day prototype built for the atrain Innovation Hub application (Problem 03,
"Build what doesn't exist yet"). Lets a leader practise a hard conversation with
Sam, a scripted AI character whose trust/stress state lives in plain backend
code — the model only writes dialogue and tags behaviour, never touches state.

**Sam is fictional.** No real colleague is represented. **Nothing you type is
stored** — sessions live in server memory only, expire after 30 minutes, and
are never written to a log or database. This is a practice tool, not an
assessment or scoring instrument.

## What's built (v0.1)

- FastAPI backend: `/session`, `/turn`, `/end`, with the trust/stress/atmosphere/
  reveal rules implemented as pure, unit-tested functions (`backend/app/state.py`)
  — not the model.
- Anthropic API calls, server-side only: a small model (Haiku 4.5) tags each
  leader message with structured behaviour tags; a mid-size model (Sonnet 5)
  writes Sam's in-character reply and the debrief suggestions.
- Safety: an output check regenerates or falls back to a fixed line if Sam's
  reply ever mentions state, scores, or the system prompt.
- React + Vite frontend: start screen, chat with an atmosphere indicator
  (guarded/neutral/open — never raw numbers), debrief screen with a trust
  timeline, the three biggest-swing turns quoting your real words, whether
  Sam's hidden concern came out, and two plain-language suggestions.
- Per-IP rate limiting and a daily call budget switch.
- Golden-set tests for tagging accuracy, scripted good/bad conversation
  direction, and five role-break attack prompts, run in GitHub Actions on
  every push.

## Test results (from CI)

Latest run on `main`: **`backend-tests` — 49 passed, 0 failed.** **`frontend-build` — passed**
(npm install + vite build, no errors). Actions tab:
https://github.com/beawesome8/Tough-Talk---Difficult-Conversation-Simulator/actions

The three required test categories, broken out:

- **Tagging accuracy** — `test_tagging_accuracy_at_least_10_of_12`: PASSED,
  scoring 12/12 exact matches on the golden set (bar was >=10/12).
- **State direction** — `test_good_conversation_ends_with_high_trust_and_reveal`
  and `test_bad_conversation_ends_with_low_trust_and_no_reveal`: both PASSED.
- **Role break** — all 5 `test_attack_prompt_never_leaks_state[...]` parametrized
  cases: PASSED, zero state leaks across the 5 attack prompts.

The remaining 41 passed tests are the pure/unit/contract suite (state engine,
session store, safety checks, dialogue prompt builder, endpoint contract tests,
rate limiting) that don't need a live API call.

One pre-existing deprecation warning is emitted during the run, from
`starlette.testclient`'s `anyio.abc.BlockingPortal` alias — it comes from a
third-party dependency, not this project's code, and is harmless.

## Running locally

Backend:
```
cd backend
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # .venv/bin/pip on Linux/Mac
set ANTHROPIC_API_KEY=your-key-here             # export on Linux/Mac
.venv/Scripts/uvicorn app.main:app --reload --port 8000
```

Frontend:
```
cd frontend
npm install
npm run dev
```

## What's not built (out of scope for v0.1)

Voice, multiple scenarios, accounts, saved history, and scoring against a
formal competency framework. These are possible next steps, not gaps in a
promised feature set.

## Next steps if this is useful

A second scenario; adaptive scenarios that steer toward behaviours the leader
hasn't practised yet; connecting the debrief to a competency framework with
an assessor in the loop.
