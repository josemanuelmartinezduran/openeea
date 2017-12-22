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

class ejerciciogasto(osv.Model):
    _name = 'ejerciciogasto_formulario'
    _description = 'Formulario presupuesto'
    _columns = {
        'claveproyecto': fields.char("Clave del Proyecto"),
		'fechadepresupuesto': fields.date("Fecha del ejercicio de gasto"),
		'tabla_test1': fields.one2many('presupuesto_tabla1','name1','Linea de Ejercicio de gasto'),
   }
   
  
class presupuestostabla1(osv.Model):
    _name = 'presupuesto_tabla1'
    _description = 'Formulario presupuesto tabla'
    _columns = {
		'name1': fields.integer('ID'),
        'plaza': fields.many2one('res.country.state.city','Plaza'),
		'ejecutivo': fields.many2one('res.partner','Ejecutivo GEA'),
		'capacitacion': fields.many2one('event.event','Capacitacion'),
		'piloto': fields.date("Piloto"),
		'inicio': fields.date("Inicio"),
		'fin': fields.date('Fin'),
		'tablainterna1': fields.one2many('presupuesto_tablainterna2','name'),
		'dato1':fields.related('tablainterna1','concepto',type='many2one',relation='product.product', string='Concepto'),
		'dato2':fields.related('tablainterna1','presupuestado',type='integer',relation='presupuesto_tablainterna2', string='Presupuestado'),
		'dato3':fields.related('tablainterna1','ejercido',type='integer',relation='presupuesto_tablainterna2', string='Ejercido'),
		'dato4':fields.related('tablainterna1','restan',type='function',relation='presupuesto_tablainterna2', string='Por Ejercer'),
		}
   
 
class presupuestostablainterna2(osv.Model):
	def calculate_resta(self, cr, uid, ids, field_name, args, context=None):
			ret={}
			for i in self.browse(cr, uid, ids):
				val=0
				val=(i.presupuestado)-(i.ejercido+i.gasto)
				ret[i.id]=val
			return ret
	_name = 'presupuesto_tablainterna2'
	_description = 'Formulario presupuesto tabla'
	_columns = {
					'name': fields.integer('ID'),
					'concepto':fields.many2one('product.product','Concepto'),
					'presupuestado':fields.integer('Presupuestado'),
					'ejercido':fields.integer('Ejercido'),
					'fecha':fields.date('Fecha'),
					'gasto':fields.integer('Gasto'), 
					'nota':fields.char('Nota'),
					# 'restan':fields.char('Restan'),
					'restan':fields.function(calculate_resta, method=True, type='integer', arg=None, string='Restan'), # campo calculado: presupuestado- ejercido y gasto
				}
  
