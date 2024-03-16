import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Opening the website on Chrome
driver = webdriver.Chrome()
driver.get("https://food.grab.com/sg/en/restaurants")
driver.maximize_window()

# Function for append data to json file
def write_json(new_data, filename="restaurants.json"):
    try:
        with open(filename, "r+") as file:
            file_data = json.load(file)
            file_data["restaurants"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
    except FileNotFoundError:
        with open(filename, "w") as file:
            json.dump({"restaurants": [new_data]}, file, indent=4)

for i in range(15):
    try:
        # wait for the data to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
        )
        
        # get the data from website
        data = driver.find_element("id", "__NEXT_DATA__").get_attribute("innerHTML")
        parsedData = json.loads(data)

        restaurantLists = parsedData["props"]["initialReduxState"]["pageRestaurantsV2"]["entities"]["restaurantList"]

        # append restaurant to json file
        for key in restaurantLists:
            restaurant = {}
            restaurant["title"] = restaurantLists[key]["name"]
            restaurant["latitude"] = restaurantLists[key]["latitude"]
            restaurant["longitude"] = restaurantLists[key]["longitude"]
            write_json(restaurant)

        # catch the load more button and clicking it
        load_more = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "load-more-btn")]'))
        )
        load_more.click()
    except Exception as e:
        print(f"An error occurred: {e}")

driver.quit()
