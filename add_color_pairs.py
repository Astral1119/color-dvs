id = "ID (NOT URL) GOES HERE"
url = f"https://docs.google.com/spreadsheets/d/{id}/edit#gid=0"
hex_range = "HEX RANGE GOES HERE (e.g. 'B2:B')"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_values(spreadsheet_id, range_name):
  """
  Creates the batch_update the user has access to.
  Load pre-authorized user credentials from the environment.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  # pylint: disable=maybe-no-member
  try:
    service = build("sheets", "v4", credentials=creds)

    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )
    rows = result.get("values", [])
    print(f"{len(rows)} rows retrieved")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get(url)
input("Press Enter after you've signed in and navigated to Data Validation settings...")

def add_color_to_item(idx, hex_code):
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
    values = get_values(id, hex_range)

    wait = WebDriverWait(driver, 10)
    rows = wait.until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, 'waffle-condition-arg-row')
    ))
    
    num_rows = len(rows)
    num_values = len(values["values"])

    if num_rows != num_values:
        raise ValueError(f"Number of rows ({num_rows}) does not match number of values ({num_values})")

    for idx, row in enumerate(values["values"]):
        hex_code = row[0]
        add_color_to_item(idx, hex_code)

except Exception as e:
    print(f"Error occurred: {e}")
finally:
    input("Process completed. Press Enter to close the browser...")
    driver.quit()
