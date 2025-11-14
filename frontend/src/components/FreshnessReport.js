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

  const getFreshnessStatus = (days) => {
    if (days <= 2) {
      return { emoji: "🥩", status: "Fresh", color: "bg-green-100", textColor: "text-green-800" };
    }
    if (days <= 4) {
      return { emoji: "⚠️", status: "Caution", color: "bg-yellow-100", textColor: "text-yellow-800" };
    }
    return { emoji: "⛔", status: "Expired", color: "bg-red-100", textColor: "text-red-800" };
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="bg-white rounded-xl shadow-2xl p-8 max-w-md w-full transform transition hover:shadow-3xl">
        {/* Product Emoji */}
        <div className="text-center mb-6">
          <div className="text-6xl mb-4 animate-bounce">
            {batch.product === "Chicken"
              ? "🍗"
              : batch.product === "Beef"
              ? "🥩"
              : batch.product === "Pork"
              ? "🍖"
              : "🦐"}
          </div>
          <h1 className="text-3xl font-bold text-gray-900">{batch.product}</h1>
          <p className="text-gray-600 mt-1">Freshness Report</p>
        </div>

        {/* Freshness Status */}
        <div className="mb-6">
          <div
            className={`${getFreshnessStatus(batch.days_on_shelf).color} ${getFreshnessStatus(batch.days_on_shelf).textColor} p-6 rounded-lg text-center`}
          >
            <div className="text-4xl mb-2">
              {getFreshnessStatus(batch.days_on_shelf).emoji}
            </div>
            <div className="text-2xl font-bold mb-2">
              {getFreshnessStatus(batch.days_on_shelf).status}
            </div>
            <p className="text-sm">
              {batch.days_on_shelf <= 2
                ? "Product is fresh and ready to consume"
                : batch.days_on_shelf <= 4
                ? "Product should be consumed soon"
                : "Product is past expiration"}
            </p>
          </div>
        </div>

        {/* Days Counter */}
        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg text-center mb-6">
          <div className="text-sm font-medium text-blue-800 mb-2">Days on Shelf</div>
          <div className="text-5xl font-bold text-blue-900">{batch.days_on_shelf}</div>
          <div className="text-xs text-blue-600 mt-2">
            {batch.days_on_shelf === 1 ? "1 day ago" : `${batch.days_on_shelf} days ago`}
          </div>
        </div>

        {/* Details */}
        <div className="bg-gray-50 p-6 rounded-lg mb-6 space-y-4">
          <div className="border-b pb-4">
            <p className="text-xs font-semibold text-gray-600 uppercase tracking-wide">
              Butcher Date
            </p>
            <p className="text-lg font-semibold text-gray-900 mt-1">
              {new Date(batch.butcher_date).toLocaleDateString("en-US", {
                weekday: "long",
                year: "numeric",
                month: "long",
                day: "numeric",
              })}
            </p>
          </div>
          <div>
            <p className="text-xs font-semibold text-gray-600 uppercase tracking-wide">
              Store Arrival
            </p>
            <p className="text-lg font-semibold text-gray-900 mt-1">
              {new Date(batch.arrival_date).toLocaleDateString("en-US", {
                weekday: "long",
                year: "numeric",
                month: "long",
                day: "numeric",
              })}
            </p>
          </div>
        </div>

        {/* Batch ID */}
        <div className="text-center text-xs text-gray-500">
          <p>Batch ID: {batch.id}</p>
        </div>

        {/* Footer Message */}
        <div className="mt-8 pt-6 border-t text-center">
          <p className="text-xs text-gray-500">
            Thank you for checking freshness with us! 🙏
          </p>
        </div>
      </div>
    </div>
  );
}

export default FreshnessReport;
