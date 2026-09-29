# CBO Risk-Based Pricing Platform

A Flask web app that converts the "Furtuu Risk-Based Price" Excel workbook into a
multi-product, multi-user platform:

- **Login system** with two roles: `admin` (full edit rights) and `user` (Input Dashboard only).
- **One dashboard per original sheet**, per product: Scorecard, Risk-Adjusted Pricing,
  Cost of Fund, PD Transformation, Reference Tables (Vlookup sheet).
- **Input Dashboard**: pick a product from a dropdown, select the "Assessment Result" for
  every scorecard row (exactly like column E in the original sheet), and the app
  recalculates the weighted score, grade, PD and interest rate live.
- **Admin area**: edit every number in the workbook — category weights, sub-parameter
  weights, scoring attributes/scores, cost-of-fund funding sources, RWA mapping,
  repayment-schedule/tenure rates, operational cost components, PD-grade stress values,
  and the pricing waterfall inputs (Cost of Capital, Target ROE, LGD, EAD, access fee...).
  You can **add or delete** categories, sub-parameters, scoring attributes, funding
  sources, RWA options, repayment schedules and operational cost components.
- **Multi-product / value-chain support**: "Add New Product" (Admin menu) creates a brand
  new, fully independent value chain (e.g. Horticulture, Dairy). You can clone an
  existing product's full structure as a starting point, or start blank. Every table is
  scoped by `product_id`, so editing one product's numbers **never** touches another
  product — except renaming a product, which correctly updates its name everywhere
  *that same* product appears.

## Quick start

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Open http://127.0.0.1:5000 — the database (SQLite, `instance/furtuu.db`) and default
users are created automatically on first run.

**Default accounts** (change immediately):
- Admin: `admin` / `admin123`
- Loan officer (user role): `loanofficer` / `officer123`

## Project layout

```
run.py                     entry point
config.py                  Flask config (reads DATABASE_URL / SECRET_KEY env vars)
app/
  __init__.py               app factory
  models.py                 SQLAlchemy models (Product, ScoreCategory, SubParameter,
                             ScoringOption, PDGrade, CostOfFundSource, RWAOption,
                             RepaymentSchedule, OperationalCostComponent, PricingInput, User)
  calculations.py           pure calculation engine — every formula from the workbook
  seed.py                   creates default admin/user + seeds the Furtuu product with
                             the exact figures from the source Excel file
  blueprints/
    auth.py                 login / logout / user management
    dashboards.py            read-only per-sheet dashboards
    input_dashboard.py       the interactive Input Dashboard
    admin.py                 all CRUD (products, scorecard builder, pricing inputs,
                              cost of fund, reference tables, PD grades)
  templates/                 Jinja2 + Bootstrap 5 templates
  static/css/style.css
```

## How the formulas map to the workbook

| Workbook sheet | Where in the app |
|---|---|
| Furtuu- Score card Weighted | `calculations.compute_scorecard()` + Scorecard Dashboard / Input Dashboard |
| Risk-Adjusted Price | `calculations.compute_pricing()` + Pricing Dashboard |
| Cost of Fund | `calculations.compute_cost_of_fund()` + Cost of Fund Dashboard |
| PD Transformation / S&P PD and Rating | `calculations.compute_pd_transformation()` + PD Transformation Dashboard |
| Vlookup sheet | RWA options / Repayment schedules / Operational cost components — Reference Dashboard |

Weighted score, grade breakpoints (≥90 Grade 1 … <30 Grade 8), the PD lookup, the
Cost of Fund weighted average, the PD-Transformation multiplier
`(Upper Bound PD + Stress) / Upper Bound PD`, and the full pricing waterfall
(Target Return + Cost of Fund + Expected Credit Loss + Operational Cost + Tenure Charge,
less the Access Fee) are all reproduced exactly as in the spreadsheet and verified
against it — e.g. seeded Furtuu total weighted score = 94.4, Grade 1, cost of fund =
4.500% (4,500.17 ETB on a 100,000 ETB loan), matching the source file cell-for-cell.

**One intentional correction:** in the source file, the "Repayment/Tenure charge" input
(cell E28) was pointed at the *13-month Poultry Layer* schedule (1.6%) even though the
sheet is pricing the *9-month Furtuu* product. The seeded data here instead uses the
correct "9 months-Grains (Furtuu)" schedule (0.9%), which changes the final annual
interest rate from the original's 23.75% to 23.05%. You can flip it back to the original
mismatched selection in Admin → Pricing Inputs → Repayment Schedule if you want an exact
replica including that quirk.

## What's in this version (Clean & Productive Use Energy Financing update)

This build folds in the **"Clean and Productive Use Energy Financing — Risk Based
Pricing"** workbook on top of the original Furtuu platform. It ships as **5 products**:

