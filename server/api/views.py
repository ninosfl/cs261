import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from trades.models import Company, Product, CurrencyValue

from jellyfish import damerau_levenshtein_distance as edit_dist

@csrf_exempt
def api_main(request, func):
    """
    API main view. Takes a request and a function which performs back-end
    processing on request data.
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid method"})
    try:
        json_dict = json.loads(request.body.decode("utf-8"))
    except json.decoder.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Malformed JSON"})
    return JsonResponse(func(json_dict))

def get_company(name):
    try:
        return Company.objects.get(name=name)
    except Company.DoesNotExist:
        return None

def get_product(name):
    try:
        return Product.objects.get(name=name)
    except Product.DoesNotExist:
        return None

def validate_company(data):
    """ Validate single company. Expected data: name """
    result = {"success": False}
    if "name" not in data:
        result["error"] = "No name provided"
        return result

    if get_company(data["name"]) is None:
        result["error"] = "Company does not exist"
        result["success"] = False
    else:
        result["success"] = True

    # possibly a perfomance bottleneck
    result["names"] = closest_matches(data["name"], [c.name for c in Company.objects.all()])
    return result

def closest_matches(x, ws):
    """
    Given a string and an iterable of strings returns the 5 with the smallest
    edit distance in order of the closest string first. All strings with edit
    distance > 5 are filtered out.
    """
    distances = {w: edit_dist(x, w) for w in ws}
    filtered_distances = {w: d for w, d in distances.items() if d <= 5}
    sorted_distances = sorted(filtered_distances, key=filtered_distances.get)
    return sorted_distances[:5]

def company(_, company_name):
    comp = get_company(company_name)
    result = {
        "success": comp is not None,
        "suggestions": closest_matches(
            company_name, [c.name for c in Company.objects.all()]
        ),
    }
    if comp:
        result["company"] = {
            "name": comp.name,
            "id": comp.id
        }
    return JsonResponse(result)

def product(_, product_name):
    prod = get_product(product_name)
    result = {"success": prod is not None}
    if prod:
        result["product"] = {
            "name": prod.name,
            "seller_company": prod.seller_company
        }
    result["suggestions"] = closest_matches(product_name, [p.name for p in Product.objects.all()])
    return JsonResponse(result)

def company_product(_, company_name, product_name):
    result = {}
    comp = get_company(company_name)
    result["company_exists"] = bool(comp)
    if comp:
        result["product_suggestions"] = closest_matches(
            product_name, [p.name for p in comp.product_set.all()]
        )
    return JsonResponse(result)

def validate_product(data):
    """ Validate single product. Exected data: product, buyingParty, sellingParty"""
    result = {"success": False}

    # Shape of request is as expected (all necessary data is given)
    not_specified = {"product", "sellingParty", "buyingParty"}.difference(data)
    if not_specified:
        result["error"] = f"Values not specified: {', '.join(not_specified)}"
        return result

    # Validate buyer existance
    if not get_company(data["buyingParty"]):
        result["error"]= "Buying company does not exist"
        return result

    # Validate seller existance
    seller = get_company(data["sellingParty"])
    if not seller:
        result["error"] = "Selling company does not exist"
        return result

    # Get closest distance matches 
    result["products"] = closest_matches(
        data["product"], [p.name for p in Product.objects.all()])

    # Validate product existance
    prod = get_product(data["product"])
    if not prod:
        result["error"] = "Product does not exist"
        return result

    # Validate product sold by given company
    if prod.seller_company != seller:
        result["error"] = "Selling party does not match product selling company."
        if prod.seller_company.name == data["buyingParty"]:
            result["error"] += " Buying and selling parties can be swapped around"
            result["canSwap"] = True
        else:
            result["canSwap"] = False
        return result

    result["success"] = True
    return result

def currency_exists(currency_code):
    return currency_code in [CurrencyValue.objects.get(date=timezone.now().date())]

def validate_trade(data):
    """
    Validate a whole trade. Expected data: product, sellingParty, buyingParty,
    quantity, underlyingPrice, underlyingCurrency, strikePrice.
    """
    result = {"success": False}
    expected_keys = {"product", "sellingParty", "buyingParty", "quantity",
                     "underlyingPrice", "underlyingCurrency", "strikePrice"}
    not_specified = expected_keys.difference(data)
    if not_specified:
        result["error"] = f"Values not specified: {', '.join(not_specified)}"
        return result

    # Fields that should definitely be valid
    prod = get_product(data["product"])
    if not prod:
        result["error"] = "Product does not exist"
        return result
    seller = get_company(data["sellingParty"])
    if not seller:
        result["error"] = "Selling company does not exist"
        return result
    buyer = get_company(data["buyingParty"])
    if not buyer:
        result["error"] = "Buying party does not exist"
        return result

    # Validate quantity
    try: 
        if data["quantity"] <= 0:
            result["error"] = "Quantity must be positive"
            return result
    except ValueError:
        result["error"] = "Quanity given must be an integer"
        return result

    product_validation_result = validate_product(data)
    if not product_validation_result["success"]:
        return product_validation_result

    result["probabilityErroneous"] = ai_magic(data)
    result["success"] = True
    return result

def ai_magic(data):
    return 0

def validate_maturity_date(data):
    """
    Validate maturity date based on server's current time.
    Expected data: date
    """
    result = {"success": False}

    # Validate shape of data
    if "date" not in data:
        result["error"] = "No date specified."
        return result

    today = timezone.now().date()

    # Attempt to parse given date string
    try:
        date = datetime.strptime(data["date"], "%d/%m/%Y").date()
    except ValueError:
        result["error"] = "Invalid date string given. Expected format DD/MM/YYYY"
        return result

    # Validate date.
    if date < today:
        result["error"] = f"Date cannot be in the past. Server date is {today.strftime('%d/%m/%Y')}"
        return result

    result["success"] = True
    return result
