from views import add_company

def setup_routes(app):
    app.router.add_post('/add_company', add_company)