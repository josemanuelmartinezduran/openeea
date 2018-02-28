# -*- coding: utf-8 -*-
from osv import osv, fields

class jmdbank (osv.Model):
    _inherit = "account.bank.statement"
    _columns = {
            'proyecto_id': fields.many2one("project.project",  string="Proyecto")
        }


class jmdbank (osv.Model):
    _inherit = "account.bank.statement.line"
    _columns = {
            'proyecto_id': fields.many2one("project.project",  string="Proyecto")
        }
