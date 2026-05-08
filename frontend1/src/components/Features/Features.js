import React from "react";
import "./Features.css";
import { useNavigate } from "react-router-dom";

// 🔥 Icons
import { MapPin, Gauge, HandHelping } from "lucide-react";

function Features() {
  const navigate = useNavigate();

  return (
    <div className="features">

      {/* Card 1 */}
      <div 
        className="card"
        onClick={() => navigate("/analyse/disaster")}
      >
        <div className="icon">
          <MapPin size={40} />
        </div>
        <h3>Disaster with Location</h3>
        <p>
          Detect disaster type and extract accurate location from tweets 
          using NLP techniques.
        </p>
      </div>

      {/* Card 2 */}
      <div 
        className="card"
        onClick={() => navigate("/analyse/priority")}
      >
        <div className="icon">
          <Gauge size={40} />
        </div>
        <h3>Priority Scoring</h3>
        <p>
          Assign priority levels to disaster reports for faster response.
        </p>
      </div>

      {/* Card 3 */}
      <div 
        className="card"
        onClick={() => navigate("/analyse/human-needs")}
      >
        <div className="icon">
          <HandHelping size={40} />
        </div>
        <h3>Predict Human Needs</h3>
        <p>
          Analyze text to detect needs like food, shelter, and medical help.
        </p>
      </div>

    </div>
  );
}

export default Features;