const mongoose = require("mongoose");

const disasterSchema = new mongoose.Schema(
    {
        disasterType: {
            type: String,
            required: true
        },

        severity: {
            type: Number,
            required: true,
            min: 1,
            max: 5
        },

        location: {
            type: String,
            required: true
        },

        affectedPeople: {
            type: Number,
            required: true,
            min: 0
        },

        description: {
            type: String,
            default: ""
        },

        status: {
            type: String,
            default: "ACTIVE"
        }
    },
    {
        timestamps: true
    }
);

module.exports = mongoose.model("Disaster", disasterSchema);