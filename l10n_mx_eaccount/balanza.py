# -*- coding: utf-8 -*-
from osv import osv, fields


class jmd_asset(osv.Model):
    _name = "sat.balanza"
    _inherit = "mail.thread"
    _columns = {
        'name': fields.char("Mes"),
        'lineas_ids': fields.many2one("sat.balanza.line", string="Lineas")
        }
    
class jmd_balanzaline(osv.Model):
    _name = "sat.balanza.line"
    _inherit = "mail.thread"
    _columns = {
        'name': fields.char("Nombre"),
        'codigo': fields.char("Código"),
        'naturaleza': fields.char("Naturaleza"),
        'casat': fields.char("Codigo Agrupador SAT"),
        'saldo_inicial': fields.char("Saldo inicial"),
        'cargos': fields.char("Cargos"),
        'abonos': fields.char("Abonos"),
        }