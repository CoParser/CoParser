

         
#Code Generated by CoParser:c2b9311d Rule: 2025-01-19 13:04:13
  
      
def get_html(url):
    import time
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)       
        time.sleep(10)
        page_source = page.content()
        browser.close()
        with open("debug.html", "w", encoding="utf-8") as file:
            file.write(page_source)
        return page_source

def extract_SellPrice(lxml_tree):
    from lxml.cssselect import CSSSelector
    import re
    from decimal import Decimal

    def validate_function(value):
        try:
            Decimal(value)
            return True
        except:
            return False

    try:
        selector = CSSSelector("#corePriceDisplay_desktop_feature_div .a-price .a-price-whole")
        elements = selector(lxml_tree)
        if elements:
            price_whole = elements[0].text_content().strip()
            price_fraction_selector = CSSSelector("#corePriceDisplay_desktop_feature_div .a-price .a-price-fraction")
            fraction_elements = price_fraction_selector(lxml_tree)
            price_fraction = fraction_elements[0].text_content().strip() if fraction_elements else "00"
            raw_price = f"{price_whole}.{price_fraction}"
            cleaned_price = re.sub(r"\.\.+", ".", raw_price)
            if validate_function(cleaned_price):
                return Decimal(cleaned_price)

        selector = CSSSelector("#corePrice_desktop .a-price .a-offscreen")
        elements = selector(lxml_tree)
        if elements:
            raw_price = elements[0].text_content().strip().replace("$", "")
            cleaned_price = re.sub(r"\.\.+", ".", raw_price)
            if validate_function(cleaned_price):
                return Decimal(cleaned_price)

        return None

    except:
        return None

def extract_SellPrice2(lxml_tree):
    from lxml.cssselect import CSSSelector
    import re
    from decimal import Decimal

    def validate_function(value):
        try:
            Decimal(value)
            return True
        except:
            return False

    try:
        selector = CSSSelector("#corePrice_desktop .a-price-range .a-price .a-offscreen")
        elements = selector(lxml_tree)
        if elements:
            prices = [re.sub(r"\.\.+", ".", el.text_content().strip().replace("$", "")) for el in elements]
            valid_prices = [Decimal(price) for price in prices if validate_function(price)]
            if valid_prices:
                return max(valid_prices)

        return extract_SellPrice(lxml_tree)

    except:
        return None

def extract_ProductName(lxml_tree):
    from lxml.cssselect import CSSSelector
    import re
    def validate_function(value):
        return bool(value.strip())
    try:
        selector = CSSSelector("#productTitle")
        elements = selector(lxml_tree)
        if elements:
            value = elements[0].text_content().strip()
            value = re.sub(r'\s+', ' ', value)
            if validate_function(value):
                return value

        return None

    except:
        return None

def extract_TotalReview(lxml_tree):
    from lxml.cssselect import CSSSelector
    import re
    def validate_function(value):
        return value.isdigit()
    try:
        selector = CSSSelector("#acrCustomerReviewText")
        elements = selector(lxml_tree)
        if elements:
            value = elements[0].text_content().strip()
            value = re.sub(r'[^\d]', '', value)
            if validate_function(value):
                return int(value)

        return None

    except:
        return None

def extract_Availability(lxml_tree):
    from lxml.cssselect import CSSSelector
    def validate_function(value):
        return value.lower() in ["in stock", "out of stock"]
    try:
        selector = CSSSelector("#availability span.a-size-medium")
        elements = selector(lxml_tree)
        if elements:
            value = elements[0].text_content().strip()
            if validate_function(value):
                return value.lower() == "in stock"

        return None

    except:
        return None

def extract_ProductImage(lxml_tree):
    from lxml.cssselect import CSSSelector
    def validate_function(value):
        return value.startswith("http")
    try:
        selector = CSSSelector("#landingImage")
        elements = selector(lxml_tree)
        if elements:
            value = elements[0].get("src", "").strip()
            if validate_function(value):
                return value

        return None

    except:
        return None

def extract_AverageReview(lxml_tree):
    from lxml.cssselect import CSSSelector
    import re
    def validate_function(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    try:
        selector = CSSSelector("#acrPopover span.a-size-base")
        elements = selector(lxml_tree)
        if elements:
            value = elements[0].text_content().strip()
            value = re.sub(r'[^\d\.]', '', value)
            if validate_function(value):
                return float(value)

        return None

    except:
        return None

if __name__ == '__main__':
        import lxml.html
        url='https://www.amazon.com/dp/B0D3DWTKKM/ref=sspa_dk_detail_4'
        html=get_html(url)
        tree = lxml.html.fromstring(html)
        result={}
        
        result['SellPrice']=extract_SellPrice(tree)
        result['SellPrice2']=extract_SellPrice2(tree)
        result['ProductName']=extract_ProductName(tree)
        result['TotalReview']=extract_TotalReview(tree)
        result['Availability']=extract_Availability(tree)
        result['ProductImage']=extract_ProductImage(tree)
        result['AverageReview']=extract_AverageReview(tree)

        print(result)
     


