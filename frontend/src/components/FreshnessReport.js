import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

function FreshnessReport() {
  const { id } = useParams();
  const [batch, setBatch] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBatch = async () => {
      try {
        const response = await axios.get(`${API_URL}/batches/${id}`);
        setBatch(response.data);
      } catch (err) {
        setError("Failed to fetch batch details");
        console.error("Error:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchBatch();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading freshness report...</p>
        </div>
      </div>
    );
  }

  if (error || !batch) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="text-5xl mb-4">☹️</div>
          <p className="text-gray-600">{error || "Batch not found"}</p>
        </div>
      </div>
    );
  }

  const getFreshnessEmoji = (days) => {
    if (days <= 2) return "🥩";
    if (days <= 4) return "⚠️";
    return "⛔";
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
        <div className="text-center">
          <div className="text-6xl mb-4">
            {getFreshnessEmoji(batch.days_on_shelf)}
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {batch.product}
          </h1>
          <p className="text-gray-600">Freshness Report</p>
        </div>

        <div className="mt-8 space-y-6">
          <div className="bg-blue-50 p-4 rounded-lg text-center">
            <div className="text-sm font-medium text-blue-800">
              Days on Shelf
            </div>
            <div className="text-3xl font-bold text-blue-900">
              {batch.days_on_shelf}
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex justify-between">
              <span className="text-gray-600">Butchered On:</span>
              <span className="font-medium">{batch.butcher_date}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Arrived in Store:</span>
              <span className="font-medium">{batch.arrival_date}</span>
            </div>
          </div>
        </div>

        <div className="mt-8 text-center">
          <p className="text-xs text-gray-400">
            Thank you for checking freshness with us!
          </p>
        </div>
      </div>
    </div>
  );
}

export default FreshnessReport;
