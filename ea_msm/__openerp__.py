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
    'name': 'Estadistica Aplicada MSM', 
    'version': '0.1',
    'depends': [
        'purchase'
    ],
    'author': 'H&D Datentechnik Mexico',
    'category': 'Customization',
    'description': '''Modulos personalizados para implementación en Estadistica Aplicada''',
    'update_xml': [
        'security/menu_sec.xml',
        'security/ir.model.access.csv'
    ],
    'data': [
        'view/clave_proy.xml'
    ],
    'demo': [
        #Aqui van datos de demostración
    ],
    'test': [
        #Archivos de testing
    ],
    'installable': True,
    'autoinstall': False,
}
