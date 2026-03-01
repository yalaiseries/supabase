import argparse
import csv
import io
import json
import re
import sys
import time
from pathlib import Path
from typing import Iterable
from urllib import error, parse, request


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send Supabase invite/reset links in bulk from a CSV email list."
    )
    parser.add_argument("--supabase-url", required=True, help="Supabase project URL, e.g. https://<ref>.supabase.co")
    parser.add_argument("--service-role-key", required=True, help="SERVICE_ROLE_KEY value")
    parser.add_argument("--input", required=True, help="Path to CSV file")
    parser.add_argument("--email-column", default="email", help="CSV column name containing email addresses")
    parser.add_argument("--name-column", default="", help="Optional CSV column name containing full name")
    parser.add_argument(
        "--mode",
        choices=["auto", "invite", "reset", "both"],
        default="auto",
        help="auto=invite then fallback reset for existing users",
    )
    parser.add_argument(
        "--redirect-to",
        default="",
        help="Optional redirect URL used in invite/recovery links",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and print actions without sending")
    parser.add_argument("--report", default="", help="Optional output CSV report path")
    parser.add_argument("--sleep-seconds", type=float, default=0.0, help="Delay between each email send")
    parser.add_argument("--retry-429", type=int, default=0, help="Retry attempts when API returns 429")
    parser.add_argument("--retry-wait-seconds", type=float, default=30.0, help="Wait time before retrying a 429 response")
    parser.add_argument(
        "--stop-on-consecutive-429",
        type=int,
        default=0,
        help="Stop processing when this many consecutive 429 responses occur (0 disables)",
    )
    return parser.parse_args()


def normalize_email(value: str) -> str:
    return (value or "").strip().lower()


def is_valid_email(value: str) -> bool:
    return bool(EMAIL_RE.match(value))


def read_csv_text(input_value: str) -> str:
    value = (input_value or "").strip()
    if value.lower().startswith(("http://", "https://")):
        with request.urlopen(value, timeout=20) as response:
            return response.read().decode("utf-8-sig", errors="ignore")

    csv_path = Path(value)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    return csv_path.read_text(encoding="utf-8-sig")


def load_contacts(input_value: str, email_column: str, name_column: str = "") -> list[tuple[str, str]]:
    csv_text = read_csv_text(input_value)

    with io.StringIO(csv_text, newline="") as handle:
        reader = csv.DictReader(handle)
        headers = [h.strip() for h in (reader.fieldnames or []) if h]
        if not headers:
            raise ValueError("CSV has no header row")

        resolved_email_col = None
        for h in headers:
            if h.lower() == email_column.lower():
                resolved_email_col = h
                break

        resolved_name_col = None
        if name_column:
            for h in headers:
                if h.lower() == name_column.lower():
                    resolved_name_col = h
                    break
        else:
            for candidate in ("full name", "name"):
                for h in headers:
                    if h.lower() == candidate:
                        resolved_name_col = h
                        break
                if resolved_name_col:
                    break

        contacts_by_email: dict[str, str] = {}
        for row in reader:
            if resolved_email_col:
                candidate = normalize_email(str(row.get(resolved_email_col, "")))
            else:
                candidate = ""
                for h in headers:
                    value = normalize_email(str(row.get(h, "")))
                    if "@" in value:
                        candidate = value
                        break
            if candidate and is_valid_email(candidate):
                full_name = ""
                if resolved_name_col:
                    full_name = str(row.get(resolved_name_col, "")).strip()

                if candidate not in contacts_by_email:
                    contacts_by_email[candidate] = full_name
                elif not contacts_by_email[candidate] and full_name:
                    contacts_by_email[candidate] = full_name

    contacts = sorted(contacts_by_email.items(), key=lambda item: item[0])
    if not contacts:
        raise ValueError("No valid emails found in CSV")
    return contacts


def http_post_json(url: str, headers: dict[str, str], payload: dict) -> tuple[int, str]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url=url, data=body, method="POST")
    for key, value in headers.items():
        req.add_header(key, value)

    try:
        with request.urlopen(req, timeout=20) as response:
            return response.getcode(), response.read().decode("utf-8", errors="ignore")
    except error.HTTPError as e:
        text = e.read().decode("utf-8", errors="ignore")
        return e.code, text
    except (error.URLError, TimeoutError, OSError) as e:
        return 0, str(e)


def send_invite(supabase_url: str, service_role_key: str, email: str, redirect_to: str) -> tuple[int, str]:
    url = f"{supabase_url.rstrip('/')}/auth/v1/invite"
    if redirect_to:
        url = f"{url}?{parse.urlencode({'redirect_to': redirect_to})}"

    headers = {
        "apikey": service_role_key,
        "authorization": f"Bearer {service_role_key}",
        "content-type": "application/json",
    }
    return http_post_json(url, headers, {"email": email})


def send_reset(supabase_url: str, service_role_key: str, email: str, redirect_to: str) -> tuple[int, str]:
    url = f"{supabase_url.rstrip('/')}/auth/v1/recover"
    if redirect_to:
        url = f"{url}?{parse.urlencode({'redirect_to': redirect_to})}"

    headers = {
        "apikey": service_role_key,
        "authorization": f"Bearer {service_role_key}",
        "content-type": "application/json",
    }
    return http_post_json(url, headers, {"email": email})


