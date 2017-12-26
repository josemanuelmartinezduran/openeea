# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdfaltas(osv.Model):
    _inherit = "mail.thread"
    _name = "hr.faltas"
    _columns = {
            'name': fields.many2one("hr.employee",
                string="Solicitante", ondelete="set null"),
            'fecha': fields.date("Fecha"),
            'tipo': fields.selection([("Vacaciones", "Vacaciones"),
                ("Incapacidad", "Incapacidad"), ("Permiso", "Permiso")],
                string="Tipo de Ausencia"),
        }