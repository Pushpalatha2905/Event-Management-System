import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import qrcode
from PIL import Image
import io
import base64

# Download NLTK data with error handling
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('vader_lexicon')
except LookupError:
    st.warning("Downloading NLTK data...")
    nltk.download('punkt', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    st.success("NLTK data downloaded successfully!")

# Embedded CSS for attractive design
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #e0f7fa, #b2ebf2);
        font-family: 'Arial', sans-serif;
    }
    h1, h2, h3 {
        color: #0277bd;
    }
    .stButton>button {
        background-color: #0277bd;
        color: white;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #01579b;
    }
    .stTextInput>input, .stTextArea>textarea, .stSelectbox select {
        border: 2px solid #b3e5fc;
        border-radius: 10px;
        padding: 10px;
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
        margin: 15px 0;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .hero {
        text-align: center;
        padding: 40px;
        background: linear-gradient(135deg, #0277bd, #01579b);
        color: white;
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Sample Data
events = [
    {"id": 1, "title": "Tech Summit 2025", "date": "2025-05-10", "location": "Remote", "description": "Explore tech trends."},
    {"id": 2, "title": "Data Conference", "date": "2025-06-15", "location": "New York", "description": "Dive into data analytics."}
]
speakers = {"Tech Summit 2025": [{"name": "Jane Doe", "bio": "Python expert with 10 years experience."}]}
sponsors = {"Tech Summit 2025": [{"name": "TechCorp", "details": "Leading tech innovator."}]}

# AI Functions
def match_skills_to_role(skills):
    roles = {"speaker": ["python", "data", "tech"], "volunteer": ["organize", "team", "help"]}
    tokenized_skills = set(word_tokenize(skills.lower()))
    best_role, best_score = "attendee", 0
    for role, keywords in roles.items():
        score = len(tokenized_skills.intersection(set(keywords))) / len(keywords)
        if score > best_score:
            best_role, best_score = role, score
    return best_role if best_score > 0.3 else "attendee"

def analyze_sentiment(feedback):
    try:
        sia = SentimentIntensityAnalyzer()
        score = sia.polarity_scores(feedback)
        return "Positive" if score['compound'] > 0.1 else "Negative" if score['compound'] < -0.1 else "Neutral"
    except Exception as e:
        st.error(f"Sentiment analysis failed: {e}")
        return "Unknown"

def suggest_schedule(preferences):
    times = ["09:00", "11:00", "14:00", "16:00"]
    return random.choice(times) if "morning" in preferences.lower() else random.choice(times[2:])

def generate_qr(ticket_id):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"Ticket ID: {ticket_id}")
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def create_ticket_pdf(name, event_title, ticket_id):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [
        Paragraph(f"<b>Event Ticket</b>", styles['Title']),
        Paragraph(f"Name: {name}", styles['Normal']),
        Paragraph(f"Event: {event_title}", styles['Normal']),
        Paragraph(f"Ticket ID: {ticket_id}", styles['Normal'])
    ]
    doc.build(story)
    buffer.seek(0)
    return buffer

# Main App
def main():
    st.sidebar.title("🌟 EventSync")
    page = st.sidebar.radio("Navigate", ["Home", "Register", "Agenda", "Speakers & Sponsors", "Check-in", "Feedback", "Analytics"], label_visibility="collapsed")

    if page == "Home":
        st.markdown("<div class='hero'><h1>EventSync: Your Event Hub</h1><p>Plan, Attend, Succeed!</p></div>", unsafe_allow_html=True)
        st.button("Register Now", on_click=lambda: st.query_params.update({"page": "Register"}))

    elif page == "Register":
        st.title("📝 Event Registration")
        with st.form("reg_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            event = st.selectbox("Select Event", [e["title"] for e in events])
            skills = st.text_input("Your Skills (e.g., Python, Organizing)")
            submit = st.form_submit_button("Register & Pay")
            if submit:
                ticket_id = f"{random.randint(1000, 9999)}-{name.split()[0]}"
                st.session_state.attendees = st.session_state.get("attendees", []) + [{"name": name, "email": email, "event": event, "ticket_id": ticket_id}]
                st.success(f"Registered! Ticket ID: {ticket_id}. Confirmation sent to {email} (simulated).")
                qr_img = generate_qr(ticket_id)
                st.image(qr_img, caption="Your QR Code")
                pdf = create_ticket_pdf(name, event, ticket_id)
                st.download_button("Download Ticket PDF", pdf, f"{ticket_id}_ticket.pdf", "application/pdf")
                role = match_skills_to_role(skills)
                st.info(f"AI Suggestion: You’d be great as a {role} for this event!")

    elif page == "Agenda":
        st.title("🗓️ Event Agenda")
        for event in events:
            st.markdown(f"<div class='card'><h3>{event['title']}</h3><p>Date: {event['date']}</p><p>Location: {event['location']}</p><p>{event['description']}</p></div>", unsafe_allow_html=True)

    elif page == "Speakers & Sponsors":
        st.title("🎤 Speakers & Sponsors")
        event = st.selectbox("Select Event", [e["title"] for e in events])
        st.subheader("Speakers")
        for speaker in speakers.get(event, []):
            st.markdown(f"<div class='card'><h3>{speaker['name']}</h3><p>{speaker['bio']}</p></div>", unsafe_allow_html=True)
        st.subheader("Sponsors")
        for sponsor in sponsors.get(event, []):
            st.markdown(f"<div class='card'><h3>{sponsor['name']}</h3><p>{sponsor['details']}</p></div>", unsafe_allow_html=True)

    elif page == "Check-in":
        st.title("✅ Check-in")
        ticket_id = st.text_input("Enter Ticket ID")
        if st.button("Validate QR"):
            attendees = st.session_state.get("attendees", [])
            if any(a["ticket_id"] == ticket_id for a in attendees):
                st.success(f"Valid Ticket! Welcome, {next(a['name'] for a in attendees if a['ticket_id'] == ticket_id)}!")
            else:
                st.error("Invalid Ticket ID.")

    elif page == "Feedback":
        st.title("📊 Feedback")
        with st.form("feedback_form"):
            event = st.selectbox("Event", [e["title"] for e in events])
            feedback = st.text_area("Your Feedback")
            time_pref = st.text_input("Preferred Session Time (e.g., morning)")
            submit = st.form_submit_button("Submit")
            if submit:
                st.session_state.feedback = st.session_state.get("feedback", []) + [{"event": event, "text": feedback}]
                sentiment = analyze_sentiment(feedback)
                st.success(f"Thanks! Sentiment: {sentiment}")
                schedule = suggest_schedule(time_pref)
                st.info(f"AI Suggestion: Next session at {schedule}")

    elif page == "Analytics":
        st.title("📈 Analytics")
        attendees = st.session_state.get("attendees", [])
        feedback = st.session_state.get("feedback", [])
        st.write(f"Total Attendees: {len(attendees)}")
        for event in events:
            count = sum(1 for a in attendees if a["event"] == event["title"])
            st.markdown(f"<div class='card'><p>{event['title']}: {count} attendees</p></div>", unsafe_allow_html=True)
        st.subheader("Feedback Insights")
        for fb in feedback:
            sentiment = analyze_sentiment(fb["text"])
            st.markdown(f"<div class='card'><p>{fb['event']}: {fb['text']} (Sentiment: {sentiment})</p></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
