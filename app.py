import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
import base64
from datetime import datetime

# Set page config as the FIRST Streamlit command
st.set_page_config(page_title="EventSync - Event Management", layout="wide")

# Attempt to import NLTK with fallback
try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    NLTK_AVAILABLE = True
    # Download NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('vader_lexicon')
    except LookupError:
        st.warning("Downloading NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('vader_lexicon', quiet=True)
        st.success("NLTK data downloaded!")
except ImportError:
    NLTK_AVAILABLE = False
    st.error("NLTK module not found. AI features (sentiment analysis, skill matching) will be disabled.")

# Session State Initialization
if 'attendees' not in st.session_state:
    st.session_state.attendees = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = []

# Embedded CSS for Attractive Design
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f0f4f8, #d9e6f2);
        font-family: 'Arial', sans-serif;
    }
    h1, h2, h3 {
        color: #1a73e8;
    }
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background 0.3s;
    }
    .stButton>button:hover {
        background-color: #1557b0;
    }
    .stTextInput>input, .stTextArea>textarea, .stSelectbox select {
        border: 2px solid #1a73e8;
        border-radius: 10px;
        padding: 10px;
        background-color: #fff;
    }
    .stSidebar {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .card {
        background: #ffffff;
        padding: 20px;
        margin: 10px 0;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .hero {
        text-align: center;
        padding: 40px;
        background: linear-gradient(135deg, #1a73e8, #0d47a1);
        color: white;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🌟 EventSync")
menu = st.sidebar.radio("Menu", ["Home", "Register", "Attendees", "Agenda", "Speakers & Sponsors", "Check-in", "Feedback & Analytics"], label_visibility="collapsed")

# Sample Data
events = [
    {"title": "Tech Summit 2025", "date": "2025-05-10", "location": "Remote", "description": "Explore tech trends."},
    {"title": "Data Conference", "date": "2025-06-15", "location": "New York", "description": "Dive into data analytics."}
]
speakers = {"Tech Summit 2025": [{"name": "Jane Doe", "bio": "Python expert"}]}

# Utility Functions
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def match_skills_to_role(skills):
    if not NLTK_AVAILABLE:
        return "attendee (AI unavailable)"
    roles = {"speaker": ["python", "data", "tech"], "volunteer": ["organize", "team", "help"]}
    tokenized_skills = set(word_tokenize(skills.lower()))
    best_role, best_score = "attendee", 0
    for role, keywords in roles.items():
        score = len(tokenized_skills.intersection(set(keywords))) / len(keywords)
        if score > best_score:
            best_role, best_score = role, score
    return best_role if best_score > 0.3 else "attendee"

def analyze_sentiment(feedback):
    if not NLTK_AVAILABLE:
        return "Unknown (AI unavailable)"
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(feedback)
    return "Positive" if score['compound'] > 0.1 else "Negative" if score['compound'] < -0.1 else "Neutral"

# Pages
if menu == "Home":
    st.markdown("<div class='hero'><h1>Welcome to EventSync</h1><p>Your All-in-One Event Management Solution</p></div>", unsafe_allow_html=True)
    st.button("Get Started", on_click=lambda: st.query_params.update({"page": "Register"}))

elif menu == "Register":
    st.subheader("📋 Event Registration")
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email")
        with col2:
            phone = st.text_input("Phone Number")
            ticket_type = st.selectbox("Ticket Type", ["Free", "VIP", "Student"])
        skills = st.text_input("Your Skills (e.g., Python, Organizing)")
        submit = st.form_submit_button("Register")
        if submit:
            if name and email and phone:
                attendee = {
                    "Name": name,
                    "Email": email,
                    "Phone": phone,
                    "Ticket Type": ticket_type,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Ticket ID": f"{random.randint(1000, 9999)}-{name.split()[0]}"
                }
                st.session_state.attendees.append(attendee)
                st.success(f"Registration successful! Ticket ID: {attendee['Ticket ID']} (Email confirmation simulated).")
                role = match_skills_to_role(skills)
                st.info(f"AI Suggestion: You’d be great as a {role}!")
            else:
                st.error("Please fill all fields.")

elif menu == "Attendees":
    st.subheader("📋 Registered Attendees")
    df = pd.DataFrame(st.session_state.attendees)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, "attendees.csv", "text/csv")
    else:
        st.info("No attendees registered yet.")

elif menu == "Agenda":
    st.subheader("🗓️ Event Agenda")
    for event in events:
        st.markdown(f"<div class='card'><h3>{event['title']}</h3><p>Date: {event['date']}</p><p>Location: {event['location']}</p><p>{event['description']}</p></div>", unsafe_allow_html=True)

elif menu == "Speakers & Sponsors":
    st.subheader("🎤 Speakers & Sponsors")
    event = st.selectbox("Select Event", [e["title"] for e in events])
    st.markdown("<h3>Speakers</h3>", unsafe_allow_html=True)
    for speaker in speakers.get(event, []):
        st.markdown(f"<div class='card'><h4>{speaker['name']}</h4><p>{speaker['bio']}</p></div>", unsafe_allow_html=True)
    st.markdown("<h3>Sponsors</h3>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h4>TechCorp</h4><p>Leading tech innovator</p></div>", unsafe_allow_html=True)

elif menu == "Check-in":
    st.subheader("✅ Check-in")
    ticket_id = st.text_input("Enter Ticket ID")
    if st.button("Validate"):
        df = pd.DataFrame(st.session_state.attendees)
        if ticket_id in df['Ticket ID'].values:
            name = df[df['Ticket ID'] == ticket_id]['Name'].iloc[0]
            st.success(f"Valid Ticket! Welcome, {name}!")
            qr_img = generate_qr_code(ticket_id)
            st.markdown(f'<img src="data:image/png;base64,{qr_img}" width="200"/>', unsafe_allow_html=True)
        else:
            st.error("Invalid Ticket ID.")

elif menu == "Feedback & Analytics":
    st.subheader("📊 Feedback & Analytics")
    with st.form("feedback_form"):
        feedback_name = st.text_input("Your Name")
        rating = st.slider("Rate the Event (1-5)", 1, 5, 3)
        comments = st.text_area("Comments")
        submit = st.form_submit_button("Submit Feedback")
        if submit:
            if feedback_name and comments:
                feedback_entry = {
                    "Name": feedback_name,
                    "Rating": rating,
                    "Comments": comments,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Sentiment": analyze_sentiment(comments)
                }
                st.session_state.feedback.append(feedback_entry)
                st.success(f"Thanks, {feedback_name}! Sentiment: {feedback_entry['Sentiment']}")
            else:
                st.error("Please fill all fields.")

    # Analytics
    df_attendees = pd.DataFrame(st.session_state.attendees)
    df_feedback = pd.DataFrame(st.session_state.feedback)
    if not df_attendees.empty:
        st.markdown("<h3>Ticket Type Distribution</h3>", unsafe_allow_html=True)
        st.bar_chart(df_attendees['Ticket Type'].value_counts())
    if not df_feedback.empty:
        st.markdown("<h3>Feedback Insights</h3>", unsafe_allow_html=True)
        st.dataframe(df_feedback[['Name', 'Rating', 'Sentiment']], use_container_width=True)
        st.markdown("<h3>Average Rating</h3>", unsafe_allow_html=True)
        st.write(f"{df_feedback['Rating'].mean():.2f}/5")

if __name__ == "__main__":
    st.title("🎉 AI-Powered Event Management System")
    main()
