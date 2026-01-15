# WeWork/BowX SPAC Merger — Ground Truth (Q1-Q36)

**Source Document:** BowX Acquisition Corp S-4/A Filing (September 2021)
**Deal:** WeWork merger via SPAC, valued at $9B
**Outcome:** Bankruptcy filed November 2023
**Ground Truth Established:** Questions 1-36 of 40

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

## Q21: Who are the key executives and what is their track record?

**Answer:** CEO Sandeep Mathrani — experienced real estate executive, but traditional property management background.

| Company                         | Role | Period              | Notes                          |
| ------------------------------- | ---- | ------------------- | ------------------------------ |
| Brookfield Properties Retail    | CEO  | Aug 2018 - Feb 2020 | 1.5 years                      |
| General Growth Properties (GGP) | CEO  | Dec 2010 - Aug 2018 | Led post-bankruptcy turnaround |
| Vornado Realty Trust            | EVP  | 2002 - 2010         | 9 years                        |
| Forest City Ratner              | EVP  | 1994 - 2002         | Retail development             |

**Positive:** GGP turnaround experience (GGP went bankrupt in 2009, Mathrani helped recapitalize).

**Concern:** All experience is traditional property management (malls, retail REITs). WeWork is a different business model — subscription/membership, tech-adjacent, flex-space operations with $34B in lease liabilities (not assets).

**Source:** S-4, Management section; LinkedIn

---

## Q22: What is SoftBank's role and ongoing obligations?

**Answer:** SoftBank is WeWork's largest shareholder, primary lender, and co-obligor on critical credit facilities.

**SoftBank Exposure as of June 30, 2021:**

| Facility                             | Amount                   | Notes                 |
| ------------------------------------ | ------------------------ | --------------------- |
| 2020 LC Facility (Letters of Credit) | $1.7B outstanding        | SBG is **co-obligor** |
| SoftBank Senior Unsecured Debt       | $2.2B outstanding        | Direct lending        |
| LC Debt Facility                     | $349M outstanding        | —                     |
| SoftBank Senior Secured Notes        | $1.1B available          | Undrawn               |
| **Total SoftBank Exposure**          | **~$4.25B+ outstanding** | Plus $1.1B available  |

**Critical Terms:**

- LC Facility termination: **February 10, 2023** (18 months post-deal)
- SoftBank is **co-obligor** — if WeWork can't pay, SoftBank is on the hook
- Facility secured by "substantially all assets" of WeWork

**Red Flag — SoftBank Conflict:**
SoftBank _needed_ this SPAC deal to create exit liquidity for their $4B+ exposure. The LC facility expired Feb 2023 — without public listing or refinancing, WeWork collapses and SoftBank loses billions.

**Source:** S-4, Pages 135, 282

---

## Q23: What related party transactions exist?

**Answer:** Extensive SoftBank sweetheart deals and Neumann landlord conflicts.

**SoftBank Penny Warrants:**

| Transaction                           | Shares         | Value at $10/share              |
| ------------------------------------- | -------------- | ------------------------------- |
| Penny warrants on LC facility renewal | 14,431,991     | ~$144M                          |
| Penny warrants at merger closing      | 47,366,404     | ~$474M                          |
| **Total penny warrants**              | **61,798,395** | **~$618M for essentially free** |

**Adam Neumann Landlord Conflicts:**

- WeWork leased buildings from entities **Neumann had ownership interest in**
- WeCap Investment Group (Steven Langman, former board member) also had landlord relationships
- Filing admits: _"the interests of the landlord entity and its stockholders may not align with the interests of the Company"_
- Filing admits: _"Company may have achieved more favorable terms if such transactions had not been entered into with related parties"_

**Source:** S-4, Pages 40, F-81, F-256-257

---

## Q24: What are management's incentives/compensation in the deal?

**Answer:** Executives received substantial compensation while the company was burning cash and needed lifelines.

**2020 Executive Compensation:**

| Executive        | Role                 | Salary | Bonus  | Options | **Total**  |
| ---------------- | -------------------- | ------ | ------ | ------- | ---------- |
| Sandeep Mathrani | CEO                  | $1.28M | $1.50M | $4.76M  | **$7.54M** |
| Benjamin Dunham  | CFO                  | $446K  | $790K  | $1.29M  | **$2.53M** |
| Anthony Yazbeck  | President, Intl      | $789K  | $1.57M | $1.24M  | **$3.63M** |
| Shyam Gidumal    | President, Americas  | $568K  | $317K  | $1.30M  | **$2.19M** |
| Samad Jahansouz  | Chief People Officer | $600K  | $1.29M | $1.49M  | **$3.39M** |

**Former Executive Golden Parachutes (2020):**

