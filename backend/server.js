const dns = require("dns");

dns.setServers(["8.8.8.8", "1.1.1.1"]);

const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const path = require("path");

require("dotenv").config();

const app = express();

// ===============================
// MIDDLEWARE
// ===============================

app.use(cors());
app.use(express.json());

// ===============================
// SERVE FRONTEND
// ===============================

app.use(
    express.static(
        path.join(__dirname, "../frontend")
    )
);

app.get("/", (req, res) => {
    res.sendFile(
        path.join(
            __dirname,
            "../frontend/index.html"
        )
    );
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

// ===============================
// AI ROUTE
// ===============================

const aiRoutes = require("./aiRoutes");

// ===============================
// API ROUTES
// ===============================

app.use(
    "/api/disasters",
    disasterRoutes
);

app.use(
    "/api/zones",
    zoneRoutes
);

app.use(
    "/api/resources",
    resourceRoutes
);

app.use(
    "/api/alerts",
    alertRoutes
);

app.use(
    "/api/reports",
    reportRoutes
);

app.use(
    "/api/allocations",
    allocationRoutes
);

// ===============================
// AI API
// ===============================
//
// POST:
// /api/ai/analyze
//
// This sends the request to:
// backend/aiRoutes.js
//
// which then runs:
// ../ai/run_ai.py
// ===============================

app.use(
    "/api/ai",
    aiRoutes
);

// ===============================
// SERVER
// ===============================

const PORT = process.env.PORT || 5000;

mongoose
    .connect(process.env.MONGO_URI)
    .then(() => {

        console.log(
            "MongoDB connected successfully"
        );

        app.listen(
            PORT,
            () => {
                console.log(
                    `Server running on http://localhost:${PORT}`
                );

                console.log(
                    "AI API available at http://localhost:" +
                    `${PORT}/api/ai/analyze`
                );
            }
        );
    })
    .catch((error) => {

        console.log(
            "MongoDB connection error:",
            error
        );
    });