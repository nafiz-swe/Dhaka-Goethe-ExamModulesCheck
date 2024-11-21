from flask import Flask, render_template_string, redirect
import requests
from flask_mail import Mail, Message
import sqlite3

app = Flask(__name__)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your mail server
app.config['MAIL_PORT'] = 587  # Typically 587 for TLS
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'shosurbari@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'uiahdjkcnrkutsak'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'shosurbari@gmail.com'  # Default sender

mail = Mail(app)

# Function to check if the specified text exists in the page (case-insensitive)
def check_condition_text(url, condition_text):
    try:
        # Fetch the page content
        response = requests.get(url)
        if response.status_code == 200:
            # Check if the condition text exists in a case-insensitive manner
            return condition_text.lower() in response.text.lower()  # Convert both to lowercase for comparison
        else:
            return False
    except Exception as e:
        print(f"Error fetching the page: {e}")
        return False

def send_email(recipient, subject, body):
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)

def get_user_emails():
    # Connect to the SQLite database (adjust the path if necessary)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM users')
    emails = [row[0] for row in cursor.fetchall()]
    conn.close()
    return emails

@app.route('/')
def check_pages():
    # URL to check
    dhaka_url = 'https://www.goethe.de/ins/bd/en/spr/prf/gzb1.cfm'
    # Path to the audio file
    audio_path = 'static/alert_sound.mp3'  # Add your audio file here
    # Condition text to check
    condition_text = 'select'  # Change this to your desired condition text

    # Check if the condition text is available on the Dhaka page
    if check_condition_text(dhaka_url, condition_text):
        # Send email notifications
        user_emails = get_user_emails()
        email_body = "আপনার সিট বুকিং করতে লিঙ্কে ক্লিক করুন: " + dhaka_url
        for email in user_emails:
            send_email(email, "Exam Booking Date Open", email_body)

        return render_template_string(f"""
            <html>
            <head>
                <title>Deutsch</title>
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
                    span {{
                        color: red;
                    }}
                    .message {{
                        text-align: center;
                        animation: fadeIn 1s ease-in-out;
                        background-color: rgba(255, 255, 255, 0.9); /* White background with transparency */
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    }}
                    @keyframes fadeIn {{
                        from {{
                            opacity: 0;
                        }}
                        to {{
                            opacity: 1;
                        }}
                    }}
                    h1 {{
                        color: #a0c814; /* H1 text color */
                    }}
                    p {{
                        color: #6f4e37; /* Coffee color for p tag */
                    }}
                    button {{
                        background-color: #4CAF50; /* Green */
                        border: none;
                        color: white;
                        padding: 15px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                    }}
                </style>
                <script>
                    let countdown = 60; // Set countdown time
                    setInterval(function() {{
                        document.getElementById('countdown').innerText = countdown;
                        countdown--;
                    }}, 1000); // 1 second interval
                    setTimeout(function() {{
                        location.reload(); // Reloads the page every 60 seconds
                    }}, 60000); // 60 seconds

                    // Play audio on button click
                    function playAudio() {{
                        var audio = new Audio('{audio_path}');
                        audio.play();
                    }}
                </script>
            </head>
            <body>
                <div class="message">
                    <h1>Dhaka Goethe-Zertifikat B1 সিট বুকিং চেক করা হচ্ছে...</h1>
                    <p>Dhaka Goethe থেকে সিট বুকিং ওপেন করা মাত্রই সর্বপ্রথম আপনিই জানতে পারবেন ইন শা আল্লাহ।</p>
                    <p>Wird innerhalb von <span id="countdown">60</span> Sekunden erneut geladen.</p>
                    <button onclick="playAudio()">Click to Play Sound</button>
                </div>
            </body>
            </html>
        """)
    else:
        return redirect(dhaka_url)

if __name__ == '__main__':
    app.run(debug=True)
