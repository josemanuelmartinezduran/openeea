# -*- coding: utf-8 -*-
from osv import osv, fields


class myclass(osv.Model):
    _inherit = "hr.payslip"
    _columns = {
            'cobrada': fields.boolean(string="Cobrada")
        }