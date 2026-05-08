import React from "react";
import "./Hero.css";
import ai from "../../assests/ai.png";

function Hero() {
  return (
    <section className="hero-box">

      {/* LEFT CONTENT */}
      <div className="hero-left">


        <h1>
          AI Powered <br />
          <span>Disaster Management System</span>
        </h1>

        <p className="hero-desc">
          Detect disasters, analyze real-time reports,
          predict human needs and prioritize emergency
          response using Artificial Intelligence.
        </p>

        <div className="hero-buttons">
          <button className="primary-btn">
            Get Started
          </button>

          <button className="secondary-btn">
            Learn More
          </button>
        </div>

      </div>

      {/* RIGHT IMAGE */}
      <div className="hero-right">

        {/* Glow */}
        <div className="image-glow"></div>

        {/* AI IMAGE */}
        <img src={ai} alt="AI" className="ai" />

      </div>

    </section>
  );
}

export default Hero;