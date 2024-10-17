from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB configuration
app.config['MONGO_URI'] = "mongodb+srv://vedant:vedant@portfolio.e8ky0.mongodb.net/lovemail"
mongo = PyMongo(app)

poems = [
    """In a world of chaos, you are my calm,  
    A soothing melody, a healing balm.  
    Your laughter is my favorite song,  
    With you is where I truly belong.""",

    """When stars align and the moonlight glows,  
    My heart whispers secrets only it knows.  
    Your eyes, like galaxies, draw me in deep,  
    In your embrace, my soul finds peace in sleep.""",

    """With every heartbeat, my love for you grows,  
    Like a river that flows, forever it knows.  
    You're the dream I chase, my heart's desire,  
    In your presence, I feel my soul catch fire.""",

    """Like a rose in bloom, your beauty does shine,  
    Each moment with you feels perfectly divine.  
    Together we dance in this symphony sweet,  
    With you by my side, my life is complete.""",

    """Through the storms and the trials, we'll always stand tall,  
    With you as my partner, I can conquer it all.  
    So take my hand, let's write our own tale,  
    Together forever, love will never fail.""",

    # Hindi Shayaris
    """तुम्हारे बिना हर लम्हा अधूरा सा लगता है,  
    जैसे चाँद बिना रात का, सवेरा बिना उजाला।  
    तुम हो मेरी खुशियों की सबसे खूबसूरत कहानी,  
    तुम्हारी मोहब्बत ही है, जो दिल को है भाए.""",

    """तेरे इश्क में खो जाने को जी चाहता है,  
    तेरे हर लफ्ज़ में अपना नाम सुनने को जी चाहता है।  
    तुम्हारी बाहों में सुकून मिले ऐसा ख्वाब है,  
    बस तुझे अपने दिल के करीब लाने को जी चाहता है.""",

    """जब से देखा तुम्हे, दिल में एक जादू सा है,  
    तुम्हारी मुस्कान में सारा जहां बसा सा है।  
    तुम हो मेरी ज़िंदगी का वो खूबसूरत ख्वाब,  
    जिसे हर रोज़ देखने की ख्वाहिश सदा बसा सा है.""",

    """हर सुबह तुम्हारे ख्यालों से होती है,  
    तुम्हारी यादों में ही मेरी खुशियाँ छुपी हैं।  
    तुम्हारे बिना ये जीवन अधूरा है,  
    तुम मेरी ज़िंदगी की सबसे प्यारी किताब हो.""",

    """तेरा नाम लूँ जुबां से, ये ख्वाब बन जाए,  
    तेरी खुशबू में बसा हर लम्हा, खुदा बन जाए।  
    दिल से दिल की बातें हों, ये प्यार का असर,  
    तुझसे मिलने की चाहत में हर एक पल गुजर जाए.""",

    # Marathi Shayaris
    """तू माझ्या मनात, हृदयात एक चंद्र आहेस,  
    तुझ्या हसण्यात जीवनाचा आनंद आहेस.  
    तुझ्या प्रेमात एक वेगळाच जादू आहे,  
    तूच माझ्या हृदयाचा गोड स्वप्न आहेस.""",

    """प्रेमाचे तुझ्या पावलांनी, गार्डन सजले आहे,  
    प्रत्येक क्षणी तुझ्या गाण्याने, मन जिंकले आहे.  
    तुझ्या सोबत फिरताना, जरा थांबून बघ,  
    आपण प्रेमाची कहाणी, एकत्र रचले आहे.""",

    """तू आहेस माझा सूर्य, तूच माझी चांदणी,  
    तुझ्या प्रेमात बहरले, माझे मन आणि कशी.  
    तुझ्या प्रेमाचा झरा, जळतो गालिचा,  
    तुझ्या आठवणींमध्ये, जीवन फुलतो सदा.""",

    """तू जरी दूर असलीस, तरी हृदयात आहेस,  
    तुझ्या आठवणींमध्ये, सदैव मी आहेस.  
    तुझ्या प्रेमाची शिदोरी, जळते हृदयात,  
    प्रेमाच्या सागरात, लहरते सदा रात.""",

    """तुझ्या साठी सगळं काही, मी तयार आहे,  
    प्रेमात तुझ्या, जीवन हसरा आहे.  
    एक क्षण तुमच्यासोबत, जगभरचा आनंद,  
    तुझ्यावर प्रेम करणे, हीच माझी भक्ति आहे."""
]

love_quotes = [
    "“Love is not about how many days, months, or years you have been together. Love is about how much you love each other every single day.”",
    "“You know you’re in love when you can’t fall asleep because reality is finally better than your dreams.”",
    "“I have waited for this opportunity for more than half a century, to repeat to you once again my vow of eternal fidelity and everlasting love.”",
    "“Love is composed of a single soul inhabiting two bodies.”",
    "“The best thing to hold onto in life is each other.”"
]

