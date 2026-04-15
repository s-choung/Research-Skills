---
description: Single entry point for the paper-team. Parses natural language intent and dispatches to the right subagent (plan / ref / draft / critic / humanize). Use when you know what you want but do not want to pick the exact sub-command.
argument-hint: "<what you want in natural language>"
allowed-tools: Read, Glob, Grep, Task
---

## Context

- Current working directory: !`pwd`
- Manuscript: !`ls -1 Manuscript_*.docx 2>/dev/null | head -1`
- SI: !`ls -1 Supporting_Information*.docx 2>/dev/null | head -1`
- Project context: !`test -f .claude/paper-team/project-context.md && echo yes || echo no`
- Global STYLE_PROFILE: !`test -f ~/.claude/paper-team/STYLE_PROFILE.md && echo yes || echo no`

## Task

User invoked: `/paper $ARGUMENTS`

Your job is to be a thin router. Parse `$ARGUMENTS` as a natural-language intent (may be Korean, English, or mixed), decide which sub-action it maps to, and dispatch the corresponding subagent via the Task tool. You do NOT do the work yourself.

### Intent -> action decision tree

Match `$ARGUMENTS` against the categories below. Use keyword + semantic match. If ambiguous, ask ONE clarifying question and STOP.

**1. PLAN** - user wants a multi-step plan for a paper goal
- Korean keywords: 계획, 플랜, 뭐부터, 어디서부터, 순서, 로드맵, 어떻게 시작
- English: plan, roadmap, how do I, where to start, what first, strategy
- Action: load `~/.claude/skills/writing-plans/SKILL.md` and produce a 3-7 step plan as in `/paper-plan` command logic. No subagent dispatch.
- Return format: numbered plan + first command to run.

**2. REF** - user wants citation candidates
- Korean: 인용, 레퍼런스, ref, 논문 찾, 참고문헌, 관련 논문, prior work
- English: reference, citation, cite, find papers, prior art, related work
- Action: dispatch `paper-ref-hunter` subagent with `query = $ARGUMENTS` (minus the routing keywords).

**3. DRAFT** - user wants new text for a section or paragraph
- Korean: 써줘, 초안, 드래프트, 작성, 추가, 문단, 섹션, intro 써, results 써, discussion 써
- English: draft, write, add paragraph, new section, new text, first pass
- Action: dispatch `paper-section-drafter` subagent. Parse target section from intent (intro / methods / results / discussion / outlook). If unclear, ask "어떤 섹션?" and STOP.

**4. CRITIC** - user wants rigor / claim-evidence review
- Korean: 검증, 크리틱, 체크, 오류, 논리, 과장, 근거, 리뷰어
- English: critique, review, check, rigor, verify, logic, claim check
- Action: dispatch `paper-scientific-critic` subagent with the target text or section.

**5. HUMANIZE** - user wants style cleanup, voice alignment, final polish
- Korean: 다듬, 휴머나이즈, AI 티, 스타일, 문체, 정리, 깔끔하게, 다시 써
- English: humanize, polish, clean up, style, voice, AI-like, rewrite style
- Action: dispatch `paper-style-enforcer` subagent in `fix` mode with the target paragraph.

### Execution rules

1. If `$ARGUMENTS` is empty, show a menu of the 5 actions + examples and STOP.
2. If `$ARGUMENTS` matches multiple categories with similar confidence, ask ONE short clarifying question:
   - Example: "이거 draft 새로 쓰라는 거야 아니면 기존 문단 다듬으라는 거야?"
3. If `$ARGUMENTS` matches one category clearly, dispatch the subagent (or run plan logic) immediately. Do NOT re-ask for confirmation.
4. For DRAFT / CRITIC / HUMANIZE actions that need a target paragraph or section:
   - If user supplied the text inline in `$ARGUMENTS`, pass it through.
   - If user referenced by location (`para:12`, `results exsolution`), resolve by reading the manuscript.
   - If unclear, ask ONE question for the target.
5. Always announce the routing decision in one line before dispatching, e.g.:
   - `Routing: HUMANIZE -> paper-style-enforcer`
6. After the subagent returns, relay the result and append "next suggested" line based on the action just completed:
   - plan -> first `/paper-*` command from the plan
   - ref -> `/paper-draft` with the picked refs
   - draft -> `/paper-critic para:drafted`
   - critic -> `/paper-draft revise:blocker1` OR `/paper-humanize` if no blockers
   - humanize -> user review

### Fallback

If `$ARGUMENTS` does not match any category (e.g. user just says `/paper 뭐해야해`), treat as PLAN intent with the user's words as the goal.

### Hard rules

- You are a ROUTER. Do not draft, critique, or humanize text yourself. Always dispatch.
- Exception: PLAN action is handled in main context (uses writing-plans skill), no subagent needed.
- Never dispatch more than one subagent per `/paper` invocation. Chains are user-controlled via subsequent `/paper` or `/paper-*` calls.
- If project-context.md is missing and the action would benefit from topic context, mention it once in the output but do not block.
