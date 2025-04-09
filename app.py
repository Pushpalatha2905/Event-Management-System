import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
import base64
from datetime import datetime

# Initialize session state
if 'attendees' not in st.session_state:
    st.session_state.attendees = []

st.set_page_config(page_title="Event Management System", layout="wide")
st.title("🎉 AI-Powered Event Management System")

# Sidebar Navigation
menu = st.sidebar.radio("Menu", ["Event Registration", "Attendee List", "Generate QR Code", "Feedback & Analytics"])

# Utility: QR Code Generator
def generate_qr_code(data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return img_b64

# 1. Event Registration Page
if menu == "Event Registration":
    st.subheader("📋 Register for the Event")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    ticket_type = st.selectbox("Ticket Type", ["Free", "VIP", "Student"])

    if st.button("Register"):
        attendee = {
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Ticket Type": ticket_type,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.attendees.append(attendee)
        st.success("Registration successful! QR code will be available in the 'Generate QR Code' section.")

# 2. Attendee List Page
elif menu == "Attendee List":
    st.subheader("📋 Registered Attendees")
    df = pd.DataFrame(st.session_state.attendees)
    if not df.empty:
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, "attendees.csv", "text/csv")
    else:
        st.info("No attendees registered yet.")

# 3. QR Code Generation
elif menu == "Generate QR Code":
    st.subheader("🎫 Generate Ticket QR Code")
    email_input = st.text_input("Enter your registered email")
    attendee_df = pd.DataFrame(st.session_state.attendees)
    
    if st.button("Generate QR"):
        matched = attendee_df[attendee_df['Email'] == email_input]
        if not matched.empty:
            data = matched.to_json()
            qr_img = generate_qr_code(data)
            st.markdown(f'<img src="data:image/png;base64,{qr_img}" width="200"/>', unsafe_allow_html=True)
            st.success("QR Code Generated!")
        else:
            st.warning("No registration found with this email.")

# 4. Feedback & Analytics
elif menu == "Feedback & Analytics":
    st.subheader("📊 Event Feedback & Insights")
    with st.form("Feedback Form"):
        feedback_name = st.text_input("Your Name")
        rating = st.slider("Rate the Event", 1, 5)
        comments = st.text_area("Additional Comments")
        submitted = st.form_submit_button("Submit Feedback")
        if submitted:
            st.success("Thanks for your feedback!")

    
    # Analytics Demo (from session data)
    df = pd.DataFrame(st.session_state.attendees)
    if not df.empty:
        st.markdown("### Ticket Type Distribution")
        st.bar_chart(df['Ticket Type'].value_counts())
