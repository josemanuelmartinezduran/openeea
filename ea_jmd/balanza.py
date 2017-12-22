# -*- coding: utf-8 -*-
from osv import osv, fields


class myclass(osv.Model):
    _inherit = "mail.thread"
    _name = "account.balanza"
    _columns = {
            'name': fields.char("Codigo de la balanza"),
            'fecha': fields.date("Fecha de Generación"),
            'company_id': fields.many2one("res.company"),
            'account_ids': fields.one2many("account.balanza.account",
                'balanza_id', string="Cuentas")
        }

    def get_balanza(self, cr, uid, ids, context=None):
        ret = {}
        return ret

class jmdbalanzaaccount(osv.Model):

    _inherit = "mail.thread"
    _name= "account.balanza.account"
    _columns={
            'name': fields.char("Codigo de la Cuenta"),
            'cargos': fields.float("Cargos"),
            'abonos': fields.float("Abonos"),
            'saldo': fields.float("Saldo"),
            'balanza_id': fields.many2one("account.balanza", string="Balanza")
        }