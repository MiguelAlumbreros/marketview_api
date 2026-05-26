from __future__ import annotations

import concurrent.futures
import datetime
import logging
import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values


ROOT_DIR = Path(__file__).resolve().parent
SDK_DIR = ROOT_DIR / "mv-python-api"

if str(SDK_DIR) not in sys.path:
    sys.path.insert(0, str(SDK_DIR))

# Load .env early so module-level constants below pick up .env values.
for _env_file in [ROOT_DIR / ".env", SDK_DIR / ".env"]:
    if _env_file.exists():
        load_dotenv(_env_file)
        break

from mvconnectivity import MvWSConnection

OUTPUT_PATH = ROOT_DIR / "output.csv"
LOG_PATH = ROOT_DIR / "job.log"
ENVIRONMENT = os.getenv("MV_ENV", "onboard")

DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = int(os.getenv("PG_PORT", "5432"))
DB_NAME = os.getenv("PG_DATABASE", "postgres")
DB_USER = os.getenv("PG_USER", "postgres")
DB_PASSWORD = os.getenv("PG_PASSWORD")
DB_TABLE = os.getenv("PG_TABLE", "marketview_history")

CHUNK_SIZE_DAYS = 50
SYMBOL_CHUNK_SIZE = 300  # max symbols per API request (avoids HTTP 414)
OUTPUT_MODE = "csv"   # "csv" | "db" | "both"
FRESH_CSV = True     # If True, replace OUTPUT_PATH wholesale instead of upserting
PARALLEL_FETCH = True
PARALLEL_WORKERS = 4   # max threads when PARALLEL_FETCH is True; None = one per chunk

# Symbol registry — edit here to add/remove products.
# Each entry: MV symbol key → {commodity, exchange, area, strip, product, description}
front_units = 36
SYMBOLS = {

    # GAS — ICE TTF
    **{f"/TFN<{i}>":         {"commodity": "gas",   "exchange": "ICE", "area": "NL", "strip": "month",   "product": "TTF",      "description": f"TTF front {i+1} month"}   for i in range(front_units)},
    **{f"/TFN_QUARTER<{i}>": {"commodity": "gas",   "exchange": "ICE", "area": "NL", "strip": "quarter", "product": "TTF",      "description": f"TTF front {i+1} quarter"} for i in range(front_units)},
    **{f"/TFN_YEAR<{i}>":    {"commodity": "gas",   "exchange": "ICE", "area": "NL", "strip": "cal",     "product": "TTF",      "description": f"TTF front {i+1} cal"}     for i in range(front_units)},

    # POWER — EEX Spain Baseload (months start at <1>)
    **{f"/E.FEB_WEEK<{i}>":  {"commodity": "power", "exchange": "EEX", "area": "SP",       "strip": "week",    "product": "Baseload", "description": f"Spain Baseload power front {i+1} week"}    for i in range(front_units)},
    **{f"/E.FEW_WEEK<{i}>":  {"commodity": "power", "exchange": "EEX", "area": "SP",       "strip": "weekend", "product": "Baseload", "description": f"Spain Baseload power front {i+1} weekend"} for i in range(front_units)},
    **{f"/E.FEBM<{i+1}>":    {"commodity": "power", "exchange": "EEX", "area": "SP",       "strip": "month",   "product": "Baseload", "description": f"Spain Baseload power front {i+1} month"}   for i in range(front_units)},
    **{f"/E.FEBQ<{i}>":      {"commodity": "power", "exchange": "EEX", "area": "SP",       "strip": "quarter", "product": "Baseload", "description": f"Spain Baseload power front {i+1} quarter"} for i in range(front_units)},
    **{f"/E.FEBY<{i}>":      {"commodity": "power", "exchange": "EEX", "area": "SP",       "strip": "cal",     "product": "Baseload", "description": f"Spain Baseload power front {i+1} cal"}     for i in range(front_units)},

    # EUA — ICE monthly contracts
    **{f"/ECF<{i+1}>":       {"commodity": "EUA",   "exchange": "ICE", "area": "EU",          "strip": "month",   "product": "EUA",      "description": f"EUAs front {i+1} month"}   for i in range(front_units)},

    # GAS — EEX PVB (Spain)
    **{f"/E.GEBM<{i}>": {"commodity": "gas", "exchange": "EEX", "area": "SP",       "strip": "month",   "product": "PVB", "description": f"EEX PVB gas front {i+1} month"}   for i in range(front_units)},
    **{f"/E.GEBQ<{i}>": {"commodity": "gas", "exchange": "EEX", "area": "SP",       "strip": "quarter", "product": "PVB", "description": f"EEX PVB gas front {i+1} quarter"} for i in range(front_units)},
    **{f"/E.GEBY<{i}>": {"commodity": "gas", "exchange": "EEX", "area": "SP",       "strip": "cal",     "product": "PVB", "description": f"EEX PVB gas front {i+1} cal"}     for i in range(front_units)},

    # GAS — EEX TTF (Netherlands, via EEX)
    **{f"/E.G3BM<{i}>": {"commodity": "gas", "exchange": "EEX", "area": "NL", "strip": "month",   "product": "TTF", "description": f"EEX TTF gas front {i+1} month"}   for i in range(front_units)},
    **{f"/E.G3BQ<{i}>": {"commodity": "gas", "exchange": "EEX", "area": "NL", "strip": "quarter", "product": "TTF", "description": f"EEX TTF gas front {i+1} quarter"} for i in range(front_units)},
    **{f"/E.G3BY<{i}>": {"commodity": "gas", "exchange": "EEX", "area": "NL", "strip": "cal",     "product": "TTF", "description": f"EEX TTF gas front {i+1} cal"}     for i in range(front_units)},

#     # CO2 — ICE Dec contracts 2020–2027
#     **{
#         f"/ECFZ{yr % 100:02d}": {
#             "commodity": "CO2", "exchange": "ICE", "area": "EU",
#             "strip": "month", "description": f"EUAs Dec {yr}",
#         }
#         for yr in range(2020, 2028)
#     },
}

