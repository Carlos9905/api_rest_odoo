from odoo import http
from odoo.http import json, Response


class SaleApi(http.Controller):
    @http.route("/api/v1/get_sale_order", type="http", auth="user", methods=["GET"])
    def get_sale_order(self, **kw):
        sales = http.request.env["sale.order"].sudo().search([])
        output = "<h2>Ordenes de ventas</h2><ul>"

        for sale in sales:
            output += "<li>" + sale["name"] + "</li>"
        output += "</ul>"
        return output

    @http.route(
        "/api/v1/create_sale_order",
        type="json",
        auth="user",
        methods=["POST"],
        csrf=False,
    )
    def create_sale_order(self, **kw):
        register = http.request.env["sale.order"].sudo().create(kw)
        if register:
            return {"message": "Insert"}
        else:
            return {"error": "Failed to insert"}

    def build_response(self, entity):
        response = json.dumps(entity, ensure_ascii=False).encode("utf8")
        return Response(
            response, content_type="aplication/json;charset=utf-8", status=200
        )
