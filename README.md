# financial-alert

## Persistent market history

The Docker action stores daily OHLCV records in SQLite at
`data/prices.sqlite` in the GitHub workspace by default. Each record is keyed
by ticker and trading date, so reruns update existing dates instead of
creating duplicates.

The workflow in `.github/workflows/update-market-history.yml` demonstrates
persisting the database between runs with GitHub Actions artifacts:

1. It downloads the newest unexpired `financial-alert-history` artifact, if
   one exists.
2. It runs the action, which backfills full history for new tickers and
   refreshes the latest week for tickers already in the database.
3. It uploads the updated database as a new artifact.

Artifacts expire after 7 days. The scheduled workflow refreshes the artifact
on weekdays; if it does not run before an artifact expires, the next run starts
a new database. SQLite is compact for many time-series datasets, but its size
depends on the number of tickers, history, and columns; it is not guaranteed
that a million rows will fit in only a few megabytes.

The database accumulates daily rows over time. Each uploaded artifact is a
complete snapshot of the database, not just the rows added during that run;
older snapshots expire automatically after 7 days.

To use the action in another workflow, restore the artifact before invoking the
action and upload `data/prices.sqlite` afterward. Artifacts belong to a
workflow run, so the caller workflow must manage its own restore and upload.