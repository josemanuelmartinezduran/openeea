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

from osv import osv, fields

import time

#Estadistica aplicada: Control de Encuestas

class editor_variables(osv.osv):
    _name = 'editor_variables'
    _columns = {
        'variable': fields.char('Variable', size=120, required=True),
        'comparador': fields.selection((('=', 'Igual a'),('>=', 'Mayor o igual a'),('<' , 'Menor a')),'Comparador'),
        'valor': fields.char('Valor', size=50),
    }
    
editor_variables()



class editor_cuotas_fve(osv.osv):
    _name = 'editor_cuotas_fve'
    _columns = {
        'nombre_cuota': fields.char('Nombre de la cuota', size=120, required=True),
		'variables': fields.one2many('editor_variables', 'variable', 'Variables'),
    }
    
editor_cuotas_fve()



class editor_encuestas(osv.osv):
    _name = 'editor_encuestas'
    _columns = {
        'plaza': fields.char('Plaza', size=120, required=True),
		'complejidad': fields.char('Complejidad'),
		'cuota': fields.many2one('editor_cuotas_fve', 'nombre_cuota', 'Cuota'),
		'cantidad': fields.integer('Cantidad'),
		'clave': fields.char('Clave', size=120),
    }
    
editor_encuestas()


class control_encuestas(osv.osv):
	_name = 'control_encuestas'
	_columns = {
		'nombre_estudio': fields.char('Nombre del estudio', sizze=120, required=True),
		'responsable': fields.many2one('res.users','responsible_id','Responsable', required=True),
		'encuesta': fields.one2many('editor_encuestas','cuota','Cuota'),
	}
	
#control_encuestas()
