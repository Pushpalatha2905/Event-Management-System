import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.colored_header import colored_header
from PIL import Image
import qrcode
import io
import base64

# Initialize data stores
if 'events' not in st.session_state:
    st.session_state.events = []

if 'registrations' not in st.session_state:
    st.session_state.registrations = {}

# Page config
st.set_page_config(page_title="EventSync | Event Management System", layout="wide", page_icon="🎉")

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🎉 Welcome to EventPro+ 🎉</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Plan, Register, and Attend Events Seamlessly!</p>", unsafe_allow_html=True)
add_vertical_space(1)

# Theme toggle
theme = st.sidebar.radio("Choose Theme", ["🌞 Light Mode", "🌙 Dark Mode"])
if theme == "🌙 Dark Mode":
    st.markdown("""<style>body { background-color: #1e1e1e; color: white; }</style>""", unsafe_allow_html=True)

# ---------------- EVENT CREATION ----------------
with st.expander("📝 Create New Event", expanded=False):
    with st.form("event_form"):
        name = st.text_input("Event Name")
        description = st.text_area("Event Description", height=100)
        location = st.text_input("Location")
        date = st.date_input("Date")
        time = st.time_input("Time")
        host = st.text_input("Hosted By")
        submit = st.form_submit_button("➕ Add Event")

        if submit:
            if name and location:
                new_event = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "description": description,
                    "location": location,
                    "date": str(date),
                    "time": str(time),
                    "host": host
                }
                st.session_state.events.append(new_event)
                st.success("✅ Event Created Successfully!")
            else:
                st.warning("❗ Please fill in all required fields.")

# ---------------- EVENT DISPLAY ----------------
colored_header("📅 Upcoming Events", description="Discover events & register now!", color_name="green-70")

for event in st.session_state.events:
    with st.container(border=True):
        st.subheader(event["name"])
        st.caption(f"📍 {event['location']} | 🗓️ {event['date']} at ⏰ {event['time']}")
        st.write(f"📝 {event['description']}")
        st.markdown(f"👤 Hosted by: **{event['host']}**")

        # Registration Button
        if st.button(f"🎟️ Register for {event['name']}", key=event["id"]):
            with st.form(f"register_{event['id']}"):
                name = st.text_input("Your Name")
                email = st.text_input("Email Address")
                register = st.form_submit_button("✅ Submit Registration")

                if register:
                    if name and email:
                        registration_id = str(uuid.uuid4())
                        if event["id"] not in st.session_state.registrations:
                            st.session_state.registrations[event["id"]] = []

                        st.session_state.registrations[event["id"]].append({
                            "name": name,
                            "email": email,
                            "registered_at": datetime.now().isoformat(),
                            "ticket_id": registration_id
                        })

                        # Generate QR code
                        qr = qrcode.make(f"{event['name']} | {name} | {registration_id}")
                        buf = io.BytesIO()
                        qr.save(buf)
                        buf.seek(0)
                        img_base64 = base64.b64encode(buf.read()).decode()

                        st.success("🎉 Registered Successfully!")
                        st.image(f"data:image/png;base64,{img_base64}", caption="🎫 Your QR Code Ticket")

                    else:
                        st.warning("Please enter your details.")

# ---------------- ANALYTICS ----------------
with st.expander("📊 View Registration Stats"):
    if st.session_state.registrations:
        for event in st.session_state.events:
            count = len(st.session_state.registrations.get(event["id"], []))
            st.markdown(f"**{event['name']}**: {count} Registrations")
    else:
        st.info("No registrations yet.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; font-size:14px;'>EventSync | <b>Vignan's Univeristy Events </b> | © 2025</p>",
    unsafe_allow_html=True
)
