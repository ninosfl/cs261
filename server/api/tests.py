from datetime import datetime
from decimal import Decimal

from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone

from trades.models import Company, CurrencyValue, DerivativeTrade, Product
from api.views import create_trade

class TestSubmit(TestCase):
    def test_url_correct(self):
        self.assertEqual(reverse("api-submit"), "/api/submit/")
    def test_correct_function_chosen(self):
        self.assertEqual(resolve("/api/submit/").kwargs["func"], create_trade)
    def test_trade_created(self):
        test_date = timezone.now().date()
        CurrencyValue.objects.create(date=test_date, currency="AAA", value="1")
        CurrencyValue.objects.create(date=test_date, currency="BBB", value="1")
        selling_company = Company.objects.create(name="X")
        Company.objects.create(name="Y")
        Product.objects.create(name="x", seller_company=selling_company)
        trade_data = {
            "buyingParty": "Y",
            "sellingParty": "X",
            "product": "x",
            "quantity": "10",
            "underlyingCurrency": "AAA",
            "underlyingPrice": "1",
            "maturityDate": "2020-01-01",
            "notionalCurrency": "BBB",
            "strikePrice": "1"
        }
        response = create_trade(trade_data.copy()) # copy because passed data is modified
        self.assertTrue(response["success"])
        new_trade = response["trade"]
        self.assertTrue(DerivativeTrade.objects.all())
        self.assertEqual(new_trade["buyingParty"], trade_data["buyingParty"])
        self.assertEqual(new_trade["sellingParty"], trade_data["sellingParty"])
        self.assertEqual(new_trade["product"], trade_data["product"])
        self.assertEqual(new_trade["quantity"], int(trade_data["quantity"]))
        self.assertEqual(new_trade["underlyingCurrency"], trade_data["underlyingCurrency"])
        self.assertEqual(new_trade["underlyingPrice"], Decimal(trade_data["underlyingPrice"]))
        self.assertEqual(new_trade["maturityDate"], datetime.strptime(trade_data["maturityDate"], "%Y-%m-%d").date())
        self.assertEqual(new_trade["notionalCurrency"], trade_data["notionalCurrency"])
        self.assertEqual(new_trade["strikePrice"], Decimal(trade_data["strikePrice"]))
