# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdjob(osv.Model):
    _inherit = "hr.job"
    _columns = {
            'codigo': fields.char("Codigo"),
            'area': fields.char("Area"),
        }