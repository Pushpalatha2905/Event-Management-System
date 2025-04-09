import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
import qrcode
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="NextGen Events | Vignan University 🎟️", page_icon="🎉", layout="centered")

# --- SESSION STATE ---
if 'participants' not in st.session_state:
    st.session_state.participants = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = []

# --- HEADER ---
st.markdown("""
    <div style="text-align:center">
        <h1 style="color:#4CAF50;">🎉 NextGen Events Platform</h1>
        <p><b>Organize, Engage & Analyze Events at Vignan University</b></p>
    </div>
""", unsafe_allow_html=True)
st.markdown("---")

# --- SIDEBAR NAVIGATION ---
page = st.sidebar.radio("🔎 Navigate", ["🏠 Home", "📥 Register", "📋 Attendees", "📅 Agenda", "🎤 Speakers & Sponsors", "📊 Analytics", "✅ QR Check-in", "📝 Feedback"])

# --- PAGE CONTENTS ---

if page == "🏠 Home":
    st.image("https://img.freepik.com/free-vector/event-management-abstract-concept-illustration_335657-3880.jpg", use_column_width=True)

    st.markdown("""
        <div style="background-color:#f9f9f9; padding: 20px; border-radius: 15px; border: 1px solid #ddd;">
            <h3 style="color:#4CAF50;">📢 Why Use This Platform?</h3>
            <ul style="font-size:16px; line-height:1.7;">
                <li>🚀 Fast and easy event registration</li>
                <li>✅ QR Ticket generation for seamless check-in</li>
                <li>📬 Instant email confirmation (simulated)</li>
                <li>📊 Real-time event analytics</li>
                <li>🗣️ Speaker and sponsor highlights</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align:center; margin-top:30px;">
            <h4 style="color:#FF5722;">🌟 Join. Experience. Network. Grow. 🌟</h4>
            <p style="font-size:15px;">Make every event at Vignan University unforgettable with NextGen Events! 🎓✨</p>
        </div>  
    """, unsafe_allow_html=True)

    st.success("Made for Students by PushpaLatha @ Vignan's University ✨")

elif page == "📥 Register":
    st.subheader("📥 Event Registration")

    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Full Name", max_chars=50)
            email = st.text_input("📧 Email")
            phone = st.text_input("📱 Phone Number")
        with col2:
            event_name = st.selectbox("🎯 Select Event", ["AI Conference 2025", "Startup Pitch Fest", "Tech Expo", "Crypto Workshop"])
            num_tickets = st.number_input("🎫 Number of Tickets", min_value=1, max_value=5, value=1)
            event_date = st.date_input("📅 Event Date", min_value=datetime.today())
        submitted = st.form_submit_button("✅ Register Now")

        if submitted and name and email:
            participant_id = str(uuid.uuid4())[:8]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for _ in range(num_tickets):
                st.session_state.participants.append({
                    "ID": participant_id,
                    "Name": name,
                    "Email": email,
                    "Phone": phone,
                    "Event": event_name,
                    "Date": event_date.strftime("%Y-%m-%d"),
                    "Timestamp": timestamp
                })

            st.success(f"🎉 Registered for {event_name}!")
            st.balloons()

            # QR Code
            qr_data = f"{participant_id} | {name} | {event_name}"
            qr = qrcode.make(qr_data)
            buf = io.BytesIO()
            qr.save(buf, format="PNG")
            st.image(buf.getvalue(), caption="🎟️ Your Event QR Ticket", width=200)

elif page == "📋 Attendees":
    st.subheader("📋 All Attendees")
    if len(st.session_state.participants) == 0:
        st.info("No participants yet.")
    else:
        df = pd.DataFrame(st.session_state.participants)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode()
        st.download_button("⬇️ Download CSV", data=csv, file_name="participants.csv", mime="text/csv")

elif page == "📅 Agenda":
    st.subheader("📅 Event Agenda")
    st.markdown("""
    | Time | Topic | Speaker |
    |------|-------|---------|
    | 10:00 AM | Opening Keynote | Dr. Kumar |
    | 11:00 AM | AI in Education | Prof. Reddy |
    | 12:30 PM | Networking Lunch | - |
    | 02:00 PM | Startup Panel | Alumni Entrepreneurs |
    """)

elif page == "🎤 Speakers & Sponsors":
    st.subheader("🎤 Speakers")
    st.markdown("- **Anitha** – AI Visionary")
    st.markdown("- **P.Sambaiah** – ML Expert ")
    st.markdown("- **Alumni Entrepreneurs** – Real-world insights")

    st.subheader("💼 Sponsors")
    st.markdown("🧠 Vignan AI Lab  |  💻 TechVibe Solutions  |  🚀 Startup Valley")

elif page == "📊 Analytics":
    st.subheader("📊 Real-Time Event Analytics")
    if len(st.session_state.participants) == 0:
        st.info("No data yet.")
    else:
        df = pd.DataFrame(st.session_state.participants)
        st.markdown("#### 🔢 Registrations per Event")
        st.bar_chart(df['Event'].value_counts())

        st.markdown("#### 📆 Registration Timeline")
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        timeline = df.groupby(df['Timestamp'].dt.date).size()
        st.line_chart(timeline)

elif page == "✅ QR Check-in":
    st.subheader("✅ QR Code Check-in System")
    st.info("📷 Scan QR Code at entry for validation. (Simulation only)")
    st.image("https://img.freepik.com/free-vector/qr-code-smartphone-screen-scanning-app_107791-4267.jpg", width=300)

elif page == "📝 Feedback":
    st.subheader("📝 Share Your Experience")

    with st.form("feedback_form"):
        name = st.text_input("🙋 Your Name")
        rating = st.slider("⭐ Rating", 1, 5)
        comments = st.text_area("💬 Comments")
        if st.form_submit_button("📩 Submit Feedback"):
            st.session_state.feedback.append({
                "Name": name,
                "Rating": rating,
                "Comments": comments,
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            st.success("✅ Thank you for your feedback!")

    if st.session_state.feedback:
        st.markdown("### 🔍 Recent Feedback")
        st.table(pd.DataFrame(st.session_state.feedback))

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align:center; font-size:14px;'>NextGen Events | <b>Vignan University</b> | © 2025</p>", unsafe_allow_html=True)
