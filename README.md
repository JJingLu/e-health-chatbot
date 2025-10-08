## E-Health Preventive Check-Up Chatbot (Streamlit)

### 🚀 Live Demo
**[Try the chatbot online](https://your-streamlit-app-url.streamlit.app/)** *(Deploy link will be added after GitHub setup)*

### Local Setup Instructions

1. Install dependencies (recommended to use virtual environment)
```bash
pip install -r requirements.txt
```

2. Launch the application
```bash
streamlit run app_strict.py
```

3. Open your browser and visit the local address provided in the console.

### 🌐 Streamlit Cloud Deployment

This application is designed to be deployed on Streamlit Cloud for easy sharing and collaboration.

**Deployment Steps:**
1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your GitHub account
4. Select this repository and set `app_strict.py` as the main file
5. Deploy and share the public URL

### Features Overview
- **First Visit**: Covers main questions and branches from the script; automatically generates doctor dialogue and receptionist prompts.
- **Second Visits**: Includes common entry and privacy controls (4 types of second visit scenarios available).
- **Session State**: Uses `st.session_state` to manage patient information and conversation progress.
- **Resource Downloads**: Sidebar provides downloadable "exercise/diet" pamphlet `txt` files.
- **Reset & Home**: Return to home page anytime to restart the full experience.

### Directory Structure
- `app_strict.py` - Main application (strictly follows the script)
- `assets/` - Pamphlet resources directory
- `requirements.txt` - Dependencies
- `README.md` - Documentation


