from fastapi import FastAPI



app = FastAPI()

@app.get('/story')
async def create_story():
    return 