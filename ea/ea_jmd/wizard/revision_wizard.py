# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdrevision(osv.TransientModel):
    _name = "revision.wizard"

    def cancel_interviews(self, cr, uid, ids, context=None):
        ret = {}
        return ret

    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'descartadas': fields.integer("Encuestas Descartadas"),
            'revisor': fields.many2one("hr.employee", string="Empleado"),
            'investigador': fields.many2one("hr.employee",
                string="Investigador"),
            'motivo': fields.text("Motivo")
        }