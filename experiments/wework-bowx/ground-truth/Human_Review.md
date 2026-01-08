# WeWork/BowX SPAC Merger — Ground Truth (Q1-Q20)

**Source Document:** BowX Acquisition Corp S-4/A Filing (September 2021)
**Deal:** WeWork merger via SPAC, valued at $9B
**Outcome:** Bankruptcy filed November 2023
**Ground Truth Established:** Questions 1-20 of 40

---

## Q1: What is WeWork's revenue for the most recent reported period?

**Answer:**

- H1 2021 (6 months ended June 30): **$1,191M**
- FY 2020 (full year): **$3,416M**

**Source:** S-4, Page 254, Condensed Consolidated Results of Operations

---

## Q2: What is the revenue growth rate year-over-year?

**Answer:**

- H1 2021 vs H1 2020: **-38.6%** ($1,191M vs $1,939M)
- FY 2020 vs FY 2019: **-1.2%** ($3,416M vs $3,459M)
- FY 2019 vs FY 2018: **+89.8%** ($3,459M vs $1,822M)

**Source:** S-4, Page 254, Condensed Consolidated Results of Operations

---

## Q3: What are the operating losses for the most recent period?

**Answer:**

- H1 2021: **$(2,356M)** operating loss
- H1 2020: **$(2,040M)** operating loss
- FY 2020: **$(4,347M)** operating loss

**Source:** S-4, Page 254, "Loss from operations" line item

---

## Q4: What is the cash burn rate?

**Answer:**

- Cash used in operating activities (H1 2021): **$(1,159M)**
- Cash used in investing activities (H1 2021): **$(187M)**
- **Total burn (H1 2021): $(1,346M)**
- **Monthly burn rate: ~$224M/month**

**Calculation:**

```
Operating: $(1,158,957) + Investing: $(186,628) = $(1,345,585)
$(1,345,585) ÷ 6 months = $224M/month
```

**Source:** S-4, Page 286, Statement of Cash Flows

---

## Q5: What is the cash runway at current burn rate?

**Answer:**

- Cash at end of H1 2021: **$855M**
- Monthly burn rate: **$224M**
- **Runway: ~3.8 months**

**Calculation:**

```
$855M ÷ $224M/month = 3.8 months
```

**Source:** S-4, Page 286 (cash balance), calculated runway

**Note:** WeWork required the SPAC proceeds to survive. Without the deal, they had less than 4 months of cash.

---

## Q6: What is the stated path to profitability and timeline?

**Answer:**
WeWork projected reaching **Adjusted EBITDA profitability in 2022** with $243M positive EBITDA.

| Year      | Revenue     | Adjusted EBITDA |
| --------- | ----------- | --------------- |
| 2020A     | $3,210M     | $(1,754M)       |
| 2021E     | $2,655M     | $(1,463M)       |
| **2022E** | **$4,348M** | **$243M**       |
| 2023E     | $5,650M     | $1,256M         |
| 2024E     | $6,785M     | $1,996M         |

**Source:** S-4, Page 147, "Current Projections"

**Note:** Initial projections showed 2022E EBITDA of $485M. This was revised down to $243M before the deal closed.

---

## Q7: What are the key assumptions underlying the projections?

**Answer:**

| Assumption            | 2020A | 2021E | 2022E | 2023E | 2024E |
| --------------------- | ----- | ----- | ----- | ----- | ----- |
| Physical Occupancy    | 44%   | 74%   | 86%   | 87%   | 86%   |
| Total Occupancy       | 45%   | 81%   | 94%   | 101%  | 100%  |
| Physical Memberships  | 380k  | 541k  | 706k  | 776k  | 839k  |
| Total Memberships     | 387k  | 591k  | 772k  | 907k  | 937k  |
| Net ARPM              | $494  | $463  | $494  | $528  | $547  |
| Physical Workstations | 865k  | 730k  | 823k  | 894k  | 971k  |

**Source:** S-4, Page 147-148, "Key assumptions underlying the Current Projections"

**Red Flags:**

- Occupancy assumed to nearly double from 44% to 86% in two years
- Total occupancy of 101% in 2023 assumes "All Access" fills beyond physical capacity
- Revenue growth of 64% (2021→2022) projected while H1 2021 showed -39% YoY decline

---

## Q8: What is the contribution margin per membership?

**Answer:** **NEGATIVE**

| Metric                          | H1 2021     | Per Member/Month |
| ------------------------------- | ----------- | ---------------- |
| Revenue                         | $1,191M     | ~$441            |
| Location operating expenses     | $1,599M     | ~$592            |
| **Location-level contribution** | **$(408M)** | **$(151)**       |

WeWork loses approximately **$150/month per member** at the location level, before any corporate overhead (sales, G&A, etc.).

**Source:** S-4, Page 254 (revenue & location expenses), Page 147 (memberships) — calculated

---

## Q9: What is the revenue per available desk/workstation?

**Answer:**

- Net ARPM (revenue per membership): **$463-494/month**
- Revenue per physical workstation: **~$3,600-3,700/year**

