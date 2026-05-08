import React, { useEffect, useState } from "react";
import axios from "axios";
import BackButton from "../components/BackButton/BackButton";

import {
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid,
  PieChart, Pie, Cell, Legend, ResponsiveContainer
} from "recharts";

import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

import "./Dashboard.css";

// Fix default marker icon issue
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",

  iconUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",

  shadowUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

// Disaster marker PNG URLs
const disasterMarkers = {
  Flood:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png",

  Fire:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",

  Cyclone:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-violet.png",

  Heatwave:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png",

  Other:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-grey.png"
};

function Dashboard() {

  const [disasterData, setDisasterData] = useState([]);
  const [priorityStats, setPriorityStats] = useState([]);
  const [needsStats, setNeedsStats] = useState([]);
  const [loading, setLoading] = useState(true);

  const cityCoords = {
    Delhi: [28.6139, 77.2090],
    Mumbai: [19.0760, 72.8777],
    Chennai: [13.0827, 80.2707],
    Kolkata: [22.5726, 88.3639],
    Bangalore: [12.9716, 77.5946],
    Hyderabad: [17.3850, 78.4867]
  };

  useEffect(() => {

    axios.get("http://localhost:5000/api/dashboard")

      .then(res => {

        setDisasterData(res.data.disaster || []);

        const priorityChart =
          Object.entries(res.data.priority || {})
            .map(([level, value]) => ({
              level,
              value
            }));

        setPriorityStats(priorityChart);

        setNeedsStats(res.data.needs || []);

        setLoading(false);

      })

      .catch(err => {

        console.log(err);
        setLoading(false);

      });

  }, []);

  // Calculate counts
  const locationCounts = {};
  const disasterCounts = {};

  disasterData.forEach(item => {

    if (item.location)

      locationCounts[item.location] =
        (locationCounts[item.location] || 0) + 1;

    if (item.disaster)

      disasterCounts[item.disaster] =
        (disasterCounts[item.disaster] || 0) + 1;

  });

  const topLocations = Object.entries(locationCounts)

    .sort((a, b) => b[1] - a[1])

    .slice(0, 5)

    .map(([location, count]) => ({
      location,
      count
    }));

  const disasterTypes = Object.entries(disasterCounts)

    .map(([name, value]) => ({
      name,
      value
    }));

  if (loading)

    return (

      <div className="loading-container">

        <BackButton />

        <h2>
          Loading Dashboard...
        </h2>

      </div>
    );

  return (

    <div className="dashboard-container">

      {/* HEADER */}
      <div className="dashboard-header">

        <BackButton />

        <h1 className="dashboard-title">
          🚀 Disaster Management Dashboard
        </h1>

      </div>

      {/* STATS */}
      <div className="stats-grid">

        <div className="stats-card">
          <h3>Total Reports</h3>
          <p>{disasterData.length}</p>
        </div>

        <div className="stats-card">
          <h3>High Priority</h3>

          <p>
            {priorityStats.find(
              p => p.level === "HIGH"
            )?.value || 0}
          </p>

        </div>

        <div className="stats-card">
          <h3>Active Needs</h3>
          <p>{needsStats.length}</p>
        </div>

      </div>

      {/* CHARTS */}
      <div className="charts-grid">

        {/* BAR CHART */}
        <div className="chart-box">

          <h3>
            📍 Top Locations
          </h3>

          <ResponsiveContainer width="100%" height={250}>

            <BarChart data={topLocations}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="location" />

              <YAxis />

              <Tooltip />

              <Bar
                dataKey="count"
                fill="#0088FE"
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

        {/* PIE CHART */}
        <div className="chart-box">

          <h3>
            🌪️ Disaster Types
          </h3>

          <ResponsiveContainer width="100%" height={250}>

            <PieChart>

              <Pie
                data={disasterTypes}
                dataKey="value"
                nameKey="name"
                outerRadius={80}
                label
              >

                {disasterTypes.map((d, i) => (

                  <Cell
                    key={i}
                    fill={
                      d.name in disasterMarkers

                        ? d.name === "Flood"
                          ? "#0000FF"

                          : d.name === "Fire"
                          ? "#FF0000"

                          : d.name === "Cyclone"
                          ? "#8A2BE2"

                          : d.name === "Heatwave"
                          ? "#FFA500"

                          : "#7f7f7f"

                        : "#7f7f7f"
                    }
                  />

                ))}

              </Pie>

              <Tooltip />

              <Legend />

            </PieChart>

          </ResponsiveContainer>

        </div>

        {/* PRIORITY */}
        <div className="chart-box">

          <h3>
            🚨 Priority Levels
          </h3>

          <ResponsiveContainer width="100%" height={250}>

            <BarChart data={priorityStats}>

              <CartesianGrid strokeDasharray="3 3" />

              <XAxis dataKey="level" />

              <YAxis />

              <Tooltip />

              <Bar
                dataKey="value"
                fill="#ff4d4d"
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

        {/* NEEDS */}
        <div className="chart-box">

          <h3>
            🧑‍🤝‍🧑 Human Needs
          </h3>

          <div className="needs-wrapper">

            {needsStats.map((need, i) => (

              <span
                key={i}
                className="need-pill"
              >
                {need}
              </span>

            ))}

          </div>

        </div>

        {/* MAP */}
        <div className="map-box">

          <h3>
            🗺️ Disaster Map
          </h3>

          <MapContainer
            center={[20.5937, 78.9629]}
            zoom={5}
            className="map-container"
          >

            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"

              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            />

            {disasterData.map((d, i) => {

              const coords = cityCoords[d.location];

              if (!coords) return null;

              const icon = new L.Icon({

                iconUrl:
                  disasterMarkers[d.disaster]
                  || disasterMarkers.Other,

                iconSize: [25, 41],

                iconAnchor: [12, 41],

                popupAnchor: [0, -41],

                shadowUrl:
                  "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",

                shadowSize: [41, 41],

                shadowAnchor: [12, 41],

              });

              return (

                <Marker
                  key={i}
                  position={coords}
                  icon={icon}
                >

                  <Popup>

                    <strong>
                      {d.location}
                    </strong>

                    <br />

                    {d.disaster}

                    <br />

                    {d.tweet}

                  </Popup>

                </Marker>
              );
            })}

          </MapContainer>

        </div>

      </div>

    </div>
  );
}

export default Dashboard;