from flask import Flask, render_template_string
import requests
import time
import webbrowser
import threading

app = Flask(__name__)

# Function to check if the specified text exists in the page (case-insensitive)
def check_condition_text(url, condition_text):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Searching for "Select Module" text hidden in the page's source
            return condition_text.lower() in response.text.lower()
        else:
            return False
    except Exception as e:
        print(f"Error fetching the page: {e}")
        return False

# Function to check periodically
def check_periodically():
    dhaka_url = 'https://www.goethe.de/ins/bd/en/spr/prf/gzb1.cfm'
    condition_text = 'Select Modules'  # We now check for "Select Module"

    while True:
        if check_condition_text(dhaka_url, condition_text):
            # If "Select Module" is found, open the link in a new tab
            webbrowser.open_new_tab(dhaka_url)

        time.sleep(120)  # Wait for 2 minutes before checking again

@app.route('/')
def check_pages():
    # Start the periodic check in a separate thread to run continuously
    threading.Thread(target=check_periodically, daemon=True).start()

    return render_template_string(f"""
        <html>
        <head>
            <title>Checking Goethe Page...</title>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #a0c814; /* Background color */
                    font-family: Arial, sans-serif;
                    color: #fff; /* White text color */
                }}
                .message {{
                    text-align: center;
                    background-color: rgba(255, 255, 255, 0.9); /* White background with transparency */
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }}
                h1 {{
                    color: #a0c814; /* H1 text color */
                }}
                p {{
                    color: #6f4e37; /* Coffee color for p tag */
                }}
            </style>
            <script>
                let countdown = 59; // Start countdown from 59 seconds (1 minute)
                let interval = setInterval(function() {{
                    document.getElementById('countdown').innerText = countdown;
                    countdown--;

                    if (countdown < 0) {{
                        countdown = 59; // Reset countdown to 59 seconds after reaching 0
                    }}
                }}, 1000); // 1 second interval
            </script>
        </head>
        <body>
            <div class="message">
                <h1>Checking for Select Module...</h1>
                <p>Time remaining before next check: <span id="countdown">59</span> seconds.</p>
            </div>
        </body>
        </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # Use reloader=False to prevent Flask from restarting during periodic checks
