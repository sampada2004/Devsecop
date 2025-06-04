# Deploying RITBuddy Frontend to Netlify

This guide will help you deploy the RITBuddy frontend to Netlify.

## Prerequisites

- A Netlify account
- Git repository with your RITBuddy project

## Deployment Steps

### Option 1: Deploy via Netlify UI

1. Log in to your Netlify account
2. Click "Add new site" > "Import an existing project"
3. Connect to your Git provider and select your repository
4. Configure the deployment settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Base directory: (leave empty or specify `Frontend` if deploying from the root of your repository)
5. Click "Deploy site"

### Option 2: Deploy via Netlify CLI

1. Install Netlify CLI globally:
   ```
   npm install -g netlify-cli
   ```

2. Login to Netlify:
   ```
   netlify login
   ```

3. Navigate to your Frontend directory:
   ```
   cd path/to/RITBuddy/Frontend
   ```

4. Initialize Netlify site:
   ```
   netlify init
   ```

5. Follow the prompts to create a new site or connect to an existing one

6. Deploy your site:
   ```
   netlify deploy --prod
   ```

## Environment Variables

Your frontend has been configured to use environment variables for API endpoints. You'll need to set these in Netlify:

1. Go to your site's dashboard in Netlify
2. Navigate to Site settings > Build & deploy > Environment
3. Add the following environment variable:
   - Key: `VITE_API_URL`
   - Value: Your backend API URL (e.g., `https://your-backend-url.com`)

## Handling Backend API

Since your frontend makes API calls to a backend server, you have two options:

1. **Deploy your backend separately** and update the `VITE_API_URL` environment variable to point to your deployed backend URL.

2. **Use Netlify Functions** to create serverless functions that can handle your API requests. This would require refactoring your backend code.

## Troubleshooting

- If you see 404 errors on page refresh, the `netlify.toml` file has been configured with redirects to handle this.
- If your API calls are failing, check that your environment variables are set correctly.
- For more help, refer to the [Netlify documentation](https://docs.netlify.com/).
