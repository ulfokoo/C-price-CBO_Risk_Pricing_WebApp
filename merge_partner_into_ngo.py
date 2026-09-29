from app import create_app
from app.models import db, Product, NGOSupportItem, NGOSupportTier

# Max price reduction (in %) each scheme can give at its top range
VALUES = {
    "seed money": 2.0,
    "guarantee fund / de-risking": 2.0,
    "matching fund": 1.5,
    "subsidized scheme financing": 1.0,
    "technical support": 0.5,
}
CAP = 7.0  # overall cap (%) across ALL items together

app = create_app()
with app.app_context():
    for product in Product.query.all():
        opts = list(product.partner_funding_options)
        if not opts:
            continue
        # remove the old generic placeholder item (replaced by the 5 schemes below)
        for it in list(product.ngo_support_items):
            if it.name.strip().lower().startswith("ngo / partner support level"):
                db.session.delete(it)
        db.session.flush()
        names = {i.name.strip().lower() for i in product.ngo_support_items}
        order = len(product.ngo_support_items)
        for opt in opts:
            if opt.name.strip().lower() in names:
                continue
            top = VALUES.get(opt.name.strip().lower(), 1.0) / 100.0
            old_max = max([t.reduction_pct for t in opt.tiers] or [1.0]) or 1.0
            order += 1
            item = NGOSupportItem(product_id=product.id, name=opt.name, percent=0.0,
                                  max_price_impact_pct=top, is_active=True, display_order=order)
            db.session.add(item); db.session.flush()
            for n, t in enumerate(opt.tiers, 1):
                db.session.add(NGOSupportTier(item_id=item.id, label=t.label,
                                              rate_reduction=round(top * t.reduction_pct / old_max, 5),
                                              display_order=n))
        if product.pricing_input:
            product.pricing_input.ngo_max_price_impact_pct = CAP / 100.0
        print("merged:", product.name)
    db.session.commit()
print("Done.")