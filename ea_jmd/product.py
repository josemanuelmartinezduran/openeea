# -*- coding: utf-8 -*-
from osv import osv, fields


class myclass(osv.Model):
    _inherit = "product.product"

    _columns = {
            'cost': fields.float("Costo"),
            
        }
