from odoo import http
from odoo.http import json, Response


class SaleApi(http.Controller):

    # Trae todas la ordenes de ventas
    @http.route("/api/v1/get_sale_order", type="http", auth="user", methods=["GET"])
    def get_sale_order(self, **kw):
        sales = http.request.env["sale.order"].sudo().search([])
        output = "<h2>Ordenes de ventas</h2><ul>"
        lista = []
        for sale in sales:
            lista.append(sale["name"])
            # output += "<li>" + sale["name"] + "</li>"
        # output += "</ul>"
        return self.build_response(lista)

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
            order_line["order_id"] = sale.id
            http.request.env["sale.order.line"].sudo().create(order_line)
        return {"message": "Insert"}, 200

    def build_response(self, entity):
        response = json.dumps(entity, ensure_ascii=False).encode("utf8")
        return Response(
            response, content_type="application/json;charset=utf-8", status=200
        )
