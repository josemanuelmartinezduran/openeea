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
    'name': 'Cuestionario',
    'version': '1.0',
    'category': 'Knowledge Management',
    'description': """
Modulo de cuestionario para Estadistica Aplicada
================================================
- Formulario
- Privilegios
""",
    'author': 'H&amp;D Datentechnik Mexico',
    'website': 'http://www.hud.mx/',
    'depends': [
        'knowledge'
    ],
    'data': [
        'security/cuestionario_security.xml',
        'view/cuestionario_view.xml',
        'view/cuestionario_data.xml',
        'wizard/cuestionario_configuration_view.xml',
        'security/ir.model.access.csv',
        'report/cuestionario_report_view.xml',
    ],
    'demo': [ 
        'view/cuestionario_demo.xml'
    ],
    'test': [
        'test/cuestionario_test2.yml'
    ],
    'js': [
        'static/src/js/cuestionario.js'
    ],
    'installable': True,
    'auto_install': False,
    'images': [
        'images/1_directories.jpeg',
        'images/2_storage_media.jpeg',
        'images/3_directories_structure.jpeg'
    ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