| Executive                            | Total Payout | Key Components                                |
| ------------------------------------ | ------------ | --------------------------------------------- |
| Arthur Minson (Former Co-CEO)        | **$8.74M**   | $8.3M severance                               |
| Sebastian Gunningham (Former Co-CEO) | **$11.30M**  | $8.3M severance + $2.2M loan forgiveness      |
| Eugen Miropolski (Former President)  | **$32.10M**  | $12.9M loan forgiveness + $10.3M tax gross-up |

**Red Flags:**

- CEO got $7.5M while company burned $224M/month
- $8.3M severance packages for departing Co-CEOs
- Miropolski's $32M exit included loan forgiveness AND company paid his taxes on it
- Option grants at $2.10/share — executives get cheap stock while SPAC investors pay $10/share
- Total exec comp ~$71M in a year the company had 3.8 months runway

**Source:** S-4, Pages 313-315, Executive Compensation Tables

---

## Q25: What is Adam Neumann's ongoing relationship/exposure?

**Answer:** Despite being ousted after 2019 IPO collapse, Neumann retained substantial ownership and voting control.

**Neumann's Holdings Post-Merger:**

| Holding                                    | Amount                                |
| ------------------------------------------ | ------------------------------------- |
| WE Holdings LLC                            | 57,790,545 shares (sole voting power) |
| ANINCENTCO entities (1, 2, 3)              | 544,030 shares                        |
| WeWork Partnerships Profits Interest Units | 19,884,233 units                      |
| Class C Common Stock                       | 19,884,233 shares                     |
| **Total Voting Power Post-Merger**         | **10.9% - 11.7%**                     |

**Red Flags:**

- Neumann was fired for cause but retained ~11% voting power
- Gets ~20M profit interest units — additional upside despite his failures
- Was both landlord AND CEO (leased his own buildings to WeWork)
- No clawback of his prior compensation despite company's near-collapse

**Source:** S-4, Pages 40, beneficial ownership tables

---

## Q26: What are the top disclosed risk factors?

**Answer:** The fatal structural flaw is DISCLOSED — but buried on page 34-35 among dozens of risk factors.

**THE SMOKING GUN DISCLOSURE (Pages 34-35):**

Direct quotes from the S-4:

> _"The average length of the initial term of its leases is approximately **15 years**, and the average term of its membership agreements is **15 months**."_

> _"As of June 30, 2021, the Company's subsidiaries' future undiscounted minimum lease cost payment obligations under signed operating and finance leases was **$36.6 billion** and committed sales contracts to be recognized as revenue in the future totaled approximately **$3 billion**."_

**Additional Risk Disclosures:**

| Risk Category       | Disclosure                                                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Lease inflexibility | _"long-term leases that, with limited exceptions, do not contain early termination provisions"_                                |
| Fixed costs         | _"fixed monthly or quarterly payments that are not tied to space utilization or the size of its member base"_                  |
| No exit option      | _"the Company has not been able to, and may not be able to, reduce its rent under the lease or otherwise terminate the lease"_ |
| Cumulative losses   | $12.5B+ in net losses (2018-H1 2021)                                                                                           |
| Landlord actions    | _"a small number of landlords have sued to enforce the corporate guarantees"_                                                  |
| Security draws      | _"landlords have drawn under the letters of credit or demanded payment under the surety bonds"_                                |

**Related Party Conflicts (Page 40):**

- SoftBank debt facilities = related party transactions
- Neumann retained board observer rights (starting Feb 2022) despite being fired
- $14M paid in 2020 for indemnification of former executives' legal fees

**Red Flag:** The fatal information WAS IN THE FILING. The 26:1 liability mismatch ($36.6B vs $3B) was explicitly stated. Investors had the data — they didn't act on it.

**Source:** S-4, Pages 34-35, 40

---

## Q27: Are there any material litigation or disputes?

**Answer:** Yes — BowX itself had accounting issues requiring restatement, and a director had prior bankruptcy.

**BowX Warrant Accounting Issue:**

- BowX had to **restate financial statements** in 2021
- Warrants originally classified as equity should have been liabilities
- Filing warns of _"potential for litigation or other disputes... claims invoking federal and state securities laws"_

**BowX Director Background:**

- Hamid Hashemi (BowX director) was CEO of **iPic Entertainment**
- iPic Entertainment filed **Chapter 11 bankruptcy in August 2019**
- Hashemi oversaw a company that failed — now on the board approving WeWork deal

**BowX Material Weakness (Page 82):**

> _"we did not maintain effective internal control over financial reporting as of December 31, 2020 because of a material weakness in our internal control over financial reporting related to the accounting for a significant and unusual transaction related to the warrants"_

