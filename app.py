import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
from PIL import Image
import qrcode
import io
import base64

# Set page config with better theme
st.set_page_config(page_title="NextGen Events | Vignan University 🎟️" , layout="centered", page_icon="🎉")

# Initialize session state
if 'participants' not in st.session_state:
    st.session_state.participants = []

# Header UI
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎉 Smart Event Management System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Plan, register, and analyze your events with ease.</p>", unsafe_allow_html=True)
st.divider()

# Sidebar Navigation
page = st.sidebar.radio("🔎 Navigate", ["Register", "Participants List", "Analytics"])

# Event Registration Page
if page == "Register":
    st.subheader("📥 Register for an Event")

    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Name", max_chars=50)
            email = st.text_input("📧 Email")
            phone = st.text_input("📱 Phone Number")
        with col2:
            event_name = st.selectbox("🎯 Select Event", ["AI Conference 2025", "Startup Pitch Fest", "Tech Expo", "Crypto Workshop"])
            num_tickets = st.number_input("🎫 Number of Tickets", min_value=1, max_value=10, value=1)
            event_date = st.date_input("📅 Event Date", min_value=datetime.today())
        submitted = st.form_submit_button("✅ Register Now")

        if submitted:
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

            st.success(f"🎉 Registered successfully for {event_name}!")
            st.balloons()

            # Generate QR code for the ticket
            qr_data = f"{participant_id} - {name} - {event_name}"
            qr = qrcode.make(qr_data)
            buf = io.BytesIO()
            qr.save(buf, format="PNG")
            st.image(buf.getvalue(), caption="🎟️ Your Event QR Ticket", width=200)

# Participants Page
elif page == "Participants List":
    st.subheader("📋 Registered Participants")
    if len(st.session_state.participants) == 0:
        st.info("No participants registered yet.")
    else:
        df = pd.DataFrame(st.session_state.participants)
        st.dataframe(df, use_container_width=True)

        # Download CSV
        csv = df.to_csv(index=False).encode()
        st.download_button("📥 Download CSV", data=csv, file_name="participants.csv", mime="text/csv")

# Analytics Page
elif page == "Analytics":
    st.subheader("📊 Event Registration Insights")

    if len(st.session_state.participants) == 0:
        st.info("No data available for analytics.")
    else:
        df = pd.DataFrame(st.session_state.participants)

        st.markdown("#### 📈 Event-wise Registrations")
        event_counts = df['Event'].value_counts()
        st.bar_chart(event_counts)

        st.markdown("#### ⏱️ Registration Over Time")
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df_time = df.groupby(df['Timestamp'].dt.date).size()
        st.line_chart(df_time)

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; font-size:14px;'>EventSync | <b>Vignan's University Events</b> | © 2025</p>", unsafe_allow_html=True)
