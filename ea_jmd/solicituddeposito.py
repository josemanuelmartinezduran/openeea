# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdsolicitud(osv.Model):
    _name = "purchase.moneyrequest"
    _inherit = "mail.thread"

    _columns = {
            'name': fields.char(string="Motivo", size=40),
            'proyecto': fields.many2one("project.project", "Proyecto"),
            'monto': fields.float("Monto"),
            'cuenta_bancaria': fields.char("Cuenta Bancaria"),
            'beneficiario': fields.char("Beneficiario"),
            'banco': fields.char("Banco"),
            'depositado': fields.boolean("Depositado"),
        }