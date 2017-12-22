# -*- coding: utf-8 -*-
from osv import osv, fields


class myclass(osv.Model):
    _inherit = "hr.department"
    _columns = {
            'codigo': fields.char("Codigo"),
            'area': fields.char("Area"),
        }