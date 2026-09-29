"""Scorecard definitions parsed from the Clean and Productive Use Energy Financing
workbook: Animal-Livestock, Cireals, Horticulture, and MSME-Scorecard sheets.
Format matches seed.py's SCORECARD_DEF: [(category_name, [(sub_name, weight_pct, [(label, score), ...], selected_label), ...]), ...]
"""

ANIMAL_LIVESTOCK_SCORECARD = [
    ('1. Market & Commercial Risk (25%)', [
        ('Output Price Volatility (5%)', 5.0, [('Stable prices (low volatility)', 100.0), ('Moderate', 75.0), ('Low', 50.0), ('Highly volatile', 25.0)], 'Highly volatile'),
        ('Input Price Volatility (5%)', 5.0, [('Stable prices (low volatility)', 100.0), ('Moderate', 75.0), ('Low', 50.0), ('Highly volatile', 25.0)], 'Stable prices (low volatility)'),
        ('Market Linkage 5%', 5.0, [('Formal contract/offtaker secured', 100.0), ('Informal but regular buyers', 75.0), ('Random  buyers', 50.0), ('Spot/unreliable', 25.0)], 'Formal contract/offtaker secured'),
        ('Infrastructure and logistic 4%', 4.0, [('Strong', 100.0), ('Moderate', 70.0), ('Limited', 40.0)], 'Moderate'),
        ('Demand Stability (Seasonality effect) 4%', 4.0, [('Strong/consistent demand', 100.0), ('Moderate demand', 75.0), ('Fluctuating demand', 50.0), ('Weak or uncertain demand', 25.0)], 'Strong/consistent demand'),
        ('Quality Input Availability 2%', 2.0, [('Available', 100.0), ('Minor constraint', 70.0), ('Rare', 40.0)], 'Rare'),
    ]),
    ('2. Economy Risk (4%)', [
        ('Inflation Risk Outlook (Tendency) 4%', 4.0, [('Stable', 100.0), ('Moderate', 70.0), ('High', 40.0)], 'Moderate'),
    ]),
    ('3. Poltical Risk (6%)', [
        ('Political Stablity  4%', 4.0, [('Stable', 100.0), ('Moderate', 70.0), ('Unstable', 40.0)], 'Stable'),
        ('Government Priority (Sector Support) 2%', 2.0, [('Highly Prioritized', 100.0), ('Moderate Priority', 70.0), ('Low Priority', 40.0)], 'Highly Prioritized'),
    ]),
    ('4. Product Risk (30%)', [
        ('Vulnerability to Disease 7%', 7.0, [('Resistant', 100.0), ('Vulnerable', 70.0), ('Highly Vulnerable', 40.0)], 'Resistant'),
        ('Diseases control and veterinary Service Avaliablity 6%', 6.0, [('Available', 100.0), ('Moderate', 70.0), ('Limited', 40.0)], 'Available'),
        ('Location suitability 5%', 5.0, [('Suitable', 100.0), ('Moderate', 70.0), ('less suitable', 40.0)], 'Suitable'),
        ('Stock density 4%', 4.0, [('Standard', 100.0), ('Dense', 70.0), ('Highly Dense', 40.0)], 'Standard'),
        ('Perishability 4%', 4.0, [('Durable', 100.0), ('Moderate', 75.0), ('Perishable', 50.0), ('Highly Perishable', 25.0)], 'Durable'),
        ('Production cycle (Tenure) 4%', 4.0, [('2- 5 months', 100.0), ('5-9 months', 70.0), ('>9month', 40.0)], '2- 5 months'),
    ]),
    ('5. Counter Party Risk 20%', [
        ('Age 1%', 1.0, [('Male', 100.0), ('Female', 80.0)], 'Male'),
        ('Marital Status 2%', 2.0, [('Single', 75.0), ('Married', 100.0), ('Divorced', 50.0), ('Widowed', 50.0)], 'Single'),
        ('Education and training 3%', 3.0, [('Formal Education + Training', 100.0), ('Formal Education/ Particular Training', 70.0), ('Illiterate/no training', 40.0)], 'Formal Education + Training'),
        ('Expriance 6%', 6.0, [('> 5 years', 100.0), ('3-5 years', 75.0), ('1-3years', 50.0), ('No experience', 25.0)], '> 5 years'),
        ('Other Income Sources 4%', 4.0, [('Regular income', 100.0), ('seasonal income', 70.0), ('No', 40.0)], 'Regular income'),
        ('Requested Loan amount relative to maximum loan limit (leverage) 4%', 4.0, [('[0% - 40]', 100.0), ('[40% - 60%]', 75.0), ('[60% - 80%]', 50.0), ('[80% - 100%]', 25.0)], '[0% - 40]'),
    ]),
    ('6. Banking Relationship 15%', [
        ('Previous Credit exposure limit', 1.0, [('>900, 000', 100.0), ('700,000 - 900,000', 80.0), ('500,000 - 700,000', 60.0), ('200,000 - 400,000', 45.0), ('< 200,000', 20.0)], '>900, 000'),
        ('Borrowing Frequancy', 3.0, [('> 5 times', 100.0), ('4- 5 times', 75.0), ('2-3 times', 50.0), ('1 time', 25.0)], '> 5 times'),
        ('Repayment Tendency', 4.0, [('Regular Payment (no arrears)', 100.0), ('Minor delays (1-30 days in Arrears)', 75.0), ('30-89 days in Arrears', 50.0), ('Default history discipline (90 days)', 25.0)], 'Regular Payment (no arrears)'),
        ('Re-structured history', 2.0, [('Yes', 50.0), ('No', 100.0)], 'Yes'),
        ('Account Turnover 2%', 2.0, [('> 12 times', 100.0), ('6-12 times', 75.0), ('6-4 times', 50.0), ('< 3  times', 25.0)], '> 12 times'),
        ('Account performance against credit exposure 3%', 3.0, [('Good', 100.0), ('Moderate', 70.0)], 'Good'),
    ]),
]