FIELDS = ["symbol", "date", "contractdate", "close", "low", "high", "volume"]

START_DATE = datetime.date(2021, 1, 1)
END_DATE: datetime.date | None = None   # None = today

OUTPUT_COLUMNS = [
    "symbol",
    "description",
    "commodity",
    "exchange",
    "area",
    "strip",
    "product",
    "market_date",
    "delivery_date",
    "end_delivery_date",
    "close",
    "low",
    "high",
    "volume",
]


def _configure_logging() -> logging.Logger:
    """Set up logging to both a rotating file and stdout.

    Returns:
        Configured logger for this script.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger("scheduled_mv_daily_to_csv")


def _load_credentials() -> tuple[str, str]:
    """Load MV API credentials from a .env file or environment variables.

    Searches ROOT_DIR/.env then SDK_DIR/.env. Raises RuntimeError if
    MV_USERNAME or MV_PASSWORD cannot be found after loading.

    Returns:
        Tuple of (username, password).

    Raises:
        RuntimeError: If MV_USERNAME or MV_PASSWORD is not set.
    """
    candidate_env_files = [
        ROOT_DIR / ".env",
        SDK_DIR / ".env",
    ]

    for env_file in candidate_env_files:
        if env_file.exists():
            load_dotenv(env_file)
            break

    username = os.getenv("MV_USERNAME")
    password = os.getenv("MV_PASSWORD")

    if not username or not password:
        raise RuntimeError(
            "Missing MV credentials. Set MV_USERNAME and MV_PASSWORD in a .env file or environment variables."
        )

    return username, password


def _get_upsert_keys(df: pd.DataFrame) -> list[str]:
    """Validate that df contains the required PostgreSQL upsert key columns.

    Args:
        df: DataFrame to validate.

    Returns:
        List of upsert key column names: ["symbol", "strip", "delivery_date", "market_date"].

    Raises:
        RuntimeError: If any required key column is missing from df.
    """
    required_keys = ["symbol", "strip", "delivery_date", "market_date"]
    missing_keys = [column for column in required_keys if column not in df.columns]
    if missing_keys:
        raise RuntimeError(
            f"Could not determine upsert keys. Missing required columns: {', '.join(missing_keys)}"
        )
    return required_keys


def _build_symbol_lookup() -> dict[str, dict[str, str]]:
    """Build a flat lookup dict from the SYMBOLS registry.

    Returns:
        Dict mapping each MV symbol string to its metadata fields
        (description, commodity, exchange, area, strip).
    """
    return {
        symbol: {
            "description": config["description"],
            "commodity": config["commodity"],
            "exchange": config["exchange"],
            "area": config["area"],
            "strip": config["strip"],
            "product": config["product"],
        }
        for symbol, config in SYMBOLS.items()
    }


def _normalize_existing_output(df: pd.DataFrame) -> pd.DataFrame:
    """Align a legacy CSV DataFrame to the current OUTPUT_COLUMNS schema.

    Renames legacy column names (date → market_date, contractdate → delivery_date)
    and fills any missing output columns with pd.NA.

    Args:
        df: DataFrame read from an existing output CSV.

    Returns:
        DataFrame with exactly the OUTPUT_COLUMNS column set.
    """
    normalized = df.copy()

    legacy_column_map = {
        "date": "market_date",
        "contractdate": "delivery_date",
    }
    normalized = normalized.rename(columns=legacy_column_map)

    for column in OUTPUT_COLUMNS:
        if column not in normalized.columns:
            normalized[column] = pd.NA

    return normalized[OUTPUT_COLUMNS]


EEX_DELIVERY_START_OFFSET = {
    "week": pd.Timedelta(days=-7),
    "weekend": pd.Timedelta(days=-2),
}


def _shift_eex_delivery_to_period_start(df: pd.DataFrame) -> None:
    """Shift EEX week/weekend delivery_date back to the start of the delivery period.

    MV reports delivery_date past the actual start: week strips need -7 days,
    weekend strips need -2 days. Other strips are untouched. Mutates df in place.
    """
    for strip_val, offset in EEX_DELIVERY_START_OFFSET.items():
        mask = df["strip"] == strip_val
        if mask.any():
            df.loc[mask, "delivery_date"] += offset


def _prepare_output_frame(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Enrich and reshape the raw MV API DataFrame into the output schema.

    Joins symbol metadata (description, commodity, exchange, area, strip),
    renames API column names (date → market_date, contractdate → delivery_date),
    computes end_delivery_date from the strip type, and formats all dates as
    YYYY-MM-DD strings.

    Args:
        raw_df: Raw DataFrame returned by the MV API (contains symbol, date,
                contractdate, close, low, high, volume).

    Returns:
        DataFrame with exactly the OUTPUT_COLUMNS column set.
    """
    symbol_lookup = _build_symbol_lookup()
    prepared = raw_df.copy()

    prepared["description"] = prepared["symbol"].map(
        lambda value: symbol_lookup.get(value, {}).get("description")
    )
    prepared["commodity"] = prepared["symbol"].map(
        lambda value: symbol_lookup.get(value, {}).get("commodity")
    )
    prepared["exchange"] = prepared["symbol"].map(
        lambda value: symbol_lookup.get(value, {}).get("exchange")
    )
    prepared["area"] = prepared["symbol"].map(
        lambda value: symbol_lookup.get(value, {}).get("area")
    )
    prepared["strip"] = prepared["symbol"].map(
        lambda value: symbol_lookup.get(value, {}).get("strip")
    )
    prepared["product"] = prepared["symbol"].map(
        lambda value: symbol_lookup.get(value, {}).get("product")
    )

    prepared = prepared.rename(
        columns={
            "date": "market_date",
            "contractdate": "delivery_date",
        }
    )

    for column in OUTPUT_COLUMNS:
        if column not in prepared.columns:
            prepared[column] = pd.NA

    prepared["market_date"] = pd.to_datetime(prepared["market_date"], errors="coerce")
    prepared["delivery_date"] = pd.to_datetime(prepared["delivery_date"], errors="coerce")

    # MV reports EEX week/weekend delivery_date past the period start; shift back.
    _shift_eex_delivery_to_period_start(prepared)

    end_dates = pd.Series(pd.NaT, index=prepared.index, dtype="datetime64[ns]")
    for strip_val, offset in [
        ("month", pd.offsets.MonthEnd(0)),
        ("quarter", pd.offsets.QuarterEnd(0)),
        ("cal", pd.offsets.YearEnd(0)),
        ("week", pd.Timedelta(days=7)),
        ("weekend", pd.Timedelta(days=1)),
    ]:
        mask = prepared["strip"] == strip_val
        if mask.any():
            end_dates[mask] = prepared.loc[mask, "delivery_date"] + offset
    prepared["end_delivery_date"] = end_dates

    prepared["market_date"] = prepared["market_date"].dt.strftime("%Y-%m-%d")
    prepared["delivery_date"] = prepared["delivery_date"].dt.strftime("%Y-%m-%d")
    prepared["end_delivery_date"] = prepared["end_delivery_date"].dt.strftime("%Y-%m-%d")

    return prepared[OUTPUT_COLUMNS]