def short_message(raw: str, max_len: int = 160) -> str:
    text = (raw or "").replace("\n", " ").replace("\r", " ").strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def process_email(
    supabase_url: str,
    service_role_key: str,
    mode: str,
    redirect_to: str,
    email: str,
) -> tuple[str, str, int, str]:
    if mode == "invite":
        code, msg = send_invite(supabase_url, service_role_key, email, redirect_to)
        return (email, "invite", code, short_message(msg))

    if mode == "reset":
        code, msg = send_reset(supabase_url, service_role_key, email, redirect_to)
        return (email, "reset", code, short_message(msg))

    if mode == "both":
        c1, m1 = send_invite(supabase_url, service_role_key, email, redirect_to)
        c2, m2 = send_reset(supabase_url, service_role_key, email, redirect_to)
        status = max(c1, c2)
        msg = f"invite={c1}; reset={c2}; detail={short_message(m1 or m2)}"
        return (email, "both", status, msg)

    invite_code, invite_msg = send_invite(supabase_url, service_role_key, email, redirect_to)
    if 200 <= invite_code < 300:
        return (email, "invite", invite_code, short_message(invite_msg))

    existing_user = invite_code in {400, 409, 422} and ("already" in invite_msg.lower() or "exists" in invite_msg.lower())
    if existing_user:
        reset_code, reset_msg = send_reset(supabase_url, service_role_key, email, redirect_to)
        return (email, "reset", reset_code, short_message(reset_msg))

    return (email, "invite", invite_code, short_message(invite_msg))


def process_email_with_retry(
    supabase_url: str,
    service_role_key: str,
    mode: str,
    redirect_to: str,
    email: str,
    retry_429: int,
    retry_wait_seconds: float,
) -> tuple[str, str, int, str]:
    attempts = max(0, int(retry_429)) + 1
    wait_seconds = max(0.0, float(retry_wait_seconds))

    latest = (email, mode, 0, "")
    for attempt in range(1, attempts + 1):
        latest = process_email(
            supabase_url=supabase_url,
            service_role_key=service_role_key,
            mode=mode,
            redirect_to=redirect_to,
            email=email,
        )
        status = latest[2]
        if status != 429:
            return latest

        if attempt < attempts:
            print(f"  ↳ rate-limited (429), waiting {wait_seconds:.1f}s then retry {attempt}/{attempts - 1}")
            time.sleep(wait_seconds)

    return latest


def write_report(path: Path, rows: Iterable[tuple[str, str, str, int, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["email", "full_name", "action", "http_status", "message"])
        for row in rows:
            writer.writerow(row)


def main() -> int:
    args = parse_args()
    try:
        contacts = load_contacts(args.input, args.email_column, args.name_column)
    except Exception as e:
        print(f"ERROR loading CSV: {e}")
        return 1

    print(f"Loaded {len(contacts)} unique valid emails")
    print(f"Mode: {args.mode}")
    if args.redirect_to:
        print(f"Redirect: {args.redirect_to}")
    if args.sleep_seconds > 0:
        print(f"Per-email delay: {args.sleep_seconds}s")
    if args.retry_429 > 0:
        print(f"429 retry: {args.retry_429} (wait {args.retry_wait_seconds}s)")
    if args.stop_on_consecutive_429 > 0:
        print(f"Stop on consecutive 429: {args.stop_on_consecutive_429}")

    results: list[tuple[str, str, str, int, str]] = []

    if args.dry_run:
        for email, full_name in contacts:
            results.append((email, full_name, "dry-run", 0, "No request sent"))
        print("Dry-run complete. No API calls were made.")
    else:
        consecutive_429 = 0
        for idx, (email, full_name) in enumerate(contacts, start=1):
            email_result = process_email_with_retry(
                supabase_url=args.supabase_url,
                service_role_key=args.service_role_key,
                mode=args.mode,
                redirect_to=args.redirect_to,
                email=email,
                retry_429=args.retry_429,
                retry_wait_seconds=args.retry_wait_seconds,
            )
            result = (email_result[0], full_name, email_result[1], email_result[2], email_result[3])
            results.append(result)
            email_text, name_text, action, status, _ = result
            label = f"{name_text} <{email_text}>" if name_text else email_text
            print(f"[{idx}/{len(contacts)}] {label} -> {action} ({status})")

            if status == 429:
                consecutive_429 += 1
            else:
                consecutive_429 = 0

            if args.stop_on_consecutive_429 > 0 and consecutive_429 >= args.stop_on_consecutive_429:
                print(
                    f"Stopping early due to {consecutive_429} consecutive 429 responses. "
                    "Please wait before retrying remaining users."
                )
                break

            if args.sleep_seconds > 0 and idx < len(contacts):
                time.sleep(max(0.0, float(args.sleep_seconds)))

    if args.report:
        write_report(Path(args.report), results)
        print(f"Report written: {args.report}")

    failed = [] if args.dry_run else [r for r in results if not (200 <= r[3] < 300)]
    if failed:
        print(f"Completed with {len(failed)} non-2xx responses.")
        return 2

    print("Completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
