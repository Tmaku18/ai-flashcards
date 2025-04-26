"""
Module to serve the Next.js frontend from FastAPI
"""

import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import subprocess
import sys


def setup_frontend_serving(app: FastAPI):
    """
    Configure FastAPI to serve the Next.js frontend
    """
    frontend_dir = os.path.join(os.getcwd(), "frontend")

    # Check if we're running in production (deployed) or development
    is_production = not os.path.exists(os.path.join(frontend_dir, "src"))

    if is_production:
        # In production, serve the built Next.js app
        print("Setting up production frontend serving")

        # Serve static files from .next/static
        app.mount(
            "/_next/static",
            StaticFiles(directory=os.path.join(frontend_dir, ".next", "static")),
            name="next-static",
        )

        # Serve files from the public directory
        app.mount(
            "/",
            StaticFiles(directory=os.path.join(frontend_dir, "public")),
            name="public",
        )

        # Serve the Next.js app for all other routes
        @app.get("/{full_path:path}", response_class=HTMLResponse)
        async def serve_frontend(request: Request, full_path: str):
            # API routes are handled by FastAPI
            if full_path.startswith("api/"):
                return {"message": "API endpoint not found"}

            # Special case for favicon.ico
            if full_path == "favicon.ico":
                favicon_path = os.path.join(frontend_dir, "public", "favicon.ico")
                if os.path.exists(favicon_path):
                    return FileResponse(favicon_path)

            # Serve the Next.js app
            index_path = os.path.join(frontend_dir, "server.js")
            if os.path.exists(index_path):
                # Execute the Next.js server
                try:
                    # Change to the frontend directory
                    os.chdir(frontend_dir)

                    # Start the Next.js server
                    process = subprocess.Popen(
                        ["node", "server.js"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )

                    # Return to the original directory
                    os.chdir(os.path.dirname(os.path.dirname(frontend_dir)))

                    # Wait for the server to start
                    stdout, stderr = process.communicate(timeout=5)

                    # Check if the server started successfully
                    if process.returncode != 0:
                        print(f"Error starting Next.js server: {stderr.decode()}")
                        return {"message": "Error serving frontend"}

                    # Return the HTML from the Next.js server
                    return HTMLResponse(content=stdout.decode())
                except Exception as e:
                    print(f"Error serving Next.js app: {e}")
                    return {"message": "Error serving frontend"}

            # Fallback to the redirect.html file
            redirect_path = os.path.join(os.getcwd(), "redirect.html")
            if os.path.exists(redirect_path):
                return FileResponse(redirect_path)

            # Final fallback
            return {"message": "Frontend not found"}

    else:
        # In development, redirect to the Next.js dev server
        print("Setting up development frontend serving")

        @app.get("/{full_path:path}")
        async def redirect_to_frontend(request: Request, full_path: str):
            # API routes are handled by FastAPI
            if full_path.startswith("api/"):
                return {"message": "API endpoint not found"}

            # Redirect to the Next.js dev server
            return {
                "message": "In development mode, please access the frontend at http://localhost:3000"
            }