def _get_db_connection() -> psycopg2.extensions.connection:
    """Open and return a new psycopg2 connection using the module-level DB constants.

    Connection parameters (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD) are
    read from environment variables / .env at import time.

    Returns:
        Open psycopg2 connection (caller is responsible for closing it).
    """
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        options="-c client_encoding=UTF8",
    )


def _upsert_postgres(new_rows: pd.DataFrame) -> int:
    """Insert or update rows in the PostgreSQL table.

    Uses ON CONFLICT (symbol, strip, delivery_date, market_date) DO UPDATE to
    overwrite price/volume fields when a row already exists for that key.

    Args:
        new_rows: DataFrame in OUTPUT_COLUMNS schema to write.

    Returns:
        Number of rows processed (0 if new_rows is empty).
    """
    if new_rows.empty:
        return 0

    _get_upsert_keys(new_rows)

    prepared = new_rows.copy()
    prepared["market_date"] = pd.to_datetime(prepared["market_date"], errors="coerce").dt.date
    prepared["delivery_date"] = pd.to_datetime(prepared["delivery_date"], errors="coerce").dt.date

    numeric_columns = ["close", "low", "high", "volume"]
    for column in numeric_columns:
        prepared[column] = prepared[column].replace(r"^\s*$", pd.NA, regex=True)
        prepared[column] = pd.to_numeric(prepared[column], errors="coerce")

    text_columns = ["symbol", "description", "commodity", "exchange", "strip"]
    for column in text_columns:
        prepared[column] = prepared[column].replace(r"^\s*$", pd.NA, regex=True)

    prepared = prepared.where(pd.notna(prepared), None)

    insert_columns = OUTPUT_COLUMNS
    rows = [tuple(row[column] for column in insert_columns) for _, row in prepared.iterrows()]

    insert_sql = sql.SQL(
        """
        INSERT INTO {} ({})
        VALUES %s
        ON CONFLICT (symbol, strip, delivery_date, market_date)
        DO UPDATE SET
            description = EXCLUDED.description,
            commodity = EXCLUDED.commodity,
            exchange = EXCLUDED.exchange,
            product = EXCLUDED.product,
            close = EXCLUDED.close,
            low = EXCLUDED.low,
            high = EXCLUDED.high,
            volume = EXCLUDED.volume
        """
    ).format(
        sql.Identifier(DB_TABLE),
        sql.SQL(", ").join(sql.Identifier(column) for column in insert_columns),
    )

    connection = _get_db_connection()
    try:
        with connection.cursor() as cursor:
            execute_values(cursor, insert_sql.as_string(connection), rows)
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return len(rows)


