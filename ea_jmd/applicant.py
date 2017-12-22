# -*- coding: utf-8 -*-
from osv import osv, fields


class jmd_applicant(osv.Model):
    _inherit = "hr.applicant"
    _columns = {
        'enterprise_id': fields.many2one("ea.enterprise",
                string="Empresa"),
        }