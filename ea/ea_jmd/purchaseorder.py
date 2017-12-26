# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdpuerchaseorder(osv.Model):
    _inherit = "purchase.order"
    _columns = {
        'deducible': fields.boolean(string="Gasto Deducible"),
        'plaza': fields.many2one("plaza", "Plaza Origen"),
        'gasto_oficina': fields.boolean("Gastos de Oficina"),
        'nombre_corto': fields.related("proyecto", "nombre_corto",
            type="char", string="Nombre Corto", readonly=True, store=True)
        }