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
- 14,493 data rows (lines starting with a digit), 3,810 other lines.

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
