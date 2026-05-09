import React, { useState } from "react";
import BackButton from "../../components/BackButton/BackButton";
import "./Priority.css";

const BASE_URL = "http://127.0.0.1:5000";

function Priority() {

  const [tweets, setTweets] = useState("");
  const [city, setCity] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {

    const tweetList = tweets.split("\n");

    try {

      const response = await fetch(
        "http://localhost:5001/analyze",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            tweets: tweetList,
            city: city,
          }),
        }
      );

      const data = await response.json();

      setResult(data);

    } catch (error) {

      console.error("Error:", error);

    }
  };

  return (

    <div className="priority-container">

      {/* 🔥 HEADER */}
      <div className="priority-header">

        <BackButton />

        <h1 className="priority-title">
          🚨 Priority Analysis
        </h1>

        <div className="priority-header-space"></div>

      </div>

      {/* INPUT */}
      <div className="priority-card">

        <textarea
          rows="5"
          value={tweets}
          onChange={(e) => setTweets(e.target.value)}
          placeholder="Enter tweets (one per line)"
          className="priority-textarea"
        />

        <input
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Enter City"
          className="priority-input"
        />

        <button
          onClick={handleSubmit}
          className="priority-button"
        >
          Analyze Priority
        </button>

      </div>

      {/* RESULT */}
      {result && (

        <div className="priority-result-card">

          <h2>
            🔮 Analysis Result
          </h2>

          <p>
            <b>Total Tweets:</b> {result.total}
          </p>

          <p>
            <b>Disaster Tweets:</b> {result.disaster_count}
          </p>

          <p>

            <b>Priority Level:</b>{" "}

            <span
              style={{
                color:
                  result.priority === "HIGH"
                    ? "#ef4444"
                    : result.priority === "MEDIUM"
                    ? "#f59e0b"
                    : "#22c55e",

                fontWeight: "bold",
              }}
            >
              {result.priority}
            </span>

          </p>

          <p>
            <b>Weather:</b> {result.weather}
          </p>

          <h3>
            ⚡ Suggested Actions:
          </h3>

          <ul>

            {result.actions?.map((a, i) => (

              <li key={i}>
                {a}
              </li>

            ))}

          </ul>

        </div>

      )}

      {/* MAP */}
      {city && (

        <div className="priority-map">

          <h2>
            📍 Location
          </h2>

          <iframe
            title="map"
            width="100%"
            height="300"
            src={`https://www.google.com/maps?q=${city}&output=embed`}
            className="priority-iframe"
          ></iframe>

        </div>

      )}

    </div>
  );
}

export default Priority;