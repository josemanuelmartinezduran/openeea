# -*- coding: utf-8 -*-

import time
from openerp.osv import fields, osv

class rrhh(osv.Model):
    _name = 'hr.capacitacion'
    _description = 'Modulo de Recursos Humanos, menu Capacitacion'
    _columns = {
        'name': fields.text("Nombre")
    }

class rh_empleado(osv.Model):
    _inherit = "hr.employee"
    _columns = {
        'numero_empleado':fields.char("Numero de empleado", size=18),
        'paterno': fields.char("Apellido Paterno"),
        'materno': fields.char("Apellido Materno"),
        'nombres': fields.char("Nombres"),
        'ingreso': fields.date("Fecha de ingreso"),
        'ultima_baja': fields.date("Fecha de ultima baja"),
        'motivo_baja': fields.text("Motivo de la Baja"),
        'ultimo_ingreso': fields.date("Fecha de ultimo reingreso"),
        'salario_diario': fields.float(digits=(9, 2), 
			string="Salario Diario"),
    }
