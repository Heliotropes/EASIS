import fastapi as _fastapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.llm_api import chatting

app = _fastapi.FastAPI(debug=True)

templates = Jinja2Templates("templates")

@app.get("/", response_class=HTMLResponse)
def index(request: _fastapi.Request):
    return templates.TemplateResponse(
        request=request, name="gpt_chat.html"
    )

@app.get("/gpt/chatting/{message}")
def gpt_chat(message: str):
    response = chatting(message)
    return(response)

