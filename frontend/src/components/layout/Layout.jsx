import React from 'react';
import { Sprout } from 'lucide-react';

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 flex flex-col font-sans">
      {/* Navbar */}
      <nav className="bg-primary text-white shadow-lg sticky top-0 z-50 backdrop-blur-md bg-opacity-90">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-2">
              <Sprout size={32} className="text-secondary" />
              <span className="text-xl font-bold tracking-tight">SmartAgro</span>
            </div>
            <div className="hidden md:flex space-x-8 text-sm font-medium opacity-90">
              <a href="#" className="hover:text-secondary transition-colors">Dashboard</a>
              <a href="#" className="hover:text-secondary transition-colors">Analytics</a>
              <a href="#" className="hover:text-secondary transition-colors">History</a>
              <a href="#" className="hover:text-secondary transition-colors">Settings</a>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-primary-dark text-white/70 py-6 mt-auto">
        <div className="max-w-7xl mx-auto px-4 text-center text-sm">
          <p>© 2026 SmartAgro Analytics. Engineering Project Showcase.</p>
        </div>
      </footer>
    </div>
  );
}