**Impact:** Required restatement of audited financial statements. Management concluded internal controls were **NOT effective**.

**Source:** S-4, Page 82, BowX financial statements section

---

## Q28: Are there going concern disclosures?

**Answer:** YES — BowX explicitly warned the combined company might not be able to pay its bills.

**The Warning (Page 72):**

> _"the cash held by New WeWork and its subsidiaries... after the Closing **may not be sufficient to allow it to operate and pay its bills as they become due**"_

> _"Any such event in the future may negatively impact the analysis regarding **New WeWork's ability to continue as a going concern** at such time."_

**BowX's Own Cash Position (F-230):**

| Metric                    | Amount                                    |
| ------------------------- | ----------------------------------------- |
| Cash in operating account | **$506,000**                              |
| Working capital           | **$(2.9M) deficit**                       |
| Trust account dependency  | 100% reliant on PIPE + redemption outcome |

**The Circular Logic Problem:**

1. WeWork has 3.8 months runway
2. BowX has $506K in operating cash
3. Deal requires minimum $1B cash condition
4. If redemptions are high, they might waive the minimum
5. If they waive the minimum, combined company "may not be sufficient to pay its bills"

**Translation:** They explicitly warned investors that if too many BowX shareholders redeem, the merged company might not survive — but they might close the deal anyway.

**Source:** S-4, Pages 72, F-230

---

## Q29: What did the auditors say?

**Answer:** Ernst & Young issued a CLEAN OPINION with NO going concern language.

**Auditor:** Ernst & Young LLP

**Opinion (F-98):**

> _"In our opinion, the consolidated financial statements present fairly, in all material respects, the financial position of the Company at December 31, 2020 and 2019..."_

**Critical Audit Matters Flagged:**

| Matter                          | Issue                                           | Amount                           |
| ------------------------------- | ----------------------------------------------- | -------------------------------- |
| Impairment of Long-lived Assets | COVID impact, restructuring, lease terminations | **$1.142B impairment**           |
| Valuation of Equity Instruments | Complex Level III fair value estimates          | $419M in convertible liabilities |

**What's MISSING: Going Concern Paragraph**

Despite these conditions at audit date, EY issued NO going concern emphasis:

| Red Flag              | Status at Audit Date |
| --------------------- | -------------------- |
| Cash runway           | ~4 months            |
| Monthly burn          | $224M                |
| Lease obligations     | $36.6B               |
| Net loss (2020)       | $3.8B                |
| Accumulated deficit   | ~$12.5B              |
| Dependent on SoftBank | Yes                  |

**Auditor Failure Analysis:**

EY likely relied on:

1. SoftBank's ongoing credit support ($4B+ in facilities)
2. Expectation that SPAC deal would close
3. Management's turnaround projections

**But this is circular logic:** Company survives IF SoftBank keeps supporting AND IF SPAC closes. Neither was guaranteed.

**Red Flag:** The gatekeepers (auditors) gave a clean bill of health to a company with 3.8 months runway and $36.6B in non-cancelable obligations.

**Source:** S-4, Pages F-98 to F-99, Ernst & Young Report

---

## Q30: Are there any material weaknesses in internal controls?

**Answer:** YES — BowX disclosed a material weakness in internal controls.

**BowX Material Weakness (Page 82):**

> _"we did not maintain effective internal control over financial reporting as of December 31, 2020 because of a material weakness in our internal control over financial reporting related to the accounting for a significant and unusual transaction related to the warrants"_

**Impact:**

- Required **restatement of audited financial statements**
- Warrants reclassified from equity to liabilities
- Management concluded controls **NOT effective**

**Note:** This was BowX's internal control issue, not WeWork's. However, it raises questions about BowX's capability to evaluate a complex target.

**Source:** S-4, Page 82

---

## Q31: What is the board composition post-merger?

**Answer:** 9-member board with significant SoftBank representation and limited independence.

**Board Composition:**

| Director           | Affiliation                                 | Independence       |
| ------------------ | ------------------------------------------- | ------------------ |
| **Marcelo Claure** | SoftBank COO, **WeWork Executive Chairman** | ❌ SoftBank        |
| **Michel Combes**  | President, SoftBank Group International     | ❌ SoftBank        |
| **Kirthiga Reddy** | Partner, SoftBank Investment Advisers       | ❌ SoftBank        |
| Sandeep Mathrani   | WeWork CEO                                  | ❌ Management      |
| Bruce Dunlevie     | Benchmark Capital (VC investor since 2012)  | ⚠️ Investor        |
| Deven Parekh       | Insight Partners Managing Director          | ⚠️ Investor        |
| Jeffrey Sine       | The Raine Group co-founder                  | ⚠️ Investment bank |
| Vivek Ranadivé     | BowX Chairman & Co-CEO                      | ⚠️ SPAC sponsor    |
| Véronique Laury    | Weee Consulting founder                     | ✅ Independent     |

