# Fix Argument Parsing on Windows

On Windows, `spawn` calls result in full paths (e.g., `C:\Program Files\nodejs\node.exe`) in `process.argv`. Commander's automatic detection of the node executable sometimes fails with these paths, causing it to treat the executable as an unknown command.

## Proposed Changes

### [src/cli]
#### [MODIFY] [run-main.ts](file:///g:/AIHub/clawdbot/src/cli/run-main.ts)
- Update `runCli` to explicitly pass `{ from: "node" }` to `program.parseAsync` when the input `argv` matches `process.argv` (or has at least 2 elements and isn't a synthetic user input).
- Actually, since `runCli` is primarily used with `process.argv`, and `entry.ts` passes `process.argv`, we can conditionally apply `{ from: "node" }` if the first argument looks like an executable path or if `argv.length >= 2`.
- Remove debug logs added during investigation.
- Use `{ from: "node" }` strictly to resolve the ambiguity.

### [src]
#### [MODIFY] [entry.ts](file:///g:/AIHub/clawdbot/src/entry.ts)
- Remove debug logs added during investigation.

## Verification
- Run `pnpm clawdbot gateway` again. It should start successfully.
