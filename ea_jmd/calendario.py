# -*- coding: utf-8 -*-
from osv import osv, fields


class jmd_asset(osv.Model):
    _inherit = "mail.thread"
    _name = "ea.calendario"
    _columns = {
        'name': fields.many2one("project.project", string="Proyecto"),
        'fecha': fields.date("Fecha"),
        'plaza': fields.many2one("plaza", string="Plaza"),
        'archivo': fields.binary("Archivo"),
        'narchivo': fields.char("Nombre del Archivo")
        }
