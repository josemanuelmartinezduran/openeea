# -*- coding: utf-8 -*-
from osv import osv, fields
import datetime


class jmdreporte(osv.Model):
    _name = "ea.reporte_proyecto"
    _inherit = "mail.thread"

    def generate_report(self, cr, uid, ids, context=None):
        ret = {}
        ejercido = 0
        objeto_gasto = self.pool.get('ea.reporte_proyecto.linea_gasto')
        expense_obj = self.pool.get("ea.gasto")
        for i in self.browse(cr, uid, ids, context):
            #Eliminanado los datos obsoletos
            for gasto in i.gasto_ids:
                self.pool.get("ea.reporte_proyecto.linea_gasto").\
                    unlink(cr, uid, [gasto.id], context)
            for linea in i.proyecto.planeacion.presupuesto_linea:
                #No se deposita Start #IStandForFreedom
                for nosedeposita in linea.nosedeposita:
                    values = {
                            'concepto_gasto': nosedeposita.name,
                            'plaza':
                            nosedeposita.relation_presupuesto_linea.plaza.id,
                            'relation': i.id,
                            'tipo': 'No se deposita',
                            'total_presupuestado': nosedeposita.total
                        }
                    ejercido = 0
                    for gasto in expense_obj.browse(cr, uid,
                        expense_obj.search(cr, uid, [('proyecto', '=',
                        i.proyecto.id)]), context):
                        #Iterando en a depositar
                        for j in gasto.gasto_nosedeposita:
                            if j.presupuesto_linea_id.name == \
                                nosedeposita.name:
                                ejercido += j.monto
                    values['ejercido'] = ejercido
                    objeto_gasto.create(cr, uid, values, context)
                #A depositar Start #IStandForFreedom
                for adepositar in linea.adepositar:
                    values = {
                            'concepto_gasto': adepositar.name,
                            'plaza':
                            adepositar.relation_presupuesto_linea.plaza.id,
                            'relation': i.id,
                            'tipo': 'A depositar',
                            'total_presupuestado': adepositar.total
                        }
                    ejercido = 0
                    for gasto in expense_obj.browse(cr, uid,
                        expense_obj.search(cr, uid, [('proyecto', '=',
                        i.proyecto.id)]), context):
                        #Iterando en a depositar
                        for j in gasto.gasto_adepositar:
                            if j.presupuesto_linea_id.name == \
                                adepositar.name:
                                ejercido += j.monto
                    values['ejercido'] = ejercido
                    objeto_gasto.create(cr, uid, values, context)
                #Nomina GEA Start #IStandForFreedom
                for nominagea in linea.nominagea:
                    values = {
                            'concepto_gasto': nominagea.name,
                            'plaza':
                            nominagea.relation_presupuesto_linea.plaza.id,
                            'relation': i.id,
                            'tipo': 'Nomina GEA',
                            'total_presupuestado': nominagea.total
                        }
                    ejercido = 0
                    for gasto in expense_obj.browse(cr, uid,
                        expense_obj.search(cr, uid, [('proyecto', '=',
                        i.proyecto.id)]), context):
                        #Iterando en a depositar
                        for j in gasto.gasto_nominagea:
                            if j.presupuesto_linea_id.name == \
                                nominagea.name:
                                ejercido += j.monto
                    values['ejercido'] = ejercido
                    objeto_gasto.create(cr, uid, values, context)
                #Otros Start #IStandForFreedom
                for otros in linea.otros:
                    values = {
                            'concepto_gasto': otros.name,
                            'plaza':
                            otros.relation_presupuesto_linea.plaza.id,
                            'relation': i.id,
                            'tipo': 'Otros',
                            'total_presupuestado': otros.total
                        }
                    ejercido = 0
                    for gasto in expense_obj.browse(cr, uid,
                        expense_obj.search(cr, uid, [('proyecto', '=',
                        i.proyecto.id)]), context):
                        #Iterando en a depositar
                        for j in gasto.gasto_otros:
                            if j.presupuesto_linea_id.name == \
                                otros.name:
                                ejercido += j.monto
                    values['ejercido'] = ejercido
                    objeto_gasto.create(cr, uid, values, context)
        return ret

    def get_total(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            tiraje_obj = self.pool.get("ea.tiraje")
            for t in tiraje_obj.browse(cr, uid, tiraje_obj.search(
                cr, uid, [('idproyecto', '=', i.proyecto.id)])):
                ret[i.id] = ret[i.id] + t.cantidad
        return ret

    def get_realizadas(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            tiraje_obj = self.pool.get("ea.tiraje")
            for t in tiraje_obj.browse(cr, uid, tiraje_obj.search(
                cr, uid, [('idproyecto', '=', i.proyecto.id)])):
                ret[i.id] = ret[i.id] + t.count_realizadas
        return ret

    def get_supervisadas(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            tiraje_obj = self.pool.get("ea.tiraje")
            for t in tiraje_obj.browse(cr, uid, tiraje_obj.search(
                cr, uid, [('idproyecto', '=', i.proyecto.id)])):
                ret[i.id] = ret[i.id] + t.count_supervisadas
        return ret

    def get_supd(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            tiraje_obj = self.pool.get("ea.tiraje")
            for t in tiraje_obj.browse(cr, uid, tiraje_obj.search(
                cr, uid, [('idproyecto', '=', i.proyecto.id)])):
                ret[i.id] = ret[i.id] + t.count_supervisadasd
        return ret

    def get_supr(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            tiraje_obj = self.pool.get("ea.tiraje")
            for t in tiraje_obj.browse(cr, uid, tiraje_obj.search(
                cr, uid, [('idproyecto', '=', i.proyecto.id)])):
                ret[i.id] = ret[i.id] + t.count_supervisadasr
        return ret

    def get_osupervisadas(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            tiraje_obj = self.pool.get("ea.tiraje")
            for t in tiraje_obj.browse(cr, uid, tiraje_obj.search(
                cr, uid, [('idproyecto', '=', i.proyecto.id)])):
                ret[i.id] = ret[i.id] + t.count_osupervisadas
        return ret

    def get_prealizado(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0.0
            if i.total_entrevistas != 0:
                ret[i.id] = ((float(i.realizadas) * 100.0) /
                    float(i.total_entrevistas))
        return ret

    def get_psup(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0.0
            if i.realizadas != 0:
                ret[i.id] = ((float(i.supervisadas) * 100.0) /
                    float(i.realizadas))
        return ret

    def get_psupd(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0.0
            if i.realizadas != 0:
                ret[i.id] = ((float(i.supervisadod) * 100.0) /
                    float(i.realizadas))
        return ret

    def get_psupr(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0.0
            if i.realizadas != 0:
                ret[i.id] = ((float(i.supervisador) * 100.0) /
                    float(i.realizadas))
        return ret

    def get_psupo(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0.0
            if i.realizadas != 0:
                ret[i.id] = ((float(i.oficina) * 100.0) /
                    float(i.realizadas))
        return ret

    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'fecha': fields.date(string="Fecha del Reporte"),
            'proyecto': fields.many2one("project.project", string="Clave",
                ondelete="set null"),
            'nombre_corto': fields.related("proyecto", "nombre_corto",
                type="char", string="Nombre Corto", readonly=True, store=True),
            'gasto_ids': fields.one2many("ea.reporte_proyecto.linea_gasto",
                "relation", string="Nombre"),
            'avance_ids': fields.one2many("ea.reporte_proyecto.linea_avance",
                "relation", string="Nombre"),
            'entrevista_ids': fields.one2many(
                "ea.reporte_proyecto.linea_entrevista",
                "relation", string="Entrevistas"),
            'total_entrevistas': fields.function(get_total,
                string="Total de Entrevistas", type="integer", store=True),
            'realizadas': fields.function(get_realizadas, string="Realizadas",
                type="integer", store=True),
            'supervisadas': fields.function(get_supervisadas,
                string="Supervisadas en Campo", type="integer", store=True),
            'oficina': fields.function(get_osupervisadas,
                string="Supervisadas en Oficina", type="integer", store=True),
            'prealizado': fields.function(get_prealizado,
                string="Porcentaje Realizado", type="float", store=False),
            'psupervisado': fields.function(get_psup,
                string="Porcentaje Supervisado (Campo)", type="float",
                store=False),
            'supervisadod': fields.function(get_supd,
                string="Supervisión Directa (Campo)", type="float",
                store=True),
            'supervisador': fields.function(get_supr,
                string="Supervisión de Regreso (Campo)", type="float",
                store=True),
            'psupervisadod': fields.function(get_psupd,
                string="Procentaje Supervisión Directa (Campo)", type="float",
                store=False),
            'psupervisador': fields.function(get_psupr,
                string="Porcentaje Supervisión de Regreso (Campo)",
                type="float", store=False),
            'posupervisado': fields.function(get_psupo,
                string="Porcentaje Supervisado (Oficina)", type="float",
                store=False),
        }
    _defaults = {
        'fecha': lambda *a: datetime.date.today().strftime('%Y-%m-%d'),
    }


class jmdresportelinea(osv.Model):
    _name = "ea.reporte_proyecto.linea_gasto"
    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'concepto_gasto': fields.char("Concepto de Gasto"),
            'plaza': fields.many2one("res.country.state.city", string="Plaza"),
            'total_presupuestado': fields.float("Presupuestado"),
            'ejercido': fields.float(digits=(9, 2), string="Ejercido"),
            'relation': fields.many2one("ea.reporte_proyecto"),
            'tipo': fields.char("Tipo")
        }


class jmdlineaavance(osv.Model):
    _name = "ea.reporte_proyecto.linea_avance"
    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'cuota': fields.char("Cuota"),
            'plaza': fields.char("Plaza"),
            'planeado': fields.float("Planeado"),
            'avance': fields.float("Avance"),
            'relation': fields.many2one("ea.reporte_proyecto")
        }


class jmdavanceentrevista(osv.Model):
    _name = "ea.reporte_proyecto.linea_entrevista"
    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'cuestionario': fields.char("Cuestionario"),
            'plaza': fields.char("Plaza"),
            'planeado': fields.float("Planeado"),
            'avance': fields.float("Avance"),
            'relation': fields.many2one("ea.reporte_proyecto")
        }


class jmdrepoteincidencias(osv.Model):
    _name = "ea.reporte_proyecto.linea_incidencias"
    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'cuestionario': fields.char("Cuestionario"),
            'filtro': fields.char("Filtro"),
            'cantidad': fields.integer("Cantidad"),
        }