**Control Summary:**

- SoftBank-affiliated directors: **3 of 9 (33%)**
- Truly independent directors: **1 of 9 (11%)**
- Management/Investors/Sponsors: **5 of 9 (56%)**

**Red Flags:**

- SoftBank has 33% of board seats PLUS 65% voting control
- Marcelo Claure is both SoftBank COO AND WeWork Executive Chairman (dual role)
- Only 1 arguably independent director (Véronique Laury)
- Hamid Hashemi (executive, not board) was CEO of iPic Entertainment when it filed Ch.11 bankruptcy in Aug 2019

**Source:** S-4, Pages 297-301, "Management of New WeWork Following the Business Combination"

---

## Q32: What is the voting structure post-merger?

**Answer:** SoftBank controls 65.2% of voting power — absolute majority control.

**Post-Merger Ownership (Assuming Redemption Scenario):**

| Shareholder                        | Shares          | % Ownership |
| ---------------------------------- | --------------- | ----------- |
| **SBG (SoftBank Group)**           | 364,289,126     | **52.7%**   |
| **SVFE (SoftBank Vision Fund)**    | 81,029,831      | **12.5%**   |
| **SoftBank TOTAL**                 | **445,318,957** | **65.2%**   |
| Adam Neumann                       | 58,334,575      | 9.0%        |
| Bruce Dunlevie (Benchmark)         | 19,459,762      | 3.0%        |
| Vivek Ranadivé (BowX)              | 6,732,184       | 1.0%        |
| Murray Rode (BowX)                 | 6,347,254       | 1.0%        |
| All directors/officers (18 people) | 26,940,161      | 4.2%        |

**Control Implications:**

| Threshold                   | Who Controls                |
| --------------------------- | --------------------------- |
| Simple majority (50%+)      | **SoftBank alone**          |
| Supermajority (66%+)        | SoftBank + any small holder |
| SoftBank + Neumann combined | **74.2%**                   |

**What SoftBank Can Unilaterally Do:**

- Elect all directors
- Approve any transaction
- Block any shareholder proposal
- Amend bylaws/charter

**Red Flag:** Public shareholders have NO meaningful governance voice. SoftBank controls the board AND the vote. This is a controlled company in all but name.

**Source:** S-4, Pages 324-326, Beneficial Ownership of Securities

---

## Q33: What are the lock-up agreements?

**Answer:** Different lock-up periods for different insiders — Neumann gets preferential treatment.

**Lock-Up Periods:**

| Shareholder                | Lock-Up Period          | Shares | % of Company |
| -------------------------- | ----------------------- | ------ | ------------ |
| **Adam Neumann**           | **270 days (9 months)** | 58.3M  | 9.0%         |
| SoftBank (SBG + SVFE)      | 1 year                  | 445.3M | 65.2%        |
| Benchmark Capital          | 1 year                  | 19.5M  | 3.0%         |
| BowX Sponsor               | 1 year                  | 4.9M   | <1%          |
| Vivek Ranadivé             | 1 year                  | 6.7M   | 1.0%         |
| Murray Rode                | 1 year                  | 6.3M   | 1.0%         |
| CEO/CFO (Mathrani, Dunham) | 1 year                  | —      | —            |

**Early Release Triggers (BowX Sponsors):**

> _"if the last reported sale price... equals or exceeds **$12.00 per share** for any 20 trading days within any 30-trading day period commencing at least **150 days** after the initial Business Combination"_

**Key Loopholes:**

- Transfers to affiliates, funds, partners permitted
- Creation of liens/pledges for loans permitted (can borrow against shares)
- Neumann has special carve-out for existing pledge arrangements with StarBright WW LP
- MFN clause: if any insider gets better terms, everyone gets same terms

**Timeline of Potential Sales (Deal closed Oct 2021):**

| Date                | Who Can Sell                    |
| ------------------- | ------------------------------- |
| Mar 2022 (150 days) | BowX sponsors IF stock hits $12 |
| Jul 2022 (270 days) | **Adam Neumann**                |
| Oct 2022 (1 year)   | SoftBank, Benchmark, Management |

**Red Flags:**

- Neumann (fired founder) can sell 3 months before SoftBank and others
- Pledge arrangements allow effective monetization before lock-up expires
- MFN clause creates cascade risk if any party is released early

**Source:** S-4, Pages 223, Annex M (Lock-Up Agreement)

---

## Q34: What registration rights exist?

**Answer:** Major shareholders have demand and piggyback registration rights — company pays all costs.

