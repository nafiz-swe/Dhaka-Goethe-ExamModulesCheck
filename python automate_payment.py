import pyautogui
import webbrowser
import time

# Open the browser with the specific link
url = "https://payment.ivacbd.com/"
webbrowser.open(url)  # This will open the browser with the specified URL
time.sleep(10)  # Wait for the page to load (adjust this time based on your internet speed)

# Function to check and click the "Send OTP" button and handle popups
def click_send_otp():
    try:
        # Check if "Send OTP" button is present on screen
        otp_button_location = pyautogui.locateOnScreen('send_otp_button_image.png', confidence=0.8)

        if otp_button_location:
            pyautogui.click(otp_button_location)  # Click the "Send OTP" button
            print("Clicked Send OTP button.")
            time.sleep(2)

            # Check if the popup with the "OK" button appears
            ok_button_location = pyautogui.locateOnScreen('popup_ok_button_image.png', confidence=0.8)

            if ok_button_location:
                pyautogui.click(ok_button_location)  # Click the "OK" button
                print("Clicked OK button on popup. Retrying...")
                time.sleep(1)
                click_send_otp()  # Retry clicking "Send OTP" if the popup was found
            else:
                print("OTP sent successfully, no popup detected.")
        else:
            print("Send OTP button not found on screen.")

    except Exception as e:
        print(f"Error: {e}")

# Loop to repeatedly try sending OTP
while True:
    click_send_otp()
    time.sleep(2)  # Wait before retrying
