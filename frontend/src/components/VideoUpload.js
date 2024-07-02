import React, { useState } from 'react';
import './VideoUpload.css'; // We'll create this file for styling

function VideoUpload({ onAnalysis }) {
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    setFile(e.dataTransfer.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file first!');
      return;
    }
  
    try {
      const response = await fetch('http://localhost:8000/analyze_video');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      onAnalysis(data.emotion_scores);
    } catch (error) {
      console.error("There was a problem with the fetch operation: ", error);
      alert("Failed to analyze video. Please try again.");
    }
  };

  return (
    <div className="video-upload-container">
      <div 
        className={`drop-zone ${dragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <i className="fas fa-cloud-upload-alt"></i>
        <p>Drag & Drop your video here or</p>
        <input 
          type="file" 
          id="file-upload" 
          accept="video/*" 
          onChange={handleFileChange} 
          hidden
        />
        <label htmlFor="file-upload" className="file-upload-btn">
          Choose File
        </label>
        {file && <p className="file-name">{file.name}</p>}
      </div>
      <button 
        className="upload-btn" 
        onClick={handleUpload} 
        disabled={!file}
      >
        Upload and Analyze
      </button>
    </div>
  );
}

export default VideoUpload;