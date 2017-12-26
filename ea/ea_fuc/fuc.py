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

class ea_cuentas(osv.Model):
    _inherit = 'res.partner'
    _description = 'Campos personalizados nuevo cliente'
    _columns = {
        'tipo_cuenta': fields.selection([('chica','Chica'),('mediana','Mediana'),('grande','Grande')], "Tipo de cuenta")
    }

class ea_informes(osv.Model):
    _inherit = 'sale.order'
    _description = 'Campos personalizados analisis desempeno de ventas'
    _columns = {
        'tipo_estudio': fields.selection((('conjoint','Conjoint'),('ua','U&A'),('tracking','Tracking')), "Tipo de estudio")
    }

class ea_ordenes(osv.Model):
    _inherit = 'mrp.production.workcenter.line'
    _description = 'Campos personalizados ordenes de trabajo'
    _columns = {
        'responsable': fields.char(string='Responsable',required=True)
    }

class ea_saleordes(osv.Model):
    _inherit="sale.order"
    _columns={
       'tipo_estudio': fields.selection((('conjoint', 'Conjoint'),('uya', 'U&A'),('tracking', 'Tracking')), "Tipo de estudio")
    }