**Who Has Registration Rights:**

| Holder                | Shares  | %     | Rights                |
| --------------------- | ------- | ----- | --------------------- |
| SoftBank (SBG + SVFE) | 445.3M  | 65.2% | ✅ Demand + Piggyback |
| Adam Neumann          | 58.3M   | 9.0%  | ✅ Demand + Piggyback |
| Benchmark Capital     | 19.5M   | 3.0%  | ✅ Demand + Piggyback |
| BowX Sponsor          | 4.9M    | <1%   | ✅ Demand + Piggyback |
| Management/Directors  | Various | —     | ✅ Piggyback          |

**Key Terms:**

| Term                 | Detail                                         |
| -------------------- | ---------------------------------------------- |
| Demand registrations | Up to **3 demands** (excluding short-form)     |
| Piggyback rights     | Can tag along on any company registration      |
| Expenses             | **Company bears all costs**                    |
| Cut-back provisions  | If oversubscribed, some holders may be reduced |

**What This Means:**

1. SoftBank can demand registration of 445M shares (65% of company)
2. When one party files, everyone else can "piggyback" — creating cascade
3. Cash-strapped WeWork pays all legal/filing costs
4. Post-lock-up, massive supply can hit the market

**Red Flag:** Registration rights are the mechanism for SoftBank to convert 65% stake into cash. Company pays for insider liquidity.

**Source:** S-4, Pages 225, 332, Annex I (Registration Rights Agreement)

---

## Q35: What was the market context at deal time?

**Answer:** WeWork claimed COVID accelerated flex-space demand, but their own numbers showed the opposite.

**WeWork's Market Claims (S-4 Pages 229-236):**

| Claim                                                               | Source Cited     | Page |
| ------------------------------------------------------------------- | ---------------- | ---- |
| "Multi trillion-dollar commercial real estate market"               | WeWork           | 231  |
| Flex space to reach 13.3%-22.2% of U.S. office by 2030              | CBRE 2019 report | 231  |
| "30% of all office space will be consumed flexibly by 2030"         | JLL 2020 report  | 232  |
| ~23% market share in U.S./Canada flex space                         | CBRE estimates   | 231  |
| "COVID-19 pandemic has accelerated the shift to flexible workspace" | WeWork assertion | 232  |

**WeWork's Position Claims:**

| Claim                                                      | Detail                          | Page |
| ---------------------------------------------------------- | ------------------------------- | ---- |
| "One of the largest flexible space providers in the world" | 52M rentable sq ft globally     | 231  |
| "57% of 2021 Fortune 100 companies were WeWork members"    | As of June 2021                 | 233  |
| "$15 billion of capital invested"                          | Described as "competitive moat" | 233  |
| 763 locations in 38 countries                              | As of June 30, 2021             | 233  |

**The Contradiction — What They Said vs. What the Numbers Showed:**

| Claim                                    | Reality                            |
| ---------------------------------------- | ---------------------------------- |
| "COVID accelerated shift to flex"        | Revenue DOWN 38.6%                 |
| "Proven business model through downturn" | Occupancy DOWN to 46%              |
| "Maintained consistent revenue of $3.2B" | Hiding that H1 2021 was collapsing |
| "$1.6B liquidity access"                 | Actually 3.8 months runway         |

**Cherry-Picked Statistics:**

- "23% of NYC office leasing in Q2 2021" — Easy to capture high % of a tiny market during pandemic lows
- "1% of NYC commercial office stock" — Only 1% penetration after 10 years and billions invested

**Competition Section (Page 235):** ONE paragraph, no named competitors, no market share comparison, no mention of IWG/Regus (larger, profitable competitor) or Knotel (bankrupt Jan 2021).

**Source:** S-4, Pages 229-236, "Information About WeWork"

---

## Q36: Were comparable transactions disclosed?

**Answer: NO — Zero comparables, no valuation benchmarking.**

**Standard Valuation Elements — None Provided:**

| Element                           | Disclosed? |
| --------------------------------- | ---------- |
| Fairness opinion                  | ❌ NO      |
| Discounted cash flow (DCF)        | ❌ NO      |
| Comparable public companies       | ❌ NO      |
| Precedent transactions            | ❌ NO      |
| EV/Revenue multiple justification | ❌ NO      |
| EV/EBITDA multiple justification  | ❌ NO      |

**What Should Have Been Disclosed:**

**Public Company Comparables:**

| Company         | Description                                | Status         |
| --------------- | ------------------------------------------ | -------------- |
| IWG plc (Regus) | Global flex space leader, 3,300+ locations | **Profitable** |
| Servcorp        | Premium serviced offices                   | **Profitable** |

**Precedent Transactions:**

