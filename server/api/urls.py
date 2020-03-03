from django.urls import path

from .views import (api_main, validate_company, validate_product, ai_magic,
                    validate_maturity_date, company, product, company_product,
                    currencies,correction)

urlpatterns = [
    path("validate/company/", api_main, {"func": validate_company}, name="api-validate-company"),
    path("validate/product/", api_main, {"func": validate_product}, name="api-validate-product"),
    path("validate/trade/", api_main, {"func": ai_magic}, name="api-validate-trade"),
    path("validate/maturitydate/", api_main, {"func": validate_maturity_date}, name="api-validate-maturitydate"),
    path("currencies/<date_str>/", currencies),
    path("currencies/", currencies),
    path("company/<company_name>/product/<product_name>/", company_product),
    path("company/<company_name>/", company),
    path("corrections/", api_main, {"func": correction}, name="api-correction"),
    path("product/<product_name>/", product),
]
