# AMFI NAV file: what we found

Source: https://www.amfiindia.com/spages/NAVAll.txt
Probed on 21 Nov 2026 (file for 20 Nov 2026), 1.5 MB, 18,303 lines.

## Format
- Semicolon separated, 8 columns:
  Scheme Code; ISIN Div Payout/ISIN Growth; ISIN Div Reinvestment; Scheme Name; Plan; Option; Net Asset Value; Date
- UTF-8 with CRLF line endings, so every line ends in a hidden \r. Strip it before parsing the date.
- Date looks like 20-Nov-2026 (%d-%b-%Y).
- "-" means null (mostly missing ISINs).

## Junk and context lines
- Blank lines contain a single space.
- Category lines, e.g. "Open Ended Schemes(Children's Fund - Childrens' Fund)".
- Fund house lines, e.g. "Axis Mutual Fund".
- Data rows inherit the category and fund house from the lines above them.
- 14,481 data rows (lines matching ^[0-9]+;), 3,822 other lines. A loose "starts with a digit" rule wrongly counts 12 "360 ONE Mutual Fund" headings.

## Gotchas
- Scheme name is NOT unique. Two "Axis Children's Fund, Direct, Growth" rows exist (135762, 135764). Key on scheme code.
- Name casing differs by fund house (BANK OF INDIA LIQUID FUND vs Axis Children's Fund).
- Curly and straight apostrophes are both used.

## Freshness (rows by NAV date)
- 7,823 on 20 Nov (latest business day), 881 on 19 Nov (one day behind).
- 86 on 21 Nov, a Saturday: liquid funds declare NAVs for every calendar day.
- Old clusters on 02 Jul 2018, 24 Apr 2020, 2022 dates, plus a long tail. Roughly a third of listed schemes are stale.
- Plan: scheme_status (active, lagging, stale) in dim_scheme, freshness tests in dbt, a freshness panel in Grafana.

## Quick check
- Axis Children's Fund growth NAV: Direct 31.6264 vs Regular 27.4973, about 15% apart for the same portfolio.

# AMFI NAV history report: what we found

Source: https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt=DD-Mon-YYYY&todt=DD-Mon-YYYY
Probed on 26 Nov 2026 for 02 to 06 Nov 2026: 5.6 MB for one week.

## Format differences from NAVAll.txt
- Column order differs: Scheme Code; NAV Name; Plan; Option; ISIN Div Payout/ISIN Growth; ISIN Div Reinvestment; Net Asset Value; Date
- Option values are upper case (GROWTH) instead of "Growth Option".
- Nulls are empty fields (;;) instead of "-".
- Category lines have extra spaces: "Open Ended Schemes ( Equity Scheme - Multi Cap Fund )".
- Both sources must be conformed to one standard column set in staging.

## Row counts
- One row per scheme per business day: 8,797 / 8,788 / 8,803 / 8,813 / 8,815 for 02 to 06 Nov.
- Sum 44,016 equals the strict-rule row count, so the parse rule reconciles.

## Parsing rule (both files)
- A data row matches ^[0-9]+; (digits then a semicolon).
- Never use "starts with a digit": the fund house "360 ONE Mutual Fund" (formerly IIFL AMC) starts with a digit.

## Sizing
- About 1.1 MB of text per business day, so roughly 5 GB for 20 years of raw text.
- Raw history goes to Parquet in DuckLake; only small gold tables go to Neon (1 GB free).
- The backfill must be chunked by date range and resumable.
