import React from "react";
import { Link } from "react-router-dom";

function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <div className="text-7xl mb-6 animate-bounce">🥩</div>
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-4">
            Freshness Tracker
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Keep your meat fresh and your customers happy. Track batch freshness with our intelligent QR-based system.
          </p>
          <div className="flex gap-4 justify-center">
            <Link
              to="/login"
              className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition shadow-lg"
            >
              Sign In
            </Link>
            <Link
              to="/register"
              className="px-8 py-3 bg-white border-2 border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 font-medium transition"
            >
              Get Started
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20">
          <div className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
            <div className="text-4xl mb-4">📱</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">QR Tracking</h3>
            <p className="text-gray-600">
              Scan QR codes to instantly check freshness information for any batch.
            </p>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
            <div className="text-4xl mb-4">🔍</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Real-time Status</h3>
            <p className="text-gray-600">
              Get instant freshness indicators - green for fresh, yellow for caution, red for expired.
            </p>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Admin Dashboard</h3>
            <p className="text-gray-600">
              Manage all your batches in one centralized dashboard with full control.
            </p>
          </div>
        </div>

        {/* How It Works */}
        <div className="mt-20 bg-white rounded-lg shadow-lg p-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-5xl mb-4">1️⃣</div>
              <h4 className="font-bold text-gray-900 mb-2">Create Batch</h4>
              <p className="text-gray-600 text-sm">Add new meat batch with dates</p>
            </div>
            <div className="text-center">
              <div className="text-5xl mb-4">2️⃣</div>
              <h4 className="font-bold text-gray-900 mb-2">Generate QR</h4>
              <p className="text-gray-600 text-sm">System generates unique QR code</p>
            </div>
            <div className="text-center">
              <div className="text-5xl mb-4">3️⃣</div>
              <h4 className="font-bold text-gray-900 mb-2">Share QR Code</h4>
              <p className="text-gray-600 text-sm">Print or display at store</p>
            </div>
            <div className="text-center">
              <div className="text-5xl mb-4">4️⃣</div>
              <h4 className="font-bold text-gray-900 mb-2">Scan & Check</h4>
              <p className="text-gray-600 text-sm">Customers scan to verify freshness</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Landing;
