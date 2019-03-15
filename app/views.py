from aiohttp import web
import json
import db


async def add_company(request):
    data = await request.json()
    company = data.get('company')
    phone = data.get('phone')
    if bool(company):
        async with request.app['db_pool'].acquire() as conn:
            error = await db.insert_company(conn, company, phone)
        if error:
            response_obj = {'status': 'failed', 'error': error}
            code = 200
        else:
            response_obj = {'status': 'success'}
            code = 200
    else:
        response_obj = {'status': 'failed'}
        code = 400
    return web.Response(text=json.dumps(response_obj), status=code)


async def add_worker(request):
    data = await request.json()
    name = data.get('name')
    company = data.get('company')
    if bool(name):
        async with request.app['db_pool'].acquire() as conn:
            error = await db.insert_worker(conn, name, company)
        if error:
            response_obj = {'status': 'failed', 'error': error}
            code = 400
        else:
            response_obj = {'status': 'success'}
            code = 200
    else:
        response_obj = {'status': 'failed'}
        code = 400
    return web.Response(text=json.dumps(response_obj), status=code)


async def add_product(request):
    data = await request.json()
    name = data.get('name')
    if bool(name):
        async with request.app['db_pool'].acquire() as conn:
            error = await db.insert_product(conn, name)
        if error:
            response_obj = {'status': 'failed', 'error': error}
            code = 200
        else:
            response_obj = {'status': 'success'}
            code = 200
    else:
        response_obj = {'status': 'failed'}
        code = 400
    return web.Response(text=json.dumps(response_obj), status=code)

async def edit_responsible(request):
    data = await request.json()
    product_id = data.get('product_id')
    worker_id = data.get('worker_id')
    if bool(product_id) and bool(worker_id):
        async with request.app['db_pool'].acquire() as conn:
            data = await db.edit_responsible(conn, product_id, worker_id)
        if isinstance(data, str):
            response_obj = {'status': 'failed', 'error' : data}
            code = 400
        else:
            response_obj = {'status': 'success', 'current_list' : data}
            code = 200
    else:
        response_obj = {'status': 'failed'}
        code = 400
    return web.Response(text=json.dumps(response_obj), status=code)