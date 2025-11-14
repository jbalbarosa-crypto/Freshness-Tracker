import React, { useState, useEffect } from "react";
import axios from "axios";
import QRCode from "react-qr-code";
import { useAuth } from "../context/AuthContext";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

function AdminPortal() {
  const { user } = useAuth();
  const [batches, setBatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const [formData, setFormData] = useState({
    product: "Chicken",
    batch_identifier: "",
    butcher_date: "",
    arrival_date: "",
  });

  useEffect(() => {
    fetchBatches();
  }, []);

  const fetchBatches = async () => {
    try {
      const response = await axios.get(`${API_URL}/batches/`);
      setBatches(response.data);
    } catch (err) {
      setError("Failed to fetch batches");
      console.error("Error:", err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      await axios.post(`${API_URL}/batches/`, formData);
      setFormData({
        product: "Chicken",
        batch_identifier: "",
        butcher_date: "",
        arrival_date: "",
      });
      setShowForm(false);
      setSuccess("Batch created successfully!");
      setTimeout(() => setSuccess(null), 3000);
      fetchBatches();
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create batch");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
          <p className="text-gray-600">Welcome back, {user?.full_name || user?.email}</p>
        </div>

        {/* Alerts */}
        {error && (
          <div className="mb-4 p-4 bg-red-100 border-l-4 border-red-600 text-red-700 rounded">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-4 p-4 bg-green-100 border-l-4 border-green-600 text-green-700 rounded">
            {success}
          </div>
        )}

        {/* Add Batch Button */}
        {!showForm && (
          <button
            onClick={() => setShowForm(true)}
            className="mb-6 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 font-medium transition shadow-lg"
          >
            + Add New Batch
          </button>
        )}

        {/* Add Batch Form */}
        {showForm && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8 border-l-4 border-blue-600">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Add New Batch</h2>
              <button
                onClick={() => setShowForm(false)}
                className="text-gray-500 hover:text-gray-700 text-2xl"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Product Type
                  </label>
                  <select
                    name="product"
                    value={formData.product}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                  >
                    <option value="Chicken">🍗 Chicken</option>
                    <option value="Beef">🥩 Beef</option>
                    <option value="Pork">🍖 Pork</option>
                    <option value="Seafood">🦐 Seafood</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Batch Identifier
                  </label>
                  <input
                    type="text"
                    name="batch_identifier"
                    value={formData.batch_identifier}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                    placeholder="e.g., BATCH-001"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Butcher Date
                  </label>
                  <input
                    type="date"
                    name="butcher_date"
                    value={formData.butcher_date}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Arrival Date
                  </label>
                  <input
                    type="date"
                    name="arrival_date"
                    value={formData.arrival_date}
                    onChange={handleChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                    required
                  />
                </div>
              </div>

              <div className="flex gap-4 mt-6">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:bg-blue-300 font-medium transition"
                >
                  {loading ? "Creating..." : "Create Batch"}
                </button>
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="flex-1 bg-gray-300 text-gray-800 py-2 rounded-lg hover:bg-gray-400 font-medium transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Batches Grid */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Batches</h2>

          {batches.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-5xl mb-4">📦</div>
              <p className="text-gray-600">No batches yet. Create one to get started!</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {batches.map((batch) => (
                <div
                  key={batch.id}
                  className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition bg-gradient-to-br from-white to-gray-50"
                >
                  <div className="text-3xl mb-3">
                    {batch.product === "Chicken"
                      ? "🍗"
                      : batch.product === "Beef"
                      ? "🥩"
                      : batch.product === "Pork"
                      ? "🍖"
                      : "🦐"}
                  </div>
                  <h3 className="font-bold text-lg text-gray-900 mb-2">
                    {batch.product}
                  </h3>
                  <p className="text-sm text-gray-600 mb-1">
                    <span className="font-semibold">ID:</span> {batch.batch_identifier}
                  </p>
                  <p className="text-sm text-gray-600 mb-1">
                    <span className="font-semibold">Butchered:</span>{" "}
                    {new Date(batch.butcher_date).toLocaleDateString()}
                  </p>
                  <p className="text-sm text-gray-600 mb-4">
                    <span className="font-semibold">Arrived:</span>{" "}
                    {new Date(batch.arrival_date).toLocaleDateString()}
                  </p>
                  <div className="bg-white p-2 rounded inline-block">
                    <QRCode
                      value={`${window.location.origin}/batch/${batch.id}`}
                      size={120}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AdminPortal;
