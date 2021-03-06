# -*- coding: utf-8 -*-
from osv import osv, fields
import datetime
import time


class jmdproject(osv.Model):
    _inherit = "project.project"

    def get_clave(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        clave = "No Asignada"
        for i in self.browse(cr, uid, ids):
            clave = i.planeacion.name
            if clave:
                if len(clave) > 3:
                    if "V" in clave[-3:]:
                        clave = clave[:clave.rfind("V")]
            ret[i.id] = clave
        return ret

    def update_all(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, self.search(cr, uid, []), context=None):
            print("Actualizando " + str(i.name))
            i.update(context)

    def update(self, cr, uid, ids, context=None):
        print("-----------------_")
        for i in self.browse(cr, uid, ids, context=None):
            #Total de entrevistas
            entre = 0
            rentre = 0
            try:
                if i.cuotas:
                    for k in i.cuotas.tiraje:
                        entre += k.cantidad
                        if k.realizadas:
                            rentre += k.realizadas.count()
            except:
                print("Sin Datos de Entevitas")
            self.write(cr, uid, [i.id], {'entrevistas_plan': entre,
                'entrevistas_hechas': rentre})
            dinero = 0.0
            gdinero = 0.0
            try:
                if i.planeacion:
                    dinero = i.planeacion.total

            except:
                print("Sin Datos de Cuotas")
            solicitud_obj = self.pool.get("ea_solicitud")
            for sol in solicitud_obj.browse(cr, uid, solicitud_obj.search(cr, uid, [('proyecto', '=', i.id)])):
                gdinero += sol.total_solicitud
            self.write(cr, uid, [i.id], {'presupuesto': dinero,
                'solicitudes': gdinero})
            #Gastos de purchase order
            gorder = 0
            order_obj = self.pool.get("purchase.order")
            for order in order_obj.browse(cr, uid, order_obj.search(cr, uid, [('proyecto', '=', i.id)])):
                gorder += order.amount_untaxed
                self.write(cr,  uid,  [i.id],  {'compras': gorder})
            #Gastos de nómina
            gnomina = 0
            nomina_obj = self.pool.get("hr.bonos")
            for bono in nomina_obj.browse(cr, uid, nomina_obj.search(cr, uid, [('proyecto_id', '=', i.id)])):
                gnomina += bono.monto
                self.write(cr,  uid,  [i.id],  {'nomina': gnomina})
            #Gastos de caja chica
            gcaja = 0
            caja_obj = self.pool.get("account.bank.statement")
            for caja in caja_obj.browse(cr, uid, caja_obj.search(cr, uid, [('proyecto_id', '=', i.id)])):
                gcaja += (caja.total_entry_encoding * -1)
                self.write(cr,  uid,  [i.id],  {'caja_chica': gcaja})
            #Gastos SEA
            gsea = 0
            sea_obj = self.pool.get("ea.conciliacion")
            for sea in sea_obj.browse(cr, uid, sea_obj.search(cr, uid, [('proyecto_id', '=', i.id)])):
                gsea += sea.monto_facturado
                self.write(cr,  uid,  [i.id],  {'sea': gsea})
            #Leyendo la odt
            odt = self.pool.get("ea.project_wizard")
            print("============================")
            print(i.inicio_campo)
            print(datetime.date.today().strftime('%Y-%m-%d'))
            today = datetime.date.today().strftime('%Y-%m-%d')
            for j in odt.browse(cr, uid, odt.search(cr, uid, [('name', '=', i.name)])):
                print("Odt Encontrada")
                #Colocando las fechas
                self.write(cr, uid, [i.id],
                           {'inicio_campo': j.campo_date_start,
                            'fin_campo': j.campo_date_end,
                            'inicio_pi': j.pi_date_end,
                            'inicio_procesamiento': j.procesamiento_date_end,
                            'inicio_analisis': j.analisis_date_end,
                            'inicio_entrega': j.entrega_date_start,})
            etapa = "0no_definido"
            if (i.fases == "8especial"):
                etapa = "8especial"
            elif (today > i.inicio_entrega and i.inicio_entrega):
                etapa = "7finalizado"
            elif (today > i.inicio_analisis and i.inicio_analisis):
                etapa = "6entrega"
            elif (today > i.inicio_procesamiento and i.inicio_procesamiento):
                etapa = "5analisis"
            elif (today > i.inicio_pi and i.inicio_pi):
                etapa = "4procesamiento"
            elif (today > i.fin_campo and i.fin_campo):
                etapa = "3procesos"
            elif (today > i.inicio_campo and i.inicio_campo):
                etapa = "2campo"
            elif (i.inicio_campo):
                etapa = "1por_iniciar"
            self.write(cr, uid, [i.id], {'fases': etapa})



    _columns = {
            'responsible_id': fields.many2one("hr.employee",
                string="Lider del proyecto"),
            'demografico': fields.char("Demográfico Manejado"),
            'nombre_corto': fields.char(string="Nombre Corto", size=40),
            'planeacion': fields.many2one("ea.presupuesto",
                string="Planeación"),
            'cuotas': fields.many2one("control_encuestas", string="Cuotas"),
            'plan_tabulacion': fields.binary("Plan de Tabulación"),
            'nplan_tabulacion': fields.char("Nombre del Plan"),
            'fecha_tabulacion': fields.date("Fecha del Plan Tab."),
            'plan_analisis': fields.binary("Plan Análisis"),
            'nplan_analisis': fields.char("Nombre Plan Análisis"),
            'fecha_analisis': fields.date("Fecha del Plan Ana."),
            'clave': fields.function(get_clave, string="Clave",
                type="char", size=40, store=True),
            'kick_off': fields.many2one("event.event", string="Kick Off"),
            'parent_proj_id': fields.many2one("project.project",
                string="Proyecto Padre"),
            'fases': fields.selection([('0no_definido', 'No Definido'),
                ('1por_iniciar', 'Por Inicar'), ('2campo', 'Campo'),
                ('3procesos', 'Procesos Intermedios'),
                ('4procesamiento', 'Procesamiento'),
                ('5analisis', 'Análisis'),
                ('6entrega', 'Entrega'), ('7finalizado', 'Finalizado'),
                ('8especial', 'Especial')], string="Fase"),
            'ola': fields.char("Ola"),
            'inicio_campo': fields.date("Inicio de Campo"),
            'fin_campo': fields.date("Fin de Campo"),
            'inicio_pi': fields.date("Fin de Procesos"),
            'inicio_procesamiento': fields.date("Fin de Procesamiento"),
            'inicio_analisis': fields.date("Fin de Análisis"),
            'inicio_entrega': fields.date("Fecha de Entrega"),
            'entrevistas_plan': fields.integer("Entrevistas Planeadas"),
            'entrevistas_hechas': fields.integer("Entrevistas Realizadas"),
            'presupuesto': fields.float("Monto Presupuestado"),
            'ejecutado': fields.float("Monto Ejecutado"),
        'comentarios': fields.text("Comentarios"),
        'levantamiento': fields.char("Tipo de Levantamiento"),
        'flash_ids': fields.one2many("ea.flash", "project_id", string="Flashes"),
        'extra_ids': fields.one2many("project.task", "project_extra_id", string="Extras"), 
        'solicitudes': fields.float("Monto en Solicitudes"), 
        'comprobado': fields.float("Monto Comprobado"), 
        "caja_chica": fields.float("Caja Chica"), 
        "nomina": fields.float("Nomina"), 
        "sea": fields.float("Pago a SEA"), 
        "compras": fields.float("Compras de Estudio"), 
        "porcentaje_ejecutado": fields.float("Porcentaje Ejercido"), 
        "porcentaje_realizado": fields.float("Porcentaje Realizado")
        }


class jmdtask(osv.Model):
    _inherit = "project.task"

    def get_avance(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        total_tareas = 0
        tareas_terminadas = 0
        porcentaje = 0
        for i in self.browse(cr, uid, ids, context):
            for j in i.tareas:
                total_tareas += 1
                if j.terminado:
                    tareas_terminadas += 1
            if total_tareas > 0:
                porcentaje = tareas_terminadas / total_tareas * 100
            ret[i.id] = porcentaje
        return ret

    def get_etapa(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.project_id.etapa
        return ret

    def generate_payroll(self, cr, uid, ids, context=None):
        ret = {}
        nomina_obj = self.pool.get("project.payroll")
        for i in self.browse(cr, uid, ids, context):
            for j in i.work_ids:
                factor = 1
                if j.tipo_jornada == "Desvelon" or i.tipo_jornada == "EspecialDoble":
                    factor = 2
                if i.tipo_jornada == "EspecialTriple":
                    factor = 3
                horas = ((j.hours * factor) / i.unidades_hora)
                nomina_obj.create(cr, uid, {
                    'empleado_id': j.empleado.id,
                    'horas': horas,
                    'monto': ((horas / 8) * j.empleado.salario_diario),
                    'relation': i.id,
                    'fecha': time.strftime('%Y-%m-%d'),
                    'tipo_jornada': j.tipo_jornada
                    })
        return ret

    def send_rrhh(self, cr, uid, ids, context=None):
        ret = {}
        bono_obj = self.pool.get("hr.bonos")
        epmloyee_obj = self.pool.get("hr.employee")
        for i in self.browse(cr, uid, ids, context):
            for j in i.nominas:
                #Calculando lo días
                dias = j.horas / 8
                resto = j.horas % 8
                faltantes = 0
                for em in epmloyee_obj.browse(cr, uid, [i.empleado_id.id]):
                    faltantes += em.adeudo_horas
                if resto > 0 and j.completar:
                    faltantes += resto
                    dias += 1
                if resto > 0 and not j.completar:
                    faltantes -= resto
                bono_obj.create(cr, uid, {
                        'empleado': j.empleado_id.id,
                        'concepto': 'Productividad ' + str(lambda *a:
                            datetime.date.today().strftime('%Y-%m-%d')),
                        'tipo': "dias",
                        'dias': dias,
                    })
                epmloyee_obj.write(cr, uid, [i.empleado_id.id], {
                        'adeudo_horas': faltantes})

            self.write(cr, uid, [i.id], {
                    'enviado': '1'
                })
        return ret

    def get_sum(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            total = 0.0
            for j in i.nominas:
                total += j.monto
            ret[i.id] = total
        return ret


    _columns = {
            'tareas': fields.one2many("project.work", 'task_id',
                string="Lineas de la Tarea"),
            'avance': fields.function(get_avance,
                string="Porcentaje de avance por tarea",
                type="float", store=True),
            'unidad': fields.many2one("ea.task.unit", "Unidad de Captura"),
            'tipo_jornada': fields.many2one("ea.tipojornada",
                "Tipo de Jornada"),
            'unidades_hora': fields.float("Unidades por Hora"),
            'nominas': fields.one2many("project.payroll", 'relation',
                string="Nominas"),
            'enviado': fields.boolean("Enviado a RRHH"),
            'nombre_proyecto': fields.related("project_id", "name",
                string="Clave", type="char"),
            'nombre_corto': fields.related("project_id", "nombre_corto",
                string="Nombre Corto", type="char"),
            'monto_nomina': fields.function(get_sum, string="Total Nomina",
                type="float"),
            'etapa': fields.function(get_etapa, string="Etapa",
                type="char"),
            'estado': fields.many2one('ea.task.state', string="Estado"),
            'project_extra_id': fields.many2one("project.task", string="Proyecto"),
            'responsible_id': fields.many2one("hr.employee",
                string="Lider del proyecto"),
            'retrabajo': fields.boolean("Retrabajo"),
            'retrabajo_ids': fields.one2many("project.retrabajo", "task_id", string="Retrabajos"),
            'observaciones': fields.text("Observaciones"),

        }

class jmd(osv.Model):
    _name = "project.retrabajo"
    _inherit = "mail.thread"
    _columns = {
        'name': fields.char("Name"),
        'fecha': fields.date("Fecha"),
        'costo': fields.float("Costo"),
        'area': fields.char("Área Implicada"),
        'task_id':fields.many2one("project.task", string="Tarea")
        }

class jmdtaskstate(osv.Model):
    _name = "ea.task.state"
    _inherit = "mail.thread"
    _columns = {
        'name': fields.char("Name"),
        'etapa': fields.char("Estado")
        }


class jmdprojectpayroll(osv.Model):
    _name = "project.payroll"

    def get_restantes(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            restantes = 8 - (i.horas % 8)
            horas_reales = restantes if restantes != 8 else 0
            ret[i.id] = horas_reales
        return ret

    def get_clave(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if i.relation and i.relation.project_id:
                ret[i.id] = i.relation.project_id.name
        return ret

    def get_ncorto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if i.relation and i.relation.project_id:
                ret[i.id] = i.relation.project_id.nombre_corto
        return ret

    def action_aprobar(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if(i.enviado):
                return
            self.write(cr, uid, [i.id], {'enviado': True})
            self.pool.get("hr.bonos").create(cr, uid, {
                'name': i.relation.name,
                'empleado': i.empleado_id.id,
                'monto': i.monto,
                'es_pi': True,
                'tipo': 'monto',
                'clave': i.relation.project_id,
                'h_envio': time.strftime('%Y-%m-%d %H:%M:%S'),
                'fecha': time.strftime('%Y-%m-%d'),
                })
        return ret

    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'empleado_id': fields.many2one("hr.employee", string="Empleado"),
            'horas': fields.float("Horas"),
            'salario': fields.related("empleado_id", "salario_diario",
                type="char", string="Salario Diario"),
            'monto': fields.float("Monto"),
            'relation': fields.many2one("project.task"),
            'restantes': fields.function(get_restantes,
                string="Horas Restantes", type="float"),
            'completar': fields.boolean("Completar día"),
            'clave': fields.function(get_clave,
                string="Clave", type="char", store=True),
            'nombre_corto': fields.function(get_ncorto,
                string="Nombre Corto", type="char", store=True),
            'enviado': fields.boolean("Enviado a RRHH"),
            'fecha': fields.date("Fecha"),
            'tipo_jornada': fields.char("Tipo de Jornada")
        }

class myclass(osv.Model):
    _name = "ea.task.unit"
    _columns = {
            'name': fields.char(string="Nombre", size=40)
        }


class jmdtipojornada(osv.Model):
    _name = "ea.tipojornada"
    _columns = {
            'name': fields.char(string="Nombre", size=40)
        }


class jmdtask(osv.Model):
    _name = "project.work"
    _columns = {
            'name': fields.char(string="Tarea", size=80),
            'avance': fields.integer("Porcentaje de Avance"),
            'terminado': fields.boolean("Terminado"),
            'task_id': fields.many2one('project.task', string="Relacion")
        }


class jmdtaskwork(osv.Model):
    _inherit = "project.task.work"
    _columns = {
            'concepto': fields.char(string="Concepto", size=40),
            'cantidad': fields.float("Cantidad"),
            'unidad': fields.many2one("product.uom", string="Unidad"),
            'avance': fields.float("Avance"),
            'factor': fields.float("Factor"),
            'empleado': fields.many2one("hr.employee", string="Realizador"),
            'tipo_jornada': fields.selection([("Normal", "Normal"),
                ("Desvelon", "Desvelon"), ("Extra", "Extra"), ("EspecialTriple", "EspecialTriple"),
                ("EspecialDoble", "EspecialDoble")],
                string="Tipo de Jornada"),
            'nombre': fields.related("empleado", "nombre", type="char",
                string="Nombre", readonly=True, store=True)
        }

    _defaults = {
            'factor': 1,
            'tipo_jornada': "normal",
        }


class jmd(osv.Model):
    _name = "ea.project.task.tipo"
    _columns = {
        'name': fields.char("Name")
        }
