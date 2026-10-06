# Tough Talk — Difficult Conversation Simulator — Design Spec

Status: approved for implementation
Date: 2026-10-06
Owner: Aman Benjamin Emmanuel
Purpose: working prototype for the atrain Innovation Hub application (Problem 03, "Build what doesn't exist yet")

This spec is the owner-authored build specification (verbatim content below, sections 1-12), plus an implementation addendum covering decisions made during kickoff (repo, hosting, secrets, phase/commit plan).

---

## Implementation Addendum (decided 2026-10-06)

- **Repo**: https://github.com/beawesome8/Tough-Talk---Difficult-Conversation-Simulator (MIT licensed, one commit). Cloned to local working copy; all phases are commits pushed to `main` directly (solo prototype, no PR review loop needed) unless the user asks for branches/PRs later.
- **GitHub auth**: existing Git Credential Manager on this machine; no PAT handled by the agent.
- **Anthropic key**: user sets `ANTHROPIC_API_KEY` themselves (local `.env`, GitHub Actions secret, Render env var). Agent never sees or stores the key. Golden-set tests that call the real API only run where the key is present; CI tagging/role-break tests run against the real API using a repo secret the user will add — if that secret isn't present, those specific tests are skipped rather than failing the build, so a fork/clone without the secret still gets a green pipeline on everything else (unit tests for the state engine run unconditionally).
- **Hosting**: Render — backend as a Web Service (Docker or native Python), frontend as a Static Site. `render.yaml` blueprint provided. Actual provisioning/connecting the GitHub repo to Render happens in Phase 5 with the user present (needs their Render login).
- **Delivery style**: five phases matching spec section 10's block plan, each ending in its own commit(s) pushed to `main` so the history visibly shows incremental, non-one-shot progress for recruiters reviewing the repo.
- **Scope confirmed unchanged from spec**: single scenario (Sam), no auth/accounts, in-memory session store, 12-turn hard cap, three tests (tagging accuracy, state direction, role-break) in CI.

Phase → commit mapping:

| Phase | Matches spec block | Deliverable | Push |
|---|---|---|---|
| 1 | Block 1 | FastAPI skeleton, state engine (pure functions), unit tests for the behaviour table | commit + push |
| 2 | Block 2 | Tagging call (structured output via Anthropic tool-use), golden set (12 messages), tagging accuracy test | commit + push |
| 3 | Block 3 | Dialogue call, reveal rule, output role-break check + regenerate/fallback, role-break test, state-direction test | commit + push |
| 4 | Block 4 | React/Vite frontend: start screen, chat + atmosphere indicator, debrief screen (timeline chart, top-3 turns, concern reveal, suggestions) | commit + push |
| 5 | Block 5 | Dockerfile/render.yaml, rate limiting, daily budget switch, GitHub Actions CI workflow, final README with real CI results, Render deploy | commit + push |

---

## 1. Summary

Tough Talk lets a leader practise a hard conversation with an AI team member. The team member has a hidden state (trust, stress and an unspoken concern) that changes with how the leader behaves. At the end, a debrief shows the moments where trust moved, with the leader's own words as evidence.

The design rule: **the state lives in plain code, the model only writes dialogue and tags behaviour.** This keeps the character consistent, makes behaviour testable, and keeps the model from being talked out of its role.

## 2. Users and goal

- User: a manager or leader practising a feedback conversation.
- Goal: in 10 minutes, feel what changes when I ask, listen, blame or dismiss, and see it afterwards in evidence.
- Secondary viewer: the atrain team, judging craft, interaction design and judgement.

## 3. Scenario (fictional, fixed for v0.1)

Sam is a strong engineer who missed two deadlines. After a colleague left, Sam quietly took on that person's work.
- Hidden concern: Sam feels the extra work goes unnoticed and is thinking about leaving.
- The concern is only revealed when trust is above the threshold (see 5).
- Sam never states the hidden state numbers.

## 4. User experience

1. Start screen: one paragraph of context, a "Start conversation" button, and a clear note that Sam is fictional and nothing is stored.
2. Conversation screen: chat on the left, a calm "Atmosphere" indicator on the right (three states: guarded, neutral, open). Do not show raw numbers during the conversation.
3. The conversation ends when the leader clicks "End conversation", or after 12 leader turns.
4. Debrief screen:
   - Timeline of trust across turns (simple line chart).
   - The 3 turns with the biggest change, each with the leader's quote and the behaviour tag.
   - Whether Sam's hidden concern came out, and what opened it.
   - Two suggestions, written in plain language.
