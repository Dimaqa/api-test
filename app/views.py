from aiohttp import web
import json

async def add_company(request):
    data = await request.json()
    print(data)
    response_obj = { 'status' : 'success' }
    code = 200
    return web.Response(text=json.dumps(response_obj), status=code)