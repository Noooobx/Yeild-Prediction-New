import React, { useState } from 'react';
import axios from 'axios';
import { AnimatePresence, motion } from 'framer-motion';
import Layout from './components/layout/Layout';
import CropForm from './components/forms/CropForm';
import YieldDashboard from './components/dashboard/YieldDashboard';

const getApiUrl = () => {
  const url = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/predict';
  // Ensure the URL ends with /predict if it doesn't already
  if (url.includes('onrender.com') && !url.endsWith('/predict')) {
    return url.endsWith('/') ? `${url}predict` : `${url}/predict`;
  }
  return url;
};

const API_URL = getApiUrl();

export default function App() {
  const [formData, setFormData] = useState({
    Crop_Type: 'Rice',
    Nitrogen: 80,
    Phosphorus: 40,
    Potassium: 40,
    Soil_pH: 6.5,
    Soil_Moisture: 80,
    Soil_Type: 'Clay',
    Temperature: 25,
    Rainfall: 200,
    Humidity: 80,
    Sunlight_Hours: 8,
    Fertilizer_Type: 'Urea',
    Fertilizer_Dosage: 100,
    Irrigation_Method: 'Flood',
    Growth_Duration: 120,
    Season: 'Kharif',
    Area: 1,
    Area_Unit: 'Hectare',
    Yield_Unit: 'Ton'
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    // Simulate small delay for better UX on fast local networks
    await new Promise(resolve => setTimeout(resolve, 800));

    try {
      const response = await axios.post(API_URL, formData);
      setResult(response.data);
      // Smooth scroll to results on mobile
      if (window.innerWidth < 1024) {
        setTimeout(() => {
            const element = document.getElementById('results-section');
            if(element) element.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      }
    } catch (err) {
      console.error(err);
      setError('Failed to fetch prediction. ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Input Form */}
        <motion.div 
          initial={{ x: -20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="lg:col-span-1"
        >
          <CropForm 
            formData={formData} 
            handleChange={handleChange} 
            handleSubmit={handleSubmit} 
            loading={loading} 
          />
        </motion.div>

        {/* Right Column: Results & Dashboard */}
        <motion.div 
          id="results-section"
          initial={{ x: 20, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="lg:col-span-2 space-y-6"
        >
          <AnimatePresence mode="wait">
            {!result && !loading && !error && (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="h-full flex flex-col items-center justify-center text-gray-400 p-12 border-2 border-dashed border-gray-200 rounded-3xl"
              >
                <img src="https://cdn-icons-png.flaticon.com/512/6774/6774898.png" alt="Farm" className="w-32 h-32 opacity-50 mb-4 grayscale" />
                <h3 className="text-xl font-medium">Ready to Analyze</h3>
                <p>Fill in the crop parameters to generate a yield forecast.</p>
              </motion.div>
            )}

            {loading && (
               <motion.div 
                 initial={{ opacity: 0 }}
                 animate={{ opacity: 1 }}
                 exit={{ opacity: 0 }}
                 className="h-64 flex flex-col items-center justify-center space-y-4"
               >
                 <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
                 <p className="text-primary font-medium animate-pulse">Running ML Ensembles...</p>
               </motion.div>
            )}

            {error && (
              <motion.div 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-red-50 border border-red-200 text-red-700 p-6 rounded-2xl flex items-center gap-4"
              >
                <div className="bg-red-100 p-2 rounded-full">⚠️</div>
                <div>
                  <h4 className="font-bold">Error</h4>
                  <p>{error}</p>
                </div>
              </motion.div>
            )}

            {result && (
              <motion.div
                key="results"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <YieldDashboard result={result} inputs={formData} />
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </Layout>
  );
}
