# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class mantenimiento(osv.Model):
    _name = 'mrp.solicitud'
    _description = 'Modulo de Mantenimiento, menu Solicitud de Mantenimiento'
    _columns = {
        'name': fields.text("Nombre")
    }
