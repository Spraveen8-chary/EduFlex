import streamlit as st
import pandas as pd
from database.connect_database import get_name, fetch_user_data, update_user_data, get_id_by_email
from features.email_otp_generater import generate_otp, send_email

def update_user_form(user_data: dict):
    """Display update form and return updated data if submitted"""
    st.sidebar.markdown("### ✏️ Update Details")
    
    # Input fields
    first_name = st.sidebar.text_input("First Name", value=user_data.get("first_name", ""))
    last_name = st.sidebar.text_input("Last Name", value=user_data.get("last_name", ""))
    email = st.sidebar.text_input("Email", value=user_data.get("email", ""))

    # Button controls
    password_btn = st.sidebar.button("Change Password")
    update_btn = st.sidebar.button("Update Now")

    # Store OTP in session state
    if "otp" not in st.session_state:
        st.session_state.otp = None
        st.session_state.otp_sent_to = None

    if password_btn:
        st.session_state.otp = generate_otp()
        st.session_state.otp_sent_to = email
        send_email(email, st.session_state.otp)
        st.toast(f"📩 OTP is sent to {email}. Please check the inbox or spam folder.")

    updated_data = {}

    if st.session_state.otp:
        check_otp = st.sidebar.text_input("Enter OTP")

        if check_otp and str(check_otp) == str(st.session_state.otp):
            new_password = st.sidebar.text_input("Enter New Password", type="password")
            print("Password entered...")
            if update_btn or new_password:
                updated_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'password': new_password
                }
                print("Updated Data ... ")
                update_user_data(get_id_by_email(email), updated_data)
                st.sidebar.success("✅ Your details have been updated successfully!")
                st.session_state.otp = None  # Clear OTP after use
            elif update_btn:
                st.sidebar.error("Please enter a new password after OTP verification.")
        elif check_otp:
            st.sidebar.error("Invalid OTP. Please try again.")

    elif update_btn:
        # Update without password
        updated_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        update_user_data(get_id_by_email(email), updated_data)
        st.sidebar.success("✅ Your details have been updated successfully!")

    return updated_data


def delete_user_data():
    """Clear user data from session state"""
    delete_btn = st.sidebar.button("Delete User Data")
    if delete_btn:
        st.session_state.user_data.clear()
        st.sidebar.success("🗑️ User data deleted successfully!")


# Streamlit UI
def DASHBOARD(user = 'none'):
    st.markdown("""
        <style>
            .stSidebar > div:first-child {
                background-color: #f8f9fa;
                padding: 20px;
                border-right: 1px solid #ddd;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                border-radius: 8px;
                padding: 10px 20px;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
            .stTextInput>div>div>input {
                border-radius: 8px;
                border: 1px solid #ccc;
            }
            .card {
                background-color: white;
                padding: 15px;
                margin-top: 10px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                border-left: 5px solid #4CAF50;
            }
            .card h3 {
                margin-top: 0;
                color: #4CAF50;
            }
            .card p {
                margin: 5px 0;
                font-size: 15px;
            }
        </style>
        """, unsafe_allow_html=True)



    st.title("📊 EduFlex User Dashboard")

    st.subheader(f"Hi 👋 {' '.join([i.capitalize() for i in str(get_name(user)).split()])}")
    user_data = fetch_user_data(email=user)
    st.session_state.user_data = user_data
    st.sidebar.markdown(f"""
    <div  class="card">
        <h3>👤 Profile Info</h3>
        <p style="color:black;"><strong>🤵 Name:</strong> {str(user_data.get("first_name", "")).capitalize()} {str(user_data.get("last_name", "")).capitalize()}</p>
        <p style="color:black;"><strong>📧 Email:</strong> {user_data.get("email", "N/A")}</p>
        <p style="color:black;"><strong>🔒 Password:</strong> ***** </p>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Update","Search History", "Watched Videos", "Practiced Codes", "Certificates Earned"])
    
    if page == "Search History":
        st.header("🔍 Search History")
        data = fetch_user_data("search_history")
        df = pd.DataFrame(data, columns=["Query", "Timestamp"])
        st.dataframe(df)
    
    elif page == "Watched Videos":
        st.header("🎥 Watched Videos")
        data = fetch_user_data("watched_videos")
        df = pd.DataFrame(data, columns=["Title", "URL", "Watched On"])
        for index, row in df.iterrows():
            st.markdown(f"[{row['Title']}]({row['URL']}) - {row['Watched On']}")
    
    elif page == "Practiced Codes":
        st.header("💻 Practiced Codes")
        data = fetch_user_data("practiced_codes")
        for code_entry in data:
            with st.expander(f"{code_entry['language']} - {code_entry['timestamp']}"):
                st.code(code_entry['code'], language=code_entry['language'])
    
    elif page == "Update":
        updated_data = update_user_form(st.session_state.user_data)
        if updated_data:
            st.session_state.user_data = updated_data


    elif page == "Certificates Earned":
        st.header("🏆 Certificates Earned")
        data = fetch_user_data("certificates")
        df = pd.DataFrame(data, columns=["Certificate Name", "Issued On"])
        st.dataframe(df)
    return user


if __name__ == "__main__":
    DASHBOARD()
