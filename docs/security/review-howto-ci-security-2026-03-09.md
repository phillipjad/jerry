# Security Review: CI Pipeline How-To Guides

**Reviewer:** eng-security
**Date:** 2026-03-09
**Scope:** Three Diataxis how-to guides for CI pipeline security controls
**Files reviewed:**
- `docs/howto/update-sha-pinned-action.md`
- `docs/howto/add-ci-job.md`
- `docs/howto/add-github-actions-dependency.md`
- `docs/reference/ci-cd-pipeline-security.md` (reference baseline)

---

## L0 Executive Summary

| Severity | Count |
|----------|-------|
| High     | 2     |
| Medium   | 2     |
| Low      | 1     |
| Info     | 2     |

**Overall assessment:** Two findings require correction before these guides are published. Both High-severity findings will produce insecure configurations if followed literally. The CLCHK-001 pattern is correctly described in `add-ci-job.md`. SHA values in the examples cross-check correctly against `ci.yml` and the reference table. The trustworthiness checklist has one material gap.

**Top 3 risk areas:**

1. The `add-ci-job.md` guide instructs contributors to add new jobs without job-level `permissions:` blocks in a workflow that has only workflow-level permissions — producing jobs that silently inherit over-broad access.
2. The `add-github-actions-dependency.md` trustworthiness checklist does not require contributors to examine whether the action requests excessive permissions, which is the primary risk vector for a malicious or compromised third-party action.
3. The `ci-success` gate pattern in `add-ci-job.md` shows inline `${{ needs.*.result }}` expressions in a `run:` block — this does not expose user-controlled content, but the guide does not explain why those specific expressions are safe to inline, creating a risk that contributors apply the exception too broadly.

**Recommended immediate actions:**

1. Add a corrective note to `add-ci-job.md` Step 2 explaining that new jobs must declare job-level `permissions:` explicitly because the workflow's top-level block grants `pull-requests: write`, which new jobs should not inherit unless required.
2. Add an `actions/permissions` check to the trustworthiness checklist in `add-github-actions-dependency.md`.
3. Add a clarifying note in `add-ci-job.md` Step 8 explaining why `${{ needs.*.result }}` is safe to inline but `${{ github.event.* }}` is not.

---

## L1 Technical Findings

### FINDING-001 — High: `add-ci-job.md` Step 2 permission guidance is incomplete and will produce over-privileged jobs

**File:** `docs/howto/add-ci-job.md`, lines 28-38 (Step 2)
**CWE:** CWE-250 (Execution with Unnecessary Privileges)
**CVSS 3.1 Base Score:** 6.5 (AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N) — exploitable if a compromised action is added to the over-privileged job

**Evidence:**

`ci.yml` declares workflow-level permissions at lines 15-17:
```yaml
permissions:
  contents: read
  pull-requests: write
```

These are workflow-level defaults. Any job that does not declare its own `permissions:` block inherits this set. The guide's Step 2 example shows `contents: read` only, which is correct for read-only jobs. However, the guide does not warn contributors that:

- The workflow-level default includes `pull-requests: write`
- A new job that omits `permissions:` entirely — or that the contributor believes has only `contents: read` — actually inherits `pull-requests: write`
- The guide's prose ("Set `permissions` to the minimum the job requires") does not prevent a contributor from seeing the example and thinking "my job doesn't need anything special, I'll skip this step"

The guide's "Do not use floating tags" instruction is good, but if a contributor adds a job without a `permissions:` block because they forget Step 2, that job silently has `pull-requests: write` and the ability to post or modify PR comments. This is relevant whenever a job contains a compromised or malicious action step.

**Reproduction:** Add a new job to `ci.yml` following the guide, omit the `permissions:` block, push a branch with a pull request. The job runs with `contents: read` and `pull-requests: write` inherited from the workflow top level.

**Remediation:**

In Step 2, add an explicit warning that `permissions:` is mandatory (not optional) on every new job in this workflow, because the workflow-level default includes `pull-requests: write`. Change the guidance to:

```
Every new job MUST declare an explicit `permissions:` block.
The workflow's top-level permissions include `pull-requests: write`.
Any job that omits a `permissions:` block inherits this, even if the job
does not need to write to pull requests.
```

