from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "URL GOES HERE"

driver = webdriver.Chrome()
driver.get(url)
input("Press Enter after you've signed in and navigated to Data Validation settings...")

def add_color_to_item(idx):
    # Wait for and click "Add another item" button
    wait = WebDriverWait(driver, 10)
    # Find all rows and select the one at the specified index
    rows = wait.until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, 'waffle-condition-arg-row')
    ))
    new_row = rows[idx]
    
    # Name of the DV option
    input_field = new_row.find_element(By.CLASS_NAME, 'waffle-datavalidation-condition-arg-row-editbox')
    current_value = input_field.get_attribute('value')
    print(f"Current value: {current_value}")
    # check if current value is a color
    if current_value.startswith("#"):
        print("Color found")
        hex_code = current_value
    else:
        print("Color not found")
        return
    
    # Find and click the color picker button in the current row
    color_btn = new_row.find_element(By.CLASS_NAME, 'docs-flatcolormenubutton')
    color_btn.click()

    # Active color picker menu
    active = "//div[contains(@class, 'goog-menu') and @tabindex='0']"

    ### note that this is all necessary because gsheets does not remove the previous color picker menu
    ### when a new one is opened, so we have to find the active one each time

    # Find the Customize button within the active menu
    custom_btn = driver.find_element(By.XPATH, f"{active}//div[contains(@class, 'previewableColorMenuCustomizeButton') and text()='Customize']")
    custom_btn.click()

    # Find the hex input
    hex_input = driver.find_element(By.XPATH, f"{active}//input[@class='docs-material-hsv-color-picker-input docs-material-hex-input']")
    
    # Clear and set the hex value
    driver.execute_script("arguments[0].value = '';", hex_input)
    hex_input.send_keys(hex_code)

    # Find and click OK button
    ok_btn = driver.find_element(By.XPATH, f"{active}//div[contains(@class, 'previewableCustomColorMenuOkayButton') and text()='OK']")
    ok_btn.click()
    

try:
    wait = WebDriverWait(driver, 10)
    rows = wait.until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, 'waffle-condition-arg-row')
    ))
    print(f"Found {len(rows)} items")
    for idx in range(len(rows)):
        add_color_to_item(idx)
except Exception as e:
    print(f"Error occurred: {e}")
finally:
    input("Process completed. Press Enter to close the browser...")
    driver.quit()