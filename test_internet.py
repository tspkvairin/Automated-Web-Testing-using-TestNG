from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def test_login_invalid(driver, base_url, step):
    step("Open /login")
    driver.get(f"{base_url}/login")

    step("Enter wrong credentials")
    driver.find_element(By.CSS_SELECTOR, "#username").send_keys("wronguser")
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys("wrongpass")

    step("Click Login")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    step("Verify error message")
    flash = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#flash"))).text
    assert "Your username is invalid!" in flash


def test_login_valid_and_logout(driver, base_url, step):
    step("Open /login")
    driver.get(f"{base_url}/login")

    step("Enter valid credentials")
    driver.find_element(By.CSS_SELECTOR, "#username").send_keys("tomsmith")
    driver.find_element(By.CSS_SELECTOR, "#password").send_keys("SuperSecretPassword!")

    step("Click Login")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    step("Verify success")
    flash = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#flash"))).text
    assert "You logged into a secure area!" in flash
    assert "/secure" in driver.current_url

    step("Logout")
    driver.find_element(By.CSS_SELECTOR, "a.button.secondary.radius").click()

    step("Verify logout message")
    flash2 = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#flash"))).text
    assert "You logged out of the secure area!" in flash2


def test_checkboxes_toggle_first(driver, base_url, step):
    step("Open /checkboxes")
    driver.get(f"{base_url}/checkboxes")

    step("Wait checkbox #1 to be clickable")
    cb1 = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#checkboxes input[type='checkbox']:nth-of-type(1)")
        )
    )

    step("Wait checkbox #2 to be present (optional, for stability)")
    cb2 = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#checkboxes input[type='checkbox']:nth-of-type(2)")
        )
    )

    step("Read initial states")
    s1, s2 = cb1.is_selected(), cb2.is_selected()

    step("Click checkbox #1")
    cb1.click()

    step("Wait until checkbox #1 toggles")
    WebDriverWait(driver, 5).until(lambda d: cb1.is_selected() != s1)

    step("Verify changes")
    assert cb1.is_selected() != s1
    assert cb2.is_selected() == s2

def test_dropdown_select_option2(driver, base_url, step):
    step("Open /dropdown")
    driver.get(f"{base_url}/dropdown")

    step("Select Option 2")
    el = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dropdown")))
    Select(el).select_by_value("2")

    step("Verify value==2")
    assert el.get_attribute("value") == "2"
