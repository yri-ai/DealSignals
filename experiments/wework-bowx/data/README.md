# WeWork/BowX Research Data Collection

## Data Sources

### Primary: SEC EDGAR Filings

#### BowX Acquisition Corp (CIK: 0001830210)
- **S-4**: The gold - projections, risk factors, deal terms
- **DEFM14A**: Definitive proxy - shareholder vote materials
- **8-K**: Material events around merger

#### WeWork Inc (CIK: 0001813756)
- **10-K**: Annual reports post-merger (2021, 2022)
- **10-Q**: Quarterly financials
- **8-K**: Material events, earnings

### Supplemental Sources
- Bankruptcy court filings (Chapter 11, Nov 2023)
- News archives (lease liability coverage pre-close)
- Earnings transcripts (management commentary on projections)
- Investor deck (original SPAC presentation with projections)

## Quick Access Links

### EDGAR Links
- [BowX Acquisition Corp](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001830210)
- [WeWork Inc](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001813756)

### Specific Filing Search URLs
- [BowX S-4 Filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001830210&type=S-4&dateb=&owner=exclude&count=100)
- [BowX DEFM14A Filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001830210&type=DEFM14A&dateb=&owner=exclude&count=100)
- [BowX 8-K Filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001830210&type=8-K&dateb=&owner=exclude&count=100)
- [WeWork 10-K Filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001813756&type=10-K&dateb=&owner=exclude&count=100)
- [WeWork 10-Q Filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001813756&type=10-Q&dateb=&owner=exclude&count=100)
- [WeWork 8-K Filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001813756&type=8-K&dateb=&owner=exclude&count=100)

## Directory Structure

```
data/
├── README.md (this file)
├── bowx/
│   ├── s4/
│   ├── defm14a/
│   └── 8k/
├── wework/
│   ├── 10k/
│   ├── 10q/
│   └── 8k/
└── supplemental/
    ├── bankruptcy/
    ├── news/
    ├── transcripts/
    └── investor_deck/
```

## Data Collection Script

Due to SEC EDGAR's restrictions on automated access, you'll need to:

1. **Manual Download Option**: Visit the links above in a browser and download PDFs/HTML files manually
2. **Use the Python script**: `python scripts/download_sec_filings.py` (see below)

## Notes

- SEC EDGAR requires a User-Agent header with contact information for automated access
- Rate limiting: Max 10 requests per second
- The WeWork/BowX merger closed in October 2021
- Key filing date range: 2020-2021 for merger docs, 2021-2023 for post-merger performance
