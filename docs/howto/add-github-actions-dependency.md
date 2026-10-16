# How to Add a New GitHub Actions Dependency

> Add a SHA-pinned third-party GitHub Action to the Jerry CI pipeline and verify Dependabot will maintain it.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Before You Begin](#before-you-begin) | Prerequisites |
| [Steps](#steps) | Seven-step addition procedure |
| [Verification](#verification) | Confirm the action resolved correctly |
| [Troubleshooting](#troubleshooting) | Common failure modes |
| [Related](#related) | Reference and explanation docs |

---

## Before You Begin

You need:
- Write access to the Jerry repository
- The name of the action you want to add (e.g., `owner/action-name`)
- The desired version tag (e.g., `v2.1.0`)

## Steps

### 1. Assess the action's trustworthiness

Before touching any workflow file, run through this checklist mentally:

**Trustworthiness checklist:**

- Is the action published by `actions/*` (GitHub-owned) or a verified, widely-recognised organisation? If no, **stop** — unverified publishers require explicit team approval before proceeding.
- Open the action's `action.yml` and review what permissions and scopes it requests. Does it need `contents: write`, `id-token: write`, or make outbound network calls beyond its stated purpose? If yes, do not add it without a security review.
- Does the latest release fall within the past 12 months?
- Does the repository have a meaningful star count and active fork activity?
- Is there a `SECURITY.md` or a published security policy?
- Can `actions/github-script` cover the same need without adding a third-party dependency?

If the publisher is unverified, or if the `action.yml` requests permissions beyond its stated purpose, do not add the action. For the remaining items, if you answer "no" to more than one, reconsider the dependency.

### 2. Find the full commit SHA for the target version

1. Navigate to `https://github.com/{owner}/{action-name}/releases`.
2. Locate the release matching your target version tag (e.g., `v2.1.0`).
3. Click the tag name link to open the tag's page.
4. Copy the full 40-character commit SHA displayed on that page.

Do not use floating tags such as `@v2` or `@v2.1.0` in the workflow file. See [About CI/CD Supply Chain Security](../explanation/ci-cd-supply-chain-security.md) for background.

If you need to retrieve the SHA from the command line instead:

```bash
git ls-remote https://github.com/{owner}/{action-name}.git refs/tags/{version}
```

If only one line is returned, use the SHA in the first column. If two lines are returned (annotated tag), use the SHA from the line ending in `^{}` — that is the dereferenced commit SHA.

### 3. Add the action to the workflow file with SHA pin and version comment

In the relevant `.github/workflows/*.yml` file, add your step using this format:

```yaml
- uses: owner/action-name@FULL40CHARSHA # vX.Y.Z
```

Concrete example:

```yaml
- uses: softprops/action-gh-release@da05d552573ad5aba039eaac05058a918a7bf631 # v2.2.2
```

The `# vX.Y.Z` comment is required. Dependabot reads it to generate human-readable PR descriptions when it opens update PRs.

If the action appears in more than one workflow file, add the SHA-pinned reference to each file. Keep the version comment identical across all occurrences.

### 4. Verify Dependabot coverage

No changes to `.github/dependabot.yml` are needed.

Open `.github/dependabot.yml` and confirm the `github-actions` ecosystem block is present:

```yaml
- package-ecosystem: "github-actions"
  directory: "/"
  schedule:
    interval: "weekly"
    day: "monday"
```

The `directory: "/"` setting causes Dependabot to scan every `uses:` reference in `.github/workflows/*.yml`, including the one you just added. New actions are covered automatically.

### 5. Update the SHA-to-version mapping table in the reference document

Open `docs/reference/ci-cd-pipeline-security.md` and add a row to the SHA-to-version mapping table in the [SHA Pinning](../reference/ci-cd-pipeline-security.md#sha-pinning) section:

| Action | SHA | Version |
|--------|-----|---------|
| `owner/action-name` | `FULL40CHARSHA` | vX.Y.Z |

Use exactly the same SHA and version tag you used in the workflow file.

### 6. Update the workflow-to-action matrix

Still in `docs/reference/ci-cd-pipeline-security.md`, add a row to the workflow-to-action matrix table and mark a `Yes` in every workflow column where the action appears:

| Action | ci.yml | version-bump.yml | release.yml | docs.yml | pat-monitor.yml |
|--------|--------|------------------|-------------|----------|-----------------|
| `owner/action-name` | Yes | No | No | No | No |

### 7. Run CI to verify the action resolves correctly

Push your branch and confirm the CI run passes. A failed step referencing your new action typically means:

- The SHA was copied incorrectly (mismatched length, truncated)
- The action does not exist at that SHA (deleted or private repository)
- A required `with:` input is missing

Inspect the failed step's log output to distinguish between these cases.

## Verification

After CI passes, confirm the reference document is consistent with the workflow files:

```bash
grep -r "owner/action-name" .github/workflows/
```

Each result must show the 40-character SHA followed by the version comment. No result should show a bare tag reference such as `@v2`.

Expected result: every match line contains the full SHA and `# vX.Y.Z`.

## Troubleshooting

**Problem:** `git ls-remote` returns two lines for the same tag (the tag object SHA and the commit SHA).
**Solution:** Use the SHA on the line ending in `^{}`. That is the commit SHA the action runner resolves to.

**Problem:** CI fails with "Can't find action 'owner/action-name'" at your SHA.
**Solution:** Verify the SHA belongs to a commit in the action's repository, not to the tag object. Run `git ls-remote` again and take the `^{}` SHA.

**Problem:** Dependabot does not open a PR after the next Monday scan.
**Solution:** Confirm the action reference in the workflow file uses `@SHA # vX.Y.Z` format, not `@tag`. Dependabot only updates SHA-pinned actions in the `github-actions` ecosystem when a newer version exists. If the action is already at the latest release, no PR is expected.

## Related

- **Reference:** [CI/CD Pipeline Security Controls](../reference/ci-cd-pipeline-security.md) -- SHA-to-version mapping table, Dependabot configuration, and per-workflow action matrix
- **Explanation:** [About the Jerry Framework CI/CD Supply Chain Security Model](../explanation/ci-cd-supply-chain-security.md) -- Threat model and rationale for SHA pinning