def _build_chunks(
    startdate: datetime.date,
    enddate: datetime.date,
    chunk_size_days: int,
) -> list[tuple[datetime.date, datetime.date]]:
    """Split a date range into consecutive non-overlapping chunks.

    Args:
        startdate: First date of the full range (inclusive).
        enddate: Last date of the full range (inclusive).
        chunk_size_days: Maximum number of days per chunk.

    Returns:
        List of (chunk_start, chunk_end) date tuples that together cover the
        full range without gaps or overlap.
    """
    chunks = []
    chunk_start = startdate
    while chunk_start <= enddate:
        chunk_end = min(chunk_start + datetime.timedelta(days=chunk_size_days - 1), enddate)
        chunks.append((chunk_start, chunk_end))
        chunk_start = chunk_end + datetime.timedelta(days=1)
    return chunks


def _fetch_daily_in_chunks(
    username: str,
    password: str,
    symbols: list[str],
    fields: list[str],
    startdate: datetime.date,
    enddate: datetime.date,
    env: str,
    chunk_size_days: int,
    symbol_chunk_size: int,
    parallel: bool = False,
    workers: int | None = None,
) -> pd.DataFrame:
    """Fetch MV daily OHLCV data, chunked by both date range and symbol count.

    Builds a flat list of (date_chunk, symbol_batch) tasks and fetches each
    sequentially (or concurrently if parallel=True). Deduplicates before returning.
    """
    date_chunks = _build_chunks(startdate, enddate, chunk_size_days)
    symbol_batches = [symbols[i:i + symbol_chunk_size] for i in range(0, len(symbols), symbol_chunk_size)]
    tasks = [(dc, sb) for dc in date_chunks for sb in symbol_batches]

    if not tasks:
        return pd.DataFrame(columns=fields)

    def fetch_one(date_chunk: tuple, sym_batch: list[str], conn: MvWSConnection | None = None) -> pd.DataFrame:
        chunk_start, chunk_end = date_chunk
        if conn is None:
            conn = MvWSConnection(username, password)
        print(f"Fetching chunk: {chunk_start} -> {chunk_end} ({len(sym_batch)} symbols)")
        mv_result = conn.get_daily(symbols=sym_batch, fields=fields, startdate=chunk_start, enddate=chunk_end, env=env)
        return mv_result.to_dataframe()

    progress = tqdm(total=len(tasks), desc="Fetching chunks", unit="chunk")

    if parallel:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(fetch_one, dc, sb) for dc, sb in tasks]
            all_chunks = []
            for f in concurrent.futures.as_completed(futures):
                all_chunks.append(f.result())
                progress.update(1)
    else:
        conn = MvWSConnection(username, password)
        all_chunks = []
        for dc, sb in tasks:
            all_chunks.append(fetch_one(dc, sb, conn))
            progress.update(1)

    progress.close()

    combined = pd.concat(all_chunks, ignore_index=True)
    return combined.drop_duplicates(ignore_index=True)


