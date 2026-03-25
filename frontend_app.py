"""
Frontend Application for Audio Transcription and Note-Taking System
Streamlit implementation with intuitive UI
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
from io import BytesIO
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="Audio Notes - Transcription & Summarization",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        border-radius: 5px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        color: #721c24;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        color: #0c5460;
        margin: 1rem 0;
    }
    .transcript-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    .summary-box {
        background-color: #fff3cd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
for key, default in {
    "access_token": None,
    "user_info": None,
    "file_id": None,
    "transcript_id": None,
    "summary_id": None,
    "note_id": None,
    "transcript_data": None,
    "summary_data": None,
    "processing_stage": "upload",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def _auth_headers():
    """Return Authorization header dict if the user is logged in."""
    token = st.session_state.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

# Helper functions
def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

def signup_user(name, email, password):
    """Register a new user via the backend."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/signup",
            json={"name": name, "email": email, "password": password},
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def login_user(email, password):
    """Authenticate a user via the backend."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"email": email, "password": password},
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def logout_user():
    """Log out the current user via the backend."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/logout",
            headers=_auth_headers(),
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def upload_audio_file(file):
    """Upload audio file to backend"""
    try:
        files = {'file': (file.name, file, file.type)}
        response = requests.post(f"{API_BASE_URL}/upload-audio", files=files, headers=_auth_headers())
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def transcribe_audio(file_id):
    """Request transcription of uploaded audio"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/transcribe",
            json={"audio_file_id": file_id},
            headers=_auth_headers(),
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def summarize_transcript(transcript_id):
    """Request summarization of transcript"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/summarize",
            json={"transcript_id": transcript_id},
            headers=_auth_headers(),
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def save_notes(transcript_id, summary_id, user_notes=""):
    """Save final notes"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/save-notes",
            json={
                "transcript_id": transcript_id,
                "summary_id": summary_id,
                "user_notes": user_notes
            },
            headers=_auth_headers(),
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_saved_notes(note_id):
    """Retrieve saved notes"""
    try:
        response = requests.get(f"{API_BASE_URL}/notes/{note_id}", headers=_auth_headers())
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def list_all_notes():
    """List all saved notes"""
    try:
        response = requests.get(f"{API_BASE_URL}/notes", headers=_auth_headers())
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def export_to_text(transcript_text, summary_text, key_points):
    """Export notes as plain text"""
    text_content = f"""AUDIO TRANSCRIPTION NOTES
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 60}

FULL TRANSCRIPT
{'-' * 60}
{transcript_text}

SUMMARY
{'-' * 60}
{summary_text}

