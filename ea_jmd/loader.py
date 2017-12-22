# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdemployee(osv.Model):
    _name = "utils.employee"

    def generate_users(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            for j in i.usuarios:
                self.pool.get("res.users").copy(cr, uid, i.template.id,
                    {'name': j.name,
                    'login': j.usuario,
                    'password': j.contrasenia,
                    'email': j.correo,
                    'employee_ids': None,
                    })
        return ret

    _columns = {
            'template': fields.many2one("res.users", string="Plantilla"),
            'usuarios': fields.one2many("utils.employee.line",
            "relation", string="Usuarios")
        }


class jmdemployeeline(osv.Model):
    _name = "utils.employee.line"

    _columns = {
            'name': fields.char("Nombre"),
            'correo': fields.char("Correo"),
            'usuario': fields.char("Usuario"),
            'contrasenia': fields.char("Contraseña"),
            'relation': fields.many2one("utils.employee")
        }