# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from datetime import *


class plaza(osv.Model):

    _name = 'plaza'

    def get_nombrecorto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.nombre_estudio_id.nombre_corto
        return ret

    _columns = {
        'order_id': fields.many2one('sale.order', 'Ejecutivo de cuenta'),
        'ea_avance_line': fields.one2many('ea.avance', 'plaza_id',
             'Linea de avance'),
        'name': fields.char('Nombre de la plaza', size=30),
        'nombre_estudio_id': fields.many2one('project.project',
            'Clave del estudio'),
        'ciudad_id': fields.many2many('res.country.state.city',
            string='Ciudad'),
        'plaza': fields.boolean('Plaza/Ruta'),
        'tipo': fields.selection([('plaza', 'Plaza'), ('ruta', 'Ruta')],
            "Tipo"),
        'cotizacion': fields.many2one('sale.order', "Cotización"),
        'odt': fields.many2one('ea.project_wizard', "Orden de Trabajo"),
        'proyecto': fields.many2one('project.project', "Proyecto"),
        'es_plaza_cati': fields.boolean("Plaza para CATI"), 
        'codigo': fields.char("Codigo"),
        'nombre_corto': fields.function(get_nombrecorto, type="char",
                                        string="Nombre Corto", store=True),
        }

    _defaults = {
            'codigo': lambda self, cr, uid, context={}:
                self.pool.get('ir.sequence').get(cr, uid, 'plaza'),
        }


class jmdcuidad(osv.Model):

    _inherit = "res.country.state.city"

    _columns = {
        'relation_plaza': fields.many2one("plaza")
        }
