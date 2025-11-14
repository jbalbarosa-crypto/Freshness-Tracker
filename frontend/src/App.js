import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AdminPortal from "./components/AdminPortal";
import FreshnessReport from "./components/FreshnessReport";
import "./index.css";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Routes>
          <Route path="/" element={<AdminPortal />} />
          <Route path="/batch/:id" element={<FreshnessReport />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
