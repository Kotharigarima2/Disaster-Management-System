import React, { useState } from "react";
import "./Navbar.css";
import logo from "../../assests/logo.png";
import { NavLink } from "react-router-dom";

import {
  Home as HomeIcon,
  LayoutDashboard,
  BarChart3,
  FileText,
  ChevronRight,
} from "lucide-react";

function Navbar() {
  const [showDropdown, setShowDropdown] = useState(false);

  return (
    <nav className="navbar">

      {/* LEFT */}
      <div className="nav-left">
        <img src={logo} alt="logo" className="logo" />

        <div className="logo-text">
          <h2>Disaster AI</h2>
          
        </div>
      </div>

      {/* RIGHT */}
      <div className="nav-right">

        {/* HOME */}
        <NavLink
          to="/"
          className={({ isActive }) =>
            isActive ? "nav-box active" : "nav-box"
          }
        >
          <HomeIcon size={18} />
          <span>Home</span>
        </NavLink>

        {/* DASHBOARD */}
        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            isActive ? "nav-box active" : "nav-box"
          }
        >
          <LayoutDashboard size={18} />
          <span>Dashboard</span>
        </NavLink>

        {/* ANALYSE */}
        <div
          className="nav-box analyse-box"
          onClick={() => setShowDropdown(!showDropdown)}
        >
          <div className="analyse-content">
            <BarChart3 size={18} />
            <span>Analyse</span>
          </div>

          <ChevronRight
            size={18}
            className={`arrow ${showDropdown ? "open" : ""}`}
          />

          {/* DROPDOWN */}
          <div className={`dropdown ${showDropdown ? "show" : ""}`}>

            <NavLink
              to="/analyse/disaster"
              className="dropdown-item"
              onClick={() => setShowDropdown(false)}
            >
              Disaster with Location
            </NavLink>

            <NavLink
              to="/analyse/priority"
              className="dropdown-item"
              onClick={() => setShowDropdown(false)}
            >
              Priority Scoring
            </NavLink>

            <NavLink
              to="/analyse/human-needs"
              className="dropdown-item"
              onClick={() => setShowDropdown(false)}
            >
              Predict Human Needs
            </NavLink>

          </div>
        </div>

        {/* REPORT */}
        <NavLink
          to="/report"
          className={({ isActive }) =>
            isActive ? "nav-box active" : "nav-box"
          }
        >
          <FileText size={18} />
          <span>Report</span>
        </NavLink>

      </div>
    </nav>
  );
}

export default Navbar;