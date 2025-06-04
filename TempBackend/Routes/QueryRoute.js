import Query from "../Models/Queries.js";
import express from "express";
import fetch from "node-fetch";
import mongoose from "mongoose";

const router = express.Router();

// CREATE - Save a new query and get response
router.post("/ask", async (req, res) => {
  try {
    // Accept both query and question parameters for backward compatibility
    const queryText = req.body.query || req.body.question;
    
    if (!queryText) {
      return res.status(400).json({ error: "Query is required" });
    }
    
    // Check if we have a cached response
    const cachedQA = await Query.findOne({ question: queryText });

    if (cachedQA) {
      return res.json({ answer: cachedQA.answer, cached: true });
    }
    
    // Forward the query to the Python API
    const response = await fetch("http://127.0.0.1:5001/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: queryText }),
    });

    const data = await response.json();

    if (data.answer) {
      // Save to database (CREATE operation)
      const savedQuery = await Query.create({ 
        question: queryText, 
        answer: data.answer 
      });
      
      return res.status(200).json({ 
        answer: data.answer,
        id: savedQuery._id
      });
    }
    
    res.status(500).json({ error: "Failed to get an answer" });
  } catch (error) {
    console.error("Error processing query:", error);
    res.status(500).json({ error: "Server error" });
  }
});

// READ - Get all history items
router.get("/history", async (req, res) => {
  try {
    // Get all history items (READ operation)
    const history = await Query.find().sort({ timestamp: -1 });
    res.json(history);
  } catch (error) {
    console.error("Error fetching history:", error);
    res.status(500).json({ error: "Server error" });
  }
});

// READ - Get a specific history item by ID
router.get("/history/:id", async (req, res) => {
  try {
    const { id } = req.params;
    
    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({ error: "Invalid ID format" });
    }
    
    const historyItem = await Query.findById(id);
    
    if (!historyItem) {
      return res.status(404).json({ error: "History item not found" });
    }
    
    res.json(historyItem);
  } catch (error) {
    console.error("Error fetching history item:", error);
    res.status(500).json({ error: "Server error" });
  }
});

// UPDATE - Update a history item
router.put("/history/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const { question, answer } = req.body;
    
    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({ error: "Invalid ID format" });
    }
    
    if (!question && !answer) {
      return res.status(400).json({ error: "Nothing to update" });
    }
    
    const updateData = {};
    if (question) updateData.question = question;
    if (answer) updateData.answer = answer;
    
    const updated = await Query.findByIdAndUpdate(
      id, 
      updateData, 
      { new: true }
    );
    
    if (!updated) {
      return res.status(404).json({ error: "History item not found" });
    }
    
    res.status(200).json(updated);
  } catch (error) {
    console.error("Error updating history item:", error);
    res.status(500).json({ error: "Server error" });
  }
});

// DELETE - Delete a history item by ID
router.delete("/history/:id", async (req, res) => {
  try {
    const { id } = req.params;
    
    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({ error: "Invalid ID format" });
    }
    
    const result = await Query.findByIdAndDelete(id);
    
    if (!result) {
      return res.status(404).json({ error: "History item not found" });
    }
    
    res.status(200).json({ message: "History item deleted successfully" });
  } catch (error) {
    console.error("Error deleting history item:", error);
    res.status(500).json({ error: "Server error" });
  }
});

export default router;