**Calculation:**

```
2020A: $3,210M revenue ÷ 865k workstations = $3,711/workstation/year
2021E: $2,655M revenue ÷ 730k workstations = $3,637/workstation/year
```

**Source:** S-4, Page 147

---

## Q10: What is the occupancy rate and trend?

**Answer:**

| Year  | Physical Occupancy | Total Occupancy | Trend                   |
| ----- | ------------------ | --------------- | ----------------------- |
| 2019A | 74%                | 74%             | Pre-COVID baseline      |
| 2020A | 44%                | 45%             | COVID collapse          |
| 2021E | 74%                | 81%             | Projected full recovery |
| 2022E | 86%                | 94%             | Projected growth        |

**Source:** S-4, Page 147

**Key Finding:** Occupancy crashed from 74% to 44% due to COVID. Projections assumed not just recovery but exceeding pre-COVID levels within 2 years.

---

## Q11: What is the member churn rate?

**Answer:** **NOT DISCLOSED**

The S-4 does not disclose member churn rate directly.

**Inferrable data:**

- Physical memberships: 517k (2019A) → 380k (2020A) = -26% decline
- However, this conflates churn with COVID-driven demand collapse

**Red Flag:** Material metric omission. Churn is critical for a membership business but not provided.

**Source:** S-4, Page 147 (membership counts only)

---

## Q12: What is the average revenue per member?

**Answer:** **$463-494/month (Net ARPM)**

| Year  | Net ARPM   |
| ----- | ---------- |
| 2020A | $494/month |
| 2021E | $463/month |
| 2022E | $494/month |
| 2024E | $547/month |

**Source:** S-4, Page 147, "Core + New Leased Net ARPM"

---

## Q13: What are the total lease obligations?

**Answer:** **$34.1 BILLION**

Non-cancelable operating lease commitments as of June 30, 2021.

**Additional disclosure:** Per footnote (1), this _excludes_ an additional **$2.4 billion** relating to executed non-cancelable leases that have not yet commenced.

**True total exposure: ~$36.5 billion**

**Source:** S-4, Page 291, Contractual Obligations table

---

## Q14: What is the lease duration/maturity profile?

**Answer:**

| Period              | Amount      | % of Total |
| ------------------- | ----------- | ---------- |
| Remainder 2021      | $1.24B      | 3.6%       |
| 2022                | $2.52B      | 7.4%       |
| 2023                | $2.60B      | 7.6%       |
| 2024                | $2.65B      | 7.8%       |
| 2025                | $2.68B      | 7.9%       |
| **2026 and beyond** | **$22.45B** | **65.8%**  |
| **Total**           | **$34.14B** | 100%       |

**Key Finding:** Two-thirds of lease obligations extend past 2026 — these are 10-15+ year commitments.

**Source:** S-4, Page 291, Contractual Obligations table

---

## Q15: What are the early termination provisions?

**Answer:** **NON-CANCELABLE**

Per footnote (1) on Page 291: These are "non-cancelable operating leases" with "initial or remaining lease terms in excess of one year."

The leases include:

- Escalation clauses (rent increases over time)
- Lease incentive receivables
- Contingent lease cost payments

WeWork has **no general right to exit** these obligations early without landlord consent and likely significant breakage costs.

**Source:** S-4, Page 291, Contractual Obligations footnote (1)

---

## Q16: Sensitivity Analysis — 70% Occupancy Scenario

**Assumptions:**

- Baseline (2021E): 74% occupancy → 591k members → $3.3B revenue
- Revenue scales linearly with occupancy
- Lease costs are FIXED (non-cancelable)

**Calculation:**

```
Members: 591k × (70/74) = 559k
Revenue: 559k × $463 ARPM × 12 = $3.1B

Costs:
  Lease payments (fixed):    $2.7B
  Other location costs:      $0.6B
  Corporate overhead:        $1.0B
  Total:                     $4.3B

Operating Loss:              $(1.2B)
```

**Result:** At 70% occupancy (just 4 points below plan), WeWork loses **$1.2B/year**.

---

## Q17: Sensitivity Analysis — 50% Occupancy Scenario

**Calculation:**

```
Members: 591k × (50/74) = 399k
Revenue: 399k × $463 ARPM × 12 = $2.2B

Costs:
  Lease payments (fixed):    $2.7B  ← Revenue alone doesn't cover this
  Other location costs:      $0.4B
  Corporate overhead:        $1.0B
  Total:                     $4.1B

Operating Loss:              $(1.9B)
```

**Result:** At 50% occupancy, WeWork loses **$1.9B/year**. Revenue doesn't even cover lease costs alone.

---

## THE STRUCTURAL MISMATCH (Critical Finding)

| What WeWork Owes Landlords      | What Members Owe WeWork   |
| ------------------------------- | ------------------------- |
| **$34.1 billion**               | **$1.3 billion**          |
| 10-15 year non-cancelable terms | Month-to-month agreements |

**Ratio: 26:1**

