#!/usr/bin/env python3
"""
Download SEC EDGAR filings for WeWork/BowX research.

This script downloads the key SEC filings needed for the DealSignals research project.
Files are saved to experiments/wework-bowx/data/ (gitignored due to size).

Usage:
    python scripts/download_sec_filings.py
    python scripts/download_sec_filings.py --dry-run
    python scripts/download_sec_filings.py --filing s4  # Download only S-4

SEC EDGAR Requirements:
    - User-Agent header with contact info required
    - Rate limit: max 10 requests/second (we use 0.5s delay)
    - See: https://www.sec.gov/os/accessing-edgar-data
"""

import argparse
import time
from dataclasses import dataclass
from pathlib import Path

import httpx

# SEC EDGAR configuration
SEC_BASE_URL = "https://www.sec.gov"
SEC_ARCHIVES_URL = f"{SEC_BASE_URL}/Archives/edgar/data"

# Required by SEC - must include contact info
USER_AGENT = "DealSignals Research (research@example.com)"

# Rate limiting - SEC allows max 10 req/sec, we're conservative
REQUEST_DELAY = 0.5  # seconds between requests


@dataclass
class Filing:
    """Represents an SEC filing to download."""

    company: str  # "bowx" or "wework" (for folder organization)
    cik: str  # SEC CIK number (without leading zeros for URL)
    filing_type: str  # "S-4", "10-K", etc.
    accession: str  # Accession number (e.g., "000119312521263309")
    primary_doc: str  # Primary document filename
    description: str  # Human-readable description
    date: str  # Filing date


# Key filings for WeWork/BowX research
# NOTE: The SPAC merger S-4 filings were filed under WeWork's CIK (1813756)
# because WeWork was the registrant for the combined company post-merger.
FILINGS = [
    # ===================
    # SPAC Merger Filings (filed under WeWork CIK 1813756)
    # ===================
    Filing(
        company="merger",
        cik="1813756",
        filing_type="S-4/A",
        accession="000119312521263309",
        primary_doc="d166510ds4a.htm",
        description="S-4/A - Final merger registration statement (THE key document)",
        date="2021-09-03",
    ),
    Filing(
        company="merger",
        cik="1813756",
        filing_type="S-4/A",
        accession="000119312521274442",
        primary_doc="d166510ds4a.htm",
        description="S-4/A - Amendment with updated financials",
        date="2021-09-17",
    ),
    Filing(
        company="merger",
        cik="1813756",
        filing_type="S-4",
        accession="000119312521161979",
        primary_doc="d166510ds4.htm",
        description="S-4 - Initial merger registration statement",
        date="2021-05-18",
    ),
    # =======================
    # WeWork Post-Merger Filings (CIK 1813756)
    # Accession numbers from SEC EDGAR API query 2026-01-13
    # =======================
    Filing(
        company="wework",
        cik="1813756",
        filing_type="10-K",
        accession="000181375622000003",
        primary_doc="we-20211231.htm",
        description="10-K - 2021 Annual Report (first as public company)",
        date="2022-03-17",
    ),
    Filing(
        company="wework",
        cik="1813756",
        filing_type="10-K",
        accession="000181375623000016",
        primary_doc="we-20221231.htm",
        description="10-K - 2022 Annual Report",
        date="2023-03-29",
    ),
    # Key 10-Qs tracking deterioration
    Filing(
        company="wework",
        cik="1813756",
        filing_type="10-Q",
        accession="000181375622000035",
        primary_doc="we-20220630.htm",
        description="10-Q - Q2 2022",
        date="2022-08-08",
    ),
    Filing(
        company="wework",
        cik="1813756",
        filing_type="10-Q",
        accession="000181375622000049",
        primary_doc="we-20220930.htm",
        description="10-Q - Q3 2022",
        date="2022-11-14",
    ),
    Filing(
        company="wework",
        cik="1813756",
        filing_type="10-Q",
        accession="000181375623000040",
        primary_doc="we-20230331.htm",
        description="10-Q - Q1 2023",
        date="2023-05-10",
    ),
    Filing(
        company="wework",
        cik="1813756",
        filing_type="10-Q",
        accession="000181375623000059",
        primary_doc="we-20230630.htm",
        description="10-Q - Q2 2023 (pre-bankruptcy)",
        date="2023-08-08",
    ),
    # Bankruptcy-related 8-Ks
    Filing(
        company="wework",
        cik="1813756",
        filing_type="8-K",
        accession="000114036123056371",
        primary_doc="ef20015885_8k.htm",
        description="8-K - Bankruptcy proceedings update",
        date="2023-12-05",
    ),
    Filing(
        company="wework",
        cik="1813756",
        filing_type="8-K",
        accession="000114036123059419",
        primary_doc="ef20017367_8k.htm",
        description="8-K - Bankruptcy plan confirmation",
        date="2023-12-26",
    ),
]


def get_filing_url(filing: Filing) -> str:
    """Construct the SEC EDGAR URL for a filing."""
    return f"{SEC_ARCHIVES_URL}/{filing.cik}/{filing.accession}/{filing.primary_doc}"


