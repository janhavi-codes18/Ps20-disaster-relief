const express = require("express");
const Alert = require("../models/Alert");

const router = express.Router();

// Create an alert
router.post("/", async (req, res) => {
    try {
        const alert = await Alert.create(req.body);

        res.status(201).json({
            success: true,
            message: "Alert created successfully",
            alert: alert
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to create alert",
            error: error.message
        });
    }
});

// Get all alerts
router.get("/", async (req, res) => {
    try {
        const alerts = await Alert.find().sort({ createdAt: -1 });

        res.json({
            success: true,
            alerts: alerts
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to fetch alerts",
            error: error.message
        });
    }
});

module.exports = router;