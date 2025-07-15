import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime
import pytz
from database import init_database, get_course_data, save_chat, get_or_create_user_session

# Must be the first Streamlit command
st.set_page_config(
    page_title="University Probe Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database and get user session
init_database()
user_id = get_or_create_user_session()

# Configure Gemini AI
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Get course data from database
data = {"courses": get_course_data()}

# Create a context for the AI
context = f"""
You are a helpful university admission counselor chatbot. You have information about the following courses:

{json.dumps(data, indent=2)}

Key points to remember:
1. Always be polite and professional
2. Provide accurate information about courses based on the data provided
3. Handle general queries and greetings naturally
4. If asked about information not in the data, politely say you can only provide information about the listed courses
5. Keep responses concise but informative
6. Use appropriate emojis to make responses engaging
7. Format responses using markdown for better readability

Example interactions:
- Greet users warmly
- Answer questions about course duration, fees, and subjects
- Provide guidance on admission process
- Handle small talk naturally
- Stay focused on academic and admission related queries
"""

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = ""
if 'chat' not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

def get_ai_response(user_input):
    try:
        prompt = f"Context: {context}

User: {user_input}

Response:"
        response = st.session_state.chat.send_message(prompt)
        save_chat(user_input, response.text)
        return response.text
    except Exception as e:
        st.error("An error occurred while getting a response from the AI. Please try again.")
        return f"I apologize, but I encountered an error: {str(e)}"

# Example questions
example_questions = [
    "Hi! Can you help me with course information?",
    "What courses do you offer?",
    "Tell me about B.Tech program",
    "What is the fee structure for BPharma?",
    "What subjects are taught in B.Sc first semester?",
    "How long is the B.Tech program?",
    "What are the subjects in BPharma?",
    "Tell me about admission process",
    "What is the duration of B.Sc?",
    "Can you compare B.Tech and BCA programs?"
]

def set_question(question):
    st.session_state.current_question = question

# Custom CSS with Material Icons and sidebar styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    html, body, [class^="st"], .main, .sidebar-section, .sidebar-header, .sidebar-link, .chat-message, .user-message, .bot-message, .timestamp, .example-question, .stButton>button, .stTextInput>div>div>input {
        font-family: 'Lexend', sans-serif !important;
    }
    html, body, .main {
        background: linear-gradient(135deg, #800020 0%, #fff 100%) !important;
        min-height: 100vh;
    }
    .main {
        padding: 2rem;
        border-top: 3px solid #800020;
        border-bottom: 3px solid #800020;
    }
    .stButton>button {
        background-color: #800020;
        color: white;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        border: none;
        height: 42px;
        margin-top: 6%;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: rgb(255, 230, 236);
    }
    .bot-message {
        background-color:rgb(239, 140, 140);
    }
    .timestamp {
        color: gray;
        font-size: 0.8em;
        margin-top: 8px;
    }
    .example-question {
        background-color: #f8f9fa;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .example-question:hover {
        background-color:rgb(99, 0, 43);
        transform: translateX(5px);
    }
    .sidebar-section {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .sidebar-header {
        color: #333;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f0f0f0;
    }
    .sidebar-link {
        display: block;
        padding: 0.5rem;
        color: #666;
        text-decoration: none;
        border-radius: 5px;
        transition: all 0.3s;
    }
    .sidebar-link:hover {
        background-color: #f8f9fa;
        color: #0066cc;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("./Resources/logo_SOU_Logo.png", use_container_width=True, caption="Silver Oak University")

    # Toggle button
    st.markdown("""
        <div id="sidebar-toggle" style="text-align:right; margin-bottom:10px;">
            <span class="material-icons" id="toggle-icon" style="cursor:pointer; font-size:24px;">
                keyboard_double_arrow_right
            </span>
        </div>
        <script>
        const waitForElement = (selector, callback) => {
            const el = window.parent.document.querySelector(selector);
            if (el) return callback(el);
            setTimeout(() => waitForElement(selector, callback), 100);
        };

        waitForElement('section[data-testid="stSidebar"]', (sidebar) => {
            const toggleIcon = window.parent.document.getElementById('toggle-icon');
            let isOpen = true;
            toggleIcon.onclick = () => {
                if (isOpen) {
                    sidebar.style.width = '0';
                    sidebar.style.overflow = 'hidden';
                    sidebar.style.transition = 'width 0.3s ease';
                    toggleIcon.textContent = '>>';
                    isOpen = false;
                } else {
                    sidebar.style.width = 'inherit';
                    sidebar.style.overflow = 'auto';
                    toggleIcon.textContent = '<<';
                    isOpen = true;
                }
            };
        });
        </script>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="sidebar-section">
        <div class="sidebar-header">👋 Welcome!</div>
        <p>I'm here to help you explore our academic programs and answer your questions about admissions.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="sidebar-section"><div class="sidebar-header">💭 Example Questions</div>""", unsafe_allow_html=True)

    for question in example_questions:
        if st.button(f"🔹 {question}", key=f"btn_{question}", 
                    help="Click to ask this question",
                    use_container_width=True):
            set_question(question)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""<div class="sidebar-section">
        <div class="sidebar-header">🔗 Quick Links</div>
        <a href="https://silveroakuni.ac.in/#" class="sidebar-link">📚 University Website</a>
        <a href="https://silveroakuni.ac.in/admission" class="sidebar-link">🎓 Admission Portal</a>
        <a href="https://studentportal.silveroakuni.ac.in/UMSStudents/login.aspx" class="sidebar-link">👤 Student Dashboard</a>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="sidebar-section">
        <div class="sidebar-header">📞 Contact Support</div>
        <p>📞 Helpline: 079-35201300</p>
        <p>📧 Email: info@silveroakuni.ac.in</p>
    </div>""", unsafe_allow_html=True)

# Main chat interface
st.markdown("<h1 style='color:#800020;'>🤖 University Probe Assistant</h1>", unsafe_allow_html=True)
st.markdown("--------------------------------")

# Chat container
chat_container = st.container()

# Display chat history
for message_data in st.session_state.chat_history:
    with chat_container:
        col1, col2 = st.columns([6,4])
        if len(message_data) == 3:
            user, bot, timestamp = message_data
        else:
            user, bot = message_data
            timestamp = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M')

        with col1:
            st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {user}
                </div>
            """, unsafe_allow_html=True)
            st.caption(timestamp)
        with col2:
            st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>Assistant:</strong>
                    {bot}</div>
            """, unsafe_allow_html=True)
            st.caption(timestamp)

# Input container
st.markdown("---")
input_col1, input_col2 = st.columns([6, 1])
with input_col1:
    user_input = st.text_input("Ask your question here...", 
                              value=st.session_state.current_question,
                              key="input", 
                              placeholder="e.g., What courses do you offer?")
with input_col2:
    st.text(" ")
    send_button = st.button("Send", use_container_width=True)

if send_button and user_input:
    ai_response = get_ai_response(user_input)
    current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M')
    st.session_state.chat_history.append((user_input, ai_response, current_time))
    st.session_state.current_question = ""
    st.rerun()

# Footer
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 1rem;'>
        © 2025 Aaryan Vegda. All rights reserved.
    </div>
    """, 
    unsafe_allow_html=True
)
