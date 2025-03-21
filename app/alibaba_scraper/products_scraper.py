from dotenv import load_dotenv
import os
from time import sleep

from fastapi import HTTPException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tempfile


load_dotenv()


def get_top_deals_url():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # GUI kerak bo‘lmasa
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=options)
    driver.get(os.getenv("ALIBABA_URL"))
    driver.implicitly_wait(20)
    top_deals_link = driver.find_element(By.CSS_SELECTOR, "div.saving-spotlight-box")
    top_deals_url = top_deals_link.find_element(By.TAG_NAME, "a").get_attribute("href")
    driver.quit()
    # Clean up the temporary directory
    import shutil
    shutil.rmtree(user_data_dir)
    return top_deals_url


def change_currency(url, currency="USD"):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # GUI kerak bo‘lmasa
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # Optional
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(10)

    try:
        elements = driver.find_elements(By.CSS_SELECTOR, 'div.hide-item')

        if not elements:
            print("No elements found with the given selector!")
            return

        currency_element = elements[0]

        if currency_element.is_displayed():
            # Perform hover action
            actions = ActionChains(driver)
            actions.move_to_element(currency_element).perform()

            # Click on the currency element
            currency_search = driver.find_element(By.CSS_SELECTOR, 'div.css-hlgwow')
            currency_search.click()

            # Find the search box
            currency_search_box = currency_search.find_element(By.TAG_NAME, 'input')

            # Enter the currency
            currency_search_box.send_keys(currency)
            sleep(0.2)
            currency_search_box.send_keys(Keys.ENTER)

            # Click the save button
            save_button = driver.find_element(By.CSS_SELECTOR, 'div.tnh-l-o-control')
            save_button.click()
        else:
            print("Element is present but not visible.")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interacting with the currency element: " + str(e))
    finally:
        driver.quit()
        # Clean up the temporary directory
        import shutil
        shutil.rmtree(user_data_dir)



