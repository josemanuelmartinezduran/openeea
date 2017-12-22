# -*- coding: utf-8 -*-

from openerp.osv import fields, osv


class validacion(osv.Model):
    _name = 'capacitacion.validacion'
    _inherit = "mail.thread"
    _description = 'Modulo de validacion'
    _columns = {
        'nombre_validacion': fields.char("Nombre"),
        'fecha_capacitacion': fields.datetime('Fecha y hora\
            de la capacitacion'),
        'name': fields.many2one('project.project', 'Proyecto'),
        'nombre_corto': fields.related('name', 'nombre_corto',
                string="Nombre Corto", type="char"),
        'empleado': fields.one2many('empleado.validacion',
        'relation', string="Datos del empleado"),
    }


class jmdvalidacionemployee(osv.Model):
    _inherit = "hr.employee"
    _columns = {
            'relation_val': fields.many2one("capacitacion.validacion")
        }


class empleado_validacion(osv.Model):
    _name = 'empleado.validacion'
    _description = 'Datos del empleado'
    _columns = {
        'name_related': fields.many2one('hr.employee', 'Clave del empleado'),
        'nombre': fields.related("name_related", "nombre", type="char",
            string="Nombre", readonly=True, store=False),
        'validado': fields.boolean('Validado'),
        'fecha_validacion': fields.date('Fecha de validacion'),
        'relation': fields.many2one("capacitacion.validacion"),
        'empresa': fields.char("Empresa"),
        'ciudad': fields.char("Ciudad"),
    }


class jmdevent(osv.Model):
    _inherit = "event.event"

    def generate_validacion(self, cr, uid, ids, context=None):
        ret = {}
        validacion_obj = self.pool.get("capacitacion.validacion")
        linea_obj = self.pool.get("empleado.validacion")
        print ("En el metodo")
        for i in self.browse(cr, uid, ids, context):
            print("En el ciclo")
            id_val = validacion_obj.create(cr, uid, {
                    'nombre_validacion': i.name,
                    'fecha_capacitacion': i.date_begin})
            for j in i.asistencia_ids:
                linea_obj.create(cr, uid, {
                    'name_related': j.asistente.id,
                    'validado': False,
                    'relation': id_val
                    })

        return ret