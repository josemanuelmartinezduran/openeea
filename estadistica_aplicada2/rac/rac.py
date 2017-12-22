# -*- coding: utf-8 -*-
#Fixed By JMD #IStandForFreedom
from osv import osv, fields


class rac(osv.osv):
    _name = 'rac'
    _inherit = "mail.thread"

    def action_abierta(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'abierta'})
            return True

    def action_cerrar(self, cr, uid, ids):
            print("Cerrando")
            self.write(cr, uid, ids, {'state': 'cerrada'})
            return True

    _columns = {
        'name': fields.char('Nombre', required=True),
        'auditoria': fields.many2one('auditoria', string='Auditoria de Origen'),
        'auditor': fields.many2many('hr.employee', string='Auditor'),
        'fecha_reporte': fields.datetime('Fecha de reporte'),
        'fecha_limite': fields.datetime('Fecha limite'),
        'prioridad': fields.selection([('baja', 'Baja'), (' media', 'Media'),
            ('alta', 'Alta')], 'Prioridad'),
        'responsable': fields.many2many('hr.employee', string='Responsable'),
        'informacion': fields.one2many('rac.informacion', 'relation',
            string='Obsrevación'),
        'acciones': fields.one2many('rac.acciones', 'relation_rac',
            'Acciones'),
        'state': fields.selection([('abierta', 'Abierta'), ('cerrada',
            'Cerrada')], "Estado", readonly=True)
    }


class rac_informacion(osv.osv):
    _name = 'rac.informacion'
    _columns = {
        'name': fields.char('Observación'),
        'comentarios': fields.char('Comentarios'),
        'relation': fields.many2one("rac"),
        'emisor': fields.many2one("hr.employee", string="Emisor"),
        'receptor': fields.many2one("hr.employee", string="Receptor")
    }


class rac_acciones(osv.osv):
    _name = 'rac.acciones'
    _columns = {
        'name': fields.char('Accion'),
        'persona': fields.many2one('hr.employee', string='Persona'),
        'fecha': fields.date('Fecha'),
        'horas_dedicadas': fields.integer('Horas dedicadas'),
        'relation_rac': fields.many2one("rac", string="Relacion con RAC",
            ondelete="set null"),
        'tipo': fields.selection([('preventiva', 'Preventiva'),
            ('correctiva', 'Correctiva'), ('inmediata',
            'Correctiva Inmediata')], string="Tipo"),
        'realizado': fields.boolean("Realizado"),
}
