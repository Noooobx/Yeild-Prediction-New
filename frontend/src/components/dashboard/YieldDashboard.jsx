import React from 'react';
import { motion } from 'framer-motion';
import { Sprout, TrendingUp, BarChart3, Scale } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, BarChart, Bar, Cell } from 'recharts';
import { Card } from '../ui/Card';

export default function YieldDashboard({ result, inputs }) {
  if (!result) return null;

  // Mock Data for Visualizations based on input
  const nutrientData = [
    { subject: 'Nitrogen', A: inputs.Nitrogen, B: 120, fullMark: 150 },
    { subject: 'Phosphorus', A: inputs.Phosphorus, B: 60, fullMark: 150 },
    { subject: 'Potassium', A: inputs.Potassium, B: 60, fullMark: 150 },
    { subject: 'pH', A: inputs.Soil_pH * 10, B: 65, fullMark: 100 }, // Scale pH
    { subject: 'Moisture', A: inputs.Soil_Moisture, B: 80, fullMark: 100 },
  ];

  const trendData = [
    { year: '2021', yield: result.Yield_per_Hectare * 0.9 },
    { year: '2022', yield: result.Yield_per_Hectare * 0.8 },
    { year: '2023', yield: result.Yield_per_Hectare * 1.1 },
    { year: '2024', yield: result.Yield_per_Hectare * 0.95 },
    { year: '2025', yield: result.Yield_per_Hectare }, // Projected
  ];

  const COLORS = ['#2d6a4f', '#52b788', '#b7e4c7', '#d8f3dc'];

  return (
    <div className="space-y-6">
      {/* 1. Main KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <motion.div 
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="bg-gradient-to-br from-primary to-primary-dark rounded-2xl p-6 text-white shadow-xl relative overflow-hidden"
        >
          <div className="absolute right-0 top-0 opacity-10 transform translate-x-10 -translate-y-10">
            <Sprout size={150} />
          </div>
          <p className="text-secondary-light font-medium mb-1">Yield per Hectare</p>
          <h2 className="text-4xl font-bold flex items-baseline gap-2">
            {result.Yield_per_Hectare} <span className="text-xl font-normal opacity-80">{result.Yield_Unit}</span>
          </h2>
          <div className="mt-4 flex items-center gap-2 text-sm opacity-80 bg-white/10 w-fit px-3 py-1 rounded-full">
            <TrendingUp size={16} /> Projected Output
          </div>
        </motion.div>

        <motion.div 
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-2xl p-6 shadow-xl border border-gray-100"
        >
          <p className="text-gray-500 font-medium mb-1">Total Expected Yield</p>
          <h2 className="text-4xl font-bold text-gray-800 flex items-baseline gap-2">
            {result.Total_Yield} <span className="text-xl font-normal text-gray-400">{result.Yield_Unit}</span>
          </h2>
          <p className="mt-2 text-sm text-gray-500">
             For <span className="font-bold text-gray-700">{result.Area_in_Hectares} Ha</span> of land
          </p>
          <div className="h-2 w-full bg-gray-100 rounded-full mt-4 overflow-hidden">
            <motion.div 
              initial={{ width: 0 }}
              animate={{ width: '75%' }}
              className="h-full bg-accent"
            />
          </div>
        </motion.div>
      </div>

      {/* 2. Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Trend Chart */}
        <Card delay={0.2} className="min-h-[300px]">
          <div className="flex items-center gap-2 mb-4 text-gray-700 font-bold">
            <BarChart3 size={20} className="text-primary" />
            <h3>Yield Forecast Trend</h3>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData}>
                <defs>
                  <linearGradient id="colorYield" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2d6a4f" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#2d6a4f" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} opacity={0.3} />
                <XAxis dataKey="year" axisLine={false} tickLine={false} />
                <YAxis axisLine={false} tickLine={false} />
                <Tooltip 
                  contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)' }}
                />
                <Area type="monotone" dataKey="yield" stroke="#2d6a4f" strokeWidth={3} fillOpacity={1} fill="url(#colorYield)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Soil Balance Radar */}
        <Card delay={0.3} className="min-h-[300px]">
          <div className="flex items-center gap-2 mb-4 text-gray-700 font-bold">
            <Scale size={20} className="text-primary" />
            <h3>Soil Nutrient Balance</h3>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={nutrientData}>
                <PolarGrid opacity={0.4} />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#4b5563', fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} />
                <Radar name="Current Levels" dataKey="A" stroke="#2d6a4f" strokeWidth={2} fill="#52b788" fillOpacity={0.5} />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>
    </div>
  );
}
