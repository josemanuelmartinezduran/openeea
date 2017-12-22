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

class cajachica(osv.Model):
    _name = 'purchase.cajachica'
    _description = 'Modulo Resumen de Caja Chica para Estadistica Aplicada'
    _columns = {
        'name': fields.text("Nombre")
    }

class analisiscampo(osv.Model):
    _name = 'purchase.analisiscampo'
    _description = 'Modulo Analisis de Gastos en Campo para Estadistica Aplicada'
    _columns = {
        'name': fields.text("Nombre")
    }

class auditoria(osv.Model):
    _name = 'purchase.auditoria'
    _description = 'Modulo Auditoria para Estadistica Aplicada'
    _columns = {
        'name': fields.text("Nombre")
    }

class noconforme(osv.Model):
    _name = 'purchase.noconforme'
    _description = 'Modulo No Conformidad para Estadistica Aplicada'
    _columns = {
        'name': fields.text("Nombre")
    }

class racs(osv.Model):
    _name = 'purchase.racs'
    _description = 'Modulo RACs para Estadistica Aplicada'
    _columns = {
        'name': fields.text("Nombre")
    }

class presupuesto(osv.Model):
    _inherit = 'purchase.order'
    _descripction = 'Campos para orden de compra Estadistica Aplicada'
    _columns = {
        'proyecto': fields.char('Proyecto'),
        'justificacion': fields.char('Justifiacion de solicitud')
    }
