# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from openerp.osv import fields, osv

class presupuestos(osv.Model):
    _name = 'presupuesto_formulario'
    _description = 'Formulario presupuesto'
    _columns = {
        'claveproyecto': fields.char("Clave del Proyecto"),
        'fechadepresupuesto': fields.date("Fecha del presupuesto"),
        'tabla_test': fields.one2many('presupuesto_tabla','plaza','Linea de Presupuesto')
    }
   
  
class presupuestostabla(osv.Model):
    _name = 'presupuesto_tabla'
    _description = 'Formulario presupuesto tabla'
    _columns = {
        'plaza': fields.many2one('res.country.state.city','Plaza'),
        'ejecutivo': fields.many2one('res.partner','Ejecutivo GEA'),
        'capacitacion': fields.many2one('event.event','Capacitacion'),
        'piloto': fields.date("Piloto"),
        'inicio': fields.date("Inicio"),
        'fin': fields.date('Fin'),
        'tablainterna': fields.one2many('presupuesto_tablainterna','concepto','TEST')
    }
   
 
class presupuestostablainterna(osv.Model):
    _name = 'presupuesto_tablainterna'
    _description = 'Formulario presupuesto tabla'
    _columns = {
        'concepto':fields.many2one('product.product','Concepto'),
        'cantidad':fields.integer('Cantidad'),
        'dias':fields.integer('Dias'),
        'unidades':fields.float('Unidades'), # campo calculado: cantidad x dias
        'costo':fields.float('Costo'),
        'total':fields.float('Total') # campo calculado: unidades x costo
    }

