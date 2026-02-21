import React from 'react';
import { motion } from 'framer-motion';

export function Card({ children, className = "", delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: delay, duration: 0.5 }}
      whileHover={{ y: -5 }}
      className={`bg-white/80 backdrop-blur-md border border-white/60 rounded-2xl shadow-xl p-6 ${className}`}
    >
      {children}
    </motion.div>
  );
}
