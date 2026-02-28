from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
def health_check():
    return {"message":"Hello from the user application"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)


