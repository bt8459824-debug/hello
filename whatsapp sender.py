import time
from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

@app.route('/')
def home():
    # This loads your green dashboard when you visit http://127.0.0
    return render_template('whatsapp sender frontend2.html')

@app.route("/login", methods=["POST"])
def credentials():
    # 1. Grab data from your HTML form fields when user clicks submit
    phone_number = request.form.get("phone_number")
    clean_number = "".join(filter(str.isdigit, phone_number))
    message = request.form.get("message")
    encoded_message = message.replace(" ", "%20")
    
    try:
        num_loop = int(request.form.get("number_of_messages") or 1)
    except ValueError:
        num_loop = 1

    # 2. Start Selenium right here inside the submit route!
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True) # Keeps the browser window open
    driver = webdriver.Chrome(options=options)
    
    try:
        # Open the specific WhatsApp Web URL with your form inputs
        url = f"https://api.whatsapp.com/send?phone={clean_number}&text={encoded_message}"
        driver.get(url)
        
        print("Please scan the QR code on your phone if prompted.")
        
        # Wait up to 30 seconds for the WhatsApp send button to load
        wait = WebDriverWait(driver, 30)
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
        
        # Loop to send the message multiple times based on your form input
        for i in range(num_loop):
            send_button.click()
            time.sleep(1) 
            
    except Exception as e:
        print(f"Selenium error: {e}")
        return f"An error occurred inside the automation window: {e}", 500

    # 3. What the browser displays after finishing the loop
    return "<h1>Success!</h1><p>Messages are being processed in the automated browser window.</p>"

if __name__ == "__main__":
    app.run(debug=True, port=69696)