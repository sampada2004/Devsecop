# MongoDB CRUD Operations in RITBuddy

This document demonstrates how MongoDB CRUD (Create, Read, Update, Delete) operations are implemented in the RITBuddy project.

## Database Connection

The MongoDB connection is established in `TempBackend/Config/Database.js`:

```javascript
import mongoose from "mongoose";

const connectDB = async () => {
  try {
    const mongoURI = process.env.MONGO_URI || "mongodb://localhost:27017/RagQueries";
    console.log("MONGO_URI:", mongoURI);
    
    const conn = await mongoose.connect(mongoURI);
    console.log("MongoDB Connected");
    return conn;
  } catch (error) {
    console.error("MongoDB connection error:", error);
    process.exit(1);
  }
};

export default connectDB;
```

## Model Definition

The Query model is defined in `TempBackend/Models/Queries.js`:

```javascript
import mongoose from "mongoose";

const QuerySchema = new mongoose.Schema({
  query: {
    type: String,
    required: true
  },
  answer: {
    type: String,
    required: true
  },
  timestamp: {
    type: Date,
    default: Date.now
  }
});

// CRUD Operations
const Query = {
  // CREATE: Save a new query to the database
  saveQuery: async (queryData) => {
    const QueryModel = mongoose.model("Query", QuerySchema);
    const newQuery = new QueryModel(queryData);
    return await newQuery.save();
  },
  
  // READ: Get all history items
  getHistory: async () => {
    const QueryModel = mongoose.model("Query", QuerySchema);
    return await QueryModel.find().sort({ timestamp: -1 });
  },
  
  // DELETE: Delete a history item by ID
  deleteHistoryItem: async (id) => {
    const QueryModel = mongoose.model("Query", QuerySchema);
    return await QueryModel.deleteOne({ _id: id });
  }
};

export default Query;
```

## API Routes Using CRUD Operations

The API routes in `TempBackend/Routes/QueryRoute.js` utilize these CRUD operations:

```javascript
import Query from "../Models/Queries.js";
import express from "express";

const router = express.Router();

// CREATE - Save a new query and get response
router.post("/ask", async (req, res) => {
  try {
    const { query } = req.body;
    
    if (!query) {
      return res.status(400).json({ error: "Query is required" });
    }
    
    // Process the query and generate an answer
    const answer = "This is a sample answer to: " + query;
    
    // Save to database (CREATE operation)
    const savedQuery = await Query.saveQuery({ query, answer });
    
    res.status(200).json({ 
      message: answer,
      id: savedQuery._id
    });
  } catch (error) {
    console.error("Error processing query:", error);
    res.status(500).json({ error: "Server error" });
  }
});

// READ - Get all history items
router.get("/history", async (req, res) => {
  try {
    // Get all history items (READ operation)
    const history = await Query.getHistory();
    res.json(history);
  } catch (error) {
    console.error("Error fetching history:", error);
    res.status(500).json({ error: "Server error" });
  }
});

// DELETE - Delete a history item by ID
router.delete("/history/:id", async (req, res) => {
  try {
    const { id } = req.params;
    
    // Delete the history item (DELETE operation)
    const result = await Query.deleteHistoryItem(id);
    
    if (result.deletedCount === 0) {
      return res.status(404).json({ error: "History item not found" });
    }
    
    res.status(200).json({ message: "History item deleted successfully" });
  } catch (error) {
    console.error("Error deleting history item:", error);
    res.status(500).json({ error: "Server error" });
  }
});

export default router;
```

## Testing CRUD Operations

To demonstrate these operations to your teacher:

1. **Start the MongoDB server** (if not already running)
2. **Start the backend server**:
   ```bash
   npm start
   ```
3. **Use Postman or the browser to test the endpoints**:

   a. **CREATE**: Send a POST request to `http://localhost:5000/api/ask`
      - Body: `{ "query": "What is RIT?" }`
      - This will create a new entry in the database

   b. **READ**: Send a GET request to `http://localhost:5000/api/history`
      - This will return all history items

   c. **DELETE**: Send a DELETE request to `http://localhost:5000/api/history/:id`
      - Replace `:id` with an actual ID from the history
      - This will delete the specified history item

## Visual Demonstration

1. Show the MongoDB connection in the terminal when starting the server
2. Show the database contents before and after operations using MongoDB Compass
3. Show the API responses in Postman or browser developer tools

## Note on UPDATE Operation

While there's no explicit UPDATE endpoint in the current implementation, you could demonstrate how it would be implemented:

```javascript
// UPDATE: Update a history item
updateHistoryItem: async (id, updateData) => {
  const QueryModel = mongoose.model("Query", QuerySchema);
  return await QueryModel.findByIdAndUpdate(id, updateData, { new: true });
}

// Example route implementation
router.put("/history/:id", async (req, res) => {
  try {
    const { id } = req.params;
    const updateData = req.body;
    
    const updated = await Query.updateHistoryItem(id, updateData);
    
    if (!updated) {
      return res.status(404).json({ error: "History item not found" });
    }
    
    res.status(200).json(updated);
  } catch (error) {
    console.error("Error updating history item:", error);
    res.status(500).json({ error: "Server error" });
  }
});
```