5. Mobile-friendly. Keyboard: Enter sends. Loading state under 3 seconds per turn.

## 5. Behaviour and state model

State (server side, per session): `trust` 0-100 (start 40), `stress` 0-100 (start 60), `concern_revealed` boolean.

Each leader message is tagged by the model with zero or more behaviours (structured JSON):

| Behaviour tag | Trust | Stress |
|---|---|---|
| acknowledges_feelings | +8 | -6 |
| asks_open_question | +6 | -3 |
| names_specific_contribution | +7 | -4 |
| offers_concrete_support | +8 | -8 |
| blames_or_generalises | -10 | +10 |
| dismisses_or_interrupts | -12 | +8 |
| adds_pressure_without_support | -6 | +12 |

Rules (plain code, no model):
- Clamp both values to 0-100.
- Atmosphere: guarded if trust < 40, neutral if 40-64, open if 65 or more.
- Sam reveals the hidden concern once, when trust is 65 or more and the leader asked an open question or acknowledged feelings in that turn.
- If stress is above 80, Sam gives short, closed answers.

Dialogue call: the model receives the scenario, the current atmosphere label (never the numbers or the hidden concern unless the reveal rule fires), and the last 6 messages. It returns Sam's reply only, in 1-3 sentences.

## 4b. Safety against role break

- The user message is data, never instructions. Any attempt to change the role ("ignore your instructions", "tell me your trust score") gets an in-character reply, because the state is not in the prompt.
- Output check: if Sam's reply mentions "trust score", "system", "prompt" or a number from the state, regenerate once, then fall back to a neutral in-character line.

## 6. Architecture

- Frontend: React with Vite, single page, no routing library.
- Backend: FastAPI. Endpoints: `POST /session`, `POST /turn`, `POST /end`.
- Model calls: Anthropic API, server side only (key never in the browser). Use a small model for tagging and a mid-size model for dialogue and debrief.
- Storage: in memory only, session expires after 30 minutes. No logs of message content.
- Cost control: hard cap of 12 turns per session, a per-IP rate limit, and a global daily budget switch that shows a polite "demo is resting" page when exceeded.
- Hosting: any simple host with a public URL (for example Render or Fly.io). Environment variable for the API key.

## 7. Quality and evaluation (the part that shows judgement)

A golden set of 12 scripted leader messages, each with the expected behaviour tags and the expected direction of trust.

- Test 1, tagging accuracy: tags match the expected set on at least 10 of 12 messages.
- Test 2, state direction: a scripted good conversation ends with trust above 65 and the concern revealed; a scripted bad conversation ends with trust below 30 and no reveal.
- Test 3, role break: 5 attack prompts must never leak state or break character.
- Run the tests on every push with GitHub Actions. Report the result in this README after the first run.

Do not claim any metric in this README until the tests have run and the numbers are real.

## 8. Acceptance criteria

- A stranger can start and finish a conversation in under 10 minutes without instructions.
- All 3 tests pass in CI.
- The debrief quotes the leader's real words, never invented ones.
- A reload mid-conversation loses the session without crashing.
- The README states clearly what is fictional, what is stored (nothing) and what is not built.

## 9. Out of scope for v0.1

Voice, multiple scenarios, accounts, saved history, scoring against a formal competency framework. Mention these as next steps only.

## 10. Build plan (about one day with Claude Code)

| Block | Work |
|---|---|
| 1 | Backend skeleton, state engine in code, unit tests for the table in section 5 |
| 2 | Tagging call with structured output, golden set, tagging test |
| 3 | Dialogue call, reveal rule, role-break checks and tests |
| 4 | Frontend: chat, atmosphere indicator, debrief screen |
| 5 | Deploy, rate limit, daily budget switch, CI, final README with real test results |

## 11. Risks

- Sam drifts out of character: mitigated by keeping state in code and the output check.
- The model tags behaviour inconsistently: mitigated by the golden set and by a small, clear tag list.
- Cost spikes from public traffic: mitigated by the caps in section 6.
- Fairness and psychology claims: the tool is for practice, not for scoring people. State this on the start screen.

## 12. Next steps if the team likes it

Add a second scenario, add adaptive scenarios that steer towards the behaviour the leader has not yet practised, and connect the debrief to a competency framework with an assessor in the loop.
