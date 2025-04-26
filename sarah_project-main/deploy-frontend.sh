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
echo "Do you want to use an existing app for the frontend? (y/n)"
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
    echo "Creating Fly.io app for the frontend..."
    echo "Enter a unique app name (e.g., your-name-flashcards-frontend):"
    read app_name
    
    if [ -z "$app_name" ]; then
        app_name="sarah-flashcards-frontend-$(date +%s | cut -c 8-10)"
        echo "Using auto-generated name: $app_name"
    fi
    
    # Create the app
    fly apps create $app_name || true
fi

# Update fly.toml with the app name
cp fly.frontend.toml fly.toml
sed -i.bak "s/app = \"sarah-gsu-flashcardai-frontend\"/app = \"$app_name\"/g" fly.toml

# Deploy the app
echo "Deploying the frontend application..."
echo "Note: If you see TypeScript errors during deployment, don't worry - the build will continue anyway."
fly deploy --app $app_name --config fly.toml

echo ""
echo "Deployment complete!"
echo "Your frontend will be available at: https://$app_name.fly.dev"
echo ""
echo "Important notes:"
echo "- The app will automatically start when a request comes in"
echo "- It will automatically stop after 60 minutes of inactivity"
echo ""
echo "To view logs: fly logs --app $app_name"
echo "To open the app: fly open --app $app_name"

# Clean up
rm fly.toml.bak
mv fly.toml fly.frontend.toml
