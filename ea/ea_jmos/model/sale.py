#-*- coding: utf-8  -*-
from openerp.osv import fields, osv
from datetime import *


class sale_order_hud(osv.Model):

    _inherit = 'sale.order'

    _columns = {
        'plaza_line': fields.one2many('plaza', 'cotizacion', 'Plazas'),
        'plazas_text': fields.text("Plazas"),
    }