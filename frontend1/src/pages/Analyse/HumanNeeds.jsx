import { useState } from "react";
import BackButton from "../../components/BackButton/BackButton";
import axios from "axios";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Cell
} from "recharts";

import "./HumanNeeds.css";

function HumanNeeds() {

  const [text, setText] = useState("");
  const [needs, setNeeds] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  /* 🌟 ALL CATEGORIES */
  const allCategories = [
    { label: "Food", emoji: "🍞" },
    { label: "Water", emoji: "💧" },
    { label: "Medical Help", emoji: "🏥" },
    { label: "Shelter", emoji: "🏠" },
    { label: "General Help", emoji: "🤝" },
    { label: "Emotional Support", emoji: "❤️" },
    { label: "Search & Rescue", emoji: "🔍" },
    { label: "No Need", emoji: "❌" },
    { label: "Required Info", emoji: "⚠️" }
  ];

  /* 🚀 PREDICT FUNCTION */
  const handlePredict = async () => {

    if (!text.trim()) return;

    setLoading(true);
    setError("");

    try {

      const res = await axios.post(
        "http://127.0.0.1:5001/predict",
        { text }
      );

      setNeeds(res.data.needs || []);

    } catch (err) {

      setError("Backend not running on port 5001");
      setNeeds([]);

    } finally {

      setLoading(false);
    }
  };

  /* 📊 CHART DATA */
  const chartData = allCategories.map((cat) => ({
    need: cat.label,
    emoji: cat.emoji,
    detected: needs.includes(`${cat.label} ${cat.emoji}`) ? 1 : 0
  }));

  return (

    <div className="humanneeds-container">

      {/* 🔥 HEADER */}
      <div className="humanneeds-header">

        {/* 🔙 BACK BUTTON */}
        <div className="back-btn-wrapper">
          <BackButton />
        </div>

        {/* 🎯 TITLE */}
        <h1 className="humanneeds-title">
           Human Needs Detection
        </h1>

      </div>

      {/* ✍️ TEXTAREA WRAPPER */}
<div className="textarea-wrapper">

  <textarea
    rows="4"
    className="humanneeds-textarea"
    value={text}
    onChange={(e) => setText(e.target.value)}
    placeholder="Enter tweet..."
  />

  {/* ✨ ICON */}
  <span className="textarea-icon">
    ✍️
  </span>

</div>

      {/* 🚀 BUTTON */}
      <button
        onClick={handlePredict}
        disabled={loading}
        className="predict-btn"
      >
        {loading ? "Predicting..." : "✨ Predict"}
      </button>

      {/* ❌ ERROR */}
      {error && (
        <p className="error-text">
          {error}
        </p>
      )}

      {/* 🔮 Analysis Result */}
      <h3 className="result-heading">
        Analysis Result
      </h3>

      {/* 🚫 NO RESULT */}
{needs.length === 0 && !loading && (

  <div className="no-result-card">

    {/* ✅ ICON */}
    <div className="result-icon">
      ✔
    </div>

    {/* 📝 TEXT */}
    <div className="result-content">

      <span className="result-label">
        Result
      </span>

      <p className="no-result">
        No detected needs ❌
      </p>

    </div>

  </div>

)}

      {/* 📈 CHART */}
      {needs.length > 0 && (

        <div className="chart-wrapper">

          <ResponsiveContainer width="100%" height={360}>

            <BarChart
              data={chartData}
              margin={{
                top: 20,
                right: 20,
                left: 0,
                bottom: 70
              }}
            >

              <CartesianGrid
                strokeDasharray="4 4"
                stroke="#d8d4fe"
              />

              {/* 🌟 CUSTOM X AXIS */}
              <XAxis
                dataKey="need"
                interval={0}
                tickLine={false}
                axisLine={false}

                tick={({ x, y, payload, index }) => {

                  const item = chartData[index];

                  return (

                    <g transform={`translate(${x},${y})`}>

                      {/* 😍 EMOJI */}
                      <text
                        x={0}
                        y={20}
                        textAnchor="middle"
                        fontSize="22"
                      >
                        {item.emoji}
                      </text>

                      {/* 🏷️ LABEL */}
                      <text
                        x={0}
                        y={46}
                        textAnchor="middle"
                        fontSize="12"
                        fill="#64748b"
                        fontWeight="600"
                      >
                        {item.need}
                      </text>

                    </g>
                  );
                }}
              />

              {/* 📈 Y AXIS */}
              <YAxis
                allowDecimals={false}
                tick={{ fill: "#64748b" }}
                axisLine={false}
                tickLine={false}
              />

              {/* 💬 TOOLTIP */}
              <Tooltip
                contentStyle={{
                  borderRadius: "14px",
                  border: "none",
                  boxShadow: "0 10px 30px rgba(0,0,0,0.1)"
                }}
              />

              {/* 📊 BAR */}
              <Bar
                dataKey="detected"
                radius={[12, 12, 0, 0]}
              >

                {chartData.map((entry, index) => (

                  <Cell
                    key={`cell-${index}`}
                    fill={
                      entry.detected
                        ? "#4ade80"
                        : "#e5e7eb"
                    }
                  />

                ))}

              </Bar>

            </BarChart>

          </ResponsiveContainer>

        </div>

      )}

    </div>
  );
}

export default HumanNeeds;