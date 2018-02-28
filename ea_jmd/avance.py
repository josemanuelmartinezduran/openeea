# -*- coding: utf-8 -*-
from osv import osv, fields
import datetime
import time


class jmdavance(osv.Model):
    _name = "ea.avance"
    _inherit = "mail.thread"

    def action_capturado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'capturado'})
        return True

    def action_enviado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'enviado'})
        return True

    def action_rh(self, cr, uid, ids):
        for i in self.browse(cr, uid, ids):
            if i.gea_sea == "SEA":
                self.write(cr, uid, ids, {'state': 'edicion'})
            else:
                self.write(cr, uid, ids, {'state': 'rh'})
        return True

    def action_edicion(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'edicion'})
        for i in self.browse(cr, uid, ids, context):
            for j in i.cuota:
                #bono para el investigador
                monto = 0.0
                superv = 0.0
                if not j.cuestionario:
                    continue
                for k in j.cuestionario.salario_ids:
                            if (k.puesto == j.empleado.job_id and
                                k.tipo == "propia"):
                                monto += k.monto
                            if (k.puesto == j.empleado.job_id and
                                k.tipo == "equipo"):
                                superv += k.monto
                #if j.empleado and j.empleado.id:
                values = {
                    'name': ("Encuesta " + j.cuestionario.name),
                    'empleado': j.empleado.id,
                    'fecha': i.fecha,
                    'tipo': 'monto',
                    'state': 'aprobado',
                    'monto': monto * j.cantidad
                    }
                self.pool.get("hr.bonos").create(cr, uid, values, context)
        return True

    def action_validado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'validado'})
        return True

    def action_pi(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'pi'})
        return True

    def before2(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if not i.h_envio:
                return
            a = i.h_envio
            b = a.find(":")
            c = b - 2
            a = a[c:b]
            ret[i.id] = False
            if a < 14:
                ret[i.id] = True
        return ret

    def get_name(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = str(i.proyecto.name) + " " +\
                str(i.plaza_id.codigo) + " " + str(i.fecha)
        return ret

    def generate_all(self,  cr,  uid,  ids, context=None):
        for i in self.browse(cr,  uid,  self.search(cr,  uid ,  [])):
            i.generate_payroll()

    def generate_payroll(self, cr, uid, ids, context=None):        
        ret = {}
        inv_gea = 0
        inv_sea = 0
        sup_gea = 0
        sup_sea = 0
        nomina_obj = self.pool.get("avance.payroll")
        excepcion_obj = self.pool.get("hr.exception")
        for i in self.browse(cr, uid, ids, context):
            print("Ciclo del objeto")
            #Eliminando las anteriores
            for n in i.nominas:
                nomina_obj.unlink(cr, uid, [n.id])
            #Eliminando las excepciones
            for e in i.excepciones_ids:
                excepcion_obj.unlink(cr, uid, [e.id])
            calculados = []
            scalculados = []
            empleado_obj = self.pool.get("hr.employee")
            for j in i.cuota:
                print("Iterando en las cuotas")
                if j.stand_by or j.rechazada:
                    excepcion_obj.create(cr, uid, {
                        'name': 'Entrevista cancelada o en pausa',
                        'description': ("Folio : " + str(j.folio)),
                        'avance_id': i.id,
                        })
                    continue
                if j.empleado.id not in calculados:
                    print(("El empleado no estaba en la lista " +
                        str(j.empleado.id)))
                    eid = j.empleado.id
                    calculados.append(eid)
                    #Verificando si el empleado esta validado para el proyecto
                    idproyecto = i.proyecto.id
                    validacion_obj = self.pool.get("empleado.validacion")
                    validado = False
                    for vd in validacion_obj.browse(cr, uid,
                        validacion_obj.search(cr, uid, [('name_related.id', '=',
                        eid)])):
                        if vd.relation and vd.relation.name:
                            if idproyecto == vd.relation.name.id:
                                validado = True
                    if not validado:
                        excepcion_obj.create(cr, uid, {
                        'name': 'Investigador no validado',
                        'description': ("Empleado : " + str(j.empleado.name)
                            + str(j.empleado.nombre)),
                        'avance_id': i.id,
                        })
                        continue
                    total = 0
                    #obteniendo el puesto del empleado
                    jobid = 0
                    print("Justo antes del ciclo")
                    print((empleado_obj.search(cr, uid, [('id', '=', eid)])))
                    print("Despues de search")
                    for em in empleado_obj.browse(cr, uid, empleado_obj.search(
                        cr, uid, [('id', '=', eid)])):
                        print(("Obteniendo el puesto" + str(em.job_id.name)))
                        if(em.job_id):
                            jobid = em.job_id.id
                    total = 0
                    conteo = 0
                    for k in i.cuota:
                        if k.empleado.id == eid:
                            print("El sueldo coincide")
                            #Leyendo los sueldos
                            for s in k.tiraje.cuestionario_id.salario_ids:
                                print("Buscando un salario que\
                                    coincida con el puesto")
                                print(("Probando puesto" + str(s.puesto.id) +
                                    "contra" + str(jobid)))
                                print(("Probando plaza" + str(s.plaza_id.id) +
                                    "contra" + str(i.plaza_id.id)))
                                print(("Probando concepto" + str(s.name.name) +
                                    "contra" + str(k.concepto.name)))
                                #s.puesto.id == jobid
                                if True and\
                                    s.plaza_id.id == i.plaza_id.id and\
                                    s.name.name == k.concepto.name:
                                    print("Sueldo encontrado")
                                    #Si es investigador
                                    print(("El tipo es " + str(s.tipo) + " " +
                                        str(s.tipo) == "propia"))
                                    if str(s.tipo) == "propia":
                                        print("Percepción propia")
                                        total = total + s.monto
                                        conteo += 1
                                        print("Sumando " + str(s.monto) + " a "
                                            + str(total))
                    #Escribiendo la nómina del empleado
                    print("La prouctividad es de -------------------------------- " + str(total))
                    if j.empleado.seagea == "sea":
                        inv_sea += 1
                    else:
                        inv_gea += 1
                    nomina_obj.create(cr, uid, {
                            'empleado_id': j.empleado.id,
                            'productividad': total,
                            'relation': i.id,
                        'conteo': conteo,
                            'descripcion': i.proyecto.name + i.plaza_id.codigo
                        })
                    if total == 0.0:
                        excepcion_obj.create(cr, uid, {
                        'name': 'Salario no encontrado',
                        'description': ("Investigador : " + str(j.empleado.name)
                            + str(j.empleado.nombre) + " Revisar puesto, plaza\
                            y criterio de pago"),
                        'avance_id': i.id,
                        })
            print("====SUPERVISOR=====")
            for j in i.cuota:
                print("Iterando en las cuotas Supervisor")
                if j.stand_by or j.rechazada:
                    continue
                if j.supervisor.id not in scalculados:
                    print(("El supervisor no estaba en la lista " +
                        str(j.supervisor.id)))
                    eid = j.supervisor.id
                    scalculados.append(eid)
                    #Verificando si el empleado esta validado para el proyecto
                    idproyecto = i.proyecto.id
                    validacion_obj = self.pool.get("empleado.validacion")
                    validado = False
                    for vd in validacion_obj.browse(cr, uid,
                        validacion_obj.search(cr, uid, [('name_related.id', '=',
                        eid)])):
                        if vd.relation and vd.relation.name:
                            if idproyecto == vd.relation.name.id:
                                validado = True
                    if not validado:
                        excepcion_obj.create(cr, uid, {
                        'name': 'Supervisor no validado',
                        'description': ("Supervisor : " + str(j.supervisor.name)
                            + str(j.supervisor.nombre)),
                        'avance_id': i.id,
                        })
                        continue
                    total = 0
                    conteo = 0
                    #obteniendo el puesto del empleado
                    jobid = 0
                    print("Justo antes del ciclo")
                    print((empleado_obj.search(cr, uid, [('id', '=', eid)])))
                    print("Despues de search")
                    for em in empleado_obj.browse(cr, uid, empleado_obj.search(
                        cr, uid, [('id', '=', eid)])):
                        print(("Obteniendo el puesto" + str(em.job_id.name)))
                        if(em.job_id):
                            jobid = em.job_id.id
                    total = 0
                    for k in i.cuota:
                        if k.supervisor.id == eid and k.tiraje.cuestionario_id.salario_ids:
                            print("El sueldo coincide")
                            #Leyendo los sueldos
                            for s in k.tiraje.cuestionario_id.salario_ids:
                                print("Buscando un salario que\
                                    coincida con el puesto")
                                print(("Probando puesto" + str(s.puesto.id) +
                                    "contra" + str(jobid)))
                                print(("Probando plaza" + str(s.plaza_id.id) +
                                    "contra" + str(i.plaza_id.id)))
                                print(("Probando concepto" + str(s.name.name) +
                                    "contra" + str(k.concepto.name)))
                                #s.puesto.id == jobid
                                if True and\
                                    s.plaza_id.id == i.plaza_id.id and\
                                    s.name.name == k.concepto.name:
                                    print("Sueldo encontrado")
                                    #Si es investigador
                                    print(("El tipo es " + str(s.tipo) + " " +
                                        str(s.tipo) == "equipo"))
                                    if str(s.tipo) == "equipo":
                                        print("Percepción de equipo")
                                        total = total + s.monto
                                        conteo += 1
                                        print("Sumando " + str(s.monto) + " a "
                                            + str(total))
                    #Escribiendo la nómina del empleado
                    if j.supervisor.seagea == "sea":
                        sup_sea += 1
                    else:
                        sup_gea += 1
                    nomina_obj.create(cr, uid, {
                            'empleado_id': j.supervisor.id,
                            'productividad': total,
                        'conteo': conteo,
                            'relation': i.id,
                            'descripcion': i.proyecto.name + i.plaza_id.codigo
                        })
                    if total == 0.0:
                        excepcion_obj.create(cr, uid, {
                        'name': 'Salario no encontrado',
                        'description': ("Empleado : " + str(j.supervisor.name)
                            + str(j.supervisor.nombre) + " Revisar puesto,\
                            plaza y criterio de pago"),
                        'avance_id': i.id,
                        })
        return ret

    def calculate_all(self,  cr,  uid,  ids,  context=None):
        for i in self.browse(cr,  uid,  self.search(cr,  uid ,  [])):
            i.calculate()
    
    def calculate(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            for j in i.nominas:
                total = 0.0
                for cp in j.conceptos_pago:
                    for lp in cp.linea_ids:
                        if str(lp.tipo) == "monto":
                            total = total + lp.monto
                        elif str(lp.tipo) == "dias":
                            total = total + (float(j.salario) * lp.dias)
                total = total + j.productividad
                self.pool.get("avance.payroll").write(cr, uid, [j.id],
                    {'monto': total})
        return ret

    def enviar_all(self,  cr,  uid,  ids,  conext=None):
        for i in self.browse(cr,  uid,  self.search(cr,  uid ,  [])):
            i.enviar_rrhh()

    def enviar_rrhh(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if i.enviada:
                pass
                #return
            for j in i.nominas:
                bono_obj = self.pool.get("hr.bonos")
                print("Enviando el bono ")
                #print("Fecha " + str(i.fecha))
                print("De la persona " + str(j.empleado_id.name))
                codigos_str = ""
                for k in j.conceptos_pago:
                    codigos_str = codigos_str + k.name + ", "
                bono_obj.create(cr, uid, {
                        'name': "Productividad " + i.tipo_reporte,
                        'cantidad': j.conteo,
                        'empleado': j.empleado_id.id,
                        'monto': j.monto,
                        'tipo': 'monto',
                        'state': 'borrador',
                        'proyecto_id': i.proyecto.id,
                        'plaza': i.plaza_id.name,
                        'codigo_plaza': i.plaza_id.codigo,
                        'codigos_pago': codigos_str,
                        'fecha': i.fecha,
                        'hora_envio': i.h_envio,
                        'folio': i.folio,
                        'reporte_id': i.id,
                        'es_tableta': i.tablets,
                        'de_reporte': True,
                        'h_envio': time.strftime('%Y-%m-%d %H:%M:%S'),
                    })
                self.write(cr, uid, [i.id], {'enviada': True})
        return ret
    
    def extraarh_all(self,  cr,  uid,  ids,  context=None):
        for i in self.browse(cr,  uid,  self.search(cr,  uid ,  [])):
            print("Haciendo " + str(i.id))
            i.extraarh()
    
    def extraarh(self, cr, uid, ids, context=None):
        ret = {}
        bono_obj = self.pool.get("hr.bonos")
        for i in self.browse(cr, uid, ids, context):
            for j in i.costo_ids:
                print("Checando a " + j.name + str(j.tipo_pago))
                #Revisamos si el empleado esta por productividad
                if j.tipo_pago == "productividad":
                    bono_obj.create(cr, uid, {
                        'name': "Productividad " + i.tipo_reporte,
                        'cantidad': 0,
                        'empleado': j.id,
                        'monto': 0,
                        'tipo': 'dias',
                        'dias': 1,
                        'state': 'borrador',
                        'proyecto_id': i.proyecto.id,
                        'plaza': i.plaza_id.name,
                        'codigo_plaza': i.plaza_id.codigo,
                        'codigos_pago': "3,",
                        'fecha': i.fecha,
                        'hora_envio': i.h_envio,
                        'folio': i.folio,
                        'reporte_id': i.id,
                        'es_tableta': False,
                        'de_reporte': True,
                        'h_envio': time.strftime('%Y-%m-%d %H:%M:%S'),
                    })
                     
        
    def unsend(self,  cr,  uid,  ids,  context=None):
        for i in self.browse(cr,  uid,  ids,  context):
            print("Unsending")
            print(i.id)
            self.write(cr,  uid, [i.id],  {'enviada': False})

    def unsend_all(self,  cr,  uid,  ids,  context=None):
        for i in self.browse(cr,  uid,  self.search(cr,  uid ,  [])):
            i.unsend()
        
    def do_reject(self, cr, uid, ids, context=None):
        avance_obj = self.pool.get("ea.avance.linea")
        rechazo_obj = self.pool.get("ea.rechazadas")
        aux_obj = self.pool.get('ea.reject')
        investigador = None
        for h in self.browse(cr, uid, ids, context):
            for i in h.aux_rechazar:
                if i.procesada:
                    continue
                cantidad_anterior = 0
                nueva_cantidad = 0
                for j in avance_obj.browse(cr, uid, [i.code], context):
                    cantidad_anterior = j.cantidad
                    nueva_cantidad = cantidad_anterior
                    investigador = j.empleado.id
                    supervisor = j.supervisor.id
                if i.cantidad <= cantidad_anterior:
                    nueva_cantidad = cantidad_anterior - i.cantidad
                avance_obj.write(cr, uid, [i.code], {'cantidad': nueva_cantidad,
                    'procesada': True})
                rechazo_obj.create(cr, uid, {
                        'investigador': investigador,
                        'revisor': i.persona.id,
                        'supervisor': supervisor,
                        'comentario': i.motivo,
                        'fase': i.avance_id.state,
                        'folio': j.folio,
                        'relation_avance': i.avance_id.id
                    })
            aux_obj.write(cr, uid, [i.id], {'procesada': "True",
                'usuario': uid})
        return {}

    def set_name(self, cr, uid, ids, fecha, context=None):
        ret = {}
        values = {}
        for i in self.browse(cr, uid, ids, context):
            values['name'] = str(i.proyecto.name) + " " +\
                str(i.plaza_id.codigo) + " " + str(fecha)
        ret['value'] = values
        return ret

    def add_lines(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            avance_obj = self.pool.get("ea.avance.linea")
            print(range(5))
            print(range(i.aux_cantidad))
            for j in range(i.aux_cantidad):
                avance_obj.create(cr, uid, {
                    'empleado': i.aux_levanto.id,
                    'supervisor': i.aux_supervisor.id,
                    'tiraje': i.aux_cuestionario.id,
                    'concepto': i.aux_criterio.id,
                    'relation_avance': i.id,
                    })
        return ret

    _columns = {
            'name': fields.function(get_name, type="char",
                string="Proyecto-Plaza-Fecha", size=80),
            'proyecto': fields.many2one("project.project", string="Proyecto"),
            'nombre_corto': fields.related('proyecto', 'nombre_corto',
                string="Nombre Corto", type="char"),
            'plaza_id': fields.many2one("plaza", string="Plaza"),
            'fecha': fields.date(string="Fecha"),
            'cuota': fields.one2many("ea.avance.linea", 'relation_avance',
                string="Linea de Avance", ondelete="cascade"),
            'concepto_ids': fields.one2many("ea.avance.concepto",
                "relation", string="Conceptos de Pago"),
            'state': fields.selection([('capturado', 'Capturado'),
                ('enviado', 'Enviado'), ('rh', 'Recursos Humanos'),
                ('edicion', 'Supervisión de Oficina'),
                ('pi', 'Procesos Intermedios'),
                ('validado', 'Validado')], "Estado"),
            'incidencia_ids': fields.one2many("ea.incidencia", "relation",
                string="Incidencias", ondelete="cascade"),
            'proyecto_id': fields.related("proyecto", "id",
                type="integer", string="Id Proyecto", store=True),
            'rechazadas_ids': fields.one2many("ea.rechazadas",
                "relation_avance", string="Encuestas Rechazadas", ondelete="cascade"),
            'h_envio': fields.datetime("Hora de envío"),
            'b42': fields.function(before2, type="boolean",
                string="Antes de las 2"),
            'aux_rechazar': fields.one2many("ea.reject", "avance_id",
                string="Rechazo"),
            'nominas': fields.one2many("avance.payroll", 'relation',
                string="Nominas", ondelete="cascade"),
            'calendarizacion': fields.binary("Calendarización"),
            'cal_name': fields.char("cal_name"),
            'observaciones': fields.text("Observaciones"),
            'supervisor': fields.many2one("hr.employee",
                string="Supervisor/Investigador"),
            'gea_sea': fields.selection([("gea", "GEA"),
                ("sea", "SEA")], string="GEA / SEA"),
            'partner_id': fields.many2one("res.partner", string="SEA"),
            'aux_levanto': fields.many2one("hr.employee", string="Levantó"),
            'aux_cantidad': fields.integer("Cantidad"),
            'aux_cuestionario': fields.many2one("ea.tiraje",
                string="Cuestionario"),
            'aux_supervisor': fields.many2one("hr.employee",
                string="Supervisor"),
            'aux_criterio': fields.many2one("ea.salario.concepto",
                string="Pago Entrevista"),
            'excepciones_ids': fields.one2many("hr.exception", "avance_id",
                string="Excepciones", ondelete="cascade"),
            'codigo_sea': fields.many2one("res.partner", "Codigo del SEA"),
            'spot': fields.char("Spot"),
            'colonia': fields.char("Colonia/CLT"),
            'delegacion': fields.char("Delegación"),
            'calle1': fields.char("Calle 1"),
            'calle2': fields.char("Calle 2"),
            'cambio': fields.boolean("Cambio de Punto"),
            'inicio': fields.datetime("Inicio"),
            'colonia2': fields.char("Colonia/CLT"),
            'calle21': fields.char("Calle"),
            'calle22': fields.char("Calle"),
            'salida_oficina': fields.datetime("Hora de Salida de Oficina"),
            'llegada_campo': fields.datetime("Hora de Llegada a Campo"),
            "termino_campo": fields.datetime("Hora de Término de Campo"),
            "tienda": fields.char("Nombre de la Tienda"),
            "sucursal": fields.char("Sucursal"),
            "total": fields.float("Total de Registros"),
            "tipo": fields.selection([('entre', 'Entre Semana'),
                ('fin', 'Fin de Semana')], string="Tipo"),
            "dia_semana": fields.selection([("Lunes", "Lunes"),
                ("Martes", "Martes"), ("Miercoles", "Miercoles"),
                ("Jueves", "Jueves"), ("Viernes", "Viernes"),
                ("Sabado", "Sabado"), ("Domingo", "Domingo")],
                string="Dia de la Semana"),
            "tipo_reporte": fields.selection([('entrevista', "Entrevista"),
                                              ('registro', 'Registro')], string="Tipo"),
            'enviada': fields.boolean("Enviada"),
            'tablets': fields.boolean("Tablets"),
            'folio': fields.char("Folio"),
            'costo_ids': fields.many2many("hr.employee",  string="Cargar costos"),
            'inv_sea': fields.integer("Investigadores SEA"),
            'inv_gea': fields.integer("Investigadores GEA"),
            'sup_gea': fields.integer("Supervisores GEA"),
            'sup_sea': fields.integer("Suérvisores SEA")
        }

    _defaults = {
            'h_envio': lambda *a:
            time.strftime('%Y-%m-%d %H:%M:%S'),
            'name': 'Proyecto-Plaza-Fecha',
            'folio': lambda self, cr, uid, context={}:
                                 self.pool.get('ir.sequence').get(cr, uid, 'ea.avance'),
        }


class jmdavancepayroll(osv.Model):
    _name = "avance.payroll"

    def ve_nomina(self, cr, uid, ids, fieldname, args, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = False
            print("El usuario puede ver nomina?")
            print((self.pool.get('res.users').has_group(cr, uid,
                'ea_jmd.ver_salarios')))
            if self.pool.get('res.users').has_group(cr, uid,
                'ea_jmd.ver_salarios'):
                res[i.id] = True
        return res

    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'empleado_id': fields.many2one("hr.employee", string="Empleado"),
            'nombre': fields.related("empleado_id", "nombre", type="char",
                string="Nombre", store=True),
            'productividad': fields.float("Productividad"),
            'salario': fields.related("empleado_id", "salario_diario",
                type="char", string="Salario Diario"),
            'monto': fields.float("Monto"),
            'relation': fields.many2one("ea.avance"),
            'conceptos_pago': fields.many2many('hr.concepto',
                string="Conceptos de Pago"),
            'descripcion': fields.char("Descripción"),
        'conteo': fields.integer("Conteo"),
            've_nomina': fields.function(ve_nomina, string="Ve Nómina",
                type="boolean", store=False),
        }


class jmdexcepcion(osv.Model):
    _inherit = "mail.thread"
    _name = "hr.exception"
    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'description': fields.char("Descripcion"),
            'avance_id': fields.many2one("ea.avance", string="Avance"),
        }


class jmdavancelinea(osv.Model):
    _name = "ea.avance.linea"

    # Employees can be searched by nombre or name
    def name_search(self, cr, uid, name, args=None, operator='ilike',
        context=None, limit=100):
        if not args:
            args = []
        args = args[:]
        ids = []
        if name:
            ids = self.search(cr, uid, [('folio', 'like', name)] + args, limit=limit)
        return self.name_get(cr, uid, ids, context=context)

    #Display both names
    def name_get(self, cr, uid, ids, context=None):
        res = []
        reads = self.read(cr, uid, ids, ['folio'])
        res = []
        for record in reads:
            if record['folio']:
                name = record['folio']
            res.append((record['id'], name))
        return res

    def get_proyecto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for linea in self.browse(cr, uid, ids, context):
            ret[linea.id] = "No Especificado"
            if linea.relation_avance and linea.relation_avance.proyecto:
                ret[linea.id] = linea.relation_avance.proyecto.id
        return ret

    def get_plaza(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for linea in self.browse(cr, uid, ids, context):
            ret[linea.id] = 0
            if linea.relation_avance and linea.relation_avance.proyecto:
                ret[linea.id] = linea.relation_avance.plaza_id.id
        return ret

    def get_plazaname(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for linea in self.browse(cr, uid, ids, context):
            ret[linea.id] = 0
            if linea.relation_avance and linea.relation_avance.proyecto:
                ret[linea.id] = linea.relation_avance.plaza_id.name
        return ret

    def get_fecha(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for linea in self.browse(cr, uid, ids, context):
            ret[linea.id] = 0
            if linea.relation_avance and linea.relation_avance.proyecto:
                ret[linea.id] = linea.relation_avance.fecha
        return ret

    def get_proyecton(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for linea in self.browse(cr, uid, ids, context):
            ret[linea.id] = "No Especificado"
            if linea.relation_avance and linea.relation_avance.proyecto:
                ret[linea.id] = linea.relation_avance.proyecto.name
        return ret

    def get_nombrecorto(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for linea in self.browse(cr, uid, ids, context):
            ret[linea.id] = "No Especificado"
            if linea.relation_avance and linea.relation_avance.proyecto:
                ret[linea.id] = linea.relation_avance.proyecto.nombre_corto
        return ret

    def get_current(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.id
        return ret

    def get_name(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = "Avance "
        return ret

    def get_cuestionario(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = 0
            if i.tiraje and i.tiraje.cuestionario_id:
                ret[i.id] = i.tiraje.cuestionario_id.id
        return ret

    def aprueba_encuesta(self, cr, uid, ids, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            print("Hola ------------- ")
        return ret

    def pausa_encuesta(self, cr, uid, ids, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            status = not i.stand_by
            self.write(cr, uid, [i.id], {"stand_by": status})
        return ret

    def count_vars(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            count = 0
            for j in i.cuota_ids:
                count += 1
            ret[i.id] = count
        return ret

    def cancela_encuesta(self, cr, uid, ids, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if i.rechazada:
                return ret
            rechazadas_obj = self.pool.get("ea.rechazadas")
            rechazadas_obj.create(cr, uid, {
                'name': i.name,
                'investigador': i.empleado.id,
                'folio': i.folio,
                'supervisor': i.supervisor.id,
                'revisor': uid,
                'fase': i.relation_avance.state,
                'relation_avance': i.relation_avance.id,
                })
            self.write(cr, uid, [i.id],
                {'rechazada': True})
            #Generando el descuento
            monto = 0.0
            if i.tiraje and i.tiraje.cuestionario_id:
                print("Entrando -----------  ------------")
                for j in i.tiraje.cuestionario_id.salario_ids:
                    print("Salario " + str(j.id) + " Tipo" + str(j.tipo))
                    print("Id Plaza " + str(j.plaza_id.id) + "vs" +
                        str(i.relation_avance.plaza_id.id))
                    print("Concepto" + str(j.name.name) + "vs" + str(i.concepto.name))
                    print("Revisando" + str((j.tipo) == "propia"))
                    if str(j.tipo) == "propia":
                        print("Tipo OK")
                        if j.plaza_id and j.plaza_id.id is\
                        i.relation_avance.plaza_id.id:
                            print("Plaza OK")
                            if j.name.name is i.concepto.name:
                                print ("Concepto OK")
                                print("El monto es" + str(j.monto) +
                                    j.name.name)
                                monto = j.monto
                                break
            descuento_obj = self.pool.get("hr.descuentos")
            descuento_obj.create(cr, uid, {
                'empleado': i.empleado.id,
                'fecha': i.relation_avance.fecha,
                'name': "Entrevista cancelada folio" + str(i.folio),
                'tipo': "monto",
                'monto': monto,
                'fecha_reporte': i.relation_avance.fecha,
                'fase': i.relation_avance.state,
                'proyecto_id': i.relation_avance.proyecto.id,
                })
        return ret

    def get_idestudio(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = i.proyecto
        return ret

    _columns = {
            'name': fields.char(string="Nombre", size=40, store=True),
            'cantidad': fields.integer("Cantidad"),
            'cuestionario': fields.many2one('ea.encuesta',
                string="Cuestionario"),
            'cuota': fields.many2one("ea.cuota", string="Cuota"),
            'relation_avance': fields.many2one("ea.avance"),
            'empleado': fields.many2one("hr.employee", string="Levantó"),
            'supervisor': fields.many2one("hr.employee", string="Supervisó"),
            'proyecto': fields.function(get_proyecto, string="Proyecto",
                type="integer", store=True),
            'id_proyecto': fields.function(get_proyecto, string="Proyecto",
                type="char", store=True),
            'project_name': fields.function(get_proyecton, string="Clave",
                type="char", store=True),
            'nombre_corto': fields.function(get_nombrecorto, string="Nombre Corto",
                type="char", store=True),
            'current_id': fields.function(get_current, type="integer",
                string="Id", store=True),
            'cuota_ids': fields.many2many('ea.cuota', 'avance_cuota_rel',
                'avance_linea_id', 'ea_cuota_id', string='Cuotas'),
            'folio': fields.char("Folio"),
            'stand_by': fields.boolean("En Pausa"),
            'rechazada': fields.boolean("Rechazada"),
            'supervision': fields.many2many("ea.tipo_supervision",
                string="Tipo de Supervisión"),
            'sup_oficina': fields.many2many("ea.tipo_supervision", "ofc_sup",
                "f1", "f2", string="Supervisión de Oficina"),
            'plaza_id': fields.function(get_plaza, string="Plaza",
                type="integer", store=True),
            'plaza_name': fields.function(get_plazaname, string="Plaza",
                type="char", store=True),
            'fecha': fields.function(get_fecha, string="Fecha",
                type="date", store=True),
            'tiraje': fields.many2one("ea.tiraje", "Tiraje"),
            'idcuestionario': fields.function(get_cuestionario,
                string="Id Cuestionario", type="char"),
            'concepto': fields.many2one("ea.salario.concepto",
                string="Pago Entrevista"),
            'conteo': fields.function(count_vars, string="Variables",
                type="char"),
            'ntienda': fields.char("Nombre Tienda"),
            'sucursal': fields.char("Sucursal"),
            'dia_semana': fields.selection([('Lunes', 'Lunes'),
                ('Martes', 'Martes'), ('Miercoles', 'Miercoles'),
                ('Jueves', 'Jueves'), ('Viernes', 'Viernes'),
                ('Sabado', 'Sabado'), ('Domingo', 'Domingo')],
                string="Día de la Semana"),
            'estudioid': fields.function(get_idestudio,
                string="Id Estudio", type="char", store=True),
        }

    _defaults = {
        'name': "Avance"
        }


class jmdsupervision(osv.Model):
    _name = "ea.tipo_supervision"
    _columns = {
            'name': fields.char(string="Nombre", size=60),
            'sup_oficina': fields.many2many("ea.avance.linea", "ofc_sup",
                "f2", "f1", string="Supervision de oficina"),
        }


class jmdavanceconcepto(osv.Model):
    _name = "ea.avance.concepto"
    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'empleado': fields.many2one("hr.employee", string="Persona",
                ondelete="set null"),
            'concepto': fields.many2one("hr.concepto",
                string="Concepto de Pago", ondelete="set null"),
            'relation': fields.many2one("ea.avance"),
            'monto': fields.float(digits=(9, 2), string="Monto"),
            'comentario': fields.char("Comentario")
        }


class jmdrechazadas(osv.Model):
    _name = "ea.rechazadas"
    _columns = {
            'name': fields.char(string="Estudio", size=40),
            'investigador': fields.many2one("hr.employee",
                string="Investigador"),
            'folio': fields.char("Folio"),
            'supervisor': fields.many2one("hr.employee",
                string="Supervisor"),
            'revisor': fields.many2one("res.users",
                string="Revisor"),
            'fecha': fields.date("Fecha"),
            'comentario': fields.text("Comentario"),
            'fase': fields.selection([("rh", "Recursos Humanos"),
                ("edicion", "Edición"), ("pi", "Procesos Intermedios")],
                string="Fase de rechazo"),
            'relation_avance': fields.many2one("ea.avance", strging="Avance")
        }
    _defaults = {
            'fecha': lambda *a: datetime.date.today().strftime('%Y-%m-%d'),
            'fase': "rh"
        }


class jmdreject(osv.Model):
    _name = "ea.reject"

    _columns = {
            'code': fields.integer('ID'),
            'cantidad': fields.integer("Cantidad"),
            'motivo': fields.char("Motivo", size=250),
            'procesada': fields.boolean("Rechazo Procesado"),
            'usuario': fields.many2one("res.users", string="Usuario"),
            'persona': fields.many2one("hr.employee", string="Revisor"),
            'avance_id': fields.many2one("ea.avance")
        }

    _defauls = {
            'cantidad': 1,
        }
