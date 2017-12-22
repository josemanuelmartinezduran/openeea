# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class almacen_empleados(osv.Model):
    _name = 'stock.empleados'
    _description = 'Modulo de Almacen, menu Empleados'
    _columns = {
        'name': fields.text("Nombre")
    }
