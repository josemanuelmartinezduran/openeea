# -*- coding: utf-8
from osv import osv, fields


class jmdbonos(osv.Model):
    _name = "ea.externo"
    _inherit = "mail.thread"
    _columns = {
            'name' : fields.char("Nombre de Usuario"),
            'passwd': fields.char("Password"),
            'aplicacion': fields.selection([('input.php','Tablets'), ('input2.php', 'Proveedores'),
                ('cati.php', 'Cati')], string="Aplicación"),
            'sea_id': fields.many2one("res.partner", string="Nombre del SEA"),
            'responsable_sea': fields.char("Reponsable SEA")
        }