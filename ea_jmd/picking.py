# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdpickingour(osv.Model):
    _inherit = "stock.picking.out"

    _columns = {
            'material': fields.char("Estado del material"),
            'estudio': fields.many2one("project.project", string="Estudio"),
            'plaza': fields.many2one("plaza", string="Plaza"),
            'estado': fields.char("Estado del material"),
            'emat': fields.char("Estado del material", required=False),
            'paqueteria': fields.many2one('hd.paqueteria',
                string="Paqueteria"),
        }