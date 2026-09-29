# Synthetic fixtures

Test data for this repo. Everything here is generated, never copied or derived row-by-row from
`D:\DT data lakes`.

Rules:
- Each fixture is produced by a script or a documented seed, so it can be regenerated.
- Fixtures mimic the *shape* of a lake source (columns, types, sampling rate, gaps), not its values.
- No real names, account identifiers, locations or timestamps from the lake.
- If a test needs a property of real data (e.g. an autocorrelation ρ ≈ 0.6), generate a series with
  that property and say so in the fixture's docstring or filename.
