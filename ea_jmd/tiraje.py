# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdtiraje(osv.Model):
    _name = "ea.tiraje"

    def get_proyecto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_id and i.relation_id.project_id:
                ret[i.id] = i.relation_id.project_id.id
        return ret

    def get_proyecton(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.relation_id and i.relation_id.project_id:
                ret[i.id] = i.relation_id.project_id.name
        return ret

    def get_cuestionario(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = "No Definido"
            if i.cuestionario_id:
                ret[i.id] = i.cuestionario_id.name
        return ret

    def get_count(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.realizadas:
                ret[i.id] = ret[i.id] + 1
        return ret

    def get_scount(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.realizadas:
                if j.supervision:
                    ret[i.id] = ret[i.id] + 1
        return ret

    def get_scountd(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.realizadas:
                if j.supervision:
                    for k in j.supervision:
                        if "Directa" in k.name:
                            ret[i.id] = ret[i.id] + 1
        return ret

    def get_scountr(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.realizadas:
                if j.supervision:
                    for k in j.supervision:
                        if "De Regreso" in k.name:
                            ret[i.id] = ret[i.id] + 1
        return ret

    def get_socount(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            for j in i.realizadas:
                if j.sup_oficina:
                    ret[i.id] = ret[i.id] + 1
        return ret

    _columns = {
            'name': fields.function(get_cuestionario, type="char",
                string="Cuestionario", store=True),
            'plaza_id': fields.many2one("ea.plaza", string="Plaza"),
            'plaza': fields.many2one("plaza", string="Plaza"),
            'cuestionario_id': fields.many2one("ea.encuesta",
                string="Cuestionario"),
            'cantidad': fields.integer("Cantidad"),
            'relation_id': fields.many2one("control_encuestas"),
            'idproyecto': fields.function(get_proyecto, string="Proyecto",
                type="integer", store=True),
            'realizadas': fields.one2many("ea.avance.linea", 'tiraje',
                string="Realizadas"),
            'plaza_name': fields.related("plaza", "name", type="char",
                string="Plaza", readonly=True, store=True),
            'proyecto_name': fields.function(get_proyecton,
                string="Clave del estudio", type="char", store=True),
            'count_realizadas': fields.function(get_count,
                string="Realizadas", type="integer", store=True),
            'count_supervisadas': fields.function(get_scount,
                string="Supervisadas en Campo", type="integer", store=True),
            'count_supervisadasd': fields.function(get_scountd,
                string="Supervisadas Directas", type="integer", store=True),
            'count_supervisadasr': fields.function(get_scountr,
                string="Supervisadas de Regreso", type="integer", store=True),
            'count_osupervisadas': fields.function(get_socount,
                string="Supervisadas en Oficina", type="integer", store=True),
        }