| Event               | Date           | Relevance                                                 |
| ------------------- | -------------- | --------------------------------------------------------- |
| Knotel bankruptcy   | January 2021   | Flex-space competitor **liquidated** 9 months before deal |
| WeWork IPO (failed) | September 2019 | Pulled at $47B, then $20B, then cancelled                 |

**Implied Valuation Multiples (Not Disclosed or Justified):**

| Metric             | WeWork (at $9B EV)    | Question                      |
| ------------------ | --------------------- | ----------------------------- |
| EV/Revenue (2020)  | ~2.8x                 | How does this compare to IWG? |
| EV/Revenue (2021E) | ~3.5x                 | Premium or discount to peers? |
| EV/EBITDA          | N/A (negative EBITDA) | Can't compute — no earnings   |

**Red Flags:**

- $8.8B deal with zero valuation benchmarking
- IWG (profitable competitor) not mentioned — likely because comparison would show WeWork overvalued
- Knotel bankruptcy (most recent flex-space transaction) completely ignored
- Board self-certified as "qualified" to determine fairness

**Source:** S-4 Filing — absence confirmed through search for "IWG," "Regus," "comparable," valuation multiples

---

## Summary of Key Red Flags (Pre-Deal)

**Financial Red Flags:**

1. **Revenue declining:** -38.6% H1 2021 vs H1 2020
2. **Negative unit economics:** Losing ~$150/member/month at location level
3. **<4 months runway:** Without SPAC cash, bankruptcy was imminent
4. **Aggressive assumptions:** 44%→86% occupancy in 2 years, 101% "total occupancy"
5. **Already revised down:** EBITDA projections cut in half before deal closed
6. **Cash burn accelerating:** Operating cash burn up 588% YoY

**Structural Red Flags:** 7. **FATAL: $34B lease obligations** — 26:1 ratio vs member commitments 8. **Non-cancelable leases:** 65% of obligations extend past 2026 (10-15 year terms) 9. **Structural mismatch:** Long-term fixed costs vs. month-to-month revenue 10. **Churn not disclosed:** Material metric omission for a membership business

**Governance Red Flags:** 11. **NO FAIRNESS OPINION:** $8.8B deal with no independent valuation 12. **NO COMPARABLES ANALYSIS:** No DCF, no comps, no precedent transactions 13. **Board self-certified:** "Qualified" to determine fairness themselves

**Sponsor & Management Red Flags:** 14. **SoftBank conflict:** $4B+ exposure, needed deal to create exit liquidity 15. **SoftBank penny warrants:** 61.8M shares for essentially free (~$618M value) 16. **Neumann retained 11% voting power:** Despite being fired for cause 17. **Neumann landlord conflicts:** Leased his own buildings to WeWork 18. **$71M executive comp:** While company had 3.8 months runway 19. **$32M golden parachute:** Miropolski got loan forgiveness + tax gross-ups 20. **$8.3M severance packages:** For departing Co-CEOs during cash crisis

**Risk Disclosure & Gatekeeper Red Flags:** 21. **Fatal flaw disclosed but buried:** $36.6B vs $3B mismatch on page 34-35 22. **Going concern warning:** "May not be sufficient to pay its bills" (Page 72) 23. **BowX material weakness:** Failed internal controls, required restatement 24. **No going concern from EY:** Clean audit opinion despite 3.8 months runway 25. **BowX director's bankruptcy:** Hashemi was CEO of iPic when it filed Ch.11

**Governance & Control Red Flags:** 26. **SoftBank controls 65.2%:** Absolute majority voting control 27. **SoftBank + Neumann = 74.2%:** Supermajority control 28. **Board dominated by SoftBank:** 3 of 9 directors SoftBank-affiliated 29. **Only 1 independent director:** Véronique Laury only truly independent board member 30. **Dual role conflict:** Marcelo Claure is both SoftBank COO AND WeWork Executive Chairman

**Lock-Up & Liquidity Red Flags:** 31. **Neumann preferential lock-up:** 270 days vs 1 year for everyone else 32. **Lock-up loopholes:** Pledge arrangements allow effective early monetization 33. **Registration rights cascade:** One demand triggers piggyback rights for all insiders 34. **Company pays registration costs:** Cash-strapped WeWork funds insider liquidity

**Market & Valuation Red Flags:** 35. **COVID narrative contradiction:** Claimed "accelerated demand" while revenue down 38.6% 36. **No comparables disclosed:** IWG (profitable competitor) never mentioned 37. **Knotel bankruptcy ignored:** Most relevant precedent (flex-space failure) omitted 38. **Competition section inadequate:** One paragraph, no named competitors

---

## Document Sources

