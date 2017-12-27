# -*- coding: utf-8 -*-
from osv import osv, fields
from pprint import pprint


class jmdcuotas(osv.Model):
    _inherit = "control_encuestas"
    _description = "Modelo que controla las Cuotas"

    def on_change_project(self, cr, uid, ids, project_id, context=None):
        ret = {}
        values = {}
        new_name = ""
        project_obj = self.pool.get("project.project")
        for i in project_obj.browse(cr, uid, [project_id]):
            new_name = i.nombre_corto
        if new_name != "":
            values["name"] = new_name
        ret["value"] = values
        return ret

    def on_change_setname(self, cr, uid, ids, cotizacion_id, context=None):
        ret = {}
        values = {}
        sale_order_obj = self.pool.get("sale.order")
        for i in self.browse(cr, uid, ids, context):
            for j in sale_order_obj.browse(cr, uid, [cotizacion_id], context):
                values["name"] = j.nombre_corto
        ret["value"] = values
        return ret

    def limpia_todo(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, self.search(cr, uid, []), context=None):
            print("Actualizando " + str(i.name))
            i.limpia(context)

    def limpia(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids, context):
            for j in i.tiraje:
                for k in j.realizadas:
                    if not k.relation_avance:
                        self.pool.get("ea.avance.linea").unlink(cr, uid, [k.id])


    def action_nuevo(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'nuevo'})
        return True

    def action_autorizado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'autorizado'})
        return True
    
    def compute_realizadas(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        total = 0
        for i in self.browse(cr, uid, ids, context):
            for j in i.tiraje:
                total += len(j.realizadas)
            ret[i.id] = total
        return ret

    _columns = {
            'name': fields.char(string="Nombre Corto del Proyecto", size=40),
            'responsible_id': fields.many2one("hr.employee",
                "Nombre del responsable"),
            'project_id': fields.many2one('project.project',
                "Clave del estudio"),
            'nombre_corto': fields.related('project_id', 'nombre_corto',
                string="Nombre Corto", type="char", store=True),
            'inicio': fields.date("Fecha de inicio de Campo"),
            'fin': fields.date("Fecha de finalización de Campo"),
            'state': fields.selection([('nuevo', 'Nuevo'), ('autorizado',
                'Autorizado')], "Estado", readonly=True),
            'odt_id': fields.many2one("ea.project_wizard", "Orden de trabajo"),
            'cotizacion_id': fields.many2one("sale.order", "Cotización"),
            'realizadas': fields.function(compute_realizadas, string="Entrevistas Realizadas",
                                          type="integer", store=False),
            'tiraje': fields.one2many("ea.tiraje", "relation_id",
                    string="Cantidad de Entrevistas"),
            'plaza_id': fields.many2one("plaza", "Plaza"),
            'cuestionario_id': fields.many2one("ea.encuesta"),
            'numero_variables': fields.integer("Numero de Variables")
        }


class jmdcuotasplaza(osv.Model):
    _inherit = "editor_encuestas"

    def duplica_cuota(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids, context):
            idnuevo = self.create(cr, uid,
                {'name': i.name,
                'plaza_id': i.plaza_id.id,
                'encuesta': i.encuesta.id,
                'id_encuesta': i.id_encuesta.id}, context)
            for j in i.cuotas:
                cuota_obj = self.pool.get("ea.cuota")
                nid = cuota_obj.create(cr, uid, {
                     'name': j.name,
                     'relation_id': idnuevo})
                cuota_obj.write(cr, uid, nid, {
                    'cantidad': j.cantidad}, context)
        return {}

    def on_change_setname(self, cr, uid, ids, encuesta_id,
        place_id, context=None):
        ret = {}
        values = {}
        #Leyendo el nombre corto del estudio
        nombre_corto = ""
        for i in self.browse(cr, uid, ids, context):
            if i.id_encuesta.name:
                nombre_corto = i.id_encuesta.name
        #Leyendo el nombre de la plaza
        plaza = ""
        if place_id:
            for j in self.pool.get("plaza").browse(cr,
                uid, [place_id]):
                plaza = j.name
        #Leyendo el nombre de la encuesta
        encuesta = ""
        if encuesta_id:
            for k in self.pool.get("ea.encuesta").browse(cr,
                uid, [encuesta_id]):
                encuesta = k.name
        nombre_nuevo = nombre_corto + "-" + plaza + "-" + encuesta
        values['name'] = nombre_nuevo
        ret['value'] = values
        return ret

    def calculate_cant(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        total = 0
        for i in self.browse(cr, uid, ids, context):
            for j in i.cuotas:
                if j.cantidad:
                    total += j.cantidad
            ret[i.id] = total
        return ret

    def get_project(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if i.id_encuesta and i.id_encuesta.project_id:
                ret[i.id] = i.id_encuesta.project_id.id
            else:
                ret[i.id] = 0
        return ret

    def get_nproject(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if i.id_encuesta and i.id_encuesta.project_id:
                ret[i.id] = i.id_encuesta.project_id.name
            else:
                ret[i.id] = ""
        return ret

    def get_ncproject(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if i.id_encuesta and i.id_encuesta.project_id:
                ret[i.id] = i.id_encuesta.project_id.nombre_corto
            else:
                ret[i.id] = ""
        return ret

    def calculate_realizadas(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            realizadas = 0
            for j in i.cuotas:
                for k in j.avance_ids:
                    realizadas = realizadas + 1
            ret[i.id] = realizadas
        return ret

    _columns = {
            'name': fields.char(string="Nombre", size=80),
            'place': fields.many2one("res.country.state.city", "Plaza"),
            'encuesta': fields.many2one("ea.encuesta", "Cuestionario"),
            'cuotas': fields.one2many("ea.cuota", 'relation_id',
                string="Cuotas por plaza por cuestionario", ondelete="cascade"),
            'cant': fields.function(calculate_cant, string="Total de Encuestas",
                    type="integer", store=False),
            'plaza_id': fields.many2one("plaza", "Plaza"),
            'idproyecto': fields.function(get_project, string="Id Proyecto",
                type="integer"),
            'realizadas': fields.function(calculate_realizadas,
                string="Realizadas", type="integer"),
            'proyectonombre': fields.function(get_nproject,
                string="Proyecto", type="char", store=True),
            'nombre_corto': fields.function(get_ncproject,
                string="Nombre Corto", type="char", store=True),
        }


class jmdcuota(osv.Model):
    _name = "ea.cuota"

    def get_proyecto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for cuota in self.browse(cr, uid, ids, context):
            ret[cuota.id] = 0
            if cuota.relation_id and cuota.relation_id.id_encuesta and\
            cuota.relation_id.id_encuesta.project_id:
                ret[cuota.id] = cuota.relation_id.id_encuesta.project_id.id
        return ret

    def get_nproyecto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for cuota in self.browse(cr, uid, ids, context):
            ret[cuota.id] = 0
            if cuota.relation_id and cuota.relation_id.id_encuesta and\
            cuota.relation_id.id_encuesta.project_id:
                ret[cuota.id] = cuota.relation_id.id_encuesta.project_id.name
        return ret

    def get_ncproyecto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for cuota in self.browse(cr, uid, ids, context):
            ret[cuota.id] = 0
            if cuota.relation_id and cuota.relation_id.id_encuesta and\
            cuota.relation_id.id_encuesta.project_id:
                ret[cuota.id] = cuota.relation_id.id_encuesta.project_id.\
                    nombre_corto
        return ret

    def  get_plaza(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for cuota in self.browse(cr, uid, ids, context):
            if cuota.relation_id and cuota.relation_id.plaza_id:
                ret[cuota.id] = cuota.relation_id.plaza_id.id
            else:
                ret[cuota.id] = ""
        return ret
        
    def  get_cuestionario(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for cuota in self.browse(cr, uid, ids, context):
            ret[cuota.id] = cuota.relation_id.encuesta.id
        return ret

    def get_nplaza(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for cuota in self.browse(cr, uid, ids, context):
            if cuota.relation_id and cuota.relation_id.plaza_id:
                ret[cuota.id] = cuota.relation_id.plaza_id.name
            else:
                ret[cuota.id] = ""
        return ret

    def count_avances(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            total = 0
            for j in i.avance_ids:
                if j.relation_avance.id  != False:
                    pprint(j.relation_avance.id)
                    total += 1
            ret[i.id] = total
        return ret

    _columns = {
            'name': fields.char(string="Nombre", size=80),
            'relation_id': fields.many2one("editor_encuestas"),
            'cantidad': fields.integer("Cantidad"),
            'proyecto': fields.function(get_proyecto, string="Proyecto",
                                        type="integer", store=False),
            'nproyecto': fields.function(get_nproyecto, string="Clave Proyecto",
                                         type="char", store=True),
            'ncproyecto': fields.function(get_ncproyecto, string="Nombre Corto",
                                          type="char", store=True),
            'idplaza': fields.function(get_plaza, string="Id Plaza",
                                       type="integer", store=False),
            'nplaza': fields.function(get_nplaza, string="Plaza",
                                      type="char", store=True),
            'avance_ids': fields.many2many("ea.avance.linea",
                'avance_cuota_rel', "ea_cuota_id", 'avance_linea_id',
                string="Avances"),
            'idcuestionario': fields.function(get_cuestionario, 
                type="char",  store=True), 
            'count_avances': fields.function(count_avances,
                string="Total de realizadas", type="integer")
        }
