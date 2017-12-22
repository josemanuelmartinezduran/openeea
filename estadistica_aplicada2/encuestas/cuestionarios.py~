# -*- coding: utf-8 -*-
#IStandForFreedom
from osv import osv, fields


class archivos(osv.Model):
    _name = 'document.archivos'
    _columns = {
        'archivo_id': fields.integer('Secuencia'),
        'nom_archivo': fields.char('Nombre de archivo'),
        'ver_archivo': fields.char('Version', size=10)
    }


class cuestionarios(osv.Model):
    _name = 'document.cuestionarios'
    _description = 'Tabla para registro de cuestionarios'
    _columns = {
        'nom_estudio_id': fields.many2one('project.arranques',
            'Nombre del estudio'),
        'arch_cuestionario': fields.binary('Subir cuestionario'),
        'nom_responsable_id': fields.many2one('hr.employee',
            'Responsable'),
        'responsable': fields.date('Fecha de solicitud'),
        'archivo_ids': fields.one2many('document.archivos',
            'archivo_id', 'Archivos'),
        'state': fields.selection((('nuevo', 'Nuevo'),
            ('revisado', 'Revisado'), ('aprobado', 'Aprobado')), 'Estado'),
    }
