from starlette.applications import Starlette
from starlette.responses import JSONResponse
app = Starlette()

@app.route('/')
async def homepage(_):
    return JSONResponse({'hello': 'world'})
