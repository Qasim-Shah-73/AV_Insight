import React from 'react';
import { Bar, Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend } from 'chart.js';
import './SentiGraph.css'; // We'll create this file for styling

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

function SentiGraph({ scores }) {
  const labels = Object.keys(scores);
  const dataValues = Object.values(scores);

  const chartData = {
    labels: labels,
    datasets: [
      {
        label: 'Emotion Scores',
        data: dataValues,
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 159, 64, 0.6)',
          'rgba(199, 199, 199, 0.6)'
        ],
      },
    ],
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Emotion Scores Bar Chart',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 1,
      },
    },
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
      },
      title: {
        display: true,
        text: 'Emotion Distribution',
      },
    },
  };

  return (
    <div className="sentigraph-container">
      <div className="chart-wrapper bar-chart">
        <Bar data={chartData} options={barOptions} />
      </div>
      <div className="chart-wrapper doughnut-chart">
        <Doughnut data={chartData} options={doughnutOptions} />
      </div>
    </div>
  );
}

export default SentiGraph;