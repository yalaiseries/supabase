import argparse
import csv
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare smart invite batches from Supabase status CSV."
    )
    parser.add_argument("--input", required=True, help="Path to status CSV")
    parser.add_argument("--output-dir", required=True, help="Folder for batch CSV files")
    parser.add_argument(
        "--statuses",
        default="needs_invite",
        help="Comma-separated statuses to include (default: needs_invite)",
    )
    parser.add_argument("--batch-size", type=int, default=15, help="Rows per batch (default: 15)")
    parser.add_argument(
        "--email-column",
        default="email",
        help="Input email column name (default: email)",
    )
    parser.add_argument(
        "--name-column",
        default="full_name",
        help="Input name column (default: full_name; optional)",
    )
    parser.add_argument(
        "--summary-file",
        default="batch_summary.csv",
        help="Summary filename to generate inside output-dir",
    )
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def normalized_statuses(raw: str) -> set[str]:
    return {item.strip().lower() for item in raw.split(",") if item.strip()}


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    rows = load_rows(input_path)
    if not rows:
        print("No rows found in input CSV.")
        return 1

    statuses = normalized_statuses(args.statuses)
    email_col = args.email_column
    name_col = args.name_column

    filtered: list[dict[str, str]] = []
    for row in rows:
        status = str(row.get("status", "")).strip().lower()
        email = str(row.get(email_col, "")).strip().lower()
        if not email:
            continue
        if statuses and status not in statuses:
            continue
        filtered.append(
            {
                "email": email,
                "full_name": str(row.get(name_col, "")).strip(),
                "status": status,
            }
        )

    if not filtered:
        print("No matching rows after filtering.")
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)

    summary_rows: list[dict[str, str]] = []
    batch_size = max(1, int(args.batch_size))

    batch_index = 1
    for start in range(0, len(filtered), batch_size):
        chunk = filtered[start : start + batch_size]
        batch_file = output_dir / f"batch_{batch_index:02d}.csv"
        with batch_file.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["email", "full_name"])
            writer.writeheader()
            for item in chunk:
                writer.writerow({"email": item["email"], "full_name": item["full_name"]})

        summary_rows.append(
            {
                "batch": f"{batch_index:02d}",
                "batch_file": str(batch_file),
                "count": str(len(chunk)),
                "first_email": chunk[0]["email"],
                "last_email": chunk[-1]["email"],
            }
        )
        batch_index += 1

    summary_file = output_dir / args.summary_file
    with summary_file.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["batch", "batch_file", "count", "first_email", "last_email"],
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"Filtered rows: {len(filtered)}")
    print(f"Batches created: {len(summary_rows)}")
    print(f"Summary: {summary_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
