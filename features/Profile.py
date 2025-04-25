import streamlit as st

# ----- Streamlit Page Config -----
st.set_page_config(page_title="Sidebar User Management", page_icon="💼", layout="centered")

# ----- Default Data -----
default_user = {
    'first_name': "Praveen",
    'last_name': "Chary",
    'email': "praveen@gmail.com",
    'password': "1234"
}

# ----- Initialize session state -----
if 'user_data' not in st.session_state or not st.session_state.user_data:
    st.session_state.user_data = default_user.copy()

# ----- Functions -----
def view_user(user_data: dict):
    """Render the user profile as a styled card in the sidebar"""
    st.sidebar.markdown(f"""
    <div class="card">
        <h3>👤 Profile Info</h3>
        <p style="color:black;"><strong>Full Name:</strong> {user_data.get("first_name", "")} {user_data.get("last_name", "")}</p>
        <p style="color:black;"><strong>📧 Email:</strong> {user_data.get("email", "N/A")}</p>
        <p style="color:black;"><strong>🔒 Password:</strong> {"*" * len(user_data.get("password", ""))}</p>
    </div>
    """, unsafe_allow_html=True)

def update_user_form(user_data: dict):
    """Display update form and return updated data if submitted"""
    st.sidebar.markdown("### ✏️ Update Details")
    first_name = st.sidebar.text_input("First Name", value=user_data.get("first_name", ""))
    last_name = st.sidebar.text_input("Last Name", value=user_data.get("last_name", ""))
    email = st.sidebar.text_input("Email", value=user_data.get("email", ""))
    password = st.sidebar.text_input("Password", type="password", value=user_data.get("password", ""))
    update_btn = st.sidebar.button("Update Now")

    if update_btn:
        if first_name and last_name and email and password:
            updated = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password
            }
            st.sidebar.success("✅ Details updated successfully!")
            return updated
        else:
            st.sidebar.error("❌ Please fill in all fields.")
    return None

def delete_user_data():
    """Clear user data from session state"""
    delete_btn = st.sidebar.button("Delete User Data")
    if delete_btn:
        st.session_state.user_data.clear()
        st.sidebar.success("🗑️ User data deleted successfully!")

# ----- Sidebar Header -----
st.sidebar.title("💼 User Management")
operation = st.sidebar.radio("Select Operation", ["View", "Update", "Delete"])

# ----- Operation Logic -----
if operation == "View":
    view_user(st.session_state.user_data)

elif operation == "Update":
    updated_data = update_user_form(st.session_state.user_data)
    if updated_data:
        st.session_state.user_data = updated_data

elif operation == "Delete":
    delete_user_data()


# ----- Custom CSS Styling -----
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