Additionally, show both the "read-only job" case and the "PR-comment job" case side by side so contributors know the two patterns, rather than only the read-only pattern.

---

### FINDING-002 — High: `add-github-actions-dependency.md` trustworthiness checklist omits permission scope review

**File:** `docs/howto/add-github-actions-dependency.md`, lines 18-26 (trustworthiness checklist)
**CWE:** CWE-250 (Execution with Unnecessary Privileges), CWE-829 (Inclusion of Functionality from Untrusted Control Sphere)
**CVSS 3.1 Base Score:** 7.1 (AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N) — a third-party action that requests `contents: write` or `id-token: write` can exfiltrate secrets or push commits

**Evidence:**

The checklist asks contributors to evaluate:
- Is the publisher GitHub-owned or widely recognised?
- Is the latest release recent (within 12 months)?
- Does it have stars and fork activity?
- Is there a `SECURITY.md`?
- Can `actions/github-script` substitute?

What it does not ask:
- What permissions does the action request at runtime?
- Does the action's source code call `GITHUB_TOKEN`-dependent APIs beyond what its documented purpose requires?

A third-party action that passes all five existing checklist items can still silently request `id-token: write` (for OIDC token exfiltration) or `contents: write` (to push commits or create tags). These permissions are granted at the job level, not by the action itself, so the checklist's current framing places all trust on reputation signals rather than on what the code actually does.

The checklist also uses "more than one" as the rejection threshold for the first four items. An action can fail two of the four reputation checks (e.g., no `SECURITY.md`, low star count) and still pass the gate. For a supply-chain security control, a single "no" on the publisher identity check alone should be a hard stop.

**Reproduction:** A contributor evaluates an action published by a small but recognised vendor with a recent release and a moderate star count — passes 3 of 4 reputation items, no `SECURITY.md`. The checklist allows addition. The action's `action.yml` uses `GITHUB_TOKEN` to read and push branches. No step in the guide surfaces this.

**Remediation:**

Add the following items to the trustworthiness checklist:

```
- Read the action's `action.yml`. What `GITHUB_TOKEN` scopes does it use?
  Is that scope necessary for the action's documented purpose?
- Does the action's source code contain outbound network calls beyond
  its documented functionality (telemetry, unexpected endpoints)?
```

Also tighten the rejection threshold: failing the publisher identity check (first item — not GitHub-owned or verified organisation) should be a hard stop, not merely one vote toward "more than one no."

---

### FINDING-003 — Medium: `add-ci-job.md` Step 8 uses inline `${{ needs.*.result }}` in a `run:` block without explaining the safe-use boundary

**File:** `docs/howto/add-ci-job.md`, lines 139-142 and 153-157 (Step 8)
**CWE:** CWE-77 (Command Injection) — risk is from contributor misapplication, not from the pattern itself
**CVSS 3.1 Base Score:** 4.0 (AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:N) — indirect; the current pattern is safe but the guidance creates a precedent that contributors may apply incorrectly

**Evidence:**

`add-ci-job.md` Step 6 (CLCHK-001) correctly teaches contributors to move `${{ github.event.* }}` values into env blocks to prevent shell injection. This is well described.

Step 8 then shows `${{ needs.lint.result }}` and `${{ needs.my-new-job.result }}` used directly inside a `run:` block:
```yaml
if [[ "${{ needs.lint.result }}" != "success" ]] || \
   [[ "${{ needs.my-new-job.result }}" != "success" ]]; then
```

This is consistent with how `ci.yml` works at lines 599-621. The `needs.*.result` value is a GitHub Actions-controlled enum (`success`, `failure`, `cancelled`, `skipped`) that cannot carry user-supplied content, so inline use is safe.

However, the guide teaches CLCHK-001 in Step 6 but then uses inline `${{ }}` expressions in Step 8 without explaining why these are safe while PR title values are not. A contributor who reads Step 8 first, or who infers the rule from Step 8's example, may conclude that inlining `${{ }}` is acceptable in general and violate CLCHK-001 by inlining `${{ github.event.pull_request.title }}` in their own `run:` scripts.

The actual `ci.yml` has the same pattern (lines 599-621 use inline `needs.*.result` without env blocks), which is correct. The documentation does not contradict the implementation — but it creates a gap that can be exploited via misunderstanding.

