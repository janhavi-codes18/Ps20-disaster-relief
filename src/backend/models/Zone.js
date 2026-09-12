const mongoose = require("mongoose");

const zoneSchema = new mongoose.Schema(
    {
        zoneId: {
            type: String,
            required: true,
            unique: true
        },

        name: {
            type: String,
            required: true
        },

        location: {
            type: String,
            required: true
        },

        severity: {
            type: Number,
            required: true,
            min: 1,
            max: 5
        },

        affectedPeople: {
            type: Number,
            required: true,
            min: 0
        },

        needs: {
            food: {
                type: Number,
                default: 0
            },

            water: {
                type: Number,
                default: 0
            },

            medicine: {
                type: Number,
                default: 0
            },

            shelter: {
                type: Number,
                default: 0
            }
        }
    },
    {
        timestamps: true
    }
);

module.exports = mongoose.model("Zone", zoneSchema);