const mongoose = require("mongoose");

const allocationSchema = new mongoose.Schema(
    {
        resourceId: {
            type: String,
            required: true
        },

        zoneId: {
            type: String,
            required: true
        },

        resourceType: {
            type: String,
            required: true
        },

        quantity: {
            type: Number,
            required: true,
            min: 0
        },

        unit: {
            type: String,
            required: true
        },

        reason: {
            type: String,
            default: ""
        },

        urgency: {
            type: String,
            enum: ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
            default: "MEDIUM"
        },

        status: {
            type: String,
            enum: ["PENDING", "APPROVED", "COMPLETED"],
            default: "PENDING"
        }
    },
    {
        timestamps: true
    }
);

module.exports = mongoose.model("Allocation", allocationSchema);