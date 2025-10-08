# Streamlit Cloud Deployment Guide

## Quick Deployment Steps

### 1. Create GitHub Repository
1. Go to [GitHub](https://github.com) and create a new repository
2. Name it: `e-health-chatbot` (or any name you prefer)
3. Make it **Public** (required for free Streamlit Cloud)
4. Initialize with README (optional)

### 2. Upload Files to GitHub
Upload these files to your repository:
- `app_strict.py` (main application)
- `requirements.txt` (dependencies)
- `README.md` (documentation)
- `assets/` folder (with diet.txt and exercise.txt)
- `.gitignore` (optional but recommended)

### 3. Deploy to Streamlit Cloud
1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Click "New app"
3. Connect your GitHub account
4. Select your repository: `your-username/e-health-chatbot`
5. Set **Main file path**: `app_strict.py`
6. Click "Deploy!"

### 4. Share the URL
Once deployed, you'll get a URL like:
`https://your-app-name.streamlit.app/`

Share this URL with your collaborators - no installation required!

## Troubleshooting

### Common Issues:
- **App won't start**: Check that `requirements.txt` includes `streamlit==1.37.1`
- **Assets not loading**: Ensure `assets/` folder is uploaded to GitHub
- **Import errors**: Verify all dependencies are in `requirements.txt`

### File Structure for GitHub:
```
e-health-chatbot/
├── app_strict.py
├── requirements.txt
├── README.md
├── .gitignore
└── assets/
    ├── diet.txt
    └── exercise.txt
```

## Benefits of Streamlit Cloud
- ✅ **Free hosting**
- ✅ **Automatic updates** (when you push to GitHub)
- ✅ **No server management**
- ✅ **Easy sharing** (just send the URL)
- ✅ **Mobile-friendly**
- ✅ **HTTPS enabled**
