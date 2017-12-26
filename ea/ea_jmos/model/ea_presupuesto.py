#-*- coding: utf-8 -*-
from openerp.osv import fields, osv
from datetime import *


class presupuesto_linea_jmos(osv.Model):

    _inherit = 'ea.presupuesto_linea'

    _columns = {
        'cuota_id': fields.many2one('control_encuestas', 'Cuota del proyecto'),
        'planeacion_id': fields.many2one('ea.presupuesto',
            'Planeacion de proyecto'),
        'analisis_date_start': fields.date('Fecha de plan de analisis'),
    }