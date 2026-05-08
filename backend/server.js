const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
require("dotenv").config();

// 🔹 Routes import
const reportRoutes = require("./routes/reportRoutes");
const historicalRoutes = require("./routes/historicalRoutes");
const humanNeedRoutes = require("./routes/humanNeedRoutes");
const disasterRoutes = require("./routes/disasterRoutes");
// 🔥 NEW ML2 route
const priorityRoutes = require("./routes/priorityRoutes");
const dashboardRoutes = require("./routes/dashboardRoutes");
const app = express();

// 🔹 Middleware
app.use(cors());
app.use(express.json());

// 🔹 Routes use
app.use("/reports", reportRoutes);
app.use("/historical", historicalRoutes);
app.use("/api/human-need", humanNeedRoutes);
app.use("/api/disaster", disasterRoutes);
// 🔥 NEW ML2 API
app.use("/api/priority", priorityRoutes);
app.use("/api/dashboard", dashboardRoutes);

// 🔹 MongoDB connect
mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log("✅ MongoDB connected"))
  .catch(err => console.log("❌ DB Error:", err));

// 🔹 Test route
app.get("/", (req, res) => {
  res.send("🚀 Backend is running");
});

// 🔹 Server start
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🔥 Server running on ${PORT}`));