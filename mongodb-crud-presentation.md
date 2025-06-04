# MongoDB CRUD Operations Demo

## Live Demonstration Steps

### 1. Start the MongoDB and Backend Servers

```bash
# Start MongoDB (if not already running)
# Start the backend server
npm start
```

Show the terminal output with "MongoDB Connected" message.

### 2. Use Postman or Browser to Demonstrate CRUD Operations

#### CREATE Operation
1. Open Postman or use browser developer tools
2. Send a POST request to `http://localhost:5000/api/ask`
   - Set Content-Type: application/json
   - Body: `{ "query": "What is RIT?" }`
3. Show the response with the created item ID
4. Explain how this uses the `saveQuery` function in the Queries model

#### READ Operation
1. Send a GET request to `http://localhost:5000/api/history`
2. Show the response with all history items, including the one just created
3. Explain how this uses the `getHistory` function in the Queries model

#### DELETE Operation
1. Copy an ID from the history response
2. Send a DELETE request to `http://localhost:5000/api/history/{id}`
   - Replace {id} with the actual ID
3. Show the success response
4. Send another GET request to confirm the item was deleted
5. Explain how this uses the `deleteHistoryItem` function in the Queries model

### 3. Show the MongoDB Database Directly (Optional)

1. Open MongoDB Compass
2. Connect to `mongodb://localhost:27017`
3. Navigate to the RagQueries database
4. Show the Query collection with the stored items
5. Perform operations and refresh to show changes in real-time

### 4. Code Walkthrough

1. Show the Database Connection in `TempBackend/Config/Database.js`
2. Show the Query Model in `TempBackend/Models/Queries.js`
   - Highlight the CRUD operation functions
3. Show the API Routes in `TempBackend/Routes/QueryRoute.js`
   - Explain how each route uses the model functions

### 5. Explain Testing Approach

1. Show the test file in `TempBackend/__tests__/api.test.js`
2. Explain how the tests verify the API endpoints
3. Run the tests with `npm run test:coverage`
4. Show the coverage report for the backend

## Key Points to Emphasize

1. **Complete CRUD Implementation**:
   - CREATE: `saveQuery` function and POST `/api/ask` endpoint
   - READ: `getHistory` function and GET `/api/history` endpoint
   - DELETE: `deleteHistoryItem` function and DELETE `/api/history/:id` endpoint
   - (Mention that UPDATE could be implemented similarly)

2. **MongoDB Integration**:
   - Proper connection setup with error handling
   - Mongoose Schema definition
   - Model methods for database operations

3. **API Design**:
   - RESTful endpoints
   - Proper error handling
   - Status codes and JSON responses

4. **Testing Coverage**:
   - Tests for all API endpoints
   - Coverage reporting for backend code