CEREALS_SCORECARD = [
    ('Climate & Environmental Risk (15%)', [
        ('Rainfall Outlook', 8.0, [('Favorable / Strong', 100.0), ('Adequate / Acceptable', 75.0), ('Low', 50.0), ('Risky / Below Standard', 25.0)], 'Low'),
        ('Disease Outbreak Tendency', 7.0, [('Low', 100.0), ('Moderate', 70.0), ('High', 40.0)], 'Low'),
    ]),
    ('Market & Commercial Risk (10%)', [
        ('Output Price Volatility', 2.0, [('Stable', 100.0), ('Moderate', 75.0), ('Volatile', 50.0)], 'Stable'),
        ('Input Price Volatility', 3.0, [('Stable', 100.0), ('Moderate', 75.0), ('Volatile', 50.0), ('Highly Volatile', 25.0)], 'Stable'),
        ('Market Access', 2.0, [('Formal contract / Off-taker', 100.0), ('Informal but regular buyers', 75.0), ('Occasional buyers', 50.0), ('No reliable market', 25.0)], 'Formal contract / Off-taker'),
        ('Infrastructure Support', 2.0, [('Strong', 100.0), ('Moderate', 75.0), ('Limited', 50.0), ('Very weak / None', 25.0)], 'Strong'),
        ('Demand Stability', 1.0, [('Strong', 100.0), ('Moderate', 75.0), ('Fluctuating', 50.0), ('Weak', 40.0)], 'Strong'),
    ]),
    ('Economic Risk (4%)', [
        ('Inflation Outlook', 4.0, [('Stable', 100.0), ('Moderate', 70.0), ('High', 40.0)], 'Stable'),
    ]),
    ('Political Risk (6%)', [
        ('Political Instability', 4.0, [('Stable', 100.0), ('Moderate', 70.0), ('Unstable', 40.0)], 'Stable'),
        ('Government Priority', 2.0, [('High Priority', 100.0), ('Moderate Priority', 70.0), ('Low Priority', 40.0)], 'High Priority'),
    ]),
    ('Product Nature Risk (30%)', [
        ('Weather Shock Resilience', 6.0, [('Resilient', 100.0), ('Moderate', 75.0), ('Sensitive', 50.0), ('Highly Sensitive', 40.0)], 'Resilient'),
        ('Disease Resistance', 6.0, [('Resistant', 100.0), ('Sensitive', 70.0), ('Highly Vulnerable', 40.0)], 'Resistant'),
        ('Perishability', 5.0, [('Durable', 100.0), ('Moderately Resilient', 75.0), ('Perishable', 50.0), ('Highly Perishable', 25.0)], 'Perishable'),
        ('Location Suitability (Soil & Agro)', 6.0, [('Highly Suitable', 100.0), ('Suitable', 75.0), ('Moderate', 50.0), ('Less Suitable', 25.0)], 'Highly Suitable'),
        ('Production Cycle', 7.0, [('2–5 months', 100.0), ('5–9 months', 70.0), ('> 9 months', 40.0)], '2–5 months'),
    ]),
    ('Counterparty Risk (20%)', [
        ('Experience', 4.0, [('>5 years', 100.0), ('3–5 years', 75.0), ('1–3 years', 50.0), ('No experience', 25.0)], '>5 years'),
        ('Other Income Sources', 5.0, [('Regular', 100.0), ('Seasonal', 70.0), ('None', 40.0)], 'Regular'),
        ('Technical Capacity & Training', 4.0, [('Formal Education+ Training', 100.0), ('Formal Education / Training', 70.0), ('None', 40.0)], 'Formal Education+ Training'),
        ('Loan Amount vs Limit', 3.0, [('0–40%', 100.0), ('40–60%', 80.0), ('60–80%', 60.0), ('80–100%', 25.0)], '40–60%'),
        ('Age', 2.0, [('36-45 Years', 100.0), ('46 - 60 Years', 80.0), ('26 - 36 Years', 60.0), ('18-25 Years', 40.0), ('>60 Years', 25.0)], '26 - 36 Years'),
        ('Marital Status', 2.0, [('Married', 100.0), ('Single', 85.0), ('Divorced', 70.0), ('Widowed', 55.0)], 'Divorced'),
    ]),
    ('Banking Relationship (15%)', [
        ('Repayment Tendency', 6.0, [('Regular Payment/ No arrears', 100.0), ('1–29 days', 80.0), ('30–89 days', 60.0), ('Default (>90 days)', 0.0), ('Not Applicable (new customer)', 100.0)], 'Regular Payment/ No arrears'),
        ('Borrowing Frequency', 2.0, [('>5 times', 100.0), ('4–5 times', 80.0), ('2–3 times', 60.0), ('1 time', -5.0), ('Not Applicable (new customer)', 100.0)], '>5 times'),
        ('Previous Exposure limit', 2.0, [('>300,000', 100.0), ('200,000 - 300,000', 80.0), ('100,000 - 200,000', 60.0), ('100,000 - 50,000', 25.0), ('Not Applicable (new customer)', 100.0)], '>300,000'),
        ('Restructured History', 2.0, [('No', 100.0), ('Yes', 0.0), ('Not Applicable (new customer)', 100.0)], 'No'),
        ('Account Performance against Loan limit (3%)', 2.0, [('Good', 100.0), ('Moderate', 70.0), ('Weak', 40.0)], 'Good'),
        ('Account Turnover (2%)', 2.0, [('>5 times', 100.0), ('2–5 times', 70.0), ('<2 times', 40.0)], '>5 times'),
    ]),
]

