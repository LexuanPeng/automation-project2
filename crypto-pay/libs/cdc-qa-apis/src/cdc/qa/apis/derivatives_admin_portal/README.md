# `derivatives_admin_portal` Sub-package Documentation

## Usage Example
```python
# import sub-package
from cdc.qa.apis.derivatives_admin_portal import AdminPortalServices

# create `AdminPortalServices` instance
admin_ser = AdminPortalServices()

# call a RESTful API with the instance
print(admin_ser.valuation.set_mark_price(instrument_symbol="DOTUSD-PERP", price_value="16.8", is_override="true"))
print(admin_ser.valuation.get_detail_valuation_value_by_instrument(
        instrument_symbol="DOTUSD-PERP", field=FieldEnum.MARK_PRICE
     ))

```

## Implemented APIs
1. /admin
2. /admin/help
3. /admin/help/placeholder
