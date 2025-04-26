import uvicorn


if __name__ == "__main__":
    # Start the FastAPI server
    print("Starting server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=False)
