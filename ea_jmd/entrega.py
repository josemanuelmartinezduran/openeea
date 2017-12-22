# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdentrega(osv.Model):
    _name = "ea.entrega"
    _columns = {
            'name': fields.many2one("project.project",
                string="Nombre del Proyecto"),
            'presentador': fields.char("Nombre de quien presentó"),
            'acompanantes': fields.text("Acompañantes"),
            'revision_previa': fields.date("Fecha de la revisión previa"),
            'revision_presentacion': fields.date("Fecha de\
                la revisión de la presentación")
        }