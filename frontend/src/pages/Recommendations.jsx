import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Recommendations = () => {
    const [optimization, setOptimization] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchOptimization = async () => {
            try {
                const sessionId = localStorage.getItem('session_id');
                if (!sessionId) {
                    navigate('/upload');
                    return;
                }

                const response = await axios.post('http://localhost:8000/optimize', {}, {
                    headers: { 'x-session-id': sessionId }
                });
                setOptimization(response.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchOptimization();
    }, [navigate]);

    if (loading) return <div className="min-h-screen flex items-center justify-center">Generating Suggestions...</div>;
    if (!optimization) return <div className="min-h-screen flex items-center justify-center">Error loading suggestions.</div>;

    return (
        <div className="min-h-screen p-10 max-w-6xl mx-auto">
            <h2 className="text-3xl font-bold mb-8">Optimization Recommendations</h2>

            <div className="mb-8 p-6 bg-emerald-50 rounded-xl border border-emerald-100">
                <h3 className="text-xl font-bold text-emerald-800 mb-2">Potential Savings</h3>
                <p className="text-4xl font-bold text-emerald-600">
                    {optimization.total_potential_savings.toFixed(2)} <span className="text-lg">kg CO2e</span>
                </p>
            </div>

            <div className="grid grid-cols-1 gap-6">
                {optimization.suggestions.map((item, index) => (
                    <div key={index} className="card flex flex-col md:flex-row justify-between items-center">
                        <div>
                            <span className="inline-block px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-sm font-semibold mb-2">
                                {item.category}
                            </span>
                            <p className="text-lg font-medium text-gray-800">{item.suggestion}</p>
                        </div>
                        <div className="mt-4 md:mt-0 text-right">
                            <p className="text-sm text-gray-500">Potential Saving</p>
                            <p className="text-xl font-bold text-primary">{item.potential_saving_kg.toFixed(2)} kg</p>
                        </div>
                    </div>
                ))}
            </div>

            <div className="mt-10 text-center">
                <button
                    onClick={() => navigate('/report')}
                    className="btn-primary"
                >
                    Generate Final Report
                </button>
            </div>
        </div>
    );
};

export default Recommendations;
