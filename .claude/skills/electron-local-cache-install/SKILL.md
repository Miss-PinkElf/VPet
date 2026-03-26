---
name: electron-local-cache-install
description: |
  Handle Electron install failures during npm postinstall when the binary download breaks with network errors like "ReadError: The server aborted pending request", ECONNRESET, ETIMEDOUT, or aborted requests. Use when: (1) `npm install` fails inside `node_modules/electron`, (2) you already have the correct Electron zip locally, (3) you need to avoid changing global npm config and want install to succeed via Electron's official cache mechanism.
author: Claude Code
version: 1.0.0
date: 2026-03-16
---

# Electron Local Cache Install

## Problem
`npm install electron` downloads a platform-specific binary during `postinstall`. In restricted or flaky networks, the install can fail with errors such as:

- `ReadError: The server aborted pending request`
- `ECONNRESET`
- `ETIMEDOUT`
- other `@electron/get` download failures

A common trap is trying to only change mirrors or retry blindly, while already having a matching Electron zip available locally.

## Context / Trigger Conditions
Use this skill when ALL or MOST of the following are true:

- `npm install` fails in `node_modules/electron`
- stack trace points to `install.js` or `@electron/get`
- the failure is clearly in binary download, not app code
- you already downloaded a local artifact like:
  - `electron-v40.4.1-darwin-arm64.zip`
- the project's `package.json` Electron version may not match that local zip yet
- you want a project-scoped fix without editing global npm config

## Solution

### 1. Confirm the real failure point
Read the npm output carefully.

The key distinction is:
- **install script download failure** → fix distribution path / cache
- **TypeScript / bundler / app runtime failure** → not this skill

### 2. Align Electron version first
Before touching cache, ensure the version in `package.json` matches the local zip exactly.

Example:
- local file: `electron-v40.4.1-darwin-arm64.zip`
- project dependency should be: `"electron": "40.4.1"`

If versions do not match, Electron will not reuse the cached archive.

### 3. Compute the zip checksum
Electron cache is organized by checksum.

macOS / Linux example:

```bash
shasum -a 256 /path/to/electron-v40.4.1-darwin-arm64.zip
```

Take the resulting SHA-256 value.

### 4. Seed Electron's official cache
On macOS, Electron cache lives under:

```bash
~/Library/Caches/electron/
```

Create the cache folder using the checksum as directory name, then copy the zip into it.

Example:

```bash
mkdir -p "$HOME/Library/Caches/electron/<sha256>"
cp "/path/to/electron-v40.4.1-darwin-arm64.zip" \
  "$HOME/Library/Caches/electron/<sha256>/electron-v40.4.1-darwin-arm64.zip"
```

This lets `@electron/get` resolve the artifact from local cache instead of downloading it again.

### 5. Re-run npm install
After version alignment + cache seeding:

```bash
npm install
```

If the cache is correct, Electron installation should complete without needing network download for that artifact.

### 6. Only if no local zip is available, use mirror / proxy settings
If you do **not** already have the zip, then use Electron-supported install controls:

- `ELECTRON_MIRROR`
- `ELECTRON_CUSTOM_DIR`
- `ELECTRON_CUSTOM_FILENAME`
- `ELECTRON_GET_USE_PROXY`
- `electron_config_cache`

But when the exact zip is already present locally, cache seeding is usually the cleanest and least invasive solution.

## Verification
A successful outcome should satisfy all of these:

1. `npm install` finishes successfully
2. `electron` package is installed in the project
3. no repeated binary download failure appears
4. subsequent build command works, e.g.:

```bash
npm run build
```

Optional verification:
- confirm the exact Electron version in `package.json`
- confirm the cache file path contains the expected zip name

## Example

### Scenario
Project install fails with:

```text
npm error path .../node_modules/electron
npm error command sh -c node install.js
npm error ReadError: The server aborted pending request
```

You already have:

```text
frontend/electron/electron-v40.4.1-darwin-arm64.zip
```

### Fix
1. set `package.json` to:

```json
"electron": "40.4.1"
```

2. compute checksum:

```bash
shasum -a 256 frontend/electron/electron-v40.4.1-darwin-arm64.zip
```

3. copy into cache:

```bash
mkdir -p "$HOME/Library/Caches/electron/<sha256>"
cp "frontend/electron/electron-v40.4.1-darwin-arm64.zip" \
  "$HOME/Library/Caches/electron/<sha256>/electron-v40.4.1-darwin-arm64.zip"
```

4. rerun install:

```bash
npm install --prefix frontend
```

## Notes
- The root cause may look like a package problem, but it is often just a **binary distribution/network path issue**.
- Do not assume retries will help if you already have the local artifact.
- Do not seed cache with the wrong Electron version; cache hit depends on version + filename + checksum expectations.
- Prefer this project-scoped approach over changing global npm config when the problem is isolated to one project.
- If you need a shared team solutio