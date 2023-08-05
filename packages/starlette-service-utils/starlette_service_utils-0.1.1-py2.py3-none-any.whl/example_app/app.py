from starlette.applications import Starlette
from starlette.responses import JSONResponse

from starlette_service_utils.common import sentry_integration

app = Starlette()

sentry_integration(app)

@app.route('/')
async def homepage(_):
    return JSONResponse({'hello': 'world'})
