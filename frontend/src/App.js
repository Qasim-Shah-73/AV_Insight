import React, { useState } from 'react';
import VideoUpload from './components/VideoUpload';
import SentiGraph from './components/SentiGraph';
import './App.css';

function App() {
  const [emotionScores, setEmotionScores] = useState(null);

  const handleVideoAnalysis = (scores) => {
    setEmotionScores(scores);
  };

  return (
    <div className="App">
      <h1>Emotion Sentigraph</h1>
      <VideoUpload onAnalysis={handleVideoAnalysis} />
      {emotionScores && <SentiGraph scores={emotionScores} />}
    </div>
  );
}

export default App;