const express = require("express");
const Allocation = require("../models/Allocation");

const router = express.Router();

// Create an allocation
router.post("/", async (req, res) => {
    try {
        const allocation = await Allocation.create(req.body);

        res.status(201).json({
            success: true,
            message: "Allocation created successfully",
            allocation: allocation
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to create allocation",
            error: error.message
        });
    }
});

// Get all allocations
router.get("/", async (req, res) => {
    try {
        const allocations = await Allocation
            .find()
            .sort({ createdAt: -1 });

        res.json({
            success: true,
            allocations: allocations
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: "Failed to fetch allocations",
            error: error.message
        });
    }
});

module.exports = router;