# -*- coding: utf-8 -*-
from osv import osv, fields


class jmddescuentos(osv.Model):
    _name = "hr.descuentos"

    def action_borrador(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'borrador'})
            return True

    def action_aprobado(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'aprobado'})
            return True

    _columns = {
            'name': fields.char(string="Concepto", size=80),
            'empleado': fields.many2one("hr.employee", "Empleado"),
            'nombre': fields.related("empleado", "nombre",
                type="char", string="Nombre", readonly=True, store=False),
            'fecha': fields.date("Fecha"),
            'monto': fields.float(digits=(9, 2), string="Monto"),
            'tipo': fields.selection([('monto', 'Monto'), ('dias', 'Días')],
            "Tipo"),
            'dias': fields.integer("Días"),
            'state': fields.selection([('borrador', 'Borrador'),
                ('aprobado', 'Aprobado')], "Estado", readonly=True),
            'fecha_campo': fields.date("Fecha del Reporte de Campo"),
            'fecha_rechazo': fields.date("Fecha del Rechazo"),
            'fase': fields.date("Fecha del Rechazo"),
            'comentario': fields.text("Comentario"),
            'proyecto_id': fields.many2one("project.project",
                string="Clave"),
            'nombre_corto': fields.related("proyecto_id", "nombre_corto",
                type="char", string="Nombre Corto", readonly=True, store=True),
            'plaza': fields.char("Plaza"),
            'post': fields.boolean("Aplicar despues de la nómina")
        }