HORTICULTURE_SCORECARD = [
    ('Climate & Environmental Risk (10%)', [
        ('Topography and Agroecology', 10.0, [('Highly Suitable', 100.0), ('Suitable', 75.0), ('Less Suitable', 50.0)], 'Highly Suitable'),
    ]),
    ('Market & Commercial Risk (12%)', [
        ('Output Price Volatility', 2.0, [('Stable', 100.0), ('Moderate', 75.0), ('Volatile', 50.0)], 'Stable'),
        ('Input Price Volatility', 2.0, [('Stable', 100.0), ('Moderate', 75.0), ('Volatile', 50.0), ('Highly Volatile', 25.0)], 'Stable'),
        ('Market Access', 3.0, [('Formal contract / Off-taker', 100.0), ('Informal but regular buyers', 75.0), ('Occasional buyers', 50.0), ('No reliable market', 25.0)], 'Formal contract / Off-taker'),
        ('Infrastructure Support', 2.0, [('Strong', 100.0), ('Moderate', 75.0), ('Limited', 50.0), ('Very weak / None', 25.0)], 'Strong'),
        ('Demand Stability', 3.0, [('Strong', 100.0), ('Moderate', 75.0), ('Fluctuating', 50.0), ('Weak', 40.0)], 'Strong'),
    ]),
    ('Economic Risk (7%)', [
        ('Inflation Outlook', 7.0, [('Stable', 100.0), ('Moderate', 70.0), ('High', 40.0)], 'Stable'),
    ]),
    ('Political and Policy Risk (6%)', [
        ('Social Unrest', 4.0, [('Stable', 100.0), ('Moderate', 70.0), ('Unstable', 40.0)], 'Stable'),
        ('Government Priority', 2.0, [('High Priority', 100.0), ('Moderate Priority', 70.0), ('Low Priority', 40.0)], 'High Priority'),
    ]),
    ('Product Nature Risk (30%)', [
        ('Weather Shock Resilience', 7.0, [('Resilient', 100.0), ('Moderate', 75.0), ('Sensitive', 50.0), ('Highly Sensitive', 40.0)], 'Resilient'),
        ('Disease Resistance', 7.0, [('Resistant', 100.0), ('Vulnerable', 70.0), ('Highly Vulnerable', 40.0)], 'Resistant'),
        ('Perishability', 8.0, [('Durable', 100.0), ('Moderately Resilient', 75.0), ('Perishable', 50.0), ('Highly Perishable', 25.0)], 'Perishable'),
        ('Production Cycle', 8.0, [('Frequent', 100.0), ('Moderate', 70.0), ('Less Frequent', 40.0)], 'Frequent'),
    ]),
    ('Counterparty Risk (20%)', [
        ('Experience', 4.0, [('>5 years', 100.0), ('3–5 years', 75.0), ('1–3 years', 50.0), ('No experience', 25.0)], '>5 years'),
        ('Other Income Sources', 5.0, [('Regular', 100.0), ('Seasonal', 70.0), ('None', 40.0)], 'Regular'),
        ('Technical Capacity & Training', 4.0, [('Formal Education+ Training', 100.0), ('Formal Education / Training', 70.0), ('None', 40.0)], 'Formal Education+ Training'),
        ('Loan Amount vs Limit', 3.0, [('0–40%', 100.0), ('40–60%', 80.0), ('60–80%', 60.0), ('80–100%', 25.0)], '40–60%'),
        ('Age', 2.0, [('36-45 Years', 100.0), ('46 - 60 Years', 80.0), ('26 - 36 Years', 60.0), ('18-25 Years', 40.0), ('>60 Years', 25.0)], '26 - 36 Years'),
        ('Marital Status', 2.0, [('Married', 100.0), ('Single', 85.0), ('Divorced', 70.0), ('Widowed', 55.0)], 'Divorced'),
    ]),
    ('Banking Relationship (15%)', [
        ('Repayment Tendency', 5.0, [('Regular Payment/ No arrears', 100.0), ('1–29 days', 80.0), ('30–89 days', 60.0), ('Default (>90 days)', 0.0), ('Not Applicable (new customer)', 100.0)], '1–29 days'),
        ('Borrowing Frequency', 2.0, [('>5 times', 100.0), ('4–5 times', 80.0), ('2–3 times', 60.0), ('1 time', -5.0), ('Not Applicable (new customer)', 100.0)], '>5 times'),
        ('Previous Exposure limit', 2.0, [('>900,000', 100.0), ('900,000 - 700,001', 80.0), ('700,000- , 500,001', 60.0), ('500,000 -200,000', 25.0), ('Not Applicable (new customer)', 100.0)], '>900,000'),
        ('Restructured History', 2.0, [('No', 100.0), ('Yes', 0.0), ('Not Applicable (new customer)', 100.0)], 'No'),
        ('Account Performance against Loan limit (3%)', 2.0, [('Good', 100.0), ('Moderate', 70.0), ('Weak', 40.0)], 'Good'),
        ('Account Turnover (2%)', 2.0, [('>5 times', 100.0), ('2–5 times', 70.0), ('<2 times', 40.0)], '>5 times'),
    ]),
]

