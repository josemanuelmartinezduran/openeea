# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdstockmove(osv.Model):
    _inherit = "stock.move"

    def get_cost(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0.0
            print(("Multiplicando " + str(i.product_qty) +
                " por " + str(i.product_id.cost)))
            ret[i.id] = i.product_qty * i.product_id.standard_price
        return ret

    _columns = {
        'unit_price': fields.related("product_id", "standard_price",
            type="float", string="Costo Unitario", realtion="product.product",
            readonly=True, store=False),
        'total_cost': fields.function(get_cost, string="Costo Total",
            type="float", store=False)
        }