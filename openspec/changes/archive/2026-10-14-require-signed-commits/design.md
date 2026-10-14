## Context

ETHOS reads the commit policy from `.ethos/workspace.toml` in the tree of each commit, so a commit
is bound by the policy that its own tree records. ETHOS signs with the repository-local
`user.signingkey` and verifies against `gpg.ssh.allowedSignersFile`. Both are host Git
configuration, not repository content.

## Decisions

1. Adopt the ETHOS subject grammar unchanged. Every subject since the last publication matches it
   except one historical `style` commit, which the policy does not reach.
2. Do not re-sign existing history. Rewriting it would change commit IDs that evidence records
   name, while publication needs only a signed head.
3. Keep the signing key and the trust anchor in host Git configuration. The repository records
   the requirement, never key material.

## Rollback

Revert this change. ETHOS again creates unsigned archive commits, and `ethos publish` rejects their
heads.
