import React, { useState, useEffect } from "react";
import axios from "axios";
import QRCode from "react-qr-code";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

function AdminPortal() {
  const [batches, setBatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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

    try {
      await axios.post(`${API_URL}/batches/`, formData);
      setFormData({
        product: "Chicken",
        batch_identifier: "",
        butcher_date: "",
        arrival_date: "",
      });
      fetchBatches();
    } catch (err) {
      setError("Failed to create batch");
      console.error("Error:", err);
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
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Freshness Tracker Admin</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="bg-white shadow rounded-lg p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Add New Batch</h2>
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Product Type
              </label>
              <select
                name="product"
                value={formData.product}
                onChange={handleChange}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
              >
                <option value="Chicken">Chicken</option>
                <option value="Beef">Beef</option>
                <option value="Pork">Pork</option>
                <option value="Seafood">Seafood</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Batch Identifier
              </label>
              <input
                type="text"
                name="batch_identifier"
                value={formData.batch_identifier}
                onChange={handleChange}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Butcher Date
              </label>
              <input
                type="date"
                name="butcher_date"
                value={formData.butcher_date}
                onChange={handleChange}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Arrival Date
              </label>
              <input
                type="date"
                name="arrival_date"
                value={formData.arrival_date}
                onChange={handleChange}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-blue-300"
          >
            {loading ? "Adding..." : "Add Batch"}
          </button>
        </form>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Existing Batches</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {batches.map((batch) => (
            <div key={batch.id} className="border rounded-lg p-4">
              <h3 className="font-semibold">{batch.product}</h3>
              <p className="text-sm text-gray-600">{batch.batch_identifier}</p>
              <p className="text-sm">Butchered: {batch.butcher_date}</p>
              <p className="text-sm">Arrived: {batch.arrival_date}</p>
              <div className="mt-4">
                <QRCode
                  value={`${window.location.origin}/batch/${batch.id}`}
                  size={128}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default AdminPortal;
