<p align="center"><b>English</b> · <a href="README.es.md">Español</a></p>

<p align="center">
  <img src="assets/clipboard-soyjak.jpg" alt="Clipboard Skills — the agent that checks the list before saying done" width="640">
</p>

<h1 align="center">clipboard-skills</h1>

<p align="center"><b>Your AI agent says "done" without running a single test.<br>Clipboard Skills makes it check the list first.</b></p>

<p align="center">
  <a href="https://github.com/angelgabrieljacintohuayllasco/clipboard-skills/actions"><img src="https://github.com/angelgabrieljacintohuayllasco/clipboard-skills/actions/workflows/validate.yml/badge.svg" alt="validate skills"></a>
  <img src="https://img.shields.io/badge/skills-36-black" alt="36 skills">
  <img src="https://img.shields.io/badge/Claude_Code-%E2%9C%93-black" alt="Claude Code">
  <img src="https://img.shields.io/badge/Codex_%C2%B7_OpenCode_%C2%B7_Cursor-%E2%9C%93-black" alt="Codex OpenCode Cursor">
  <img src="https://img.shields.io/badge/license-MIT-black" alt="MIT">
</p>

---

36 skills (`SKILL.md`) that make an AI coding agent work **like a professional engineer**, not like a code generator that says "done" without verifying anything. They work in Claude Code and in any agent that supports the [Agent Skills](https://agentskills.io) format (Codex, OpenCode, Cursor…).

```bash
git clone https://github.com/angelgabrieljacintohuayllasco/clipboard-skills.git && cd clipboard-skills && ./install.sh
```

> The skill bodies are written in Spanish. Every `description` carries English trigger phrases, so they fire in either language, and the agent answers in whatever language you use.

## The clipboard guy

Works the same for an engineer with twenty years of experience and for someone who can only describe what they want: the agent detects the register, asks the questions a developer would ask a client, **recommends the constraints and quality metrics**, builds in verified slices and **blocks delivery when the numbers don't add up**. That's the clipboard guy: he doesn't sign off without going through the list.

Before / after, with `quality-gate` installed:

| Without clipboard | With clipboard |
|---|---|
| "Done, login implemented ✅" | `GATE: BLOCKED — new-code coverage 71% (≥80%), complexity 14 at src/auth/session.ts:88 (≤10)` |
| "Tests pass" (ran nothing) | Real command output pasted. No output, it didn't run. |
| Installs `requests-oauth2-helper` (doesn't exist) | Verifies the package exists before installing (anti-slopsquatting) |
| Silently fills the gap in the spec | Asks, or writes the assumption down |

## The idea

Three practices that hold AI-assisted development together today:

1. **Constraints before review.** Robert C. Martin stopped reading his agents' code: instead he surrounds them with extreme constraints and measures test coverage, dependency structure, cyclomatic complexity, module size and mutation score. He infers quality from those metrics. This pack turns that into one file per project (`constitution.md`) and one command (`gate`) that exits non-zero.
2. **The machine doesn't see everything.** Grady Booch's objection is also true: metrics don't catch an inverted permission check or a destructive migration. So there is a second layer: a short list of zones where human review stays mandatory (`diff-review`).
3. **Spec before code.** The flow that replaced "vibe coding": clarify intent, mark the gaps instead of filling them, plan under constraints, implement, verify against the spec (`intake` → `constitution` → `architecture` → `feature` → `quality-gate`).

And one fact that orders the priorities: according to DORA's AI report, **AI amplifies the system you already have**. With a weak pipeline, what accelerates is technical debt.

## How it's used

```
REQUEST
  ├─ vague / new project ───────────► intake ──► constitution ──► architecture ──► feature
  ├─ feature in a live repo ────────► feature
  ├─ something broken ──────────────► triage ──► fixer / ui-bug / agent-debug / refactor / rebuild
  └─ finished ──────────────────────► quality-gate ──► deploy ──► project-memory
```

Real conversation with `intake` active:

> **User:** build me a WhatsApp CRM
> **Agent:** Seven questions, then I'll propose the quality rules. (1) Official API channel or unofficial? — I recommend official: unofficial is free but can cost you the phone number. (2) How many messages a day?… (7) What's the worst thing that happens if it fails at 3 AM?
> **Agent:** Recommended profile **P2**: ≥80% coverage on new code, complexity ≤10, zero secrets in the repo, conversation and duplicate tests, gate in one command. Adds ~20% time, removes most of the risk. Go?

## Install

```bash
git clone https://github.com/angelgabrieljacintohuayllasco/clipboard-skills.git
cd clipboard-skills
./install.sh                                        # all, into ~/.claude/skills
./install.sh ~/.claude/skills intake constitution quality-gate   # only some
```

Windows: `.\install.ps1` or `.\install.ps1 -Skills intake,constitution,quality-gate`. Other agent: pass its skills directory as the destination, or copy the folders under `skills/` by hand.

Each folder is independent: take only `intake`, `constitution` and `quality-gate` and you already have 80% of the value.

## The skills

### Process core
| Skill | What for |
|---|---|
| `dev-router` | Which skill applies and in what order; adapts the register to who is asking |
| `intake` | The discovery interview: spec, acceptance criteria, assumptions, rigor profile |
| `constitution` | Verifiable constraints and thresholds + wiring of the gates |
| `architecture` | Decisions that are expensive to reverse, with ADRs and dependency boundaries |
| `feature` | Implement a vertical slice under the constitution |
| `test-strategy` | What to test, at which level, and what NOT to test |
| `quality-gate` | Run the metrics and **block** delivery if they fail |
| `code-standard` | How code is written: names, functions, KISS, YAGNI, DRY, smell catalog |
| `diff-review` | Risk-based human review, where metrics are blind |
| `tech-debt` | Measure the debt, make the interest visible, payment plan |
| `project-memory` | Project memory inside the repo (`AGENTS.md` + `docs/project/`) |
| `agentic-coding` | The agent's method: explore → plan → execute → verify with evidence → adversarial review in fresh context |

### Cross-cutting
| Skill | What for |
|---|---|
| `app-security` | Defensive baseline (OWASP Top 10:2025) per application type |
| `ai-security` | Anything that uses AI or agents: OWASP LLM Top 10 + Agentic, prompt injection, excessive agency, slopsquatting |
| `data-layer` | Modeling, safe migrations, integrity, tested backups |
| `observability` | The system warns before the client does |
| `performance` | Measure, fix what dominates, measure again |
| `deploy` | Publish in a way that can be undone |

### Domains
| Skill | What for |
|---|---|
| `web-app` | Websites and web apps: states, forms, accessibility, responsive, SEO |
| `api-backend` | Contracts, idempotency, retries, webhooks, background jobs |
| `bot-dev` | Messaging bots: channel, state, resilience, handoff to a human |
| `automation` | Scripts, cron, scraping, ETL: idempotent, resumable and loud when failing |
| `desktop-app` | Electron/Tauri/native: secure bridge, packaging, signing, updates |
| `mobile-app` | Android/iOS/APK: permissions, offline, signing, store requirements |

### Diagnosis and repair
| Skill | What for |
|---|---|
| `triage` | Patch, restructure, debug the agent or rebuild? Read-only |
| `fixer` | Reproduce, root cause, surgical fix and regression test |
| `ui-bug` | Visual and interactive bugs: diagnosed by looking |
| `agent-debug` | AI bots that decide wrong: state, prompt, classifiers, tools, data |
| `refactor` | Restructure with behavior frozen |
| `rebuild` | Rebuild while rescuing business rules and old bugs |
| `env-doctor` | Why it won't start: every layer before concluding |

### Support
| Skill | What for |
|---|---|
| `consulta` | Answer and document without touching code |
| `valida-idea` | Honest verdict before building, with a kill criterion |
| `batch` | One repetitive change across many files, verified |
| `readme-generator` | A real README, no invented commands |
| `changelog-generator` | Commits → consequences for whoever uses it |

## Rigor profiles

| | P1 Prototype | P2 Standard | P3 Critical |
|---|---|---|---|
| When | demo, personal use | product with users | money, personal data, irreversible |
| Coverage (new code) | — | ≥80% | ≥90% core |
| Mutation | — | ≥60% | ≥80% |
| Complexity per function | ≤15 | ≤10 | ≤10 |
| File | ≤600 LOC | ≤400 LOC | ≤300 LOC |
| Dependency cycles | avoid | 0 | 0 |
| Human review | no | sensitive zones | whole domain |
| Rollback | — | documented | rehearsed |

The thresholds come from public references: SonarQube's default quality profile (80% coverage on new code, ≤3% duplication, cognitive complexity ≤15), McCabe's classic limit (cyclomatic complexity ≤10) and common mutation-testing practice (75-85% is solid). They are adjusted per project **with a written reason**, and they never go down: ratchet.

## File conventions

```
AGENTS.md                      # operating context for agents and people
docs/project/spec.md           # what is being built and acceptance criteria
docs/project/constitution.md   # constraints and thresholds, with their command
docs/project/architecture.md   # map + decisions/ADR-000X.md
docs/project/state.md          # status, pending items, red zones
docs/project/bugs.md           # symptom → root cause → fix → prevention
docs/project/gotchas.md        # non-obvious traps
docs/project/runbook.md        # deploy, roll back, restore
```

Templates ready in `skills/constitution/templates/`. If you keep a notes vault (Obsidian or other), `project-memory` explains how to mirror these files per project without duplicating the source of truth.

## Principles that run through the whole pack

- No pasted command output, it didn't run. "Tests pass" is not evidence.
- Every gap is asked about or declared as an assumption. Never filled silently.
- Every question comes with a default recommendation: asking without recommending is offloading the work.
- One change, one purpose. No mixing fix with refactor with feature.
- Thresholds only go up.
- What isn't documented gets paid for again.

## Validate

```bash
python scripts/validate_skills.py
```

Checks frontmatter (`name`, `description`), name = folder, length limits and that there are no personal paths or emails. Runs in CI on every push.

## Sibling packs

- [`agent-modes`](https://github.com/angelgabrieljacintohuayllasco/agent-modes) — work modes for the agent: `extremly` (extreme problem-solving), `maraton` (unattended execution with on-disk state), `investigacion` (source-graded research), `ver-video`, `mcp-master`, `obsidian-memory`.
- [`marketing-skills`](https://github.com/angelgabrieljacintohuayllasco/marketing-skills) — Meta Ads and TikTok Ads with hard money guardrails.

## License

MIT. The clipboard guy is a soyjak: internet public domain, as it should be.

## Sources

- Robert C. Martin on not reviewing his agents' code and measuring instead — [tweet](https://x.com/unclebobmartin/status/2044114698451476492), [coverage of the debate](https://startupfortune.com/uncle-bob-martin-says-he-no-longer-reads-ai-generated-code-and-the-developer-world-is-split/)
- GitHub Spec Kit — constitution → specify → clarify → plan → tasks → implement flow — [repo](https://github.com/github/spec-kit)
- SonarQube, default quality profile and metrics — [documentation](https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates)
- Mutation testing, practical thresholds — [Stryker guide](https://qaskills.sh/blog/mutation-testing-stryker-guide-2026)
- DORA, ROI of AI-assisted development — [report](https://dora.dev/ai/roi/report/)
- OWASP Top 10:2025 — [list](https://owasp.org/Top10/2025/)
- AGENTS.md as repo context for agents — [specification](https://agentsstandard.com/)
