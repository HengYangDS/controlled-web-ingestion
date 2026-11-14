# Tasks

## 1. Runtime

- [x] 1.1 Bind the repository family to the 0.2.0-beta.10 runtime, installed with native Mise from
      the release's own declaration and checked against its manifest's source commit, through its
      console's `hook install`, keeping 0.2.0-beta.9 as the rollback; done when CURRENT names the
      0.2.0-beta.10 runtime and ROLLBACK the 0.2.0-beta.9 one, and `ethos status` reports the lane
      ready. CURRENT names the 0.2.0-beta.10 runtime `526c2ebafeba`, whose manifest's source commit
      is `b10254f87`, and ROLLBACK the 0.2.0-beta.9 runtime `9427601ab2b1`; `ethos status` reports
      the lane ready and the `repair-paradigm` preview conforming.
- [x] 1.2 Apply 0.2.0-beta.10's Markdown list rule to the July implementation plan; done when the
      Markdown gate passes and the change removes only blank lines. The bound runtime's
      `canonical_spacing` removed 13 blank lines from the plan and changed no other line;
      `ethos lane format --apply` reports no change because the Prettier ignore names `docs/plans/`.
      The Markdown gate passes.
- [x] 1.3 State the frozen status in `README.md` with its pin floor and thaw condition; done when
      every `mise run check` command and the documentation gates pass. The README has a `Status`
      section: frozen since 14 November 2026 on ETHOS 0.2.0-beta.10 with uv at 0.13.7, thawing on a
      named consumer or a security advisory. This answers the deferred item of the supply Change:
      the owner chose on 14 November to keep uv 0.13.7. The tracked pipelines hold no schedule
      trigger. Every `mise run check` command and the documentation gates pass.
