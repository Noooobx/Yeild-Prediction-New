import React from 'react';
import { motion } from 'framer-motion';

export function InputField({ label, name, value, onChange, type = "text", step, placeholder, error }) {
  return (
    <div className="space-y-1">
      <label className="text-sm font-medium text-gray-700">{label}</label>
      <motion.input
        whileFocus={{ scale: 1.01, borderColor: '#2d6a4f' }}
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        step={step}
        placeholder={placeholder}
        className={`w-full px-4 py-2.5 rounded-xl border ${error ? 'border-red-500 bg-red-50' : 'border-gray-300 bg-white/50'} focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all shadow-sm`}
      />
      {error && <p className="text-xs text-red-500">{error}</p>}
    </div>
  );
}

export function SelectField({ label, name, value, onChange, options }) {
  return (
    <div className="space-y-1">
      <label className="text-sm font-medium text-gray-700">{label}</label>
      <motion.select
        whileFocus={{ scale: 1.01, borderColor: '#2d6a4f' }}
        name={name}
        value={value}
        onChange={onChange}
        className="w-full px-4 py-2.5 rounded-xl border border-gray-300 bg-white/50 focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all shadow-sm appearance-none cursor-pointer"
      >
        {options.map(opt => (
          <option key={opt} value={opt}>{opt}</option>
        ))}
      </motion.select>
    </div>
  );
}
