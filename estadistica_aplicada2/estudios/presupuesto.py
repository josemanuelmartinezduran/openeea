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
	'tabla_test': fields.one2many('presupuesto_tabla','name1','Linea de Presupuesto'),
   }
   
  
class presupuestostabla(osv.Model):
    _name = 'presupuesto_tabla'
    _description = 'Formulario presupuesto tabla'
    _columns = {
		'name1': fields.integer('ID'),
        'plaza': fields.many2one('res.country.state.city','Plaza'),
		'ejecutivo': fields.many2one('res.partner','Ejecutivo GEA'),
		'capacitacion': fields.many2one('event.event','Capacitacion'),
		'piloto': fields.date("Piloto"),
		'inicio': fields.date("Inicio"),
		'fin': fields.date('Fin'),
		'tablainterna10': fields.one2many('presupuesto_tablainterna10','name'),
		'tablainterna20': fields.one2many('presupuesto_tablainterna20','name'),
		'tablainterna30': fields.one2many('presupuesto_tablainterna30','name'),
		'tablainterna40': fields.one2many('presupuesto_tablainterna40','name'),
		'tablainterna50': fields.one2many('presupuesto_tablainterna50','name'),
   }
   
 
class presupuestostablainterna10(osv.Model):
	def calculate_units(self, cr, uid, ids, field_name, args, context=None):
			ret={}
			for i in self.browse(cr, uid, ids):
				val=0
				val=i.cantidad*i.dias 
				ret[i.id]=val
			return ret
	def calculate_total(self, cr, uid, ids, field_name, args, context=None):
				ret={}
				for i in self.browse(cr, uid, ids):
					val=0
					val=i.unidades*i.costo
					ret[i.id]=val
				return ret		
	_name = 'presupuesto_tablainterna10'
	_description = 'Formulario presupuesto tabla'
	_columns = {
					'name': fields.integer('ID'),
					'concepto':fields.many2one('product.product','Concepto'),
					'cantidad':fields.integer('Cantidad'),
					'dias':fields.integer('Dias'),
					'unidades':fields.function(calculate_units, method=True, type='integer', arg=None, string='Unidades'), 
					'costo':fields.integer('Costo'),
					'total':fields.function(calculate_total, method=True, type='integer', arg=None, string='Total'), 
					}
   
class presupuestostablainterna20(osv.Model):
	def calculate_units(self, cr, uid, ids, field_name, args, context=None):
			ret={}
			for i in self.browse(cr, uid, ids):
				val=0
				val=i.cantidad*i.dias 
				ret[i.id]=val
			return ret
	def calculate_total(self, cr, uid, ids, field_name, args, context=None):
				ret={}
				for i in self.browse(cr, uid, ids):
					val=0
					val=i.unidades*i.costo
					ret[i.id]=val
				return ret		
	_name = 'presupuesto_tablainterna20'
	_description = 'Formulario presupuesto tabla'
	_columns = {
					'name': fields.integer('ID'),
					'concepto':fields.many2one('product.product','Concepto'),
					'cantidad':fields.integer('Cantidad'),
					'dias':fields.integer('Dias'),
					'unidades':fields.function(calculate_units, method=True, type='integer', arg=None, string='Unidades'), 
					'costo':fields.integer('Costo'),
					'total':fields.function(calculate_total, method=True, type='integer', arg=None, string='Total'), 
					}
   
   
class presupuestostablainterna30(osv.Model):
	def calculate_units(self, cr, uid, ids, field_name, args, context=None):
			ret={}
			for i in self.browse(cr, uid, ids):
				val=0
				val=i.cantidad*i.dias 
				ret[i.id]=val
			return ret
	def calculate_total(self, cr, uid, ids, field_name, args, context=None):
				ret={}
				for i in self.browse(cr, uid, ids):
					val=0
					val=i.unidades*i.costo
					ret[i.id]=val
				return ret		
	_name = 'presupuesto_tablainterna30'
	_description = 'Formulario presupuesto tabla'
	_columns = {
					'name': fields.integer('ID'),
					'concepto':fields.many2one('product.product','Concepto'),
					'cantidad':fields.integer('Cantidad'),
					'dias':fields.integer('Dias'),
					'unidades':fields.function(calculate_units, method=True, type='integer', arg=None, string='Unidades'), 
					'costo':fields.integer('Costo'),
					'total':fields.function(calculate_total, method=True, type='integer', arg=None, string='Total'), 
					}
					
class presupuestostablainterna40(osv.Model):
	def calculate_units(self, cr, uid, ids, field_name, args, context=None):
			ret={}
			for i in self.browse(cr, uid, ids):
				val=0
				val=i.cantidad*i.dias 
				ret[i.id]=val
			return ret
	def calculate_total(self, cr, uid, ids, field_name, args, context=None):
				ret={}
				for i in self.browse(cr, uid, ids):
					val=0
					val=i.unidades*i.costo
					ret[i.id]=val
				return ret		
	_name = 'presupuesto_tablainterna40'
	_description = 'Formulario presupuesto tabla'
	_columns = {
					'name': fields.integer('ID'),
					'concepto':fields.many2one('product.product','Concepto'),
					'cantidad':fields.integer('Cantidad'),
					'dias':fields.integer('Dias'),
					'unidades':fields.function(calculate_units, method=True, type='integer', arg=None, string='Unidades'), 
					'costo':fields.integer('Costo'),
					'total':fields.function(calculate_total, method=True, type='integer', arg=None, string='Total'), 
					}

class presupuestostablainterna50(osv.Model):
	def calculate_units(self, cr, uid, ids, field_name, args, context=None):
			ret={}
			for i in self.browse(cr, uid, ids):
				val=0
				val=i.cantidad*i.dias 
				ret[i.id]=val
			return ret
	def calculate_total(self, cr, uid, ids, field_name, args, context=None):
				ret={}
				for i in self.browse(cr, uid, ids):
					val=0
					val=i.unidades*i.costo
					ret[i.id]=val
				return ret		
	_name = 'presupuesto_tablainterna50'
	_description = 'Formulario presupuesto tabla'
	_columns = {
					'name': fields.integer('ID'),
					'concepto':fields.many2one('product.product','Concepto'),
					'cantidad':fields.integer('Cantidad'),
					'dias':fields.integer('Dias'),
					'unidades':fields.function(calculate_units, method=True, type='integer', arg=None, string='Unidades'), 
					'costo':fields.integer('Costo'),
					'total':fields.function(calculate_total, method=True, type='integer', arg=None, string='Total'), 
					}