MSME_SCORECARD = [
    ('1. ESG Risk (10%)', [
        ('Waste management Preparedness', 4.0, [('High', 100.0), ('Moderate', 75.0), ('Low', 50.0)], 'High'),
        ('Occupational Health and Safety Readness', 4.0, [('High', 100.0), ('Moderate', 75.0), ('Low', 50.0)], 'Moderate'),
        ('Financial Record Keepping', 2.0, [('Audited Financial Stament Available', 100.0), ('Basic Records', 75.0), ('No Records', 50.0), ('Not Applicable (Smallholder)', 100.0)], 'Not Applicable (Smallholder)'),
    ]),
    ('2. Market & Commercial Risk (25%)', [
        ('Output Price Volatility (5%)', 3.0, [('Stable prices (low volatility)', 100.0), ('Moderate', 75.0), ('Low', 50.0), ('Highly volatile', 25.0)], 'Stable prices (low volatility)'),
        ('Input Price Volatility (5%)', 4.0, [('Stable prices (low volatility)', 100.0), ('Moderate', 75.0), ('Low', 50.0), ('Highly volatile', 25.0)], 'Stable prices (low volatility)'),
        ('Market Linkage 5%', 5.0, [('Formal contract/offtaker secured', 100.0), ('Informal but regular buyers', 75.0), ('Random  buyers', 50.0), ('Spot/unreliable', 25.0)], 'Formal contract/offtaker secured'),
        ('Infrastructure and logistic 4%', 4.0, [('Strong', 100.0), ('Moderate', 70.0), ('Limited', 40.0)], 'Strong'),
        ('Output Demand Stability  4%', 4.0, [('Strong/consistent demand', 100.0), ('Moderate demand', 75.0), ('Fluctuating demand', 50.0), ('Weak or uncertain demand', 25.0)], 'Strong/consistent demand'),
        ('Raw Material Availability', 2.0, [('Consistently Available', 100.0), ('Generally Available', 70.0), ('Seasonal Shortage', 40.0)], 'Consistently Available'),
        ('Supplier Diversification', 3.0, [('Multiple Reliable Suppliers', 100.0), ('Several Suppliers', 70.0), ('Few Suppliers', 40.0)], 'Multiple Reliable Suppliers'),
    ]),
    ('3. Economic Risk (4%)', [
        ('Inflation Risk Outlook (Tendency)', 4.0, [('Stable', 100.0), ('Moderate', 70.0), ('High', 40.0)], 'Stable'),
    ]),
    ('4.Poletical and Policy Risk (6%)', [
        ('Social Unrest', 4.0, [('Stable', 100.0), ('Moderate', 70.0), ('Unstable', 40.0)], 'Moderate'),
        ('Government Priority', 2.0, [('High Priority', 100.0), ('Moderate Priority', 70.0), ('Low Priority', 40.0)], 'Moderate Priority'),
    ]),
    ('5. Operational Risk 23%', [
        ('Processing Technology', 3.0, [('Modern & Automated', 100.0), ('Semi-Automated', 70.0), ('Mostly Manual', 40.0)], 'Semi-Automated'),
        ('Utility Reliability (Water)', 5.0, [('Obsolete Equipment', 100.0), ('Reliable', 70.0), ('Minor Interruptions', 40.0)], 'Minor Interruptions'),
        ('Skilled Workforce Availability', 5.0, [('Frequent Interruptions', 100.0), ('Highly Unreliable', 70.0), ('Highly Skilled', 40.0)], 'Highly Skilled'),
        ('Input Perishability/Durability', 6.0, [('Durable', 100.0), ('Moderate', 75.0), ('Perishable', 50.0), ('Highly Perishable', 25.0)], 'Durable'),
        ('Storage', 4.0, [('Available', 100.0), ('Not Available', 70.0)], 'Available'),
    ]),
    ('6. Counter Party Related Risk 18%', [
        ('Experience', 5.0, [('> 5 years', 100.0), ('3-5 years', 75.0), ('1-3years', 50.0), ('No experience', 25.0)], '> 5 years'),
        ('Education background', 4.0, [('Formal Education and Training', 100.0), ('Formal Education or Particular Training', 70.0), ('Illiterate/no training', 40.0)], 'Formal Education and Training'),
        ('Other Sources of Income if any', 5.0, [('Regular income', 100.0), ('Seasonal income', 70.0), ('No', 40.0)], 'Regular income'),
        ('Loan requested against maximum loan limit (leverage)', 4.0, [('(0%- 40%)', 100.0), ('(41%-60%)', 75.0), ('(61%-80%)', 50.0), ('(81%- 100%]', 25.0)], '(0%- 40%)'),
    ]),
    ('7.Banking relationship 14%', [
        ('Previous Credit Exposure Limit', 1.0, [('>900,000', 100.0), ('900,000 - 700,001', 80.0), ('700,000- , 500,001', 60.0), ('500,000 -200,000', 40.0), ('<200,000', 20.0), ('Not applicable (New Customer)', 100.0)], '<200,000'),
        ('Borrowing Frequency', 2.0, [('> 5 times', 100.0), ('4- 5 times', 75.0), ('2-3 times', 50.0), ('1 time', 25.0), ('Not applicable (New Customer)', 100.0)], '1 time'),
        ('Repayment Tendency', 5.0, [('Regular Payment (no arrears)', 100.0), ('Minor delays (1-30 days in Arrears)', 75.0), ('30-89 days in Arrears', 50.0), ('Default history discipline (90 days)', 0.0), ('Not applicable (New Customer)', 100.0)], 'Default history discipline (90 days)'),
        ('Re-structured history', 2.0, [('No', 100.0), ('Yes', 0.0)], 'Yes'),
        ('Account Turnover', 2.0, [('> 12 times', 100.0), ('12-6 times', 75.0), ('6-4  times', 50.0), ('< 3 times', 25.0)], '> 12 times'),
        ('Account performance against credit exposure', 2.0, [('Good', 100.0), ('Moderate', 70.0), ('Weak', 40.0)], 'Good'),
    ]),
]

