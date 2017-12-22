# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdusers(osv.Model):
    _inherit="res.users"
    _columns = {
        'cnomina': fields.many2one("ea.ciudadnomina", string="Oficina Nómina")
    }