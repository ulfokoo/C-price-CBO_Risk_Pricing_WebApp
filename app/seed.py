from app import db
from app.models import (
    User, Product, ScoreCategory, SubParameter, ScoringOption, PricingInput,
    CostOfFundSource, RWAOption, RepaymentSchedule, OperationalCostComponent, PDGrade,
    NGOSupportItem, NGOSupportTier, LGDCoverageCategory, LGDCoverageTier,
    PartnerFundingOption, PartnerFundingTier, EligibilityCriterion,
)
from app.seed_scorecards import (
    ANIMAL_LIVESTOCK_SCORECARD, CEREALS_SCORECARD, HORTICULTURE_SCORECARD, MSME_SCORECARD,
)


def ensure_default_admin():
    if User.query.count() == 0:
        admin = User(username="admin", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        officer = User(username="loanofficer", role="user")
        officer.set_password("officer123")
        db.session.add(officer)
        db.session.commit()

    if Product.query.count() == 0:
        seed_furtuu_product()
        seed_new_products()


# ---------------------------------------------------------------------------
# Categories -> [(sub-parameter name, weight%, [(option label, score), ...], selected_label)]
# ---------------------------------------------------------------------------
SCORECARD_DEF = [
    ("Rainfall & Disease Risk (15%)", [
        ("Rainfall Outlook", 8, [
            ("Favorable / Strong", 100), ("Adequate / Acceptable", 75), ("Low", 50),
            ("Risky / Below Standard", 25)], "Favorable / Strong"),
        ("Disease Outbreak Tendency", 7, [
            ("Low", 100), ("Moderate", 70), ("High", 40)], "Moderate"),
    ]),
    ("Market & Commercial Risk (10%)", [
        ("Output Price Volatility", 2, [
            ("Stable", 100), ("Moderate", 75), ("Volatile", 50), ("Highly Volatile", 25)], "Stable"),
        ("Input Price Volatility", 3, [
            ("Stable", 100), ("Moderate", 75), ("Volatile", 50), ("Highly Volatile", 25)], "Stable"),
        ("Market Access", 2, [
            ("Formal contract / Off-taker", 100), ("Informal but regular buyers", 75),
            ("Occasional buyers", 50), ("No reliable market", 25)], "Formal contract / Off-taker"),
        ("Infrastructure Support", 2, [
            ("Strong", 100), ("Moderate", 75), ("Limited", 50), ("Very weak / None", 25)], "Strong"),
        ("Demand Stability", 1, [
            ("Strong", 100), ("Moderate", 75), ("Fluctuating", 50), ("Weak", 40)], "Strong"),
    ]),
    ("Economic Risk (4%)", [
        ("Inflation Outlook", 4, [
            ("Stable", 100), ("Moderate", 70), ("High", 40)], "Stable"),
    ]),
    ("Political Risk (6%)", [
        ("Political Instability", 4, [
            ("Stable", 100), ("Moderate", 70), ("Unstable", 40)], "Stable"),
        ("Government Priority", 2, [
            ("High Priority", 100), ("Moderate Priority", 70), ("Low Priority", 40)], "High Priority"),
    ]),
    ("Product Nature Risk (30%)", [
        ("Weather Shock Resilience", 6, [
            ("Resilient", 100), ("Moderate", 75), ("Sensitive", 50), ("Highly Sensitive", 40)], "Resilient"),
        ("Disease Resistance", 6, [
            ("Resistant", 100), ("Sensitive", 70), ("Highly Vulnerable", 40)], "Resistant"),
        ("Perishability", 5, [
            ("Durable", 100), ("Moderately Resilient", 75), ("Perishable", 50),
            ("Highly Perishable", 25)], "Perishable"),
        ("Location Suitability (Soil & Agro)", 6, [
            ("Highly Suitable", 100), ("Suitable", 75), ("Moderate", 50), ("Less Suitable", 25)],
         "Highly Suitable"),
        ("Production Cycle", 7, [
            ("2-5 months", 100), ("5-9 months", 70), ("> 9 months", 40)], "2-5 months"),
    ]),
    ("Counterparty Risk (20%)", [
        ("Experience", 4, [
            (">5 years", 100), ("3-5 years", 75), ("1-3 years", 50), ("No experience", 25)], ">5 years"),
        ("Other Income Sources", 5, [
            ("Regular", 100), ("Seasonal", 70), ("None", 40)], "Regular"),
        ("Technical Capacity & Training", 4, [
            ("Formal Education+ Training", 100), ("Formal Education / Training", 70),
            ("None", 40)], "Formal Education+ Training"),
        ("Loan Amount vs Limit", 3, [
            ("0-40%", 100), ("40-60%", 80), ("60-80%", 60), ("80-100%", 25)], "40-60%"),
        ("Age", 2, [
            ("36-45 Years", 100), ("46-60 Years", 80), ("26-36 Years", 60), ("18-25 Years", 40),
            (">60 Years", 25)], "26-36 Years"),
        ("Marital Status", 2, [
            ("Married", 100), ("Single", 85), ("Divorced", 70), ("Widowed", 55)], "Divorced"),
    ]),
    ("Banking Relationship (15%)", [
        ("Repayment Tendency", 6, [
            ("Regular Payment/ No arrears", 100), ("1-29 days", 80), ("30-89 days", 60),
            ("Default (>90 days)", 0), ("Not Applicable (new customer)", 100)],
         "Regular Payment/ No arrears"),
        ("Borrowing Frequency", 2, [
            (">5 times", 100), ("4-5 times", 80), ("2-3 times", 60), ("1 time", -5),
            ("Not Applicable (new customer)", 100)], ">5 times"),
        ("Previous Exposure limit", 2, [
            (">300,000", 100), ("200,000 - 300,000", 80), ("100,000 - 200,000", 60),
            ("100,000 - 50,000", 25), ("Not Applicable (new customer)", 100)], ">300,000"),
        ("Restructured History", 2, [
            ("No", 100), ("Yes", 0), ("Not Applicable (new customer)", 100)], "No"),
        ("Account Performance against Loan limit", 2, [
            ("Good", 100), ("Moderate", 70), ("Weak", 40)], "Good"),
        ("Account Turnover", 2, [
            (">5 times", 100), ("2-5 times", 70), ("<2 times", 40)], ">5 times"),
    ]),
]

PD_GRADES_DEF = [
    # (grade_num, internal_name, sp_band, score_range, min_score, mid_pd, upper_bound_pd%, stress%, is_default)
    (1, "Exceptionally Low Risk", "AAA-AA", "100 - 90", 90, 0.05, 0.05, 1.0, False),
    (2, "Very Low Risk", "A", "89 - 80", 80, 0.10, 0.10, 1.5, False),
    (3, "Low Risk", "BBB+", "79 - 70", 70, 0.25, 0.30, 2.0, False),
    (4, "Moderate Risk", "BBB", "69 - 60", 60, 0.75, 1.00, 2.5, False),
    (5, "Potential Risk", "BB", "59 - 50", 50, 2.00, 5.00, 3.0, False),
    (6, "High Risk", "B+", "49 - 40", 40, 4.50, 15.00, 3.5, False),
    (7, "Very High Risk", "B-", "39 - 30", 30, 8.00, 40.00, 4.0, False),
    (8, "Default", "CCC-D", "< 30", 0, 15.00, 100.00, 4.5, True),
]


def seed_furtuu_product():
    product = Product(
        name="Furtuu (Grain Value Chain)",
        description="Cooperative Bank of Oromia agricultural loan for grain producers — 9-month tenor.",
    )
    db.session.add(product)
    db.session.flush()

    for cat_idx, (cat_name, subs) in enumerate(SCORECARD_DEF, start=1):
        cat = ScoreCategory(product_id=product.id, name=cat_name, display_order=cat_idx)
        db.session.add(cat)
        db.session.flush()
        for sp_idx, (sp_name, weight_pct, options, selected_label) in enumerate(subs, start=1):
            sp = SubParameter(category_id=cat.id, name=sp_name, weight=weight_pct / 100.0,
                               display_order=sp_idx)
            db.session.add(sp)
            db.session.flush()
            selected_id = None
            for opt_idx, (label, score) in enumerate(options, start=1):
                opt = ScoringOption(sub_parameter_id=sp.id, label=label, score=score,
                                     display_order=opt_idx)
                db.session.add(opt)
                db.session.flush()
                if label == selected_label:
                    selected_id = opt.id
            sp.selected_option_id = selected_id

    # PD Grades
    for num, iname, sp_band, rng, minscore, midpd, upper, stress, is_def in PD_GRADES_DEF:
        db.session.add(PDGrade(
            product_id=product.id, grade_number=num, grade_label=f"Grade {num}",
            internal_grade_name=iname, sp_band=sp_band, score_range_label=rng,
            min_score=minscore, mid_pd=midpd, upper_bound_pd=upper / 100.0,
            stress_agri_digital=stress / 100.0, is_default_grade=is_def,
        ))

    # RWA options (Vlookup sheet)
    rwa_retail = RWAOption(product_id=product.id, label="Retail Exposure- meeting NBE criteria",
                            rwa_value=0.75, display_order=1)
    db.session.add(rwa_retail)
    db.session.add(RWAOption(product_id=product.id, label="Non-Regulatory Retail", rwa_value=1.0,
                              display_order=2))

    # Repayment schedules (Vlookup sheet)
    schedules = [
        ("2 months-Poultry Broiler", 2, 0.25),
        ("5 months-OX/Shoat fattening", 5, 0.5),
        ("7 months-Grains (Michu Agri)", 7, 0.75),
        ("9 months-Grains (Furtuu)", 9, 0.9),
        ("13 months-Poultry Layer", 13, 1.6),
    ]
    furtuu_schedule = None
    for i, (label, months, rate_pct) in enumerate(schedules, start=1):
        rs = RepaymentSchedule(product_id=product.id, label=label, tenure_months=months,
                                rate=rate_pct / 100.0, display_order=i)
        db.session.add(rs)
        db.session.flush()
        if "Furtuu" in label:
            furtuu_schedule = rs

    # Operational cost components (Vlookup sheet)
    for i, (name, val_pct) in enumerate(
            [("Tech", 1.5), ("Commission", 0.37), ("Miscellaneous", 1.0)], start=1):
        db.session.add(OperationalCostComponent(product_id=product.id, name=name, value=val_pct / 100.0,
                                                  display_order=i))

    # Cost of Fund sources (as of March 31, 2026 — figures from the source workbook)
    cof_sources = [
        ("Savings Deposit (Excluding IFB)", 95952803.96, 7.0),
        ("Non-interest Bearing Deposit", 80163083.96, 0.0),
        ("Fixed Time Deposits", 14998167.22, 12.56),
        ("Interbank Money Market Borrowing", 0.0, 17.9),
    ]
    for i, (name, bal, rate_pct) in enumerate(cof_sources, start=1):
        db.session.add(CostOfFundSource(product_id=product.id, name=name, balance=bal,
                                         annual_rate=rate_pct / 100.0, display_order=i))

    db.session.flush()

    # Pricing inputs
    pin = PricingInput(
        product_id=product.id,
        cost_of_capital=0.1388 + 0.045,   # T-bill 13.88% + 4.5% equity risk premium
        target_return_on_rwa=0.19,
        liquidity_premium=0.0,
        loan_amount=100000.0,
        rwa_option_id=rwa_retail.id,
        loss_given_default=0.5,
        exposure_at_default=1.0,
        repayment_schedule_id=furtuu_schedule.id if furtuu_schedule else None,
        expected_access_fee_pct=0.035,
    )
    db.session.add(pin)
    db.session.commit()


# ===========================================================================
# New products seeded from the "Clean and Productive Use Energy Financing —
# Risk Based Pricing" workbook: Animal-Livestock, Cireals, MSME-Scorecard and
# Horticulture score cards, each priced through the shared risk-adjusted
# pricing waterfall (PD Calibration + LGD Calibration + Partner-Funding
# Scheme), matching the 'Normal-Risk-Adjusted Price-MSME' /
# 'Risk-Adjusted Price-Non retail' sheets exactly.
# ===========================================================================

# 'PD Calibration' sheet: Average PD for Agri-loan (KBA Loan performance
# dashboard, Jun 2026) = 26%. Each grade's relative weight against that
# average gives its Calibrated PD.
AVERAGE_PD = 0.26
PD_WEIGHTS = [0.05, 0.10, 0.175, 0.25, 0.45, 0.6, 0.8, 1.0]

# Reference grade metadata (Internal Grade / S&P band / Score range) is
# unchanged from 'S&P PD and Rating' / 'PD Transformation' — kept here purely
# as informational reference data (Upper Bound PD + Agri/Digital stress); the
# grades below are calibrated (PD Calibration) rather than stress-adjusted.
PD_GRADES_NEW = [
    # (grade_num, internal_name, sp_band, score_range, min_score, mid_pd, upper_bound_pd%, stress%, is_default, pd_weight)
    (1, "Exceptionally Low Risk", "AAA-AA", "100 - 90", 90, 0.05, 0.05, 1.0, False, PD_WEIGHTS[0]),
    (2, "Very Low Risk", "A", "89 - 80", 80, 0.10, 0.10, 1.5, False, PD_WEIGHTS[1]),
    (3, "Low Risk", "BBB+", "79 - 70", 70, 0.25, 0.30, 2.0, False, PD_WEIGHTS[2]),
    (4, "Moderate Risk", "BBB", "69 - 60", 60, 0.75, 1.00, 2.5, False, PD_WEIGHTS[3]),
    (5, "Potential Risk", "BB", "59 - 50", 50, 2.00, 5.00, 3.0, False, PD_WEIGHTS[4]),
    (6, "High Risk", "B+", "49 - 40", 40, 4.50, 15.00, 3.5, False, PD_WEIGHTS[5]),
    (7, "Very High Risk", "B-", "39 - 30", 30, 8.00, 40.00, 4.0, False, PD_WEIGHTS[6]),
    (8, "Default", "CCC-D", "< 30", 0, 15.00, 100.00, 4.5, True, PD_WEIGHTS[7]),
]

# 'LGD- Calibration' sheet: Applicable LGD = 1 - reduction, for unsecured
# (Insurance Coverage) and secured (Collateral Coverage) loans.
LGD_CATEGORIES_DEF = [
    ("Insurance Coverage (Unsecured Loan)", [
        (">75%", 0.75), ("50%-75%", 0.5), ("0%-49%", 0.0), ("None", 0.0),
    ]),
    ("Collateral Coverage (Secured Loan)", [
        (">75%", 0.75), ("50%-75%", 0.5), ("0%-49%", 0.0), ("None", 0.0),
    ]),
]

# 'Partener-Funding Scheme' + 'Justification' + 'Impact-range' sheets: each
# scheme discounts whichever waterfall inputs it affects.
# (name, pricing_impact, adjustment_basis, affects_cof, affects_lgd, affects_op_cost, affects_ead, tiers)
PARTNER_FUNDING_DEF = [
    ("Seed Money", "Reduces Cost of Funds, LGD and EAD",
     "Partner contribution is recognized as funding support, risk mitigation and customer equity contribution",
     True, True, False, True,
     [(">50%", 0.5), ("40%-50%", 0.4), ("30%-39%", 0.3), ("20%-29%", 0.2), ("None", 0.0)]),
    ("Guarantee Fund / De-risking", "Reduces Cost of Funds and LGD",
     "Guarantee coverage reduces the Bank's exposure and expected loss",
     True, True, False, False,
     [(">50%", 0.5), ("40%-50%", 0.4), ("30%-39%", 0.3), ("20%-29%", 0.2), ("None", 0.0)]),
    ("Matching Fund", "Reduces Cost of Funds and Operational Cost",
     "Partner funding reduces the Bank's funding requirement",
     True, False, True, False,
     [(">85%", 0.85), ("70%-85%", 0.7), ("50%-69%", 0.5), ("30%-49%", 0.3), ("10%-29%", 0.1), ("None", 0.0)]),
    ("Subsidized Scheme Financing", "Reduces EAD through equity contribution",
     "Normal pricing applies unless specifically approved as a strategic-client arrangement",
     False, False, False, True,
     [(">50%", 0.5), ("40%-50%", 0.4), ("30%-39%", 0.3), ("20%-29%", 0.2), ("None", 0.0)]),
    ("Technical Support", "Reduces Operating Cost",
     "Partner-provided technical support reduces the Bank's operational cost allocation",
     False, False, True, False,
     [("Provided", 0.5), ("None", 0.0)]),
]

# 'NGO pricing' / Sheet3: flat, capped reduction of the final annual rate
# based on overall NGO/partner support against the loan portfolio.
NGO_TIERS_DEF = [
    (">50%", 0.02), ("40%-50%", 0.014), ("30%-39%", 0.008),
    ("20%-29%", 0.003), ("10%-19%", 0.002), ("0%", 0.0),
]
NGO_CAP = 0.02

# 'Eligibility' + 'Weight summary' (New Parameters to be included)
ELIGIBILITY_DEF = [
    ("Water Availability", "Reliable water source confirmed for the full production cycle", True),
    ("ESG Risk Screening", "No unresolved environmental, social or governance red flags", True),
    ("Irrigation Access", "Irrigation infrastructure available, or rainfall outlook is favorable", False),
    ("Temperature Suitability", "Agro-climatic zone suitable for the financed crop / livestock", True),
    ("Flood Risk Exposure", "Farm / production site is not in a high flood-risk zone", True),
]

# Shared Cost of Fund (as of June 30, 2026 — figures from the source workbook)
COST_OF_FUND_SOURCES = [
    ("Savings Deposit (Excluding IFB)", 84629124.48, 7.0),
    ("Non-interest Bearing Deposit (Demand and IFB)", 89436224.56, 0.0),
    ("Fixed Time Deposits", 18819550.90, 15.0),
    ("Interbank Money Market Borrowing", 0.0, 17.9),
]

# Shared Vlookup reference tables
RWA_OPTIONS_DEF = [
    ("Retail Exposure- meeting NBE criteria", 0.75),
    ("Non-Retail", 1.0),
]
REPAYMENT_SCHEDULES_DEF = [
    ("Monthly", 1, 0.0),
    ("Quartely", 3, 0.25),
    ("Semi-Annualy", 6, 0.5),
]
OP_COST_COMPONENTS_DEF = [
    ("Tech", 0.0), ("Commission", 0.37), ("Misclaneous", 1.0),
]

NEW_PRODUCTS_DEF = [
    dict(
        key="animal_livestock",
        name="Animal & Livestock (Clean & Productive Use Energy)",
        description="Cooperative Bank of Oromia clean & productive-use-energy financing for animal / livestock value chains.",
        scorecard=ANIMAL_LIVESTOCK_SCORECARD,
        loan_amount=50000.0, rwa_label="Non-Retail",
        lgd_category_idx=1, lgd_tier_label=">75%", repayment_label="Monthly",
    ),
    dict(
        key="cereals",
        name="Cereals (Clean & Productive Use Energy)",
        description="Cooperative Bank of Oromia clean & productive-use-energy financing for cereal / grain producers.",
        scorecard=CEREALS_SCORECARD,
        loan_amount=50000.0, rwa_label="Non-Retail",
        lgd_category_idx=1, lgd_tier_label=">75%", repayment_label="Monthly",
    ),
    dict(
        key="horticulture",
        name="Horticulture (Clean & Productive Use Energy)",
        description="Cooperative Bank of Oromia clean & productive-use-energy financing for horticulture producers using solar/clean technology.",
        scorecard=HORTICULTURE_SCORECARD,
        loan_amount=50000.0, rwa_label="Non-Retail",
        lgd_category_idx=1, lgd_tier_label=">75%", repayment_label="Monthly",
    ),
    dict(
        key="msme",
        name="MSME (Value-Adding Agri-Business)",
        description="Cooperative Bank of Oromia credit scoring & risk-based pricing for value-adding agri-business MSMEs.",
        scorecard=MSME_SCORECARD,
        loan_amount=50000.0, rwa_label="Retail Exposure- meeting NBE criteria",
        lgd_category_idx=0, lgd_tier_label="0%-49%", repayment_label="Quartely",
    ),
]


def _build_scorecard(product, scorecard_def):
    for cat_idx, (cat_name, subs) in enumerate(scorecard_def, start=1):
        cat = ScoreCategory(product_id=product.id, name=cat_name, display_order=cat_idx)
        db.session.add(cat)
        db.session.flush()
        for sp_idx, (sp_name, weight_pct, options, selected_label) in enumerate(subs, start=1):
            sp = SubParameter(category_id=cat.id, name=sp_name, weight=weight_pct / 100.0,
                               display_order=sp_idx)
            db.session.add(sp)
            db.session.flush()
            selected_id = None
            for opt_idx, (label, score) in enumerate(options, start=1):
                opt = ScoringOption(sub_parameter_id=sp.id, label=label, score=score,
                                     display_order=opt_idx)
                db.session.add(opt)
                db.session.flush()
                if label == selected_label:
                    selected_id = opt.id
            sp.selected_option_id = selected_id


def _build_pd_grades(product):
    for num, iname, sp_band, rng, minscore, midpd, upper, stress, is_def, weight in PD_GRADES_NEW:
        db.session.add(PDGrade(
            product_id=product.id, grade_number=num, grade_label=f"Grade {num}",
            internal_grade_name=iname, sp_band=sp_band, score_range_label=rng,
            min_score=minscore, mid_pd=midpd, upper_bound_pd=upper / 100.0,
            stress_agri_digital=stress / 100.0, is_default_grade=is_def, pd_weight=weight,
        ))


def _build_reference_tables(product):
    rwa_by_label = {}
    for i, (label, val) in enumerate(RWA_OPTIONS_DEF, start=1):
        r = RWAOption(product_id=product.id, label=label, rwa_value=val, display_order=i)
        db.session.add(r)
        db.session.flush()
        rwa_by_label[label] = r

    repay_by_label = {}
    for i, (label, months, rate_pct) in enumerate(REPAYMENT_SCHEDULES_DEF, start=1):
        rs = RepaymentSchedule(product_id=product.id, label=label, tenure_months=months,
                                rate=rate_pct / 100.0, display_order=i)
        db.session.add(rs)
        db.session.flush()
        repay_by_label[label] = rs

    for i, (name, val_pct) in enumerate(OP_COST_COMPONENTS_DEF, start=1):
        db.session.add(OperationalCostComponent(product_id=product.id, name=name,
                                                  value=val_pct / 100.0, display_order=i))

    for i, (name, bal, rate_pct) in enumerate(COST_OF_FUND_SOURCES, start=1):
        db.session.add(CostOfFundSource(product_id=product.id, name=name, balance=bal,
                                         annual_rate=rate_pct / 100.0, display_order=i))

    return rwa_by_label, repay_by_label


def _build_lgd_calibration(product):
    categories = []
    for cat_idx, (cat_name, tiers) in enumerate(LGD_CATEGORIES_DEF, start=1):
        cat = LGDCoverageCategory(product_id=product.id, name=cat_name, display_order=cat_idx)
        db.session.add(cat)
        db.session.flush()
        tier_objs = []
        for t_idx, (label, reduction) in enumerate(tiers, start=1):
            t = LGDCoverageTier(category_id=cat.id, label=label, reduction_pct=reduction,
                                 display_order=t_idx)
            db.session.add(t)
            db.session.flush()
            tier_objs.append(t)
        categories.append({"category": cat, "tiers": tier_objs})
    return categories


def _build_partner_funding(product):
    for opt_idx, (name, impact, basis, aff_cof, aff_lgd, aff_op, aff_ead, tiers) in enumerate(
            PARTNER_FUNDING_DEF, start=1):
        opt = PartnerFundingOption(
            product_id=product.id, name=name, pricing_impact=impact, adjustment_basis=basis,
            affects_cost_of_fund=aff_cof, affects_lgd=aff_lgd, affects_op_cost=aff_op,
            affects_ead=aff_ead, is_active=True, display_order=opt_idx,
        )
        db.session.add(opt)
        db.session.flush()
        for t_idx, (label, reduction) in enumerate(tiers, start=1):
            db.session.add(PartnerFundingTier(option_id=opt.id, label=label,
                                               reduction_pct=reduction, display_order=t_idx))


def _build_ngo_support(product):
    item = NGOSupportItem(product_id=product.id, name="NGO / Partner Support Level (against Loan Portfolio)",
                           percent=0.0, max_price_impact_pct=NGO_CAP, is_active=True, display_order=1)
    db.session.add(item)
    db.session.flush()
    for t_idx, (label, reduction) in enumerate(NGO_TIERS_DEF, start=1):
        db.session.add(NGOSupportTier(item_id=item.id, label=label, rate_reduction=reduction,
                                       display_order=t_idx))


def _build_eligibility(product):
    for i, (criterion, requirement, mandatory) in enumerate(ELIGIBILITY_DEF, start=1):
        db.session.add(EligibilityCriterion(product_id=product.id, criterion=criterion,
                                             requirement=requirement, is_mandatory=mandatory,
                                             display_order=i))


def _seed_one_new_product(spec):
    product = Product(
        name=spec["name"], description=spec["description"],
        average_pd=AVERAGE_PD, use_pd_calibration=True, apply_tenure_scaling=False,
    )
    db.session.add(product)
    db.session.flush()

    _build_scorecard(product, spec["scorecard"])
    _build_pd_grades(product)
    rwa_by_label, repay_by_label = _build_reference_tables(product)
    lgd_categories = _build_lgd_calibration(product)
    _build_partner_funding(product)
    _build_ngo_support(product)
    _build_eligibility(product)
    db.session.flush()

    lgd_tier = None
    cat = lgd_categories[spec["lgd_category_idx"]]
    for t in cat["tiers"]:
        if t.label == spec["lgd_tier_label"]:
            lgd_tier = t
            break

    pin = PricingInput(
        product_id=product.id,
        cost_of_capital=0.1388 + 0.045,   # T-bill 13.88% + 4.5% equity risk premium
        target_return_on_rwa=0.19,
        liquidity_premium=0.0,
        loan_amount=spec["loan_amount"],
        rwa_option_id=rwa_by_label[spec["rwa_label"]].id,
        loss_given_default=0.5,
        exposure_at_default=1.0,
        lgd_tier_id=lgd_tier.id if lgd_tier else None,
        ngo_max_price_impact_pct=NGO_CAP,
        repayment_schedule_id=repay_by_label[spec["repayment_label"]].id,
        expected_access_fee_pct=0.035,
    )
    db.session.add(pin)
    db.session.commit()
    return product


def seed_new_products():
    """Seeds the 4 products from the 'Clean and Productive Use Energy Financing —
    Risk Based Pricing' workbook: Animal-Livestock, Cireals, Horticulture and
    MSME-Scorecard, each with its own scorecard, PD Calibration, LGD
    Calibration, Cost of Fund, Vlookup reference tables, NGO support and
    Partner-Funding Scheme."""
    for spec in NEW_PRODUCTS_DEF:
        _seed_one_new_product(spec)
