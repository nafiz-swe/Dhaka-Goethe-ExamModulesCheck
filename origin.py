from flask import Flask, render_template_string, redirect
import requests

app = Flask(__name__)

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

@app.route('/')
def check_pages():
    # URL to check
    dhaka_url = 'https://www.goethe.de/ins/bd/en/spr/prf/gzb1.cfm'
    # Path to your image (make sure the path is correct)
    image_path = 'static/goeath.jpeg'
    # Path to the audio file
    audio_path = 'static/alert_sound.mp3'  # Add your audio file here
    # Condition text to check
    condition_text = 'exp '  # Change this to your desired condition text

    # Check if the condition text is available on the Dhaka page
    if check_condition_text(dhaka_url, condition_text):
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
                    img {{
                        max-width: 150px; /* Responsive image */
                        height: auto; /* Maintain aspect ratio */
                        margin-bottom: 20px; /* Space between image and text */
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
                    let countdown = 30; // Set countdown time
                    setInterval(function() {{
                        document.getElementById('countdown').innerText = countdown;
                        countdown--;
                    }}, 1000); // 1 second interval
                    setTimeout(function() {{
                        location.reload(); // Reloads the page every 30 seconds
                    }}, 30000); // 30 seconds

                    // Play audio on button click
                    function playAudio() {{
                        var audio = new Audio('{audio_path}');
                        audio.play();
                    }}
                </script>
            </head>
            <body>
                <div class="message">
                    <img src="{image_path}" alt="Goethe Image">
                    <h1>Dhaka Goethe-Zertifikat B1 সিট বুকিং চেক করা হচ্ছে...</h1>
                    <p>Dhaka Goethe থেকে সিট বুকিং ওপেন করা মাত্রই সর্বপ্রথম আপনিই জানতে পারবেন ইন শা আল্লাহ।</p>
                    <p>Wird innerhalb von <span id="countdown">30</span> Sekunden erneut geladen.</p>
                    <button onclick="playAudio()">Click to Play Sound</button>
                </div>
            </body>
            </html>
        """)
    else:
        return redirect(dhaka_url)

if __name__ == '__main__':
    app.run(debug=True)
