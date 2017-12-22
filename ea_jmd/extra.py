# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdextra(osv.Model):
    _name = "ea.extra"
    _inherit = "mail.thread"

    def autoriza(self, cr, uid, ids, context=None):
        print("Entrando")
        for i in self.browse(cr, uid, ids, context):
            if i.autorizado:
                return
            print("En el for")
            self.write(cr, uid, [i.id], {
                'jefe': uid,
                'autorizado': True,
                'fecha_autorizacion': fields.datetime.now()})
            self.pool.get("hr.bonos").create(cr, uid, {
                'name': i.motivo,
                'empleado': i.name.id,
                'monto': i.monto,
                'tipo': i.tipo,
                'dias': i.dias,
                'proyecto_id': i.proyecto_id.id,
                'plaza': i.plaza_id.name,
                'codigo_plaza': i.plaza_id.codigo,
                'es_extra': True,
                'fecha': i.fecha
                })

    _columns = {
            'name': fields.many2one("hr.employee", string="Solicitante"),
            'jefe': fields.many2one("res.users", string="Jefe que autoriza"),
            'monto': fields.float("Monto"),
            'dias': fields.float("Días"),
            'motivo': fields.text("Motivo", required=True),
            'autorizado': fields.boolean("Autorizado"),
            'aceptado': fields.boolean("Aceptado"),
            'tipo': fields.selection([('monto', 'Monto'), ('dias', 'Días')],
            "Tipo"),
            "proyecto_id": fields.many2one("project.project", string="Estudio", required=True),
            'nombre_corto': fields.related("proyecto_id", "nombre_corto",
                type="char", string="Nombre Corto", readonly=True, store=True),
            'plaza_id': fields.many2one("plaza", string="Plaza"),
            'codigo_nomina': fields.related("plaza_id", "codigo",
                type="char", string="Código de Estudio", readonly=True, store=True),
            "fecha": fields.date("Fecha en que se generó"),
            "fecha_autorizacion": fields.datetime("Fecha y Hora de Autorización"),
        }