def get_products_list(page_down_number=2):
    """Returns a list of products from the Top Deals page."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # GUI kerak bo‘lmasa
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=options)

    try:
        top_deals_url = get_top_deals_url()

        change_currency(top_deals_url, currency="USD")

        driver.get(top_deals_url)
        driver.implicitly_wait(12)

        # Click page down n times to load all products
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(page_down_number):
            body.send_keys(Keys.PAGE_DOWN)
            sleep(1)

        # Find all products
        product_list = []
        main_products = driver.find_element(By.CSS_SELECTOR,
                                            os.getenv("FILTER_FOR_PRODUCT_CLASS"))
        raw_product_list = main_products.find_elements(By.CSS_SELECTOR,
                                                       os.getenv("RAW_PRODUCT_LIST_CLASS"))

        # Get product details
        for index, raw_product in enumerate(raw_product_list):
            # Get product link and image link
            a_tag = raw_product.find_element(By.TAG_NAME, "a")
            product_link = a_tag.get_attribute("href")
            image_tag = raw_product.find_element(By.TAG_NAME, "img")
            image_link = image_tag.get_attribute("src")

            # Append product details to the product list
            for i in raw_product.text.split("orders\n"):
                product = i.split("\n")
                if len(product) > 3:
                    continue

                product_dict = {
                    "title": product[0],
                    "price": float(product[1].split("-")[-1].replace("$", "").replace(",", "")),
                    "min_order": product[2],
                    "product_link": product_link,
                    "image_link": image_link
                }
                product_list.append(product_dict)
    except:
        raise HTTPException(status_code=404, detail="No products found.")
    finally:
        driver.quit()
        # Clean up the temporary directory
        import shutil
        shutil.rmtree(user_data_dir)
    return product_list


def get_product_by_link_from_website(product_link):
    """Get product details by product link from the website"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # GUI kerak bo‘lmasa
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # Optional
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(product_link)
        driver.implicitly_wait(7)

        product_details = {}
        try:
            reject_button = driver.find_element(By.CSS_SELECTOR, 'div[class="gdpr-btn gdpr-reject-btn"]')
            reject_button.click()
        except Exception:
            print("No GDPR button found.", Exception)
        product_details["title"] = driver.find_element(By.CSS_SELECTOR, "div.module_title").text
        price_list = driver.find_element(By.CSS_SELECTOR, "div.price-list")

        product_details["price"] = float(
            price_list.text.split("\n")[1].split("-")[-1].replace(",", "").replace("$", ""))
        parent_img_links_list = driver.find_elements(By.CSS_SELECTOR, "div[role='group']")
        product_details["images_links"] = []

        for img_link in parent_img_links_list:
            image_link = img_link.find_element(By.CSS_SELECTOR, "div").get_attribute("style")
            if not image_link:
                break
            product_details["images_links"].append(
                image_link.replace(r"//", "https://").split("\"")[-2].replace("jpg_80x80", "jpg_720x720q50"))

        try:
            see_more_button_parent_div = driver.find_element(By.CSS_SELECTOR, 'div[class="attribute-info"]')
            see_more_button_parent = see_more_button_parent_div.find_element(By.CSS_SELECTOR, 'div[class="more-bg"]')
            see_more_button = see_more_button_parent.find_element(By.TAG_NAME, 'a')
            see_more_button.click()
            sleep(0.8)
        except Exception:
            print("No 'See More' button found.")

        descriptions = {}
        description_parent_div = driver.find_element(By.CSS_SELECTOR, 'div[class="attribute-info"]')

        description_attribute_titles = description_parent_div.find_elements(By.TAG_NAME, "h3")
        for i in range(len(description_attribute_titles)):
            descriptions[description_attribute_titles[i].text] = {}

        description_attribute_list = description_parent_div.find_elements(By.CSS_SELECTOR,
                                                                          "div[class='attribute-list']")
        for i in range(len(description_attribute_list)):
            description_attribute_items = description_attribute_list[i].find_elements(By.CSS_SELECTOR,
                                                                                      "div[class='attribute-item']")
            for j in range(len(description_attribute_items)):
                description_attribute_key = description_attribute_items[j].find_element(By.CSS_SELECTOR,
                                                                                        "div.left").text
                description_attribute_value = description_attribute_items[j].find_element(By.CSS_SELECTOR,
                                                                                          "div.right").text
                if description_attribute_key == "Single gross weight:":
                    try:
                        descriptions['weight'] = float(description_attribute_value.replace("kg", "").strip())
                    except ValueError:
                        descriptions['weight'] = 0.0

                description = {description_attribute_key: description_attribute_value}
                descriptions[description_attribute_titles[i].text].update(description)

        if not descriptions.get("weight"):
            descriptions["weight"] = 0

        product_details["descriptions"] = descriptions

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error getting product details: {e}")
    finally:
        driver.quit()
        # Clean up the temporary directory
        import shutil
        shutil.rmtree(user_data_dir)
    return product_details


