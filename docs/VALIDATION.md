# BSG validation

What has been checked, how, and what remains a user trial. Dates are when each check last ran.

## Automated checks

`python -m unittest discover -s tests -v`: **40 tests pass** (2026-10-28, Python 3 on WSL).

Coverage: non-destructive initialization, stable slice IDs, completion prerequisites, stale decision and check revisions, required human feedback, dependency cycles, read-only help, blocked build recommendations, evidence path boundaries, malformed records, pause recommendations, existing non-BSG planning folders, draft plans that do not substitute for slice context, readiness requiring a populated plan, handoff creation and byte-for-byte preservation of existing instructions, `CLAUDE.md` mirroring for each Claude instruction-file variant, malformed markers blocking every write, pre-release markers counting as attached, installation for either host or both with auto-detection, idempotent installs that refuse to overwrite modified files, and plugin manifest consistency.

Additional coverage: stage-dependent record requirements, early failed-check evidence, deferred decision records, legacy scaffold compatibility, generated-summary preservation and idempotence, missing views with read-only status, malformed-marker preflight, invalid-index rejection, escaped table content, and symlink output protection. A CLI smoke test exercised init → slice → sync → status → validate in a temporary project. The skill structure validator also passed. These checks do not establish live interview behavior.

The helpers have no third-party runtime dependencies.

## Independent behavioral evaluation

A subagent read the skill and simulated four scenarios; see [BEHAVIORAL-REVIEW.md](BEHAVIORAL-REVIEW.md). This was a scenario evaluation with synthetic helper probes, not a live end-to-end build. The fixes it produced require verification checks to be defined before a slice becomes ready, validate executed-check metadata, and clarify that a scoped pause can coexist with allowed independent work. Regression tests cover them.

## Live installs

Plugin install verified from the public repository with the README's two commands on Windows 11 (Claude Code bundled with the desktop app) and WSL 2 Ubuntu 24.04 (Claude Code CLI, `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` because SSH to GitHub had no host key). `claude plugin details bsg` lists one skill with all of its files.

## First live project

The first real run shaped and planned a nine-slice CLI project and built its first slice. It exposed three gaps that are now fixed in the skill text: the brief and slice map were saved to files but never shown in the conversation; phases ended without a recap or a recommended next step; and the build offer was repeated after being declined and lacked the "start it while we shape the next slice" option. One open question remains for live validation: whether the guidance on delegating substantial implementation and handling tiny tasks directly produces the intended balance, since the lead built the first slice inline.

## Remaining user trial

Use BSG on a new project end to end. Exercise a human checkpoint and change a shared decision while a worker is building. Verify that the lead keeps the conversation responsive, redirects only affected work, recaps at each phase, and records the outcome honestly. Host-specific picker behavior, parallel persistence across turns, and the subjective quality of the interview are confirmed only through use.
