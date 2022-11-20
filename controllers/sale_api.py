from odoo import http

class SaleApi(http.Controller):

    # Trae todas la ordenes de ventas
    @http.route("/api/v1/get_sale_order", type="http", auth="user", methods=["GET"])
    def get_sale_order(self, **kw):
        sales = http.request.env["sale.order"].sudo().search([])
        output = "<h2>Ordenes de ventas</h2><ul>"

        for sale in sales:
            output += "<li>" + sale["name"] + "</li>"
        output += "</ul>"
        return output

    # Crea ordenes de ventas
    @http.route(
        "/api/v1/create_sale_order",
        type="json",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def create_sale_order(self, **kw):
        sale = http.request.env["sale.order"].sudo().create(kw["params"])
        for order_line in kw["order_line"]:
            http.request.env["sale.order.line"].sudo().create({
                "order_id": sale.id,
                "product_id":order_line["product_id"],
                "product_uom_qty":order_line["product_uom_qty"]
            })
        return {"message": "Insert"}, 200