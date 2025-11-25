import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Report = () => {
    const [downloading, setDownloading] = useState(false);
    const navigate = useNavigate();

    const handleDownload = async () => {
        setDownloading(true);
        try {
            const sessionId = localStorage.getItem('session_id');
            const response = await axios.post('http://localhost:8000/generate-report', {}, {
                headers: { 'x-session-id': sessionId },
                responseType: 'blob'
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'Sustainability_Report.pdf');
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (err) {
            console.error(err);
            alert("Failed to generate report. Please ensure all steps are completed.");
        } finally {
            setDownloading(false);
        }
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-6 text-center">
            <h2 className="text-4xl font-bold mb-6">Your Report is Ready</h2>
            <p className="text-xl text-gray-600 max-w-2xl mb-10">
                We have compiled your data, analysis, and recommendations into a comprehensive PDF report.
            </p>

            <button
                onClick={handleDownload}
                disabled={downloading}
                className="btn-primary text-xl px-10 py-4"
            >
                {downloading ? 'Generating PDF...' : 'Download PDF Report'}
            </button>

            <button
                onClick={() => {
                    localStorage.removeItem('session_id');
                    navigate('/');
                }}
                className="mt-8 text-gray-500 hover:text-gray-800 underline"
            >
                Start New Analysis
            </button>
        </div>
    );
};

export default Report;
