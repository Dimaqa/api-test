from aiohttp import web
import json
import db


async def add_company(request):
    try:
        data = await request.json()
        company = data['company']
        phone = data.get('phone')
    except:
        response_obj = {'status': 'failed', 'error': 'company name required'}
        code = 400
    else:
        async with request.app['db_pool'].acquire() as conn:
            error = await db.insert_company(conn, company, phone)
        if error:
            response_obj = {'status': 'failed', 'error': error}
            code = 400
        else:
            response_obj = {'status': 'success'}
            code = 200
    return web.Response(text=json.dumps(response_obj), status=code)


async def add_worker(request):
    try:
        data = await request.json()
        name = data['name']
        company = data.get('company')
    except:
        response_obj = {'status': 'failed', 'error': 'name required'}
        code = 400
    else:
        async with request.app['db_pool'].acquire() as conn:
            error = await db.insert_worker(conn, name, company)
        if error:
            response_obj = {'status': 'failed', 'error': error}
            code = 400
        else:
            response_obj = {'status': 'success'}
            code = 200

    return web.Response(text=json.dumps(response_obj), status=code)


async def add_product(request):
    try:
        data = await request.json()
        name = data['name']
    except:
        response_obj = {'status': 'failed', 'error': 'name required'}
        code = 400
    else:
        # search in redis first
        val = await request.app['redis_pool'].get(name)
        if bool(val):
            # if we found in redis, no need to add again
            response_obj = {'status': 'success'}
            code = 200
        else:
            # else add to db and redis
            async with request.app['db_pool'].acquire() as conn:
                error = await db.insert_product(conn, name)
            if error:
                response_obj = {'status': 'failed', 'error': error}
                code = 400
            else:
                await request.app['redis_pool'].set(name, 'True')
                response_obj = {'status': 'success'}
                code = 200
    return web.Response(text=json.dumps(response_obj), status=code)


async def edit_responsible(request):
    try:
        data = await request.json()
        product_id = data['product_id']
        worker_id = data['worker_id']
    except:
        response_obj = {'status': 'failed', 'error': 'both id required'}
        code = 400
    else:
        async with request.app['db_pool'].acquire() as conn:
            data = await db.edit_responsible(conn, product_id, worker_id)
        # If we returned str, thats a eror, else dict with results
        if isinstance(data, str):
            response_obj = {'status': 'failed', 'error': data}
            code = 400
        else:
            response_obj = {'status': 'success', 'current_list': data}
            code = 200
    return web.Response(text=json.dumps(response_obj), status=code)
