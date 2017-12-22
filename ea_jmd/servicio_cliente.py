# -*- coding: utf-8 -*-
#@josemanuelmartz
from osv import osv, fields


class no_conformidad(osv.osv):
    _name = 'ea.servicio'
    _inherit = "no_conformidad"

    def action_borrador(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'Borrador'})
        return True

    def action_generada(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'Generada'})
        return True

    def action_validada(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'Validada'})
        return True

    def action_resuelta(self, cr, uid, ids):
        print("Resolviendo")
        self.write(cr, uid, ids, {'state': 'Resuelta'})
        return True

    def action_cancelada(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'Cancelada'})
        return True

    def get_usuario(self, cr, uid, ids):
        return uid

    _columns = {
            'state': fields.selection([('Borrador', 'Borrador'), ('Generada', 'Generada'),
                ('Validada', 'Validada'), ('Resuelta', 'Resuelta'),
                ('Cancelada', 'Cancelada')], string="Estado"),
        }

    _defaults = {
        'name': lambda self, cr, uid, context={}:
            self.pool.get('ir.sequence').get(cr, uid, 'ea.servicio'),
        }