import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar/Navbar";

import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Report from "./pages/Report";

// ✅ New Analyse pages
import Disaster from "./pages/Analyse/Disaster";
import Priority from "./pages/Analyse/Priority";
import HumanNeeds from "./pages/Analyse/HumanNeeds";

function App() {
  return (
    <Router>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />

        {/* ❌ Removed this */}
        {/* <Route path="/analyse" element={<Analyse />} /> */}

        {/* ✅ Added these */}
        <Route path="/analyse/disaster" element={<Disaster />} />
        <Route path="/analyse/priority" element={<Priority />} />
        <Route path="/analyse/human-needs" element={<HumanNeeds />} />

        <Route path="/report" element={<Report />} />
      </Routes>
    </Router>
  );
}

export default App;