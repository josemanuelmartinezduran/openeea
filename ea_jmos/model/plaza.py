# -*- coding: utf-8 -*-
from osv import osv, fields


class plaza(osv.Model):

    _name = 'plaza'
    _inherit = "mail.thread"

    _columns = {
        'order_id': fields.many2one('sale.order', 'Ejecutivo de cuenta'),
        'ea_avance_line': fields.one2many('ea.avance', 'plaza_id',
             'Linea de avance'),
        'name': fields.char('Nombre de la plaza', size=30),
        'nombre_estudio_id': fields.many2one('project.project',
            'Nombre del estudio'),
        'ciudad_id': fields.many2one('res.country.state.city', 'Ciudad'),
        'plaza': fields.boolean('Plaza'),
        }
