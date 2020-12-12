from selenium import webdriver


driver = webdriver.Chrome(executable_path=r"chromedriver.exe")

driver.get("http://user:z4$9byH!jc@3.16.46.200:8080/")


# Creating a list of CATALOG ITEMS here

catalog_listing_arrow = driver.find_element_by_xpath('//*[@id="companyInput"]/span[2]')   # listing items only works with visible ones, open the list before listing it lol
catalog_listing_arrow.click()

catalog_listing = [el.text for el in driver.find_elements_by_xpath("//ul[@id='companyDropDown']/li")]    # lists items in the list -_-  ## can also add .find_elements_by_tag_name("li")
print(catalog_listing)

for list_elem in catalog_listing:
    element = driver.find_element_by_xpath(f"//ul[@id='companyDropDown']/li[text()='{list_elem}']")
    driver.execute_script("arguments[0].click();", element)             # works with hidden elements

# element = driver.find_element_by_xpath(f"//ul[@id='companyDropDown']/li[text()='Aaron Watson']")
# driver.execute_script("arguments[0].click();", element)             # works with hidden elements

#driver.close()