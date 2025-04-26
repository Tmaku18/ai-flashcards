# Deploying the Flashcard App to Fly.io

This guide explains how to deploy the Flashcard App to Fly.io with serverless-like behavior (scale to zero).

## Prerequisites

1. A Fly.io account (sign up at https://fly.io)
2. Fly CLI installed (https://fly.io/docs/hands-on/install-flyctl/)
3. Docker installed locally

## Deployment Steps

### 1. Prepare for Deployment

Make sure your code is committed and you're ready to deploy.

### 2. Run the Deployment Script

```bash
chmod +x deploy.sh
./deploy.sh
```

This script will:

- Install the Fly CLI if needed
- Prompt you for a unique app name (or generate one)
- Create a new Fly.io app with your chosen name
- Create a persistent volume for your database
- Set up necessary secrets (API keys)
- Deploy your application

### 3. Access Your Application

Once deployed, your application will be available at:

```
https://your-app-name.fly.dev
```

Where `your-app-name` is the name you chose during deployment.

## Understanding Serverless Behavior

Your application is configured with "scale to zero" capabilities:

- **Auto Start**: When a request comes in, Fly.io will automatically start your application
- **Auto Stop**: After a period of inactivity (about 60 minutes), your application will shut down
- **Persistent Data**: Your database is stored on a persistent volume, so data remains even when the app stops

This means you only pay for the time your application is actually running, similar to serverless functions.

## Common Commands

```bash
# View logs
fly logs

# SSH into your application
fly ssh console

# Open your application in a browser
fly open

# Scale your application manually
fly scale count 1  # Start the application
fly scale count 0  # Stop the application

# Check application status
fly status
```

## Troubleshooting

If you encounter issues:

1. Check the logs: `fly logs`
2. Ensure your volume is mounted correctly: `fly volumes list`
3. Verify your secrets are set: `fly secrets list`

For more help, visit the Fly.io documentation: https://fly.io/docs/
