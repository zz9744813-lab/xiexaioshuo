from fastapi import FastAPI

app = FastAPI(title="AI Novel System", description="Backend for AI Novel Generation System")

@app.get("/")
async def root():
    return {"message": "Welcome to AI Novel System API"}