quote_list = [
    ("The best thing to hold onto in life is each other.", "Audrey Hepburn"),
    ("Love all, trust a few, do wrong to none.", "William Shakespeare"),
    ("I have waited for this opportunity for more than half a century, to repeat to you once again my vow of eternal fidelity and everlasting love.", "Gabriel Garcia Marquez"),
    ("You know you're in love when you can't fall asleep because reality is finally better than your dreams.", "Dr. Seuss"),
    ("Love is composed of a single soul inhabiting two bodies.", "Aristotle"),
    ("I am yours, don’t give myself back to me.", "Rumi"),
    ("To love and be loved is to feel the sun from both sides.", "David Viscott"),
    ("The greatest happiness of life is the conviction that we are loved; loved for ourselves, or rather, loved in spite of ourselves.", "Victor Hugo"),
    ("We accept the love we think we deserve.", "Stephen Chbosky"),
    ("Love is not about possession. Love is about appreciation.", "Osho"),
    ("In the end, we only regret the chances we didn’t take.", "Lewis Carroll"),
    ("You know you’re in love when you can’t fall asleep because reality is finally better than your dreams.", "Dr. Seuss"),
    ("Love is a canvas furnished by nature and embroidered by imagination.", "Voltaire"),
    ("Love is an irresistible desire to be irresistibly desired.", "Robert Frost"),
    ("You come to love not by finding the perfect person, but by seeing an imperfect person perfectly.", "Sam Keen"),
    ("I have found the one whom my soul loves.", "Song of Solomon 3:4"),
    ("Love is composed of a single soul inhabiting two bodies.", "Aristotle"),
    ("A friend is someone who knows all about you and still loves you.", "Elbert Hubbard"),
    ("You don't love someone for their looks, or their clothes, or for their fancy car, but because they sing a song only you can hear.", "Oscar Wilde"),
    ("The best thing to hold onto in life is each other.", "Audrey Hepburn"),
    ("There is no remedy for love but to love more.", "Henry David Thoreau"),
    ("Love is the only force capable of transforming an enemy into a friend.", "Martin Luther King Jr."),
    ("I love you, not only for what you are, but for what I am when I am with you.", "Roy Croft"),
    ("Being deeply loved by someone gives you strength while loving someone deeply gives you courage.", "Lao Tzu"),
    ("Love is a promise; love is a souvenir, once given never forgotten, never let it disappear.", "John Lennon"),
    ("Love is when the other person’s happiness is more important than your own.", "H. Jackson Brown Jr."),
    ("I knew I loved you before I met you.", "Savage Garden"),
    ("Love does not dominate; it cultivates.", "Johann Wolfgang von Goethe"),
    ("To love is to recognize yourself in another.", "Eckhart Tolle"),
    ("Every love story is beautiful, but ours is my favorite.", "Unknown"),
    ("You are my sun, my moon, and all my stars.", "E.E. Cummings"),
    ("Love is friendship that has caught fire.", "Anne Sexton"),
    ("We are most alive when we're in love.", "John Updike"),
    ("In the end, love is all that matters.", "Unknown"),
    ("True love stories never have endings.", "Richard Bach"),
    ("Where there is love there is life.", "Mahatma Gandhi"),
    ("The heart has its reasons of which reason knows nothing.", "Blaise Pascal"),
]

