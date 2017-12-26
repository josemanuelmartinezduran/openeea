# -*- coding: utf-8 -*-
#IStandForFreedom
#JMD Incidencias
from osv import osv, fields


class jmdincidencia(osv.Model):
    _name = "ea.incidencia"

    def get_proyecto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.proyecto_id.id
            if i.relation:
                ret[i.id] = i.relation.proyecto.id
        return ret

    def get_nombre(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.proyecto_id.nombre_corto
            if i.relation:
                ret[i.id] = i.relation.proyecto.nombre_corto
        return ret

    def get_plaza(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for linea in self.browse(cr, uid, ids, context):
            ret[linea.id] = 0
            if linea.relation and linea.relation.proyecto:
                ret[linea.id] = linea.relation.plaza_id.id
        return ret

    _columns = {
        'name': fields.char(string="Nombre", size=40),
        'cuestionario': fields.many2one("ea.encuesta", string="Cuestionario"),
        'filtro': fields.char("Filtro/Pregunta", size=40),
        'cantidad': fields.integer("Cantidad"),
        'tipo': fields.many2one("ea.incidencia.tipo", string="Tipo"),
        'fecha': fields.date("Fecha"),
        'relation': fields.many2one("ea.avance"),
        'proyecto': fields.function(get_proyecto, string="Clave del proyecto",
            type="char", size=40, store=False),
        'plaza_id': fields.function(get_plaza, string="Plaza",
                type="integer", store=True),
        'nombre_corto': fields.function(get_nombre, string="Nombre corto",
            type="char", size=40, store=False),
        'geasea': fields.selection([("GEA", "GEA"), ("SEA", "SEA")],
                string="GEA/SEA"),
        'proyecto_id': fields.many2one("project.project", string="Id del Proyecto"),
        'nombrecorto_rel': fields.related('proyecto_id',"nombre_corto" , string="Nombre corto",
            type="char", size=40, store=False),
        }




class jmdtipoincidencia(osv.Model):
    _name = "ea.incidencia.tipo"
    _inherit = "mail.thread"
    _columns = {
        'name': fields.char("Nombre")
    }
