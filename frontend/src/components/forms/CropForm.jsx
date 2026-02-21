import React from 'react';
import { motion } from 'framer-motion';
import { Sprout, Ruler, FlaskConical, CloudRain, Tractor } from 'lucide-react';
import { InputField, SelectField } from '../ui/FormElements';
import { Card } from '../ui/Card';

const CROPS = ['Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Tea', 'Coffee', 'Jute', 'Potato', 'Onion'];
const SOIL_TYPES = ['Clay', 'Sandy', 'Loam', 'Silt', 'Peaty', 'Chalky'];
const SEASONS = ['Kharif', 'Rabi', 'Zaid', 'Whole Year'];
const IRRIGATION_METHODS = ['Drip', 'Sprinkler', 'Flood', 'Rainfed'];
const FERTILIZER_TYPES = ['Urea', 'DAP', 'MOP', 'NPK', 'Superphosphate', 'Organic', 'None'];

export default function CropForm({ formData, handleChange, handleSubmit, loading }) {
  return (
    <Card className="h-full">
      <div className="flex items-center gap-2 mb-6 text-primary">
        <Sprout size={24} />
        <h2 className="text-xl font-bold">Crop Configuration</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Section 1: Crop Basics */}
        <section className="space-y-4">
          <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Basic Info</label>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <SelectField label="Crop Type" name="Crop_Type" value={formData.Crop_Type} onChange={handleChange} options={CROPS} />
            <SelectField label="Season" name="Season" value={formData.Season} onChange={handleChange} options={SEASONS} />
            <InputField label="Duration (Days)" name="Growth_Duration" value={formData.Growth_Duration} onChange={handleChange} type="number" />
          </div>
        </section>

        {/* Section 2: Soil & Area */}
        <section className="space-y-4">
          <label className="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center gap-2">
            <Ruler size={14} /> Field Parameters
          </label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <SelectField label="Soil Type" name="Soil_Type" value={formData.Soil_Type} onChange={handleChange} options={SOIL_TYPES} />
            <InputField label="Area Size" name="Area" value={formData.Area} onChange={handleChange} type="number" step="0.1" />
            <SelectField label="Area Unit" name="Area_Unit" value={formData.Area_Unit} onChange={handleChange} options={['Hectare', 'Acre', 'Sq_Meter']} />
          </div>
        </section>

        {/* Section 3: Nutrients */}
        <section className="space-y-4">
          <label className="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center gap-2">
            <FlaskConical size={14} /> Soil Nutrients
          </label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <InputField label="N (kg/ha)" name="Nitrogen" value={formData.Nitrogen} onChange={handleChange} type="number" />
            <InputField label="P (kg/ha)" name="Phosphorus" value={formData.Phosphorus} onChange={handleChange} type="number" />
            <InputField label="K (kg/ha)" name="Potassium" value={formData.Potassium} onChange={handleChange} type="number" />
            <InputField label="pH Level" name="Soil_pH" value={formData.Soil_pH} onChange={handleChange} type="number" step="0.1" />
          </div>
        </section>

        {/* Section 4: Weather & Irrigation */}
        <section className="space-y-4">
          <label className="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center gap-2">
            <CloudRain size={14} /> Weather & Water
          </label>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <InputField label="Temp (°C)" name="Temperature" value={formData.Temperature} onChange={handleChange} type="number" step="0.1" />
            <InputField label="Rain (mm)" name="Rainfall" value={formData.Rainfall} onChange={handleChange} type="number" />
            <InputField label="Humidity (%)" name="Humidity" value={formData.Humidity} onChange={handleChange} type="number" />
            <SelectField label="Irrigation" name="Irrigation_Method" value={formData.Irrigation_Method} onChange={handleChange} options={IRRIGATION_METHODS} />
          </div>
        </section>

        {/* Section 5: Fertilizer */}
        <section className="space-y-4">
           <label className="text-xs font-bold text-gray-400 uppercase tracking-wider flex items-center gap-2">
            <Tractor size={14} /> Fertilizer Strategy
          </label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
             <SelectField label="Type" name="Fertilizer_Type" value={formData.Fertilizer_Type} onChange={handleChange} options={FERTILIZER_TYPES} />
             <InputField label="Dosage (kg/ha)" name="Fertilizer_Dosage" value={formData.Fertilizer_Dosage} onChange={handleChange} type="number" />
             <SelectField label="Output Unit" name="Yield_Unit" value={formData.Yield_Unit} onChange={handleChange} options={['Ton', 'Kg', 'Quintal']} />
          </div>
        </section>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          type="submit"
          disabled={loading}
          className="w-full bg-primary hover:bg-primary-dark text-white font-bold py-4 rounded-xl shadow-lg shadow-primary/30 transition-all flex items-center justify-center gap-2 text-lg disabled:opacity-70 disabled:cursor-not-allowed mt-4"
        >
          {loading ? (
            <>
              <svg className="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing Data...
            </>
          ) : (
            'Generate Prediction'
          )}
        </motion.button>
      </form>
    </Card>
  );
}
