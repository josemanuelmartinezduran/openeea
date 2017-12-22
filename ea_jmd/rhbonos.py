# -*- coding: utf-8 -*-
from osv import osv, fields
import datetime


class jmdbonos(osv.Model):
    _name = "hr.bonos"
    _inherit = "mail.thread"

    def action_borrador(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'borrador'})
            return True

    def action_preaprobado(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'preaprobado'})
            return True
        
    def remove_duplicates(self, cr, uid, ids, context=None):
        marcadas = []
        for i in self.pool.get("hr.bonos").browse(cr, uid, self.pool.get("hr.bonos").search(cr, uid, [])):
            marcadas.append(i.id)
            #buscando duplicado por monto, persona y fecha
            for j in self.pool.get("hr.bonos").browse(cr, uid, self.pool.get("hr.bonos").search(cr, uid, [('empleado', '=', i.empleado.id), ('fecha', '=', i.fecha), ('monto', '=', i.monto), ('id', '!=', i.id)])):
                print "Duplicado localizado"
                if j.id not in marcadas:
                    print (str(i.id)+ " con " + str(j.id) + i.name + " es " + j.name)
                    self.pool.get("hr.bonos").unlink(cr, uid, [j.id])
        return True
    
    def action_aprobado(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'aprobado'})
            return True
            
    def get_puesto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if(i.empleado):
                ret[i.id] = i.empleado.job_id.name
        return ret
        
    def get_gea(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if(i.empleado):
                ret[i.id] = i.empleado.seagea
        return ret
        
    def get_departamento(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if(i.empleado):
                ret[i.id] = i.empleado.department_id.name
        return ret

    _columns = {
            'name': fields.char(string="Concepto", size=400),
            'empleado': fields.many2one("hr.employee", "Empleado"),
            'nombre': fields.related("empleado", "nombre",
                type="char", string="Nombre", readonly=True, store=False),
            'departamento': fields.function(get_departamento, type="char",
                                        string="Departamento", store=True),
            'puesto': fields.function(get_puesto, type="char",
                                        string="Puesto", store=True),
            'gea_sea': fields.function(get_gea, type="char",
                                        string="Gea/Sea", store=True),
            'fecha': fields.date("Fecha"),
            'monto': fields.float(digits=(9, 2), string="Monto"),
            'tipo': fields.selection([('monto', 'Monto'), ('dias', 'Días')],
            "Tipo"),
            'dias': fields.integer("Días"),
            'state': fields.selection([('borrador', 'Borrador'),
                ('aprobado', 'Aprobado')], "Estado", readonly=True),
            'proyecto_id': fields.many2one("project.project",
                string="Clave"),
            'nombre_corto': fields.related("proyecto_id", "nombre_corto",
                type="char", string="Nombre Corto", readonly=True, store=True),
            'cantidad': fields.char("Cantidad de Entrevistas"),
            'observaciones': fields.text("Observaciones"),
            'cuestionario': fields.char("Cuestionario"),
            'plaza': fields.char("Plaza"),
            'codigo_plaza': fields.char("Codigo de Estudio"),
            'codigos_pago': fields.char("Códigos de Pago"),
            'de_reporte': fields.boolean("Proviene de Reporte"),
            'h_envio': fields.datetime("Fecha y Hora de Envío"),
            'folio': fields.char("Folio del Reporte"),
            'reporte_id': fields.many2one("ea.avance", string="Liga al Reporte"),
            'es_tableta': fields.boolean("Proviene de Tabletas"),
            'es_extra': fields.boolean("Proviene de Extra"),
            'es_pi': fields.boolean("Proviene de PI"), 
            'es_cati': fields.boolean("Proviene de Cati"), 
            'es_completar': fields.boolean("Completo día"), 
        }

    _defaults = {
            'fecha': lambda *a: datetime.date.today().strftime('%Y-%m-%d'),
        }
