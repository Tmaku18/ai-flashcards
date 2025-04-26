#!/bin/bash

# Install Fly CLI if not already installed
if ! command -v flyctl &> /dev/null; then
    echo "Installing Fly CLI..."
    curl -L https://fly.io/install.sh | sh
fi

# Ensure we're logged in
echo "Please make sure you're logged into Fly.io"
echo "If not, run: fly auth login"
echo ""

# Get existing app or create a new one
echo "Checking for existing Fly.io apps..."
echo "Do you want to use an existing app? (y/n)"
read use_existing

if [[ "$use_existing" == "y" || "$use_existing" == "Y" ]]; then
    # List existing apps
    echo "Here are your existing apps:"
    fly apps list

    echo "Enter the name of the app you want to use:"
    read app_name

    if [ -z "$app_name" ]; then
        echo "No app name provided. Exiting."
        exit 1
    fi

    # Check if the app exists
    if ! fly apps list | grep -q "$app_name"; then
        echo "App '$app_name' not found. Please check the name and try again."
        exit 1
    fi
else
    # Create a new app
    echo "Creating Fly.io app with a unique name..."
    echo "Enter a unique app name (e.g., your-name-flashcards):"
    read app_name

    if [ -z "$app_name" ]; then
        app_name="sarah-flashcards-$(date +%s | cut -c 8-10)"
        echo "Using auto-generated name: $app_name"
    fi

    # Create the app
    fly apps create $app_name || true
fi

# Update fly.toml with the app name
sed -i.bak "s/app = \"flashcard-app\"/app = \"$app_name\"/g" fly.toml

# Create a volume for persistent data
echo "Creating volume for database (if it doesn't exist)..."
fly volumes create flashcard_data --size 1 --region sjc --app $app_name || true

# Set secrets
echo "Setting up secrets..."
echo "Enter your OpenAI API key (press enter to skip):"
read openai_key
if [ ! -z "$openai_key" ]; then
    fly secrets set OPENAI_API_KEY="$openai_key" --app $app_name
fi

echo "Enter your Gemini API key (press enter to skip):"
read gemini_key
if [ ! -z "$gemini_key" ]; then
    fly secrets set GEMINI_API_KEY="$gemini_key" --app $app_name
fi

# Generate a random secret key
secret_key=$(openssl rand -hex 32)
fly secrets set SECRET_KEY="$secret_key" --app $app_name

# Deploy the app
echo "Deploying the application..."
echo "Note: If you see TypeScript errors during deployment, don't worry - the build will continue anyway."
fly deploy --app $app_name

echo ""
echo "Deployment complete!"
echo "Your application will be available at:"
echo "- Main Application: https://$app_name.fly.dev"
echo "- API Documentation: https://$app_name.fly.dev/api/docs"
echo ""
echo "Important notes:"
echo "- The app will automatically start when a request comes in"
echo "- It will automatically stop after 60 minutes of inactivity"
echo "- Your database is stored on a persistent volume"
echo ""
echo "To view logs: fly logs"
echo "To open the app: fly open"
