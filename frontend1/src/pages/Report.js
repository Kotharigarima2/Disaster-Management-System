import { useState, useEffect } from "react";
import axios from "axios";

import MapComponent from "../components/Report/MapComponent";
import ReportForm from "../components/Report/ReportForm";
import Legend from "../components/Report/Legend";

import "./Report.css";

function Report() {
  const [reports, setReports] = useState([]);

  const fetchReports = async () => {
    try {
      const [liveRes, histRes] = await Promise.all([
        axios.get("http://localhost:5000/reports"),
        axios.get("http://localhost:5000/historical"),
      ]);

      const live = liveRes.data.map(r => ({
        ...r,
        lat: Number(r.lat),
        lng: Number(r.lng),
        source: "live"
      }));

      const historical = histRes.data.map(r => ({
        ...r,
        lat: Number(r.lat),
        lng: Number(r.lng),
        source: "historical"
      }));

      setReports([...live, ...historical]);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  return (
    <div className="container">
       
      <ReportForm onSuccess={fetchReports} />

      <h3 className="map-title">Disaster Map</h3>

      <div className="map-container">
        <MapComponent reports={reports} />
        <Legend />
      </div>
    </div>
  );
}

export default Report;