| Page            | Content                                                          |
| --------------- | ---------------------------------------------------------------- |
| 16              | Pre-transaction enterprise value ($8.8B)                         |
| 34-35           | **KEY:** Risk factors with $36.6B vs $3B disclosure              |
| 40              | Related party transactions, Neumann conflicts                    |
| 72              | Going concern warning ("may not be sufficient to pay its bills") |
| 82              | BowX material weakness in internal controls                      |
| 130-131         | Deal negotiation timeline and LOI terms                          |
| 135, 282        | SoftBank credit facilities and obligations                       |
| 147-148         | Projections and key assumptions                                  |
| 223             | Lock-up agreements, Neumann 270-day lock-up                      |
| 225, 332        | Registration rights agreements                                   |
| 229-236         | Market context, competitive position claims                      |
| 254             | Income statement (revenue, expenses, operating loss)             |
| 286             | Cash flow statement                                              |
| 291             | Contractual obligations table (lease liabilities)                |
| 297-301         | Board composition post-merger                                    |
| 313-315         | Executive compensation tables                                    |
| 324-326         | Beneficial ownership, voting structure                           |
| Q&A section     | No fairness opinion disclosure                                   |
| Annex I         | Registration Rights Agreement                                    |
| Annex M         | Lock-Up Agreement terms                                          |
| F-54            | Member revenue commitments                                       |
| F-81, F-256-257 | Related party transactions notes                                 |
| F-98 to F-99    | Ernst & Young audit report (clean, no going concern)             |
| F-165           | Note 18 - Leasing Arrangements                                   |
| F-230           | BowX liquidity and going concern basis                           |

**Filing:** BowX Acquisition Corp S-4/A, September 2021
**URL:** https://www.sec.gov/Archives/edgar/data/1813756/000119312521263309/d166510ds4a.htm

---

---

## Q37: What is the exit/refinancing strategy for the $36.6B in lease obligations?

**Answer:** NO CREDIBLE EXIT STRATEGY WAS DISCLOSED.

**Use of SPAC Proceeds:**

| Source                         | Amount                   |
| ------------------------------ | ------------------------ |
| PIPE Investment                | $800M (80M shares @ $10) |
| BowX Trust (after redemptions) | ~$333M                   |
| **Total Cash Raised**          | **~$1.13B**              |

**What $1.13B Covers:**

| Use                       | Amount | Duration    |
| ------------------------- | ------ | ----------- |
| Monthly cash burn         | $224M  | ~5 months   |
| Interest expense (annual) | ~$300M | ~3.8 months |
| CapEx requirement         | ~$400M | <3 months   |

**What $1.13B Does NOT Cover:**

| Obligation                      | Amount   | Gap            |
| ------------------------------- | -------- | -------------- |
| Lease obligations               | $36.6B   | 32x proceeds   |
| Near-term lease payments (2022) | ~$3.5B   | 3x proceeds    |
| SoftBank LC Facility maturity   | Feb 2023 | 16 months away |

**The Math Problem:**

- SPAC proceeds: ~$1.13B
- Lease obligations: $36.6B
- **Coverage ratio: 3.1%**

**Stated "Strategy":**

1. "Asset-light" transition to management agreements (minimal progress)
2. Lease renegotiations with landlords (no specifics)
3. Location closures and consolidation (ongoing losses during transition)
4. Achieve profitability by 2022 (required 44%→86% occupancy jump)

**Red Flag:** The filing contained NO concrete plan for addressing the $36.6B structural mismatch. The SPAC cash bought ~12-18 months of runway, not a solution.

**Source:** S-4 projections, pro forma financials

---

## Q38: What post-merger integration or business model changes were planned?

**Answer:** MINIMAL STRUCTURAL CHANGES — same business model, same risks.

**What Changed Post-Merger:**

| Element           | Pre-Merger                     | Post-Merger               |
| ----------------- | ------------------------------ | ------------------------- |
| Legal structure   | Private                        | Public (NYSE: WE)         |
| Cash position     | $855M                          | ~$2B (with SPAC proceeds) |
| SoftBank debt     | $4.25B                         | Same                      |
| Lease obligations | $36.6B                         | Same                      |
| Business model    | Long leases, short memberships | **Unchanged**             |

**What Did NOT Change:**

1. **Core structural mismatch:** 15-year leases vs. 15-month memberships remained
2. **Unit economics:** Still losing money per member at location level
3. **SoftBank dependency:** Still reliant on SoftBank credit facilities
4. **Governance:** SoftBank still controlled 65% voting power
5. **Cost structure:** Fixed lease costs remained non-cancelable

**"Turnaround" Plan:**

