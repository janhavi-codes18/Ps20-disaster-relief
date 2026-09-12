const express = require("express");
const Zone = require("../models/Zone");

const router = express.Router();

// Create a new zone
router.post("/", async (req, res) => {
    try {
        const zone = await Zone.create(req.body);

        res.status(201).json({
            success: true,
            message: "Zone created successfully",
            zone: zone
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to create zone",
            error: error.message
        });
    }
});

// Get all zones
router.get("/", async (req, res) => {
    try {
        const zones = await Zone.find().sort({ createdAt: -1 });

        res.json({
            success: true,
            zones: zones
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to fetch zones",
            error: error.message
        });
    }
});

// Get one zone
router.get("/:id", async (req, res) => {
    try {
        const zone = await Zone.findById(req.params.id);

        if (!zone) {
            return res.status(404).json({
                success: false,
                message: "Zone not found"
            });
        }

        res.json({
            success: true,
            zone: zone
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to fetch zone",
            error: error.message
        });
    }
});

module.exports = router;