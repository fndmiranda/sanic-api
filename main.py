import asyncio
import uvloop
import aiotask_context as context
from sanic import Sanic
from sanic.response import json
from core import settings
from user.views import UserListView, UserDetailView

app = Sanic(__name__)


@app.middleware('request')
async def add_key(request):
    context.set('request', request)


@app.listener('after_server_start')
async def after_server_start(app, loop):
    if not settings.ASYNC:
        loop.set_task_factory(context.task_factory)


app.add_route(UserListView.as_view(), '/user/users')
app.add_route(UserDetailView.as_view(), '/user/users/<user_id>')


@app.route("/")
async def index(request):
    return json({"hello": "world"})

if __name__ == "__main__":
    if settings.ASYNC:
        asyncio.set_event_loop(uvloop.new_event_loop())
        server = app.create_server(
            host=settings.HOST, port=settings.PORT, return_asyncio_server=True, debug=settings.DEBUG
        )
        loop = asyncio.get_event_loop()
        loop.set_task_factory(context.task_factory)
        task = asyncio.ensure_future(server)
        try:
            loop.run_forever()
        except BaseException:
            loop.stop()
    else:
        app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
