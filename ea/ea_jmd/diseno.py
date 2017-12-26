# -*- coding: utf-8 -*-
from osv import osv, fields


class jmddiseno(osv.Model):
    _inherit = "mail.thread"
    _name = 'ea.diseno'

    def action_solicitado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'solicitud'})
        return True

    def action_asignado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'asignado'})
        return True

    def action_hecho(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'hecho'})
        return True

    _columns = {
        'name': fields.many2one('project.project', 'Clave'),
        'nombre_corto': fields.related('name', 'nombre_corto',
                string="Nombre Corto", type="char"),
        'descripcion': fields.text('Descripcion'),
        'fecha_solicitud': fields.date('Fecha de solicitud'),
        'fecha_entrega': fields.date('Fecha de entrega'),
        'fecha_final': fields.date('Fecha final'),
        'responsable_id': fields.many2one('hr.employee', 'Responsable'),
        'jefe_id': fields.many2one('hr.employee', 'Jefe inmedianto'),
        'tarea_ids': fields.one2many('arranques.tarea', 'diseno_id',
            string="Tareas"),
        'observaciones': fields.text("Observaciones"),
        'material_ids': fields.one2many('arranques.material',
            'diseno_id', string="Materiales"),
        'tarea_estatus': fields.char('Estatus'),
        'material_product_id': fields.many2one('product.product', 'Material'),
        'material_cant': fields.char('Cantidad', size=25),
        'material_estatus': fields.char('Estatus'),
        'personal_puesto_id': fields.many2one('hr.job', 'Puesto'),
        'personal_num_personas': fields.char('Numero de personas', size=25),
        'personal_capacitacion': fields.char('Capacitacion'),
        'personal_plaza_id': fields.many2one('res.country.state.city', 'Plaza'),
        'planilla_proyecto': fields.char('Plantilla de proyecto'),
        'etapa_actual': fields.char('Etapa actual'),
        'permiso_especial': fields.char('Permidos especial'),
        'no_conformidad': fields.char('No conformidad'),
        'comentario': fields.char('Comentario de tarea'),
        'tareas_precargadas': fields.char('Tareas precargadas'),
        'state': fields.selection([('solicitud', 'Solicitud'),
            ('asignado', 'Asignado'), ('hecho', 'Hecho')],
            "Estado", readonly=True),
        'prioridad': fields.selection([('baja', 'Baja'),
            ('media', 'Media'), ('alta', 'Alta')],
            "Prioridad"),
        'solicitante_id': fields.many2one("hr.employee", string="Solicitante"),
    }


class jmdtarea(osv.Model):
    _inherit = "arranques.tarea"
    _columns = {
        'diseno_id': fields.many2one("ea.diseno"),
        'responable_id': fields.many2one("hr.employee", string="Responsable"),
    }


class jmdtarea(osv.Model):
    _inherit = "arranques.material"
    _columns = {
        'diseno_id': fields.many2one("ea.diseno")
    }