This is the structural flaw that caused bankruptcy:

- If occupancy drops 10%, WeWork still owes landlords full rent
- Members can walk away with 30 days notice
- WeWork needed 75%+ occupancy just to break even on rent
- The SPAC raised ~$1.3B, but annual lease payments alone were ~$2.7B

**Source:** S-4, Page 291 (obligations), F-54 (member commitments)

---

## Q18: What is the enterprise value of the deal?

**Answer:** **$8.8 billion** (pre-transaction enterprise value)

| Date           | Milestone                 | Enterprise Value | Equity Value |
| -------------- | ------------------------- | ---------------- | ------------ |
| Dec 22, 2020   | BowX preliminary proposal | $9.79B           | —            |
| Jan 15, 2021   | Initial LOI draft         | $10.11B          | $8.82B       |
| Feb 4, 2021    | Final LOI signed          | $9.80B           | $8.53B       |
| **Final deal** | **Pre-transaction EV**    | **$8.8B**        | —            |

**Key observation:** Valuation **decreased** 13% during negotiations ($10.1B → $8.8B).

**Deal structure:**

- Merger consideration: 851.3M shares of BowX Class A common stock at $10.00/share
- Implied pre-transaction equity value: $8.53B
- Minimum cash condition: $1.0B (trust account + PIPE proceeds)
- PIPE investment: $500M minimum

**Source:** S-4, Pages 16, 130-131

---

## Q19: What valuation methodology was used?

**Answer:** **NONE DISCLOSED / NO FAIRNESS OPINION**

Direct quote from S-4:

> "The BowX board of directors **did not obtain a third-party valuation or fairness opinion** in connection with its determination to approve the Business Combination."

The board claimed they were "qualified to conclude that the Business Combination was fair from a financial perspective" based on their own "financial skills and background."

The board also self-determined "that WeWork's fair market value was at least 80% of BowX's net assets" — the minimum threshold required under SPAC rules.

**Source:** S-4, Q&A section

---

## Q20: What comparable companies/transactions were used to justify valuation?

**Answer:** **NOT PROVIDED**

Without a fairness opinion, the S-4 contains:

- ❌ No DCF analysis
- ❌ No comparable public companies analysis
- ❌ No precedent transactions analysis
- ❌ No justification for the multiple paid
- ❌ No independent valuation of any kind

**Direct disclosure to investors:**

> "Investors will be relying on the judgment of the BowX board of directors... and assuming the risk that the BowX board of directors may not have properly valued such business."

**Red Flag Summary:**

| Normal SPAC Deal                      | WeWork/BowX Deal     |
| ------------------------------------- | -------------------- |
| Fairness opinion from investment bank | None                 |
| DCF analysis                          | None disclosed       |
| Comparable companies analysis         | None disclosed       |
| Multiple justified against peers      | None disclosed       |
| Independent valuation                 | Board self-certified |

**Critical context:** This is an $8.8B deal for a company:

- Burning $224M/month
- With negative unit economics (-$150/member/month)
- With $34B in non-cancelable lease obligations
- With 3.8 months cash runway
- And **no independent party validated the price**

**Source:** S-4, Q&A section

---

## Summary of Key Red Flags (Pre-Deal)

1. **Revenue declining:** -38.6% H1 2021 vs H1 2020
2. **Negative unit economics:** Losing ~$150/member/month at location level
3. **<4 months runway:** Without SPAC cash, bankruptcy was imminent
4. **Aggressive assumptions:** 44%→86% occupancy in 2 years, 101% "total occupancy"
5. **Already revised down:** EBITDA projections cut in half before deal closed
6. **Cash burn accelerating:** Operating cash burn up 588% YoY
7. **FATAL: $34B lease obligations** — 26:1 ratio vs member commitments
8. **Non-cancelable leases:** 65% of obligations extend past 2026 (10-15 year terms)
9. **Structural mismatch:** Long-term fixed costs vs. month-to-month revenue
10. **Churn not disclosed:** Material metric omission for a membership business
11. **NO FAIRNESS OPINION:** $8.8B deal with no independent valuation
12. **NO COMPARABLES ANALYSIS:** No DCF, no comps, no precedent transactions
13. **Board self-certified:** "Qualified" to determine fairness themselves

---

## Document Sources

| Page        | Content                                              |
| ----------- | ---------------------------------------------------- |
| 16          | Pre-transaction enterprise value ($8.8B)             |
| 130-131     | Deal negotiation timeline and LOI terms              |
| 147-148     | Projections and key assumptions                      |
| 254         | Income statement (revenue, expenses, operating loss) |
| 286         | Cash flow statement                                  |
| 291         | Contractual obligations table (lease liabilities)    |
| Q&A section | No fairness opinion disclosure                       |
| F-54        | Member revenue commitments                           |
| F-165       | Note 18 - Leasing Arrangements                       |

**Filing:** BowX Acquisition Corp S-4/A, September 2021
**URL:** <https://www.sec.gov/Archives/edgar/data/1813756/000119312521263309/d166510ds4a.htm>
