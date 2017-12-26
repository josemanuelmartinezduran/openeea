# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdcrmlead(osv.Model):
    _inherit = "crm.lead"
    _columns = {
            'tipo': fields.many2one("ea.tipoestudio", string="Tipo de estudio",
                ondelete="set null"),
        }