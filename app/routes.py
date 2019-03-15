from views import add_company, add_worker, add_product, edit_responsible


def setup_routes(app):
    app.router.add_post('/add_company', add_company)
    app.router.add_post('/add_worker', add_worker)
    app.router.add_post('/add_product', add_product)
    app.router.add_post('/edit_responsible', edit_responsible)