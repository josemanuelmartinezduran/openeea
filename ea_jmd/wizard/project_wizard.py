# -*- coding: utf-8 -*-
from osv import osv, fields
from openerp.exceptions import Warning


class projectwizard(osv.Model):
    _name = "ea.project_wizard"
    _inherit = "mail.thread"

    def populate(self, cr, uid, ids, context=None):
        ret = {}
        return ret

    def on_change_cotizacion(self, cr, uid, ids, saleorder_id, context=None):
        ret = {}
        values = {}
        print("I'm here")
        sales_obj = self.pool.get("sale.order")
        tid = 0
        for i in self.browse(cr, uid, ids, context):
            tid = i.id
        for j in sales_obj.browse(cr, uid, [saleorder_id], context):
            values['name'] = j.name
            values['nombre_corto'] = j.nombre_corto
            values['planeacion'] = j.budget.id
            values['cuotas'] = j.cuotas.id
            values['ent'] = j.ent
            values['observaciones'] = j.observaciones
            values['metodologia'] = j.metodologia
            values['objetivo'] = j.objetivo
            values['tiempos'] = []
            values['tmuestra'] = j.tmuestra
            values['ttiempos'] = j.ttiempos
            values['levantamiento'] = j.tipo_levantamiento

            print(ids)
            for k in j.tiempos:
                nid = self.pool.get("ea.tiempos").create(cr, uid, {
                    'fechas': k.fechas,
                    'name': k.name,
                    'odt': tid,
                    })
                values['tiempos'].append((4, nid))
            values['muestra'] = []
            for k in j.muestra:
                nid = self.pool.get("ea.muestra").create(cr, uid, {
                    'name': k.name,
                    'porcetaje': k.porcentaje,
                    'cantidad': k.cantidad,
                    'odt': tid,
                    })
                values['muestra'].append((4, nid))
        ret['value'] = values
        return ret

    def create_project(self, cr, uid, ids, context=None):
        print("Ejecutando el método")
        project_obj = self.pool.get("project.project")
        for i in self.browse(cr, uid, ids, context):
            if not i.cotizacion_id:
                raise Warning(('Error'), ('No hay cotización, el proyecto no fu&eacute; creado'))
                return {}
            if not i.cotizacion_id.confirmada:
                raise Warning(('Error'), ('La cotizacion no ha sido autorizada, el proyecto no fue creado'))
                return {}
            if i.creado:
                raise Warning(('Error'), ('El proyecto ya había sido creado'))
                return {}
            #Creando el proyecto general
            print("Entrando en el ciclo")
            values = {}
            values['name'] = i.name
            model_ids = self.pool.get('ir.model').search(cr, uid, [('model',
            '=', 'project.task')])
            values['alias_model_id'] = model_ids[0]
            values['alias_name'] = i.name
            values['etapa'] = "proyecto"
            values['date_start'] = i.date_start
            values['date'] = i.date_end
            values['nombre_corto'] = i.nombre_corto
            values['planeacion'] = i.planeacion.id
            values['cuotas'] = i.cuotas.id
            values['fecha_tabulacion'] = i.fecha_tabulacion
            values['fecha_analisis'] = i.fecha_analisis
            values['demografico'] = i.demografico
            values['levantamiento'] = i.levantamiento
            print("Por crear el proyecto")
            #Este es el padre de todos los de abajo
            #parent_id = project_obj.create(cr, uid, values, context)
            parent_id = project_obj.create(cr, uid, values, context)
            print("Proyecto creado")
            #Flashes
            for j in i.flash_ids:
                self.pool.get("ea.flash").write(cr, uid, [j.id], {'project_id': parent_id})
            #Creando proyecto de arranques
            values_arranques = {}
            values_arranques['name'] = i.name + "- Arranques"
            values_arranques['alias_model_id'] = model_ids[0]
            values_arranques['alias_name'] = i.name + "- Arranques"
            values_arranques['etapa'] = "arranques"
            values_arranques['date_start'] = i.arranques_date_start
            values_arranques['date'] = i.arranques_date_start
            values_arranques['responsible_id'] = i.arranques_responsible_id.id
            values_arranques['nombre_corto'] = i.nombre_corto
            values_arranques['parent_proj_id'] = parent_id
            print("Por crear arranques")
            print((type(values_arranques)))
            for pp, qq in (list(values_arranques.items())):
                print((str(pp) + "valor" + str(qq)))
            project_obj.create(cr, uid, values_arranques, context)
            print("Arranques creado")
            #Creando proyecto de campo
            values_campo = {}
            values_campo['name'] = i.name + "- Campo"
            values_campo['alias_model_id'] = model_ids[0]
            values_campo['alias_name'] = i.name + "- Campo"
            values_campo['etapa'] = "campo"
            values_campo['date_start'] = i.campo_date_start
            values_campo['date'] = i.campo_date_end
            values_campo['responsible_id'] = i.campo_responsible_id.id
            values_campo['nombre_corto'] = i.nombre_corto
            values_campo['parent_proj_id'] = parent_id
            print("Por crear campo")
            project_obj.create(cr, uid, values_campo, context)
            print("Campo creado")
            #Creando proyecto de pi
            values_pi = {}
            values_pi['name'] = i.name + "- PI"
            values_pi['alias_model_id'] = model_ids[0]
            values_pi['alias_name'] = i.name + "- PI"
            values_pi['etapa'] = "pi"
            values_pi['date_start'] = i.pi_date_start
            values_pi['date'] = i.pi_date_end
            values_pi['responsible_id'] = i.pi_responsible_id.id
            values_pi['nombre_corto'] = i.nombre_corto
            values_pi['parent_proj_id'] = parent_id
            print("Por crear pi")
            project_obj.create(cr, uid, values_pi, context)
            print("PI creado")
             #Creando proyecto de Diseño
            values_dg = {}
            values_dg['name'] = i.name + "- Diseño"
            values_dg['alias_model_id'] = model_ids[0]
            values_dg['alias_name'] = i.name + "- Diseño"
            values_dg['etapa'] = "diseno"
            values_dg['date_start'] = i.pi_date_start
            values_dg['date'] = i.pi_date_end
            values_dg['responsible_id'] = i.dg_responsible_id.id
            values_dg['nombre_corto'] = i.nombre_corto
            values_dg['parent_proj_id'] = parent_id
            print("Por crear dg")
            project_obj.create(cr, uid, values_dg, context)
            print("Diseño creado")
            #Creando proyecto de SO
            values_so = {}
            values_so['name'] = i.name + "- Supervisión de Oficina"
            values_so['alias_model_id'] = model_ids[0]
            values_so['alias_name'] = i.name + "- PI"
            values_so['etapa'] = "supervision"
            values_so['date_start'] = i.so_date_start
            values_so['date'] = i.so_date_end
            values_so['responsible_id'] = i.so_responsible_id.id
            values_so['nombre_corto'] = i.nombre_corto
            values_so['parent_proj_id'] = parent_id
            print("Por crear so")
            project_obj.create(cr, uid, values_so, context)
            print("Supervisión de Oficina creado")
            #Creando proyecto de procesamiento
            values_procesamiento = {}
            values_procesamiento['name'] = i.name + "- Procesamiento"
            values_procesamiento['alias_model_id'] = model_ids[0]
            values_procesamiento['alias_name'] = i.name + "- Procesamiento"
            values_procesamiento['etapa'] = "procesamiento"
            values_procesamiento['date_start'] = i.procesamiento_date_start
            values_procesamiento['date'] = i.procesamiento_date_end
            values_procesamiento['responsible_id'] = \
            i.procesamiento_responsible_id.id
            values_procesamiento['nombre_corto'] = i.nombre_corto
            values_procesamiento['parent_proj_id'] = parent_id
            print("Por crear proesamiento")
            project_obj.create(cr, uid, values_procesamiento, context)
            print("Por crear procesamiento creado")
            #Creando proyecto de analisis
            values_analisis = {}
            values_analisis['name'] = i.name + "- Analisis"
            values_analisis['alias_model_id'] = model_ids[0]
            values_analisis['alias_name'] = i.name + "- Analisis"
            values_analisis['etapa'] = "analisis"
            values_analisis['date_start'] = i.analisis_date_start
            values_analisis['date'] = i.analisis_date_end
            values_analisis['responsible_id'] = i.analisis_responsible_id.id
            values_analisis['nombre_corto'] = i.nombre_corto
            values_analisis['parent_proj_id'] = parent_id
            print("Por crear analisis")
            project_obj.create(cr, uid, values_analisis, context)
            print("Analisis creado")
            #Creando proyecto de entrega
            values_entrega = {}
            values_entrega['name'] = i.name + "- Entrega"
            values_entrega['alias_model_id'] = model_ids[0]
            values_entrega['alias_name'] = i.name + "- Entrega"
            values_entrega['etapa'] = "entrega"
            values_entrega['date_start'] = i.entrega_date_start
            values_entrega['date'] = i.entrega_date_start
            values_entrega['responsible_id'] = i.entrega_responsible_id.id
            values_entrega['nombre_corto'] = i.nombre_corto
            values_entrega['parent_proj_id'] = parent_id
            print("Por crear entrega")
            project_obj.create(cr, uid, values_entrega, context)
            print("Entrega creado")
            self.write(cr, uid, [i.id], {'creado': True})
        return {}

    _columns = {
            'name': fields.char(string="Nombre del proyecto",
                                size=120, translate=False),
            'nombre_corto': fields.char(string="Nombre corto", size=40),
            'planeacion': fields.many2one("ea.presupuesto", "Planeación"),
            'cuotas': fields.many2one("control_encuestas",
                "Cuotas del Proyecto"),
            'executive_id': fields.many2one("hr.employee",
                string="Ejecutivo"),
            'ejnombre': fields.related("executive_id", "nombre", type="char",
                string="Nombre", readonly=True, store=True),
            'date_start': fields.date("Fecha de inicio"),
            'date_end': fields.date("Fecha de finalización"),
            'arranques_responsible_id': fields.many2one("hr.employee",
                string="Responsable de Arranques"),
            'aname': fields.related("arranques_responsible_id", "nombre",
                type="char", string="Nombre", readonly=True, store=True),
            'arranques_date_start': fields.date("Fecha de inicio"),
            'arranques_date_end': fields.date("Fecha de finalización"),
            'campo_responsible_id': fields.many2one("hr.employee",
                string="Responsable de Campo"),
            'cname': fields.related("campo_responsible_id", "nombre",
                type="char", string="Nombre", readonly=True, store=True),
            'campo_date_start': fields.date("Fecha de inicio"),
            'campo_date_end': fields.date("Fecha de finalización"),
            'no_campo': fields.boolean("Sin campo"),
            'pi_responsible_id': fields.many2one("hr.employee",
                string="Responsable de PI"),
            'pname': fields.related("pi_responsible_id", "nombre",
                type="char", string="Nombre", readonly=True, store=True),
            'pi_date_start': fields.date("Fecha de inicio"),
            'pi_date_end': fields.date("Fecha de finalización"),
            'no_pi': fields.boolean("Sin PI"),
            'dg_responsible_id': fields.many2one("hr.employee",
                string="Responsable de Diseño"),
            'dname': fields.related("pi_responsible_id", "nombre",
                type="char", string="Nombre", readonly=True, store=True),
            'dg_date_start': fields.date("Fecha de inicio"),
            'dg_date_end': fields.date("Fecha de finalización"),
            'no_dg': fields.boolean("Sin Diseño"),
            'so_responsible_id': fields.many2one("hr.employee",
                string="Responsable de Supervision de Oficina"),
            'sname': fields.related("so_responsible_id", "nombre",
                type="char", string="Nombre", readonly=True, store=True),
            'so_date_start': fields.date("Fecha de inicio"),
            'so_date_end': fields.date("Fecha de finalización"),
            'no_so': fields.boolean("Sin Supervisión de Oficina"),
            'edicion_responsible_id': fields.many2one("hr.employee",
                string="Responsable de Edición"),
            'ename': fields.related("edicion_responsible_id", "nombre",
                type="char", string="Nombre", readonly=True, store=True),
            'edicion_date_start': fields.date("Fecha de inicio"),
            'edicion_date_end': fields.date("Fecha de finalización"),
            'no_edicion': fields.boolean("Sin Edición"),
            'procesamiento_responsible_id': fields.many2one("hr.employee",
                string="Responsable de Procesamiento"),
            'prname': fields.related("procesamiento_responsible_id", "nombre",
                type="char", string="Nombre", readonly=True, store=True),
            'procesamiento_date_start': fields.date("Fecha de inicio"),
            'procesamiento_date_end': fields.date("Fecha de finalización"),
            'no_procesamiento': fields.boolean("No procesamiento"),
            'analisis_responsible_id': fields.many2one("hr.employee",
                string="Responsable de Análisis"),
            'anname': fields.related("analisis_responsible_id", "nombre",
                type="char", string="Nombre", readonly=True, store=True),
            'analisis_date_start': fields.date("Fecha de inicio"),
            'analisis_date_end': fields.date("Fecha de finalización"),
            'no_analisis': fields.boolean("Sin Análisis"),
            'entrega_responsible_id': fields.many2one("hr.employee",
                string="Responsable de Entrega"),
            'ename': fields.related("entrega_responsible_id", "nombre",
                type="char", string="Nombre", readonly=True, store=True),
            'entrega_date_start': fields.date("Fecha de inicio"),
            'entrega_date_end': fields.date("Fecha de finalización"),
            'fecha_analisis': fields.date("Fecha de entrega de\
                 plan de análisis"),
            'fecha_tabulacion': fields.date("Fecha de entrega del plan \
                de tabulación"),
            'has_flash': fields.boolean("Tiene Flash"),
            'flash_date': fields.date("Fecha del Flash"),
            'cotizacion_id': fields.many2one("sale.order", "Cotización"),
            'fecha_capacitacion': fields.date("Fecha de Capacitación"),
            'metodologia': fields.related("cotizacion_id", "metodologia",
                type="text", string="Metodologia"),
            'objetivo': fields.related("cotizacion_id", "objetivo",
                type="text", string="Objetivo"),
            'manejo': fields.text("Manejo de Producto"),
            'observaciones': fields.text("Observaciones"),
            'creado': fields.boolean("Proyecto Creado"),
            'descripcion': fields.char("Descripción"),
            'fecha_expedicion': fields.date("Fecha de Expedición"),
            'version': fields.char("Versión"),
            'ent': fields.text("Entregables"),
            'tiempos': fields.one2many("ea.tiempos", 'odt',
                string="Tiempos"),
            'muestra': fields.one2many("ea.muestra", 'odt',
                string="Muestra"),
            'ttiempos': fields.text("Tiempos"),
            'tmuestra': fields.text("Muestra"),
            'adicional': fields.text("Información Adicional"),
        'demografico': fields.char("Demográfico Manejado"),
        'levantamiento': fields.char("Tipo de Levantamiento"),
        'flash_ids': fields.one2many("ea.flash", "odt_id", string="Flashes"),
        'duracion': fields.char("Duración de la Entrevista")
        }

    _defaults = {
            'manejo': '<strong>Descripción y especificaciones del \
            "<i>Uso de productos de prueba u otros estímulos \
            ISO 20252:2012, 4.7.1</i>" </strong> \
            <br /><br /> \
            En caso de que el Líder de Proyecto (Dir. Cta., y/o EC) No\
            especifiquen qué hacer con los productos y/o materiales al \
            término del estudio en campo: <i>"Los recipientes, desechos o \
            producto sobrantes no reclamados por el cliente, serán\
            eliminados en condiciones seguras sin causar riesgo para las \
            personas o el medio ambiente 15 días posteriores al término del \
            proyecto/estudio"</i>, tal como se especifica en la Propuesta \
            cotización.'
            }


class jmdflash(osv.Model):
    _name = "ea.flash"
    _inherit = "mail.thread"
    _columns = {
        'name':fields.char("Descripción"),
        'fecha': fields.date("Fecha del Flash"),
        'odt_id': fields.many2one("ea.project_wizard", string="OdT"),
        'project_id': fields.many2one("project.project", string="Proyecto"),
    }