def get_filing_index_url(filing: Filing) -> str:
    """Get the filing index page URL (lists all documents in filing)."""
    return f"{SEC_ARCHIVES_URL}/{filing.cik}/{filing.accession}/"


def download_filing(
    filing: Filing,
    output_dir: Path,
    client: httpx.Client,
    dry_run: bool = False,
) -> bool:
    """Download a single filing and save to disk."""

    # Create output path
    subdir = output_dir / filing.company / filing.filing_type.lower().replace("/", "-")
    subdir.mkdir(parents=True, exist_ok=True)

    # Output filename includes date for clarity
    filename = f"{filing.date}_{filing.primary_doc}"
    output_path = subdir / filename

    url = get_filing_url(filing)

    if dry_run:
        print(f"  [DRY RUN] Would download: {filing.description}")
        print(f"            URL: {url}")
        print(f"            To:  {output_path}")
        return True

    if output_path.exists():
        print(f"  [SKIP] Already exists: {output_path.name}")
        return True

    print(f"  [GET] {filing.description}")
    print(f"        {url}")

    try:
        response = client.get(url)
        response.raise_for_status()

        # Save the file
        output_path.write_bytes(response.content)
        size_mb = len(response.content) / (1024 * 1024)
        print(f"        Saved: {output_path.name} ({size_mb:.2f} MB)")

        # Rate limiting
        time.sleep(REQUEST_DELAY)
        return True

    except httpx.HTTPStatusError as e:
        print(f"        ERROR: HTTP {e.response.status_code}")
        return False
    except Exception as e:
        print(f"        ERROR: {e}")
        return False


def download_all_exhibits(
    filing: Filing,
    output_dir: Path,
    client: httpx.Client,
    dry_run: bool = False,
) -> int:
    """Download all exhibits from a filing's index page."""

    index_url = get_filing_index_url(filing)

    if dry_run:
        print(f"  [DRY RUN] Would fetch index: {index_url}")
        return 0

    try:
        response = client.get(index_url)
        response.raise_for_status()

        # Parse links from index page (simple regex, not full HTML parsing)
        import re

        links = re.findall(r'href="([^"]+\.(htm|pdf|xml))"', response.text, re.IGNORECASE)

        downloaded = 0
        for link, _ in links:
            if link.startswith("http"):
                continue  # Skip external links

            doc_url = f"{index_url}{link}"
            doc_response = client.get(doc_url)

            if doc_response.status_code == 200:
                subdir = output_dir / filing.company / filing.filing_type.lower().replace("/", "-")
                subdir.mkdir(parents=True, exist_ok=True)

                doc_path = subdir / f"{filing.date}_{link}"
                doc_path.write_bytes(doc_response.content)
                downloaded += 1
                time.sleep(REQUEST_DELAY)

        return downloaded

    except Exception as e:
        print(f"        ERROR fetching index: {e}")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Download SEC EDGAR filings for WeWork/BowX research"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be downloaded without downloading",
    )
    parser.add_argument(
        "--filing",
        type=str,
        help="Download only specific filing type (e.g., 's4', '10-k')",
    )
    parser.add_argument(
        "--company",
        type=str,
        choices=["merger", "wework"],
        help="Download only for specific category",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/wework-bowx/data"),
        help="Output directory (default: experiments/wework-bowx/data)",
    )
    parser.add_argument(
        "--with-exhibits",
        action="store_true",
        help="Also download all exhibits from each filing",
    )
    args = parser.parse_args()

    # Filter filings based on args
    filings_to_download = FILINGS

    if args.company:
        filings_to_download = [f for f in filings_to_download if f.company == args.company]

    if args.filing:
        filing_type = args.filing.upper().replace("-", "/")
        filings_to_download = [
            f for f in filings_to_download if filing_type in f.filing_type.upper()
        ]

    if not filings_to_download:
        print("No filings match the specified filters.")
        return

    print("=" * 70)
    print("DealSignals SEC Filing Downloader")
    print("=" * 70)
    print(f"Output directory: {args.output}")
    print(f"Filings to download: {len(filings_to_download)}")
    print(f"Dry run: {args.dry_run}")
    print()

    # Create HTTP client with required headers
    headers = {
        "User-Agent": USER_AGENT,
        "Accept-Encoding": "gzip, deflate",
    }

    success = 0
    failed = 0

    with httpx.Client(headers=headers, timeout=120, follow_redirects=True) as client:
        for filing in filings_to_download:
            print(f"\n[{filing.company.upper()}] {filing.filing_type} - {filing.date}")

            if download_filing(filing, args.output, client, args.dry_run):
                success += 1

                if args.with_exhibits and not args.dry_run:
                    exhibit_count = download_all_exhibits(filing, args.output, client)
                    if exhibit_count:
                        print(f"        + {exhibit_count} exhibits")
            else:
                failed += 1

    print()
    print("=" * 70)
    print(f"Completed: {success} succeeded, {failed} failed")
    print("=" * 70)

    if not args.dry_run and success > 0:
        print(f"\nFiles saved to: {args.output}")
        print("\nNote: These files are gitignored due to size.")
        print("Re-run this script to download on a new machine.")


if __name__ == "__main__":
    main()
