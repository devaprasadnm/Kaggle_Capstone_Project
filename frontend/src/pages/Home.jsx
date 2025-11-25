import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center text-center p-6">
            <h1 className="text-5xl font-bold text-dark mb-6">
                Carbon Emission <span className="text-primary">Intelligence Assistant</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mb-10">
                Analyze your company's carbon footprint, get AI-driven optimization suggestions, and generate comprehensive sustainability reports.
            </p>
            <Link to="/upload" className="btn-primary text-lg">
                Start Analysis
            </Link>

            <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="card">
                    <h3 className="text-xl font-bold mb-2">Data Analysis</h3>
                    <p>Upload your data and let our agents clean and process it.</p>
                </div>
                <div className="card">
                    <h3 className="text-xl font-bold mb-2">AI Prediction</h3>
                    <p>Accurate ML models predict your carbon emissions.</p>
                </div>
                <div className="card">
                    <h3 className="text-xl font-bold mb-2">Optimization</h3>
                    <p>Get actionable steps to reduce your footprint.</p>
                </div>
            </div>
        </div>
    );
};

export default Home;