**Remediation:**

In Step 8, add a brief parenthetical that explains the safe-use boundary:

```
Note: `needs.*.result` values are safe to inline because they are
GitHub Actions-controlled enums (success/failure/cancelled/skipped)
that cannot carry user-supplied content. Apply the env-block rule
(Step 6) to any expression that can contain user-controlled strings,
such as PR titles, branch names, or commit messages.
```

---

### FINDING-004 — Medium: `update-sha-pinned-action.md` Step 3 does not warn about lightweight tags

**File:** `docs/howto/update-sha-pinned-action.md`, lines 55-71 (Step 3)
**CWE:** CWE-494 (Download of Code Without Integrity Check) — partial; the step resolves the right SHA for annotated tags but does not address the lightweight tag case
**CVSS 3.1 Base Score:** 4.2 (AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:L/A:N)

**Evidence:**

The guide correctly describes the annotated tag dereference problem and shows the `^{}` technique for resolving annotated tags to their commit SHA. It then states: "Use the SHA from the `^{}` line (the dereferenced commit SHA)."

This is correct for annotated tags. But for lightweight tags (which many action maintainers use), `git ls-remote` returns exactly one line with no `^{}` suffix — the one SHA returned is the commit SHA directly. The troubleshooting section at line 134-135 addresses this correctly when two lines appear, but does not address what to do when only one line appears.

A contributor who has only ever worked with lightweight-tagged actions may follow the instruction "use the `^{}` line" and fail to find such a line, becoming confused and potentially using an incorrect SHA or abandoning the process.

This is not a security vulnerability in itself — both paths (annotated and lightweight) ultimately resolve to a commit SHA — but the incomplete description could cause a contributor to distrust a correct single-line result and attempt workarounds.

**Remediation:**

Update Step 3 to document both cases:

```
For lightweight tags, `git ls-remote` returns exactly one line. That SHA
is the commit SHA — use it directly. No `^{}` dereference is needed.

For annotated tags, `git ls-remote` returns two lines (one for the tag
object, one with `^{}`). Use the SHA from the `^{}` line.
```

The troubleshooting section already handles the "two lines" case correctly and does not need to change.

---

### FINDING-005 — Low: `add-ci-job.md` uv version example (`0.10.9`) is inconsistent with what the step says to check

**File:** `docs/howto/add-ci-job.md`, lines 53-63 (Step 4)
**CWE:** N/A (documentation accuracy issue, not a security vulnerability pattern)
**CVSS 3.1 Base Score:** 2.0 (informational)

**Evidence:**

Step 4 says: "install `uv` with `version: \"0.10.9\"` pinned." The version string `0.10.9` is hardcoded in the example and matches the current value in `ci.yml` (line 129, 172, 195, 220, etc.) and the reference doc. This is correct today.

The guide does not tell contributors where to find the current pinned `uv` version to use when adding a new job in the future. The reference doc's UV Binary Pinning section documents the value (`0.10.9`) and the authoritative source, but the how-to guide does not link to it. A contributor adding a new job months from now may copy the stale `0.10.9` from the guide rather than reading the current value from the reference doc.

This is low severity because the version is intentionally pinned (drift is caught by Dependabot or the frozen lockfile), but the guide should direct contributors to the canonical source.

**Remediation:**

In Step 4, add: "Check the current pinned version in the [UV Binary Pinning section](../reference/ci-cd-pipeline-security.md#uv-binary-pinning) rather than copying the example value, which may be stale."

---

## L1 SHA Cross-Reference Verification

Cross-checked all SHA values in the how-to guides against `ci.yml` and `docs/reference/ci-cd-pipeline-security.md`.

| SHA reference | Location in guide | SHA in ci.yml | Match |
|---|---|---|---|
| `actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8` | `add-ci-job.md` Step 3 | Line 32 | PASS |
| `astral-sh/setup-uv@d4b2f3b6ecc6e67c4457f6d3e41ec42d3d0fcb86` | `add-ci-job.md` Step 4 | Line 127 | PASS |
| `softprops/action-gh-release@da05d552573ad5aba039eaac05058a918a7bf631` | `add-github-actions-dependency.md` Step 3 | Not in ci.yml (used in release.yml) | Reference doc confirms: v2.2.2 |
| `actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8 # v5.0.0` | `update-sha-pinned-action.md` Step 4 | Line 32 | PASS |

