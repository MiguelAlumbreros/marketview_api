# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## Project: MV API Daily Fetcher

Fetches daily OHLCV data from the MarketView (MV) API for a fixed set of symbols (ICE TTF gas, EEX Spain power, ICE EUAs) and writes to CSV and/or PostgreSQL.

### Key files
- `scheduled_mv_daily_to_csv.py` — main script; all config constants are at the top
- `mv-python-api/` — MV SDK (imported as `mvconnectivity`)
- `output.csv` — default CSV output
- `job.log` — run log

### Configuration constants (top of script)
| Constant | Purpose |
|---|---|
| `OUTPUT_PATH` | CSV output path |
| `OUTPUT_MODE` | `"csv"` / `"db"` / `"both"` |
| `PARALLEL_FETCH` | Enable threaded chunk fetching |
| `PARALLEL_WORKERS` | Thread count |
| `CHUNK_SIZE_DAYS` | Days per API request chunk |
| `START_DATE` | History start date |
| `SYMBOLS` | Dict of MV symbol → metadata |

### Upsert keys
- **CSV:** `[symbol, strip, exchange, market_date, delivery_date]` — `overwrite_csv=True` (default) keeps new rows on conflict
- **PostgreSQL:** `(symbol, strip, delivery_date, market_date)` — always upserts (new wins)

### Output columns
`symbol, description, commodity, exchange, strip, market_date, delivery_date, close, low, high, volume`

### Adding symbols
Add entries to `SYMBOLS` dict following the existing pattern: MV symbol string → `{commodity, exchange, strip, description}`. No other changes needed.
