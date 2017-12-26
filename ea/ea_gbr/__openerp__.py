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
{
    'name': 'Estadistica Aplicada', 
    'version': '0.1',
    'category': 'Customization',
    'summary': 'Personalizacion de funciones para Estadistica Aplicada',
    'description': """
Funciones personalizados por: H&D Datentechnik Mexico, para la empresa: Estadistica Aplicada

Cambios en aplicaciones:

- Creacion de almacenes

Del grupo de desarrolladores:
----------------------------
Gerardo Bautista
""",
    'author': 'H&D Datentechnik Mexico',
    'website': 'https://www.hud.com.mx',
    'depends': [
        'base',
	'hr',
	'stock'
    ],
    'update_xml': [
        #'security/menu_sec.xml',
        #'security/ir.model.access.csv'
    ],
    'data': [
        'gbr_view.xml'
    ],
    'demo': [
        #Aqui van datos de demostración
    ],
    'test': [
        #Archivos de testing
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [
    ],
}
