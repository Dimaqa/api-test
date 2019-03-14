from views import add_company, add_worker

def setup_routes(app):
    app.router.add_post('/add_company', add_company)
    app.router.add_post('/add_worker', add_worker)