AV Insight
AV Insight is a real-time sentiment analysis application that processes video files to extract and analyze audio and images, providing a comprehensive sentigraph visualization of detected emotions. The system leverages advanced machine learning techniques to perform sentiment analysis on both audio and visual data, combining the results to deliver insightful emotional analysis.

Table of Contents
Features
Tech Stack
Project Structure
Setup and Installation
Usage
API Endpoints
Testing
Contributing
License
Acknowledgements
Features
Real-time video processing and emotion detection
Sentiment analysis on both audio and visual data
Comprehensive sentigraph visualization
RESTful API with FastAPI
Dockerized for consistency and portability
Tech Stack
Backend: FastAPI, Python
Frontend: React
Machine Learning: PyTorch, facenet-pytorch, fer
Containerization: Docker, Docker Compose
Project Structure
markdown

AV_Insight/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── video_processor.py
│   │   ├── audio_analyzer.py
│   │   ├── image_analyzer.py
│   │   └── sentiment_combiner.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
│
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── manifest.json
│   ├── src/
│   │   ├── components/
│   │   │   ├── VideoUpload.js
│   │   │   ├── SentigraphDisplay.js
│   │   │   └── ResultsDisplay.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── README.md
│
├── static/
│   └── index.html  # This can be removed if using the React frontend
│
├── tests/
│   ├── __init__.py
│   ├── test_video_processor.py
│   ├── test_audio_analyzer.py
│   ├── test_image_analyzer.py
│   ├── test_sentiment_combiner.py
│   └── test_api.py
│
├── uploads/
├── results/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
Setup and Installation
Prerequisites
Docker
Docker Compose
Python 3.9+
Node.js (for frontend)
Backend Setup
Clone the repository:

sh
Copy code
git clone https://github.com/yourusername/av_insight.git
cd av_insight
Create and activate a virtual environment:

sh
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install Python dependencies:

sh
Copy code
pip install --upgrade pip
pip install -r requirements.txt
Run the backend application:

sh
Copy code
uvicorn app.main:app --host 0.0.0.0 --port 8000
Frontend Setup
Navigate to the frontend directory:

sh
Copy code
cd frontend
Install frontend dependencies:

sh
Copy code
npm install
Run the frontend application:

sh
Copy code
npm start
Docker Setup
Build and run the Docker containers:
sh
Copy code
docker-compose up --build
Usage
Open your browser and navigate to http://localhost:3000 for the frontend interface.
Upload a video file using the provided interface.
The backend will process the video, perform sentiment analysis, and display the results in the frontend.
API Endpoints
POST /upload: Upload a video file
POST /analyze: Initiate sentiment analysis on the uploaded video
GET /results: Retrieve the analysis results
Example Usage
Upload a Video
sh
Copy code
curl -X POST "http://localhost:8000/upload" -F "file=@path_to_your_video.mp4"
Analyze the Video
sh
Copy code
curl -X POST "http://localhost:8000/analyze" -d '{"filename": "your_video.mp4"}'
Get Analysis Results
sh
Copy code
curl -X GET "http://localhost:8000/results?filename=your_video.mp4"
Testing
Navigate to the project root directory:

sh
Copy code
cd av_insight
Run tests:

sh
Copy code
pytest
Contributing
Contributions are welcome! Please read the CONTRIBUTING.md for guidelines.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
FastAPI
React
PyTorch
Docker