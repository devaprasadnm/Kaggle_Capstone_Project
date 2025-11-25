import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Upload = () => {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        if (!file) return;
        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const sessionId = localStorage.getItem('session_id');
            const headers = sessionId ? { 'x-session-id': sessionId } : {};

            const response = await axios.post('http://localhost:8000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    ...headers
                }
            });

            if (response.data.session_id) {
                localStorage.setItem('session_id', response.data.session_id);
            }

            navigate('/predict');
        } catch (err) {
            setError('Upload failed. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-6">
            <div className="card w-full max-w-md">
                <h2 className="text-3xl font-bold mb-6 text-center">Upload Data</h2>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-10 text-center mb-6 hover:bg-gray-50 transition">
                    <input
                        type="file"
                        accept=".csv"
                        onChange={handleFileChange}
                        className="hidden"
                        id="file-upload"
                    />
                    <label htmlFor="file-upload" className="cursor-pointer">
                        {file ? (
                            <span className="text-primary font-semibold">{file.name}</span>
                        ) : (
                            <span className="text-gray-500">Click to select CSV file</span>
                        )}
                    </label>
                </div>

                {error && <p className="text-red-500 mb-4 text-center">{error}</p>}

                <button
                    onClick={handleUpload}
                    disabled={!file || loading}
                    className={`w-full btn-primary ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                    {loading ? 'Processing...' : 'Upload & Analyze'}
                </button>
            </div>
        </div>
    );
};

export default Upload;