def get_product_variants(product_link):
    """Get product details by product link from the website"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # GUI kerak bo‘lmasa
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # Uncomment if you want to run headless
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(product_link)
        driver.implicitly_wait(12)

        product_variants = {}

        # Get all variants
        variants_parent = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="sku-info"]')
        variants = variants_parent.find_elements(By.CSS_SELECTOR, 'div[data-testid="sku-list"]')

        for variant in variants:
            variant_name = variant.find_element(By.TAG_NAME, 'span').text
            if variant_name.split("(")[1].startswith("1)"):
                continue
            variants_elements = []

            # Find variant images
            variant_elements = variant.find_elements(By.CSS_SELECTOR, 'div[data-testid="sku-list-item"] img')
            if variant_elements:
                for element in variant_elements:
                    image_link = element.get_attribute('src')
                    variants_elements.append(image_link)
            else:
                # Handle text variants
                variant_elements = variant.find_elements(By.XPATH, "//span[contains(@class, 'id-inline-block')]")

                for element in variant_elements:

                    text = element.text.strip()
                    if text:
                        variants_elements.append(text)

            product_variants[variant_name] = variants_elements

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error getting product variants: {e}")
    finally:
        driver.quit()
        # Clean up the temporary directory
        import shutil
        shutil.rmtree(user_data_dir)

    return product_variants


def search_product_by_name_from_website(name, minimum_sale=1, page_down_number=17, page=1):
    """ This function return products which are searched by name on alibaba.com """
    # Driver settings
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # GUI kerak bo‘lmasa
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=options)

    try:
        url = f"https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&keywords={name}&moqt={minimum_sale}&originKeywords={name}&tab=all&&page={page}&viewtype=G"
        driver.get(url)
        driver.implicitly_wait(12)

        # Click page down n times to load all products
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(page_down_number):
            body.send_keys(Keys.PAGE_DOWN)
            sleep(0.2)

        # define products list
        products = []

        # find products parent div
        products_parent_div = driver.find_elements(By.CSS_SELECTOR,
                                                   'div[class="organic-list app-organic-search-mb-20 viewtype-gallery"]> div')
        for i in products_parent_div:
            product_image_link = i.find_element(By.TAG_NAME, "img").get_attribute("src")
            product_title = i.find_element(By.CSS_SELECTOR, 'h2')
            product_link = product_title.find_element(By.TAG_NAME, "a").get_attribute("href")
            product_price = i.find_element(By.CSS_SELECTOR, 'div[class="search-card-e-price-main"]').text

            product_details = {
                "title": product_title.text,
                "link": product_link,
                "price": float(product_price.split("-")[-1].replace("$", "").replace(",", "")),
                "image_link": product_image_link
            }

            products.append(product_details)
        print(len(products))
    except Exception as e:
        raise HTTPException(status_code=404, detail="No products found.") from e
    finally:
        driver.quit()
        # Clean up the temporary directory
        import shutil
        shutil.rmtree(user_data_dir)
    return products


def search_product_by_image_from_website(image_path):
    file_path = os.path.abspath(image_path)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=options)

    try:
        products = []

        driver.get("https://alibaba.com/")
        driver.implicitly_wait(12)

        # Find the search bar camera
        image_upload_button_div = driver.find_element(By.CSS_SELECTOR, 'div[class="img-upload-button"]')
        image_upload_button_div.click()

        upload_file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        upload_file_input.send_keys(file_path)
        sleep(3)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(25):
            body.send_keys(Keys.PAGE_DOWN)
            sleep(0.5)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.img-search-offer-list > div'))
            )
            products_parent_div = driver.find_elements(By.CSS_SELECTOR, 'div.img-search-offer-list > div')

            for product in products_parent_div:
                product_details = {}

                image_link = product.find_element(By.TAG_NAME, 'img').get_attribute("src")
                product_title_h2 = product.find_element(By.TAG_NAME, 'h2')
                product_link = product_title_h2.find_element(By.TAG_NAME, 'a').get_attribute("href")
                product_price_parent = product.find_element(By.CSS_SELECTOR, 'a[data-spm="d_price"]')
                product_price = product_price_parent.find_element(By.CSS_SELECTOR,
                                                                  'div[class="search-card-e-price-main"]').text

                product_details["image_link"] = image_link
                product_details["product_title"] = product_title_h2.text
                product_details["product_link"] = product_link
                product_details["product_price"] = float(
                    product_price.replace("$", " ").replace(",", "").split("-")[-1])

                products.append(product_details)

        except Exception as e:
            print("Error getting products:", e)

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error searching product by image: {e}")
    finally:
        driver.quit()
        # Clean up the temporary directory
        import shutil
        shutil.rmtree(user_data_dir)
    return products


def delete_file_from_server(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False


# def get_product_comments(product_link):
#     """ Get product reviews from the website """
#     # Driver settings
#     options = webdriver.ChromeOptions()
#     options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # GUI kerak bo‘lmasa
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     # options.add_argument("--disable-gpu")  # Mac