| Initiative            | Reality Check                                    |
| --------------------- | ------------------------------------------------ |
| Occupancy improvement | Required near-impossible 44%→86% jump            |
| Cost cutting          | Already done $1.5B in 2020; limited further cuts |
| Asset-light model     | <5% of locations were management agreements      |
| Geographic focus      | Still operating 700+ locations globally          |

**Red Flag:** The SPAC was a LIQUIDITY EVENT, not a TRANSFORMATION. The fundamental business model that caused the 2019 IPO collapse remained intact.

**Source:** S-4, investor presentation, management discussion

---

## Q39: What debt covenants and restrictions existed?

**Answer:** MULTIPLE RESTRICTIVE COVENANTS with SoftBank holding significant control.

**SoftBank Credit Facility Terms:**

| Facility              | Amount            | Maturity     | Key Terms                                    |
| --------------------- | ----------------- | ------------ | -------------------------------------------- |
| 2020 LC Facility      | $1.7B outstanding | Feb 10, 2023 | SBG is co-obligor                            |
| Senior Unsecured Debt | $2.2B             | Various      | Direct SoftBank lending                      |
| LC Debt Facility      | $349M             | —            | —                                            |
| Senior Secured Notes  | $1.1B available   | —            | Collateralized by "substantially all assets" |

**Covenant Structure:**

| Covenant Type       | Requirement                                    |
| ------------------- | ---------------------------------------------- |
| Collateral          | "Substantially all assets" pledged to SoftBank |
| Negative pledge     | Restrictions on additional secured debt        |
| Change of control   | Triggers upon ownership changes                |
| Financial covenants | Minimum liquidity requirements                 |

**What Happens if WeWork Defaults:**

1. SoftBank can accelerate all facilities
2. SoftBank can seize "substantially all assets"
3. LC Facility letters of credit get called
4. Landlords can draw on security deposits
5. Cross-default triggers across all facilities

**The Circular Problem:**

- WeWork needs cash → Only SoftBank will lend
- SoftBank has $4B+ exposure → Needs WeWork to survive
- WeWork survives → Only if SoftBank keeps lending

**Red Flag:** WeWork was effectively a SoftBank subsidiary operating under the guise of a public company.

**Source:** S-4, Pages 135, 282, credit facility descriptions

---

## Q40: Overall Recommendation — Would you invest?

**Answer:** UNAMBIGUOUS NO — This deal had fatal structural flaws visible in the filing.

**Summary of Fatal Flaws:**

| Category        | Finding                                                   | Severity |
| --------------- | --------------------------------------------------------- | -------- |
| **Structural**  | $36.6B obligations vs. $3B commitments (12:1 mismatch)    | FATAL    |
| **Financial**   | <4 months runway, negative unit economics                 | Critical |
| **Governance**  | No fairness opinion, no comparables, SoftBank 65% control | Critical |
| **Gatekeepers** | Clean audit despite going concern risk, material weakness | High     |
| **Management**  | $71M exec comp during cash crisis, Neumann retained 11%   | High     |

**The Core Problem (from Page 34-35):**

> _"The average length of the initial term of its leases is approximately **15 years**, and the average term of its membership agreements is **15 months**."_

> _"Future undiscounted minimum lease cost payment obligations... was **$36.6 billion** and committed sales contracts to be recognized as revenue in the future totaled approximately **$3 billion**."_

**This is a business that:**

- Has 12x more obligations than revenue commitments
- Cannot exit its leases
- Loses money on every member
- Has no path to profitability without miraculous occupancy gains
- Is controlled by a conflicted party (SoftBank) desperate for exit liquidity

**What the Market Said:**

| Date                        | Valuation | Change    |
| --------------------------- | --------- | --------- |
| Jan 2019 (SoftBank)         | $47B      | Peak      |
| Sept 2019 (Failed IPO)      | $47B→$0   | Collapsed |
| Oct 2019 (SoftBank bailout) | $7B       | -85%      |
| Oct 2021 (SPAC)             | $9B       | +29%      |
| Nov 2023 (Bankruptcy)       | $45M      | -99.5%    |

**The Investment Thesis Required Believing:**

1. Occupancy would nearly double (44%→86%) in 2 years
2. Landlords would renegotiate $36.6B in leases
3. COVID would permanently accelerate flex-space demand (while revenue was -38.6%)
4. Unit economics would flip positive despite no evidence
5. SoftBank conflicts wouldn't harm public shareholders

**Verdict:** Every piece of information needed to reject this deal was IN THE S-4 FILING. The fatal structural flaw was explicitly disclosed on pages 34-35. Investors who read the filing could have avoided 99.5% losses.

**Source:** Complete S-4 analysis, Q1-Q39 findings

---

## Progress Status

**Completed:** Q1-Q40 (100% of 40-question methodology)
