from playwright.sync_api import sync_playwright, Playwright
import time
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from datetime import datetime


def content_grabber(page_a,xpath,time_out):
    try:
        return page_a.wait_for_selector(xpath, timeout=time_out)
    except:
        print("Content not found")

def item_find(page,selector):
    try:
        element = page.locator(selector)
        return element.inner_text() if element else "Null"
    except:
        return "Null"

def product_details(page,link):
        #page.goto("https://www.daraz.com.bd/products/g-small-super-dotted-golden-condoms-10pcs-pack-i143904091-s1068368530.html?spm=a2a0e.searchlist.sku.1.20613633W2iaUs&search=1")
        try:
            page.goto(link)
            


            #page.wait_for_load_state('load')

            current_date = datetime.now().strftime("%d-%m-%Y")

            category_div = content_grabber(page,'//*[@id="pdp-nav"]/div/div',5000)
            category_li = category_div.query_selector_all('li')
            category = [category_li.inner_text() for category_li in category_li]

            html = page.content()

            soup = BeautifulSoup(html, 'html.parser')

            #ratings_details = page.locator('//*[@id="module_product_review"]/div/div/div[2]/div[1]/div[1]').inner_text()

            price_details = soup.find('div',{'class':"pdp-product-price"}).find_all('span')
            
            price_details_list = [price_detail.text for price_detail in price_details]

            dis_price = price_details_list[0]
            actual_price = price_details_list[1] if len(price_details_list) > 1 else "Null"
            discount = price_details_list[2] if len(price_details_list) > 2 else "Null"

            products_sold = soup.find('span',{'class':"crazy-deal-details-soldtext"}).text if soup.find('span',{'class':"crazy-deal-details-soldtext"}) is not None else "Null"

            ratings = soup.find('span',{'class':"score"}).text if soup.find('span',{'class':"score"}) is not None else "Null"
            rating_tag = soup.find('span',{'class':"rating-tag-text"}).text if soup.find('span',{'class':"rating-tag-text"}) is not None else "Null"
            number_of_ratings = soup.find('div',{'class':"rate-num"}).text if soup.find('div',{'class':"rate-num"}) is not None else "Null"
            

            #print(price_details_list)
            #print(products_sold)
            #print(ratings)
            #print(rating_tag)
            #print(number_of_ratings)
            #print(category)
            #list_of_items = [dis_price,actual_price,discount]
            #print(list_of_items)
            cat_dict = {f"Category_{i+1}": cat for i, cat in enumerate(category[:-1])}
            product_name = category[-1]

            data = {
                "Date" : current_date,
                "Name" : product_name,
                **cat_dict,
                "dicounted price": dis_price,
                "Actual Price": actual_price,
                "% of discount": discount,
                "Number of Product sold": products_sold,
                "Rating": ratings,
                "Number of rating ": number_of_ratings,
                "Rating Tag": rating_tag
            }

            return data
        except:
            return {}


def run(playwright: Playwright):
    browser = playwright.chromium.launch(headless=True)
     # Open a new browser context (incognito mode)
    context = browser.new_context()
    # Open a new page
    page = context.new_page()
    
    # Set viewport size to maximize view
    page.set_viewport_size({
        "width": 1920,
        "height": 1080
    })

    page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())
    page.goto("https://www.daraz.com.bd/")

    # Click on the FlashSale element
    flash_sale = page.locator('//a[@title="FlashSale"]')
    flash_sale.click()


    list_of_product=content_grabber(page,'//*[@class="item-list J_FSItemList"]/div',5000)
    products_list_by_a = list_of_product.query_selector_all('a')
    
    # Extract the text and links from the elements
    list_of_products_links = [link.get_property('href').json_value() for link in products_list_by_a]
    list_of_products_name = [link.inner_text().splitlines()[0] for link in products_list_by_a]

    # Create a dictionary with the product data
    daraz_data = {
        "Product Names": list_of_products_name,
        "Product links": list_of_products_links
    }

     # Convert the dictionary to a pandas DataFrame
    #daraz_link = pd.DataFrame(daraz_data)

    # Display the first few rows of the DataFrame
    #print(daraz_products.head())

    #daraz_link.to_csv('daraz_products.csv',index=False,)

    data=[]

    for link in tqdm(list_of_products_links[0:10]):
        
        data.append(product_details(page,link))
    
    browser.close()

    return daraz_data,data





with sync_playwright() as playwright:
    daraz_link,product_data=run(playwright)


daraz_products = pd.DataFrame(product_data)

daraz_products["Name 2"] = daraz_link["Product Names"][0:10]

current_date = datetime.now().strftime("%d-%m-%Y")

csv_file_name = f"product_data_{current_date}.csv"
daraz_products.to_csv(csv_file_name, index=False)