#-*- coding: utf-8 -*-
from openerp.osv import fields, osv
from datetime import *


class ea_project_wizard_jmos(osv.Model):

    _inherit = 'ea.project_wizard'

    #def arranque_onchange_hud(self, cr, uid, ids, date_end,
        #context=None):
        #res = {}

        #if date_end:
            #res = {'arranques_date_start': date_end}
            #return {'value': res}
        #else:
            #return {}

    def campo_onchange_hud(self, cr, uid, ids, arranques_date_end,
        context=None):
        res = {}

        if arranques_date_end:
            res = {'campo_date_start': arranques_date_end}
            return {'value': res}
        else:
            return {}

    def pi_onchange_hud(self, cr, uid, ids, campo_date_end,
        context=None):
        res = {}

        if campo_date_end:
            res = {'pi_date_start': campo_date_end}
            return {'value': res}
        else:
            return {}

    def procesamiento_onchange_hud(self, cr, uid, ids, pi_date_end,
        context=None):
        res = {}

        if pi_date_end:
            res = {'procesamiento_date_start': pi_date_end}
            return {'value': res}
        else:
            return {}

    def analisis_onchange_hud(self, cr, uid, ids, procesamiento_date_end,
        context=None):
        res = {}

        if procesamiento_date_end:
            res = {'analisis_date_start': procesamiento_date_end}
            return {'value': res}
        else:
            return {}

    def entrega_onchange_hud(self, cr, uid, ids, analisis_date_end,
        context=None):
        res = {}

        if analisis_date_end:
            res = {'entrega_date_start': analisis_date_end}
            return {'value': res}
        else:
            return {}

    _columns = {
        'plaza_line': fields.one2many('plaza', 'nombre_estudio_id', 'Plaza'),
        }