- **Furtuu (Grain Value Chain)** — unchanged, the original product.
- **Animal & Livestock**, **Cereals**, **Horticulture**, **MSME (Value-Adding
  Agri-Business)** — new, seeded from the new workbook's own scorecards
  (`Animal-Livestock`, `Cireals`, `Horticulture- Score card`, `MSME-Scorecard`), each
  with its own weights, scoring options and default assessment (all four sum to 100%
  weight, matching the source file).

New sheets from that workbook, and where they live in the app:

| Workbook sheet | Where in the app |
|---|---|
| `PD Calibration` | Product → **PD Grades & Calibration** (Admin) / **PD Calibration** (Dashboard). Calibrated PD = grade weight × sector-average PD (26% by default), replacing the Agri+Digital stress multiplier for these 4 products. Toggle per product. |
| `LGD- Calibration` | **LGD Calibration** (Admin + Dashboard). Two categories — Insurance Coverage (unsecured) and Collateral Coverage (secured) — each mapping a coverage range to Applicable LGD = 1 − reduction. Pick a tier on Pricing Inputs, the Input Dashboard, or the LGD Calibration dashboard; it overrides the manual LGD % everywhere pricing runs. |
| `Partener-Funding Scheme` + `Justification` + `Impact-range` | **Partner-Funding Scheme** (Admin + Dashboard). Seed Money, Guarantee Fund / De-risking, Matching Fund, Subsidized Scheme Financing, and Technical Support each discount whichever waterfall input(s) they affect — Cost of Fund, LGD, Operational Cost, EAD/equity — directly, before the rest of the waterfall runs. This is separate from, and stacks with, the simpler flat-rate NGO Support mechanism. |
| `NGO pricing` / the NGO-support range table | **NGO Support** (unchanged mechanism) — reseeded with this workbook's own ranges (>50% → 2.0%, 40%-50% → 1.4%, ... 0% → 0%, capped at 2%). |
| `Eligibility` + `Weight summary` ("New Parameters") | **Eligibility** — Water Availability, ESG Risk Screening, Irrigation Access, Temperature Suitability, Flood Risk Exposure. |
| `Cost of Fund`, `Vlookup sheet`, `S&P PD and Rating` / `PD Transformation` | Same dashboards as before, reseeded with this workbook's own figures (Cost of Fund weighted average ≈4.53%; RWA Retail 75% / Non-Retail 100%; Monthly/Quarterly/Semi-Annual repayment add-ons; Tech/Commission/Miscellaneous op-cost = 1.37%). |
| `Normal-Risk-Adjusted Price-MSME` / `Risk-Adjusted Price-Non retail` | `calculations.compute_pricing()`. These two sheets share one formula; MSME defaults to Retail RWA + the Insurance LGD table, the other three products default to Non-Retail RWA + the Collateral LGD table. Unlike the original Furtuu sheet, **the repayment schedule is a flat add-on rate, not scaled by tenure/12** — each product has an `apply_tenure_scaling` flag so Furtuu keeps its original tenure-scaled behaviour while these 4 match the new sheets exactly. |
| `Grade 2`, `Sheet1`, `Sheet3` | Legacy/scratch sheets left over from earlier drafts of this workbook (broken `#REF!`/`#N/A` formulas, superseded tables) — not reproduced; their intended behaviour is superseded by the sheets above. |

**Two corrections made vs. the literal source file** (same spirit as the Furtuu
correction below): (1) `Risk-Adjusted Price-Non retail`'s LGD lookup pointed at the
*reduction* column instead of the *applicable LGD* column, which would make more
collateral coverage produce a **higher** price — fixed so Applicable LGD = 1 −
reduction everywhere, matching how the MSME sheet already did it correctly. (2) The
top pricing scenario's PD in the source file was hard-wired to a specific cell on the
Horticulture sheet regardless of which product/grade was actually being priced; this
app uses each product's own scorecard-assessed grade instead.

**Security note:** the copy of this app this was built from had a live Postgres
connection string with a plaintext password hard-coded as the fallback in
`database.py`/`.env`. That's been removed — the app now defaults to local SQLite
with no setup, and `DATABASE_URL` is available if you want to point it at your own
database instead.


- Interest-rate tenor is generalized as `Annual Rate × tenure_months / 12`, driven by
  the tenure of the selected repayment schedule — so new products with different loan
  tenors (e.g. a 5-month livestock product) price correctly out of the box.
- The "Price Across Bankable Risk Grade" table's credit risk premium is computed as
  `PD × LGD × EAD` for every grade (the source file had Grade 1's premium as a manually
  typed 0.53% instead of the formula-driven 0.525% — a tiny, likely-accidental rounding
  override that this app does not replicate).
- This ships with SQLite for zero-config local use. For a shared/production deployment,
  set `DATABASE_URL` to a Postgres/MySQL connection string and run behind a real WSGI
  server (gunicorn/uwsgi) instead of `python run.py`.