CSV_UPSERT_KEYS = ["symbol", "strip", "exchange", "market_date", "delivery_date"]


def _upsert_csv(
    df: pd.DataFrame,
    path: Path,
    logger: logging.Logger,
    overwrite: bool = True,
    fresh: bool = False,
) -> None:
    """Write df to a CSV file, merging with any existing content.

    Deduplicates on CSV_UPSERT_KEYS after concatenating new and existing rows.
    When overwrite=True, new rows win on key conflict; otherwise existing rows
    are kept. When fresh=True, any existing content is discarded and df becomes
    the sole content of the file.

    Args:
        df: DataFrame to write (must contain CSV_UPSERT_KEYS columns).
        path: Destination CSV file path. Created if it does not exist.
        logger: Logger instance for the completion message.
        overwrite: If True, new rows replace existing rows on key conflict.
        fresh: If True, replace the file wholesale instead of upserting.
    """
    if fresh or not path.exists():
        combined = df
    else:
        existing = pd.read_csv(path)
        combined = pd.concat([existing, df], ignore_index=True)
        keep = "last" if overwrite else "first"
        combined = combined.drop_duplicates(subset=CSV_UPSERT_KEYS, keep=keep)
    combined.to_csv(path, index=False)
    action = "rewritten" if fresh else "upserted"
    logger.info("CSV %s: %s (%d rows)", action, path, len(combined))


_PVBTTF_STRIP_MAP = [
    ("month",   "/E.GEBM", "/E.G3BM", "PVBTTF_M"),
    ("quarter", "/E.GEBQ", "/E.G3BQ", "PVBTTF_Q"),
    ("cal",     "/E.GEBY", "/E.G3BY", "PVBTTF_Y"),
]


def _compute_pvbttf_synthetic(prepared_df: pd.DataFrame) -> pd.DataFrame:
    """Compute PVB/TTF synthetic spread rows (EEX PVB close − EEX TTF close).

    Matches EEX PVB and EEX TTF rows by (symbol index i, market_date).
    Returns synthetic rows in OUTPUT_COLUMNS schema ready to concat.
    """
    synthetics = []
    for strip, pvb_prefix, ttf_prefix, syn_prefix in _PVBTTF_STRIP_MAP:
        for i in range(front_units):
            pvb_sym = f"{pvb_prefix}<{i}>"
            ttf_sym = f"{ttf_prefix}<{i}>"

            pvb = prepared_df[prepared_df["symbol"] == pvb_sym].copy()
            ttf = prepared_df[prepared_df["symbol"] == ttf_sym][
                ["market_date", "close", "low", "high"]
            ].copy()

            if pvb.empty or ttf.empty:
                continue

            for col in ("close", "low", "high"):
                pvb[col] = pd.to_numeric(pvb[col], errors="coerce")
                ttf[col] = pd.to_numeric(ttf[col], errors="coerce")

            merged = pvb.merge(ttf, on="market_date", suffixes=("_pvb", "_ttf"))
            if merged.empty:
                continue

            merged["symbol"] = f"{syn_prefix}<{i}>"
            merged["description"] = f"PVB/TTF gas front {i+1} {strip}"
            merged["commodity"] = "gas"
            merged["exchange"] = "EEX"
            merged["area"] = "Spain"
            merged["strip"] = strip
            merged["product"] = "PVB/TTF"
            merged["close"] = merged["close_pvb"] - merged["close_ttf"]
            merged["low"] = pd.NA
            merged["high"] = pd.NA
            merged["volume"] = pd.NA

            synthetics.append(merged[OUTPUT_COLUMNS])

    if not synthetics:
        return pd.DataFrame(columns=OUTPUT_COLUMNS)
    return pd.concat(synthetics, ignore_index=True)


