import { useState } from "react";
import axios from "axios";
import BackButton from "../BackButton/BackButton";
import "../../pages/Report.css";
export default function ReportForm({ onSuccess }) {
  const [form, setForm] = useState({
    date: "",
    time: "",
    lat: "",
    lng: "",
    type: "flood",
    location: "",
    description: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await axios.post("http://localhost:5000/reports", {
        ...form,
        lat: Number(form.lat),
        lng: Number(form.lng),
      });

      alert("✅ Report saved to database!");

      setForm({
        date: "",
        time: "",
        lat: "",
        lng: "",
        type: "flood",
        location: "",
        description: "",
      });

      if (onSuccess) onSuccess();
    } catch (err) {
      console.error(err);
      alert("❌ Error saving report");
    }
  };

  return (
    <div className="form-container">
      <div className="form-header">
    <BackButton />
    <h2>Report an Incident</h2>
  </div>

      <form onSubmit={handleSubmit}>
        {/* ROW 1 */}
        <div className="row">
          <div className="field">
            <label>Date</label>
            <input type="date" name="date" value={form.date} onChange={handleChange} />
          </div>

          <div className="field">
            <label>Time</label>
            <input type="time" name="time" value={form.time} onChange={handleChange} />
          </div>

          <div className="field">
            <label>Disaster Type</label>

            {/* 🔥 UPDATED DROPDOWN */}
            <select name="type" value={form.type} onChange={handleChange}>
              <option value="flood">Flood</option>
              <option value="fire">Fire</option>
              <option value="earthquake">Earthquake</option>
              <option value="cyclone">Cyclone</option>

              {/* NEW ADDED */}
              <option value="storm">Storm</option>
              <option value="landslide">Landslide</option>
            </select>
          </div>
        </div>

        {/* ROW 2 */}
        <div className="row">
          <div className="field">
            <label>Latitude</label>
            <input type="number" name="lat" value={form.lat} onChange={handleChange} required />
          </div>

          <div className="field">
            <label>Longitude</label>
            <input type="number" name="lng" value={form.lng} onChange={handleChange} required />
          </div>

          <div className="field">
            <label>Location</label>
            <input type="text" name="location" value={form.location} onChange={handleChange} />
          </div>
        </div>

        <div className="field">
          <label>Description</label>
          <textarea name="description" value={form.description} onChange={handleChange} />
        </div>

        <button type="submit" className="submit-btn">
          Submit Report
        </button>
      </form>
    </div>
  );
}