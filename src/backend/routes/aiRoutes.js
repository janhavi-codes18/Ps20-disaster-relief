const express = require("express");
const { spawn } = require("child_process");
const path = require("path");

const router = express.Router();

router.post("/run", (req, res) => {
    const inputData = JSON.stringify(req.body);

    const aiPath = path.join(__dirname, "../../ai/run_ai.py");

    const python = spawn("py", [aiPath]);

    let output = "";
    let errorOutput = "";

    python.stdout.on("data", (data) => {
        output += data.toString();
    });

    python.stderr.on("data", (data) => {
        errorOutput += data.toString();
    });

    python.on("close", (code) => {
        if (code !== 0) {
            console.error("AI Error:", errorOutput);

            return res.status(500).json({
                success: false,
                message: "AI execution failed",
                error: errorOutput
            });
        }

        try {
            const aiResult = JSON.parse(output);

            res.json({
                success: true,
                result: aiResult
            });

        } catch (error) {
            console.error("Invalid AI JSON:", output);

            res.status(500).json({
                success: false,
                message: "AI returned invalid JSON",
                raw_output: output
            });
        }
    });
});

module.exports = router;