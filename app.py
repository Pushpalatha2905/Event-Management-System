import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
from PIL import Image
import qrcode
import io
import base64
import altair as alt

# --- Streamlit Page Config ---
st.set_page_config(page_title="NextGen Events | Vignan University 🎓", page_icon="🎉", layout="wide")

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f9f9f9;
        }
        .main-title {
            color: #4CAF50;
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            margin-top: -20px;
        }
        .sub-title {
            text-align: center;
            font-size: 18px;
            color: #555;
        }
        .footer {
            text-align:center; 
            font-size:14px; 
            color: gray;
            padding-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Header ---
st.markdown("<h1 class='main-title'>🎉 Smart Event Management System</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>NextGen Events | Vignan University</p>", unsafe_allow_html=True)
st.divider()

# --- Session Initialization ---
if 'participants' not in st.session_state:
    st.session_state.participants = []

# --- Sidebar Navigation ---
page = st.sidebar.radio("📌 Navigate", ["🏷️ Register", "📋 Participants List", "📊 Analytics Dashboard"])

# --- Registration Page ---
if page == "🏷️ Register":
    st.subheader("📥 Register for an Event")

    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Full Name")
            email = st.text_input("📧 Email Address")
            phone = st.text_input("📱 Phone Number")
        with col2:
            event_name = st.selectbox("🎯 Choose an Event", ["AI Conference 2025", "Startup Pitch Fest", "Tech Expo", "Crypto Workshop"])
            num_tickets = st.number_input("🎫 Tickets", min_value=1, max_value=5, value=1)
            event_date = st.date_input("📅 Event Date", min_value=datetime.today())
        submitted = st.form_submit_button("✅ Submit Registration")

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

            st.success(f"✅ {name}, you've been registered for {event_name}!")
            st.balloons()

            # QR Code Generation
            qr_data = f"{participant_id} - {name} - {event_name}"
            qr = qrcode.make(qr_data)
            buf = io.BytesIO()
            qr.save(buf, format="PNG")
            st.image(buf.getvalue(), caption="🎟️ Your Event QR Ticket", width=200)

# --- Participants List Page ---
elif page == "📋 Participants List":
    st.subheader("📋 All Registered Participants")
    if len(st.session_state.participants) == 0:
        st.info("No registrations yet.")
    else:
        df = pd.DataFrame(st.session_state.participants)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode()
        st.download_button("⬇️ Download as CSV", data=csv, file_name="participants.csv", mime="text/csv")

# --- Analytics Dashboard ---
elif page == "📊 Analytics Dashboard":
    st.subheader("📊 Event Insights & Analytics")

    if len(st.session_state.participants) == 0:
        st.warning("No data yet for analytics.")
    else:
        df = pd.DataFrame(st.session_state.participants)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        st.markdown("#### 🔢 Event-wise Registrations")
        chart1 = alt.Chart(df).mark_bar(color="#4CAF50").encode(
            x='Event:N',
            y='count()',
            tooltip=['Event', 'count()']
        ).properties(width=600, height=300)
        st.altair_chart(chart1, use_container_width=True)

        st.markdown("#### ⏳ Registrations Over Time")
        timeline = df.groupby(df['Timestamp'].dt.date).size().reset_index(name='Registrations')
        line_chart = alt.Chart(timeline).mark_line(color="#2196F3", point=True).encode(
            x='Timestamp:T',
            y='Registrations:Q'
        ).properties(width=600, height=300)
        st.altair_chart(line_chart, use_container_width=True)

        st.markdown("#### 🎯 Pie Chart - Event Split")
        pie_df = df['Event'].value_counts().reset_index()
        pie_df.columns = ['Event', 'Count']
        pie_chart = alt.Chart(pie_df).mark_arc(innerRadius=50).encode(
            theta="Count:Q",
            color="Event:N",
            tooltip=['Event', 'Count']
        ).properties(width=400, height=400)
        st.altair_chart(pie_chart, use_container_width=True)

# --- Footer ---
st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown("<p class='footer'>NextGen Events | <b>Vignan University</b> | © 2025</p>", unsafe_allow_html=True)
