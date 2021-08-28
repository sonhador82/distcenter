import os
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp import web_log, web_middlewares


async def hello(request):
    return web.Response(text="hello world")


async def upload(request: Request):

    reader = await request.multipart()

    async for item in reader:
        if item.name == 'apk':
            filename = item.filename
            size = 0
            with open(os.path.join('/tmp', filename), 'wb') as fp:
                while True:
                    chunk = await item.read_chunk()
                    if not chunk:
                        break
                    size += len(chunk)
                    fp.write(chunk)

    data = {'uploaded_size': size, 'filename': filename}
    return web.json_response(data)


def init_func(argv):
    app = web.Application()
    app.add_routes(
        [
            web.get('/hello', hello),
            web.post('/upload', upload),
            web.put('/upload', upload)
        ]
    )
    return app
