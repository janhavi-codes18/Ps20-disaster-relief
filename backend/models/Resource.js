const mongoose = require("mongoose");

const resourceSchema = new mongoose.Schema(
    {
        resourceId: {
            type: String,
            required: true,
            unique: true
        },

        resourceType: {
            type: String,
            required: true,
            enum: ["food", "water", "medicine", "shelter"]
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

        location: {
            type: String,
            required: true
        },

        available: {
            type: Number,
            required: true,
            min: 0
        }
    },
    {
        timestamps: true
    }
);

module.exports = mongoose.model("Resource", resourceSchema);