# Route for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = mongo.db.users.find_one({"email": email})

        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            flash('Login successful!', 'success')
            return redirect(url_for('main'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

# Route for signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)

        # Check if the user already exists
        if mongo.db.users.find_one({"email": email}):
            flash('Email already exists!', 'error')
            return redirect(url_for('signup'))

        # Insert new user into MongoDB
        mongo.db.users.insert_one({"email": email, "password": hashed_password})
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Route for main page where confession happens
@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'user_id' not in session:
        flash('Please login first!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        receiver_email = request.form.get('receiver_email')
        receiver_name = request.form.get('receiver_name')
        message_content = request.form.get('message')
        sender_name = request.form.get('sender_name')
        
        confession_data = {
        'receiver_email': receiver_email,
        'receiver_name': receiver_name,
        'message_content': message_content,
        'sender_name': sender_name
    }

    # Insert the document into the 'confessions' collection
        mongo.db.confessions.insert_one(confession_data)


        # Email-sending logic
        sender_email = "love.mail.000000@gmail.com"  # Replace with your email
        sender_password = "gobb lgvl adib jnsc"  # Replace with your email password
        subject = "A Love Confession for You ❤️"

        try:
            # Setting up the email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Randomly select a poem from the list
            selected_poem = random.choice(poems)
            selected_quote = random.choice(love_quotes)


# Compose the email body with the selected poem
            # Compose the email body with HTML formatting
            body = f"""<html>
<head>
    <style>
        body {{
            font-family: 'Georgia', serif;
            line-height: 1.8;
            color: #333;
            background-color: #fdf6f9; /* Light background color for contrast */
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            color: #ff69b4; /* Pink color for the header */
            font-size: 36px;
            margin-bottom: 20px;
            text-shadow: 1px 1px 2px #ff1493; /* Subtle shadow effect */
        }}
        h2 {{
            color: #ff1493; /* Darker pink for subheading */
            font-size: 28px;
            margin-top: 20px;
            text-align: center;
            border-bottom: 2px solid #ff69b4; /* Bottom border for emphasis */
            padding-bottom: 10px;
        }}
        .confession {{
            background-color: rgba(255, 182, 193, 0.5); /* Light pink for confession background */
            border: 3px solid #ff69b4; /* Thicker pink border */
            border-radius: 10px; /* Rounded corners */
            padding: 20px; /* Increased padding for better spacing */
            margin: 30px 0;
            position: relative; /* For positioning the icon */
            padding-left: 50px; /* Add padding for the icon */
            font-size: 22px; /* Increased font size for confession */
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Shadow effect */
        }}
        .confession:before {{
            content: '💌'; /* Heart icon for confession */
            position: absolute;
            left: 15px;
            top: 10px;
            font-size: 35px; /* Size of the icon */
        }}
        .poem {{
            font-style: italic;
            color: #c71585; /* Deeper pink for the poem */
            margin: 30px 0;
            padding: 15px;
            border-left: 4px solid #ff69b4; /* Stylish left border */
            background-color: rgba(255, 182, 193, 0.3); /* Light pink background */
            font-size: 20px; /* Increased font size */
            border-radius: 8px; /* Rounded corners */
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Shadow effect */
        }}
        .message {{
            font-size: 18px; /* Increased font size */
            margin: 20px 0;
            background-color: rgba(255, 228, 225, 0.3); /* Very light pink for message */
            padding: 10px;
            border-radius: 5px; /* Slight rounding */
        }}
        .signature {{
            font-weight: bold;
            margin-top: 30px;
            font-size: 22px; /* Increased font size */
            color: #ff1493; /* Darker pink for the signature */
            text-align: center; /* Center alignment */
            text-shadow: 1px 1px 2px #ff69b4; /* Subtle shadow effect */
        }}
        .footer {{
            font-size: 0.9em;
            color: #777; /* Lighter text for footer */
            margin-top: 20px;
            text-align: center;
        }}
        .heart {{
            color: #ff1493; /* Heart color */
            font-size: 24px;
        }}
        .container {{
            max-width: 600px;
            margin: auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); /* Thicker shadow */
        }}
        .quote {{
            font-style: italic;
            color: #ff69b4; /* Soft pink for quotes */
            margin: 20px 0;
            padding: 10px;
            border-left: 4px solid #ff69b4; /* Stylish left border */
            background-color: rgba(255, 228, 225, 0.3); /* Light pink background */
            border-radius: 5px; /* Slight rounding */
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Shadow effect */
        }}
        .decorative-line {{
            height: 2px;
            background-color: #ff69b4; /* Color of the decorative line */
            margin: 20px 0; /* Spacing above and below the line */
        }}
        .website-link {{
            color: #ff69b4; /* Pink color for the website link */
            text-decoration: none; /* Remove underline */
            font-weight: bold; /* Bold text for emphasis */
        }}
        .website-link:hover {{
            text-decoration: underline; /* Underline on hover */
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>💖 A Special Confession 💖</h1>
        
        <h3>Dear {receiver_name},</h3>

        <div class="decorative-line"></div>
        <h2>Confession:</h2>
        <div class="confession">{message_content}</div>
        <div class="decorative-line"></div>

        <h2>A Poem Just for You:</h2>
        <div class="poem">{selected_poem}</div>
        <div class="decorative-line"></div>

        <h2>Quote of Love</h2>
        <h3 class="quote">{selected_quote}</h3>

        <p class="signature">Forever yours,<br>{sender_name} <span class="heart">❤️</span></p>
        
        <p class="footer">This message is sent with love and affection.<br>May your heart always be filled with joy and sweetness.</p>
        
        <p class="footer">Visit us at: <a href="https://www.lovemail.onrender.com" class="website-link">LoveMail</a></p>
    </div>
</body>
</html>
"""


            msg.attach(MIMEText(body, 'html'))

            # Connecting to the SMTP server and sending the email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()

            flash('Your love confession has been sent successfully!', 'success')

            return redirect(url_for('quotes'))

        except Exception as e:
            flash(f'Failed to send email. Error: {str(e)}', 'error')
    
    return render_template('main.html')


@app.route('/quotes')
def quotes():
    # Initialize or retrieve the current index from the session
    if 'current_index' not in session:
        session['current_index'] = 0
    else:
        session['current_index'] = (session['current_index'] + 1) % len(quote_list)

    # Get the current quote and author
    current_quote = quote_list[session['current_index']]

    return render_template('quotes.html', quote=current_quote)

if __name__ == '__main__':
    app.run(debug=True)
