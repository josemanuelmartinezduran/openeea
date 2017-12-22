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

class estudios(osv.Model):
    _name = 'estudios.estudios'
    _description = 'Modulo de estudios'
    _columns = {
        'name': fields.text("Nombre")
   }

class arranques(osv.Model):
    _name = 'project.arranques'
    _columns = {
        'name_arranques': fields.char('Nombre del estudio'),
        'fecha_solicitud': fields.date('Fecha de solicitud'),
        'fecha_entrega': fields.date('Fecha de entrega'),
        'tarea_descripcion': fields.text('Descripcion'),
        'tarea_responsable_id': fields.many2one('hr.employee','Responsable'),
        'tarea_fecha_ini': fields.date('Fecha de inicio'),
        'tarea_fecha_fin': fields.date('Fecha de finalizacion'),
        'tarea_estatus': fields.char('Estatus'),
        'material_product_id': fields.many2one('product.product','Material'),
        'material_cant': fields.char('Cantidad',size=25),
        'material_estatus': fields.char('Estatus'),
        'personal_puesto_id': fields.many2one('hr.job','Puesto'),
        'personal_num_personas': fields.char('Numero de personas',size=25),
        'personal_capacitacion': fields.char('Capacitacion'),
        'personal_plaza_id': fields.many2one('res.country.state.city','Plaza')
    }