KEY POINTS
{'-' * 60}
"""
    for i, point in enumerate(key_points, 1):
        text_content += f"{i}. {point}\n"
    
    return text_content

# Header
st.title("🎙️ Audio Notes - Transcription & Summarization")
st.markdown("Transform your audio recordings into organized, searchable notes")

# ──────────────────────────────────────
# Auth gate: show login/signup when not authenticated
# ──────────────────────────────────────
if st.session_state.access_token is None:
    auth_tab_login, auth_tab_signup = st.tabs(["Login", "Sign Up"])

    with auth_tab_login:
        st.subheader("Login to your account")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_btn"):
            if not login_email or not login_password:
                st.error("Please enter both email and password.")
            else:
                with st.spinner("Logging in..."):
                    result = login_user(login_email, login_password)
                if result.get("success"):
                    st.session_state.access_token = result["data"]["access_token"]
                    st.session_state.user_info = {
                        "user_id": result["data"]["user_id"],
                        "email": result["data"]["email"],
                        "name": result["data"].get("name", ""),
                    }
                    st.rerun()
                else:
                    st.error(f"Login failed: {result.get('error', 'Unknown error')}")

    with auth_tab_signup:
        st.subheader("Create a new account")
        signup_name = st.text_input("Name", key="signup_name")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up", key="signup_btn"):
            if not signup_name or not signup_email or not signup_password:
                st.error("Please fill in all fields.")
            else:
                with st.spinner("Creating account..."):
                    result = signup_user(signup_name, signup_email, signup_password)
                if result.get("success"):
                    token = result["data"].get("access_token")
                    if token:
                        st.session_state.access_token = token
                        st.session_state.user_info = {
                            "user_id": result["data"]["user_id"],
                            "email": result["data"]["email"],
                            "name": result["data"].get("name", ""),
                        }
                        st.rerun()
                    else:
                        st.success("Account created! Please check your email to confirm, then log in.")
                else:
                    st.error(f"Sign-up failed: {result.get('error', 'Unknown error')}")

    st.stop()

# ──────────────────────────────────────
# Authenticated UI below
# ──────────────────────────────────────

# Sidebar
with st.sidebar:
    st.header("📋 Navigation")

    user_name = st.session_state.user_info.get("name") or st.session_state.user_info.get("email", "")
    st.markdown(f"**Logged in as:** {user_name}")
    if st.button("Logout", key="logout_btn"):
        logout_user()
        st.session_state.access_token = None
        st.session_state.user_info = None
        st.rerun()

    page = st.radio(
        "Select Page",
        ["Upload & Process", "View Saved Notes", "API Documentation"],
        index=0
    )
    
    st.markdown("---")
    
    # API Status
    st.subheader("🔌 API Status")
    if check_api_health():
        st.success("✅ Connected")
    else:
        st.error("❌ Disconnected")
        st.warning("Please ensure the backend API is running on port 8000")
    
    st.markdown("---")
    
    # Processing Progress
    st.subheader("📊 Processing Progress")
    progress_stages = {
        "upload": 1,
        "transcribe": 2,
        "summarize": 3,
        "save": 4,
        "complete": 5
    }
    current_stage = progress_stages.get(st.session_state.processing_stage, 1)
    st.progress(current_stage / 5)
    
    stage_labels = ["Upload", "Transcribe", "Summarize", "Save", "Complete"]
    for i, label in enumerate(stage_labels, 1):
        if i < current_stage:
            st.text(f"✅ {label}")
        elif i == current_stage:
            st.text(f"⏳ {label}")
        else:
            st.text(f"⬜ {label}")

# Main content area
if page == "Upload & Process":
    st.header("📤 Upload & Process Audio")
    
    # Check API connection
    if not check_api_health():
        st.error("⚠️ Cannot connect to backend API. Please start the API server first.")
        st.code("python backend_api.py", language="bash")
        st.stop()
    
    # File upload section
    st.subheader("1️⃣ Upload Audio File")
    st.markdown("Supported formats: MP3, WAV, M4A, OGG, FLAC")
    
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=['mp3', 'wav', 'm4a', 'ogg', 'flac'],
        help="Upload your class recording or lecture audio"
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info(f"📁 **File:** {uploaded_file.name}")
            st.info(f"📊 **Size:** {uploaded_file.size / 1024:.2f} KB")
        
        with col2:
            if st.button("🚀 Upload File", key="upload_btn"):
                with st.spinner("Uploading file..."):
                    result = upload_audio_file(uploaded_file)
                    
                    if result.get("success"):
                        st.session_state.file_id = result["data"]["file_id"]
                        st.session_state.processing_stage = "transcribe"
                        st.success("✅ File uploaded successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Upload failed: {result.get('error', 'Unknown error')}")
    
    # Transcription section
    if st.session_state.file_id:
        st.markdown("---")
        st.subheader("2️⃣ Transcribe Audio")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info(f"📝 File ID: `{st.session_state.file_id}`")
        
        with col2:
            if st.button("🎯 Start Transcription", key="transcribe_btn"):
                with st.spinner("Transcribing audio... This may take a moment."):
                    result = transcribe_audio(st.session_state.file_id)
                    
                    if result.get("success"):
                        st.session_state.transcript_id = result["data"]["transcript_id"]
                        st.session_state.transcript_data = result["data"]
                        st.session_state.processing_stage = "summarize"
                        st.success("✅ Transcription complete!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ Transcription failed: {result.get('error', 'Unknown error')}")
    
    # Display transcript
    if st.session_state.transcript_data:
        st.markdown("---")
        st.subheader("📄 Transcript")
        
        transcript_text = st.session_state.transcript_data.get("transcript_text", "")
        confidence = st.session_state.transcript_data.get("confidence", 0)
        duration = st.session_state.transcript_data.get("duration_seconds", 0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Duration", f"{duration}s")
        with col2:
            st.metric("Confidence", f"{confidence*100:.1f}%")
        with col3:
            st.metric("Words", len(transcript_text.split()))
        
        st.markdown(f'<div class="transcript-box">{transcript_text}</div>', unsafe_allow_html=True)
        
        # Search functionality
        search_term = st.text_input("🔍 Search in transcript", key="search_transcript")
        if search_term:
            if search_term.lower() in transcript_text.lower():
                st.success(f"Found '{search_term}' in transcript")
                # Highlight search term (basic implementation)
                highlighted = transcript_text.replace(
                    search_term,
                    f"**{search_term}**"
                )
                st.markdown(highlighted)
            else:
                st.warning(f"'{search_term}' not found in transcript")
    
    # Summarization section
    if st.session_state.transcript_id:
        st.markdown("---")
        st.subheader("3️⃣ Generate Summary")
        
        if st.button("📝 Summarize Transcript", key="summarize_btn"):
            with st.spinner("Generating summary..."):
                result = summarize_transcript(st.session_state.transcript_id)
                
                if result.get("success"):
                    st.session_state.summary_id = result["data"]["summary_id"]
                    st.session_state.summary_data = result["data"]
                    st.session_state.processing_stage = "save"
                    st.success("✅ Summary generated!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Summarization failed: {result.get('error', 'Unknown error')}")
    
    # Display summary
    if st.session_state.summary_data:
        st.markdown("---")
        st.subheader("📋 Summary & Key Points")
        
        summary_text = st.session_state.summary_data.get("summary_text", "")
        key_points = st.session_state.summary_data.get("key_points", [])
        entities = st.session_state.summary_data.get("entities", [])
        
        st.markdown(f'<div class="summary-box"><strong>Summary:</strong><br>{summary_text}</div>', unsafe_allow_html=True)
        
        if key_points:
            st.markdown("**🔑 Key Points:**")
            for i, point in enumerate(key_points, 1):
                st.markdown(f"{i}. {point}")
        
        if entities:
            st.markdown("**🏷️ Entities Detected:**")
            st.write(", ".join(entities))
    
    # Save notes section
    if st.session_state.summary_id:
        st.markdown("---")
        st.subheader("4️⃣ Save & Export Notes")
        
        user_notes = st.text_area(
            "📝 Add your own notes (optional)",
            height=100,
            placeholder="Add any personal observations or additional notes here..."
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save Notes", key="save_btn"):
                with st.spinner("Saving notes..."):
                    result = save_notes(
                        st.session_state.transcript_id,
                        st.session_state.summary_id,
                        user_notes
                    )
                    
                    if result.get("success"):
                        st.session_state.note_id = result["data"]["note_id"]
                        st.session_state.processing_stage = "complete"
                        st.success(f"✅ Notes saved! ID: {st.session_state.note_id}")
                        st.balloons()
                    else:
                        st.error(f"❌ Save failed: {result.get('error', 'Unknown error')}")
        
        with col2:
            if st.session_state.transcript_data and st.session_state.summary_data:
                # Export options
                export_text = export_to_text(
                    st.session_state.transcript_data.get("transcript_text", ""),
                    st.session_state.summary_data.get("summary_text", ""),
                    st.session_state.summary_data.get("key_points", [])
                )
                
                st.download_button(
                    label="📥 Download as TXT",
                    data=export_text,
                    file_name=f"notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )

elif page == "View Saved Notes":
    st.header("📚 Saved Notes Library")
    
    # Check API connection
    if not check_api_health():
        st.error("⚠️ Cannot connect to backend API.")
        st.stop()
    
    # Load all notes
    if st.button("🔄 Refresh Notes List"):
        st.rerun()
    
    result = list_all_notes()
    
    if result.get("success"):
        notes_list = result["data"]["notes"]
        
        if notes_list:
            st.success(f"Found {len(notes_list)} saved note(s)")
            
            for note in notes_list:
                with st.expander(f"📄 Note ID: {note['note_id'][:8]}... (Created: {note['created_at'][:19]})"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        if st.button(f"View Details", key=f"view_{note['note_id']}"):
                            note_result = get_saved_notes(note['note_id'])
                            
                            if note_result.get("success"):
                                note_data = note_result["data"]
                                
                                st.markdown("### 📝 Full Transcript")
                                st.text_area(
                                    "Transcript",
                                    note_data["transcript"].get("transcript_text", ""),
                                    height=200,
                                    key=f"trans_{note['note_id']}"
                                )
                                
                                st.markdown("### 📋 Summary")
                                st.info(note_data["summary"].get("summary_text", ""))
                                
                                st.markdown("### 🔑 Key Points")
                                for i, point in enumerate(note_data["summary"].get("key_points", []), 1):
                                    st.markdown(f"{i}. {point}")
                                
                                if note_data.get("user_notes"):
                                    st.markdown("### 💭 User Notes")
                                    st.text_area(
                                        "Your Notes",
                                        note_data["user_notes"],
                                        height=100,
                                        key=f"user_{note['note_id']}"
                                    )
                    
                    with col2:
                        st.metric("Has User Notes", "Yes" if note['has_user_notes'] else "No")
        else:
            st.info("No saved notes yet. Upload and process an audio file to get started!")
    else:
        st.error("Failed to load notes")

elif page == "API Documentation":
    st.header("📖 API Documentation")
    
    st.markdown("""
    ### Backend API Endpoints
    
    Base URL: `http://localhost:8000`
    
    #### 1. Upload Audio
    **Endpoint:** `POST /upload-audio`
    
    **Description:** Upload an audio file for processing
    
    **Request:** Multipart form data with audio file
    
    **Response:**
    ```json
    {
        "success": true,
        "message": "Audio file uploaded successfully",
        "data": {
            "file_id": "uuid",
            "filename": "recording.mp3",
            "file_size_bytes": 1024000,
            "format": ".mp3",
            "upload_timestamp": "2024-01-01T12:00:00"
        }
    }
    ```
    
    #### 2. Transcribe Audio
    **Endpoint:** `POST /transcribe`
    
    **Description:** Send audio to ASR module for transcription
    
    **Request Body:**
    ```json
    {
        "audio_file_id": "uuid",
        "language": "en"
    }
    ```
    
    **Response:**
    ```json
    {
        "success": true,
        "message": "Audio transcribed successfully",
        "data": {
            "transcript_id": "uuid",
            "transcript_text": "...",
            "duration_seconds": 120,
            "confidence": 0.95
        }
    }
    ```
    
    #### 3. Summarize Transcript
    **Endpoint:** `POST /summarize`
    
    **Description:** Send transcript to NLP module for summarization
    
    **Request Body:**
    ```json
    {
        "transcript_id": "uuid",
        "summary_type": "standard"
    }
    ```
    
    **Response:**
    ```json
    {
        "success": true,
        "message": "Transcript summarized successfully",
        "data": {
            "summary_id": "uuid",
            "summary_text": "...",
            "key_points": ["...", "..."],
            "entities": ["..."]
        }
    }
    ```
    
    #### 4. Save Notes
    **Endpoint:** `POST /save-notes`
    
    **Description:** Store final processed output and notes
    
    **Request Body:**
    ```json
    {
        "transcript_id": "uuid",
        "summary_id": "uuid",
        "user_notes": "Optional notes"
    }
    ```
    
    **Response:**
    ```json
    {
        "success": true,
        "message": "Notes saved successfully",
        "data": {
            "note_id": "uuid",
            "created_at": "2024-01-01T12:00:00"
        }
    }
    ```
    
    #### 5. Retrieve Notes
    **Endpoint:** `GET /notes/{note_id}`
    
    **Description:** Get saved notes by ID
    
    **Response:**
    ```json
    {
        "success": true,
        "data": {
            "note_id": "uuid",
            "transcript": {...},
            "summary": {...},
            "user_notes": "..."
        }
    }
    ```
    
    #### 6. List All Notes
    **Endpoint:** `GET /notes`
    
    **Description:** List all saved notes
    
    **Response:**
    ```json
    {
        "success": true,
        "data": {
            "count": 5,
            "notes": [...]
        }
    }
    ```
    """)
    
    st.markdown("---")
    
    st.subheader("🚀 Getting Started")
    
    st.markdown("""
    ### Running the Backend API
    
    ```bash
    # Install dependencies
    pip install fastapi uvicorn aiofiles python-multipart
    
    # Run the API
    python backend_api.py
    ```
    
    ### Running the Frontend
    
    ```bash
    # Install Streamlit
    pip install streamlit requests
    
    # Run the frontend
    streamlit run frontend_app.py
    ```
    
    ### Testing with curl
    
    ```bash
    # Check API health
    curl http://localhost:8000/
    
    # Upload audio file
    curl -X POST http://localhost:8000/upload-audio \\
         -F "file=@recording.mp3"
    ```
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>🎙️ Audio Notes - Transcription & Summarization System</p>
        <p>Built with Streamlit & FastAPI</p>
    </div>
    """,
    unsafe_allow_html=True
)
