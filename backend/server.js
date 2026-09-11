const dns = require("dns");

dns.setServers(["8.8.8.8", "1.1.1.1"]);

const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const path = require("path");

require("dotenv").config();

const app = express();

app.use(cors());
app.use(express.json());

// ===============================
// SERVE FRONTEND
// ===============================

app.use(express.static(path.join(__dirname, "../frontend")));

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "../frontend/index.html"));
});

// ===============================
// ROUTES
// ===============================

const disasterRoutes = require("./routes/disasterRoutes");
const zoneRoutes = require("./routes/zoneRoutes");
const resourceRoutes = require("./routes/resourceRoutes");
const alertRoutes = require("./routes/alertRoutes");
const reportRoutes = require("./routes/reportRoutes");
const allocationRoutes = require("./routes/allocationRoutes");

// AI route temporarily removed
// const aiRoutes = require("./routes/aiRoutes");

app.use("/api/disasters", disasterRoutes);
app.use("/api/zones", zoneRoutes);
app.use("/api/resources", resourceRoutes);
app.use("/api/alerts", alertRoutes);
app.use("/api/reports", reportRoutes);
app.use("/api/allocations", allocationRoutes);

// AI route temporarily disabled
// app.use("/api/ai", aiRoutes);

// ===============================
// SERVER
// ===============================

const PORT = process.env.PORT || 5000;

mongoose
    .connect(process.env.MONGO_URI)
    .then(() => {
        console.log("MongoDB connected successfully");

        app.listen(PORT, () => {
            console.log(`Server running on http://localhost:${PORT}`);
        });
    })
    .catch((error) => {
        console.log("MongoDB connection error:", error);
    });