from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head><title>Memory Game</title></head>
        <body>
            <h1>Welcome to the Memory Game</h1>
        </body>
    </html>
    """