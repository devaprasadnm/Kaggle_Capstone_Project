import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Prediction = () => {
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchPrediction = async () => {
            try {
                const sessionId = localStorage.getItem('session_id');
                if (!sessionId) {
                    navigate('/upload');
                    return;
                }

                const response = await axios.post('http://localhost:8000/predict', {}, {
                    headers: { 'x-session-id': sessionId }
                });
                setPrediction(response.data);
            } catch (err) {
                console.error(err);
                // Handle error (maybe redirect to upload if session expired)
            } finally {
                setLoading(false);
            }
        };

        fetchPrediction();
    }, [navigate]);

    if (loading) return <div className="min-h-screen flex items-center justify-center">Loading Prediction...</div>;
    if (!prediction) return <div className="min-h-screen flex items-center justify-center">Error loading prediction.</div>;

    const data = [
        { name: 'Estimated Emission', value: prediction.emission_kg },
        { name: 'Industry Average', value: prediction.emission_kg * 0.9 } // Mock comparison
    ];

    return (
        <div className="min-h-screen p-10 max-w-6xl mx-auto">
            <h2 className="text-3xl font-bold mb-8">Emission Analysis</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                <div className="card">
                    <h3 className="text-xl font-semibold mb-4">Total Carbon Emission</h3>
                    <p className="text-5xl font-bold text-primary mb-4">
                        {prediction.emission_kg.toFixed(2)} <span className="text-lg text-gray-500">kg CO2e</span>
                    </p>
                    <p className="text-gray-700 leading-relaxed">
                        {prediction.explanation}
                    </p>
                </div>

                <div className="card h-80">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={data}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="value" fill="#10B981" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>

            <div className="mt-10 text-center">
                <button
                    onClick={() => navigate('/recommendations')}
                    className="btn-primary"
                >
                    View Optimization Suggestions
                </button>
            </div>
        </div>
    );
};

export default Prediction;