def fetch_mv_daily(
    username: str,
    password: str,
    start_date: datetime.date,
    end_date: datetime.date,
    fields: list[str] | None = None,
    output: str = "db",
    parallel: bool = False,
    workers: int | None = None,
    overwrite_csv: bool = True,
    fresh_csv: bool = False,
) -> pd.DataFrame:
    """Fetch MV daily data and write to CSV and/or PostgreSQL.

    Main entry point for programmatic use. Fetches the full symbol list defined
    in SYMBOLS for the given date range, enriches the result with symbol metadata
    and computed columns, then routes output to CSV, PostgreSQL, or both.

    Args:
        username: MV API username.
        password: MV API password.
        start_date: First date to fetch (inclusive).
        end_date: Last date to fetch (inclusive).
        fields: MV field names to retrieve; defaults to the module-level FIELDS if None.
        output: Destination — "csv", "db", or "both".
        parallel: If True, fetch chunks concurrently using threads.
        workers: Max thread count when parallel=True.
        overwrite_csv: If True, new rows overwrite existing CSV rows on key conflict.
        fresh_csv: If True, discard the existing CSV and write only the new rows.

    Returns:
        Enriched DataFrame in OUTPUT_COLUMNS schema.
    """
    logger = logging.getLogger("scheduled_mv_daily_to_csv")

    if fields is None:
        fields = FIELDS

    logger.info("Chunk size (days): %s", CHUNK_SIZE_DAYS)

    raw_df = _fetch_daily_in_chunks(
        username=username,
        password=password,
        symbols=list(SYMBOLS.keys()),
        fields=fields,
        startdate=start_date,
        enddate=end_date,
        env=ENVIRONMENT,
        chunk_size_days=CHUNK_SIZE_DAYS,
        symbol_chunk_size=SYMBOL_CHUNK_SIZE,
        parallel=parallel,
        workers=workers,
    )

    result_df = _prepare_output_frame(raw_df)

    synthetic_df = _compute_pvbttf_synthetic(result_df)
    if not synthetic_df.empty:
        result_df = pd.concat([result_df, synthetic_df], ignore_index=True)

    logger.info("Fetched rows: %s", len(result_df))

    if output in ("csv", "both"):
        _upsert_csv(result_df, OUTPUT_PATH, logger, overwrite=overwrite_csv, fresh=fresh_csv)

    if output in ("db", "both"):
        upserted_rows = _upsert_postgres(result_df)
        logger.info("Rows upserted in PostgreSQL: %s", upserted_rows)
        logger.info("PostgreSQL table: %s", DB_TABLE)

    return result_df


def main() -> None:
    """CLI entry point: configure logging, load credentials, and run the daily fetch."""
    _configure_logging()
    logger = logging.getLogger("scheduled_mv_daily_to_csv")
    logger.info("Starting MV daily fetch job")
    logger.info("Environment: %s | Output: %s | Parallel: %s | Workers: %s", ENVIRONMENT, OUTPUT_MODE, PARALLEL_FETCH, PARALLEL_WORKERS)

    try:
        username, password = _load_credentials()
        fetch_mv_daily(
            username=username,
            password=password,
            start_date=START_DATE,
            end_date=END_DATE if END_DATE is not None else datetime.datetime.now().date(),
            fields=FIELDS,
            output=OUTPUT_MODE,
            parallel=PARALLEL_FETCH,
            workers=PARALLEL_WORKERS,
            fresh_csv=FRESH_CSV,
        )
        logger.info("Log file: %s", LOG_PATH)
        logger.info("MV daily fetch job completed successfully")
    except Exception:
        logger.exception("MV daily fetch job failed")
        raise


if __name__ == "__main__":
    main()
