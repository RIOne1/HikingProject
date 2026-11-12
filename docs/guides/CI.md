# CI runner guide

The [workflow](../../.github/workflows/repository-checks.yml) uses only the owner's self-hosted Linux x64 runner with labels `self-hosted`, `linux`, `x64`, `hikingproject-local-ci`. The owner identified its image as `hikingproject-ci-runner:2.338.2`, Ubuntu 24.04.5 LTS, running in Docker on Windows. The repository does not manage or rebuild that private runner image.

## Checks and tools

| Required check | Work |
| --- | --- |
| `Documentation integrity` | Existing document/validator checks, npm clean install, Web lint/tests/typecheck/build, portable Swift/GRDB tests |
| `Contribution policy` | PR title/commits, human author, target branch, numbered branch and linked open Issue |

The legacy documentation check name is retained because it is already required by `protect-main`; its broader coverage avoids a protection-setting change or an unrequired app check. The first job has a 20-minute limit for initial downloads/compilation; contribution validation remains five minutes. Both retain same-repository filtering, read-only tokens and no persisted checkout credentials.

Node 24.20.0 is installed by SHA-pinned `actions/setup-node`. SHA-pinned `swift-actions/setup-swift` v2.4.0 installs Swift 6.2.1, a version supported by that action on Ubuntu 24.04. Local Xcode uses Swift 6.4.2; the portable package's language/tool requirements permit both. This action checks the toolchain download signature and uses the runner's local tool directory, not GitHub cache storage.

The runner image needs Git, Python 3.10+, CA certificates, curl, `file`, GnuPG, tar/gzip/xz, Clang, pkg-config and Swift's Ubuntu runtime prerequisites, plus SQLite development headers (`libsqlite3-dev`). Consult [official Swift Linux installation](https://www.swift.org/install/linux/tarball/) for the selected distribution's native dependencies. Install missing packages while building the dedicated runner image; do not give arbitrary PR jobs host-admin access or mount a Docker socket just to install them. The workflow checks the key tools/SQLite headers before setup and intentionally does not run `sudo apt` or skip Swift tests when a prerequisite is missing.

For a missing header/library or unsupported image, keep the check failing, repair the image, reconnect with the same labels and rerun the failed job. Keep its registration token private. Offline runners leave jobs queued; the workflow has no hosted fallback. See [SECURITY](../../SECURITY.md#self-hosted-ci) for host isolation and external-contribution restrictions.

## Ubuntu 24.04 image preparation

The first [foundation run](https://github.com/RIOne1/HikingProject/actions/runs/43209471551) passed Web and contribution checks but failed in Swift setup because `file` was absent. The image must be extended on the owner's PC before Linux Swift verification can pass. Add the following to the existing Dockerfile while its build user is root, before the final unprivileged `USER` instruction; retain the image's existing runner entrypoint and registration configuration:

```dockerfile
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates curl file gnupg2 gzip tar xz-utils clang \
    binutils git libc6-dev libcurl4-openssl-dev libedit2 libgcc-13-dev \
    libncurses-dev libpython3-dev libsqlite3-dev libstdc++-13-dev \
    libxml2-dev libz3-dev pkg-config tzdata zip unzip zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
```

This combines the official Ubuntu 24.04 prerequisites with this action's `file` command and GRDB's development headers. Do not run the runner service as root. Build with a new local tag and update the existing Compose/service image reference; preserve its private configuration and registered identity. Once the runner reconnects, a PR update or an authorized rerun exercises the actual toolchain. Installing packages alone is not evidence that Swift tests passed. No paid runner or cloud build is needed.

## Cost and coverage limits

No GitHub-hosted runner, artifact upload, Actions cache, paid scanner, deployment or signing secret is configured. npm packages, Swift toolchains and SPM sources download to the local runner; disk/network use still belongs to that PC. The machine must remain available while jobs run. Package downloads can fail independently of application tests; report the actual failure rather than changing the checks to pass.

Linux tests the portable catalogue/database library. It cannot build SwiftUI, link the iOS Mapbox SDK or run Xcode simulator tests. Contributors changing the app must provide local Mac evidence using [Mobile](MOBILE.md#build-and-test). This is the explicitly documented local iOS verification baseline, not automated iOS CI or outdoor/device acceptance.
