# Text-to-Image Converter

This project is a Text-to-Video Converter with AI-powered video generation and Text-to-Speech functionality. It allows users to input text, which is then converted into speech and used to generate videos using free AI services.

## 🚀 Features

- **Text-to-Speech**: Convert text to natural-sounding speech
- **AI image Generation**: Generate images using free AI services (Hugging Face Spaces)
- **100% Free**: Uses only free AI APIs and services
- **Web Interface**: Modern React frontend with TypeScript


## 📁 Project Structure

```
text-to-image-converter/
├── backend/
│   ├── src/
│   │   ├── app.py                    # Main Flask application
│   │   ├── tts.py                    # Text-to-Speech functionality
│   │   ├── video_generator.py        # Standard video generation
│   │   └── free_ai_video_generator.py # AI video generation
│   ├── requirements.txt
│   └── .env                          # API tokens (not in git)
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── TextInput.tsx
│   │   │   ├── VideoDisplay.tsx
│   │   │   └── VideoTextInput.tsx
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── types/
│   │       └── index.ts
│   ├── package.json
│   └── tsconfig.json
├── .env.example                      # Template for environment variables
├── .gitignore
└── README.md
```

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ErkanErten91/Text-to-image-converter.git
cd Text-to-image-converter
```

### 2. Environment Variables Setup
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your API tokens:
   - **Replicate API Token**: Get from [https://replicate.com/account/api-tokens](https://replicate.com/account/api-tokens)
   - **Hugging Face Token**: Get from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
   - **Runway API Token** (optional): Get from [https://runwayml.com/](https://runwayml.com/)
   - **Stability API Key** (optional): Get from [https://platform.stability.ai/account/keys](https://platform.stability.ai/account/keys)
   - **OpenAI API Key** (optional): Get from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### 3. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install flask flask-cors gtts moviepy numpy requests werkzeug pillow python-dotenv replicate huggingface-hub gradio-client

# Fix MoviePy compatibility
pip uninstall moviepy
pip install moviepy==1.0.3

# Start the backend server
cd src
python app.py
```

### 4. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health

## 🔧 Troubleshooting

### Problem: Virtual Environment Missing After Git Clone

If you get `ModuleNotFoundError: No module named 'flask'`, follow these steps:

#### 1. Navigate to Backend Directory
```powershell
cd backend
```

#### 2. Create New Virtual Environment
```powershell
python -m venv .venv
```

#### 3. Activate Virtual Environment
```powershell
.venv\Scripts\activate
```
*(You should see `(.venv)` before your prompt)*

#### 4. Install Updated Packages
```powershell
pip install flask flask-cors gtts moviepy numpy requests werkzeug pillow python-dotenv replicate huggingface-hub gradio-client
```

#### 5. Fix MoviePy Compatibility
```powershell
pip uninstall moviepy
pip install moviepy==1.0.3
```

#### 6. Restore .env File
```powershell
copy ..\.env.example .env
```

#### 7. Edit .env File with Real Tokens
```powershell
notepad .env
```
*Replace placeholders with your real API tokens*

#### 8. Start the Program
```powershell
cd src
python app.py
```

#### For Linux/Mac Users:
- Step 3: `source .venv/bin/activate`
- Step 6: `cp ../.env.example .env`
- Step 7: `nano .env` or `vim .env`

**Important Note:** The `.venv` folders are intentionally not uploaded to Git because they are very large and must be recreated locally.

## 🎯 API Endpoints

### Main Endpoints
- `POST /api/generate-free-ai-video` - Generate FREE AI video
- `POST /api/generate-ai-video` - Generate AI video (with fallback)
- `POST /api/generate-video` - Generate standard video
- `POST /api/tts` - Text to speech conversion
- `GET /api/health` - Health check
- `GET /api/status` - System status

### Configuration Endpoints
- `GET /api/options` - Get available options
- `GET /api/video-templates` - Get video templates
- `POST /api/apply-template` - Apply video template
- `POST /api/batch-generate` - Batch generate videos

### Testing Endpoints
- `GET /api/test-free-services` - Test all free services
- `GET /api/free-ai-status` - Free AI services status

## 🤖 AI Services Used

### Free AI Video Generation
- **Hugging Face Spaces**: Zeroscope v2 XL, AnimateDiff Lightning, I2VGen-XL, LaVie, VideoCrafter
- **Public AI APIs**: Pollinations AI, Dezgo AI
- **Community Services**: DeepAI Text2Video, AI Video Generator, Free Video AI

### Text-to-Speech
- **Google Text-to-Speech (gTTS)**: Free and reliable TTS service

## 💰 Cost Information
- **100% FREE**: No billing required
- **No API Limits**: Uses only free tiers and public services
- **No Local GPU Required**: All processing happens via free cloud APIs

## 🔒 Security Notes
- Never commit `.env` files to Git
- API tokens are automatically detected and blocked by GitHub
- Use `.env.example` as a template for others

## 🚀 Deployment
The application can be deployed to:
- **Heroku**: Free tier available
- **Railway**: Easy deployment
- **Vercel**: Frontend deployment
- **PythonAnywhere**: Backend deployment

## 🤝 Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License
This project is licensed under the MIT License. See the LICENSE file for more details.

## 🆘 Support
If you encounter issues:
1. Check the troubleshooting section above
2. Ensure all API tokens are correctly set
3. Verify virtual environment is activated
4. Check that all dependencies are installed
5. Open an issue on GitHub with detailed error messages

## 🎉 Acknowledgments
- Hugging Face for free AI model hosting
- Google for Text-to-Speech services
- MoviePy for video processing
- Flask and React communities