All SHA values in the examples match the reference doc's SHA-to-version mapping table. No stale or fabricated SHAs detected.

---

## L1 CLCHK-001 Pattern Verification

Reviewed the CLCHK-001 description in `add-ci-job.md` Step 6 against the actual implementation in `ci.yml` lines 544-584.

**Guide description (Step 6):** "declare it in an `env:` block on the step. Never inline `${{ github.event.* }}` directly inside a `run:` script."

**Actual `ci.yml` implementation (lines 549-552):**
```yaml
env:
  PR_TITLE: ${{ github.event.pull_request.title }}
  PR_ACTOR: ${{ github.actor }}
  BASE_SHA: ${{ github.event.pull_request.base.sha }}
```

**Assessment:** The description is accurate and the example in the guide matches the canonical pattern in `ci.yml`. The `github.actor` value is included in the env block in both the guide and `ci.yml`, which is correct — `github.actor` can carry usernames containing characters that would cause problems in some shell contexts. The guide's scope note ("GitHub context values that are safe constants (e.g., `github.event_name`, `github.ref`, `github.sha`) may be inlined only when they cannot carry user-controlled content") is technically accurate, though see FINDING-003 for the gap this creates with the Step 8 pattern.

**No vulnerability found in the CLCHK-001 description itself.**

---

## L1 Permission Scoping Verification

**Workflow-level permissions in `ci.yml`:**
```yaml
permissions:
  contents: read
  pull-requests: write
```

**Job-level permissions declared:** Zero jobs in `ci.yml` declare an explicit `permissions:` block. All jobs inherit the workflow-level grant.

**Guide instruction (Step 2 of `add-ci-job.md`):** "Set `permissions` to the minimum the job requires."

**Assessment:** The guide's instruction is correct in principle. However, the existing `ci.yml` jobs do not follow it — none declare job-level permissions. The guide is teaching a practice that is not enforced by example in the actual workflow file. A contributor looking at `ci.yml` for guidance will find no job-level `permissions:` blocks and may follow the existing pattern (omit them) rather than the guide's instruction.

This is the root cause of FINDING-001. The guide's Step 2 text is sound, but it lacks the warning that the workflow-level grant includes `pull-requests: write`, which makes explicit job-level declarations security-relevant for any new job that does not need PR write access.

---

## L2 Strategic Implications

**Systemic pattern:** Both High-severity findings share a root cause: the guides teach correct security controls but do not adequately explain the threat model that motivates them. Step 2 says "minimum required" without explaining what the default is. The trustworthiness checklist asks about reputation without asking about capability. Contributors who follow the instructions correctly get the right behavior, but contributors who skip a step or apply partial reasoning get an insecure configuration.

**Architectural observation:** The `ci.yml` workflow has workflow-level `permissions:` that include `pull-requests: write`. This grant exists because the `coverage-report` job (PR-only) posts coverage comments. A more robust architecture would remove the workflow-level `pull-requests: write` grant and add it only to `coverage-report` at the job level. This would make the default for new jobs safe-by-default — a job without a `permissions:` block would inherit only `contents: read`. Fixing this architectural issue would eliminate the precondition for FINDING-001 entirely.

**Documentation quality note:** The guides are well structured. The CLCHK-001 description is clear and matches the implementation. The SHA pinning mechanics are accurate. The two High findings are gaps in threat-model framing, not errors in the technical content. Closing them requires adding approximately 3-4 sentences to each affected step.

---

## Verification Checklist

| Check | Result |
|-------|--------|
| SHA values in examples match ci.yml | PASS |
| SHA values in examples match reference doc | PASS |
| CLCHK-001 env-block pattern correctly described | PASS |
| No inline `${{ github.event.* }}` in run: blocks in guides | PASS |
| Permission scoping instructions technically correct | PASS (with gap — see FINDING-001) |
| Trustworthiness checklist covers key vectors | PARTIAL (see FINDING-002) |
| uv version consistent with reference doc | PASS (with staleness risk — see FINDING-005) |
| Annotated tag dereference correctly described | PASS (with lightweight tag gap — see FINDING-004) |
