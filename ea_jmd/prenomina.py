# -*- coding: utf-8 -*-
from osv import osv, fields
from datetime import date


class jmdprenomina(osv.Model):
    _name = "hr.prenomina"

    def action_borrador(self, cr, uid, ids):
            self.write(cr, uid, ids, {'state': 'borrador'})
            return True

    def action_aprobado(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'aprobado'})
        return True

    def generate_lines(self, cr, uid, ids, context=None):
        values = {}
        empleado = self.pool.get('hr.employee')
        holiday_obj = self.pool.get("hr.holidays")
        bonos_obj = self.pool.get("hr.bonos")
        descuento_obj = self.pool.get("hr.descuentos")
        dias_nomina = 15
        for i in self.browse(cr, uid, ids, context):
            #Calculando los días de la nómina
            start_date = i.inicio
            end_date = i.fin
            fechai = date(int(str(start_date).split('-')[0]),
                          int(str(start_date).split('-')[1]),
                          int(str(start_date).split('-')[2]))

            fechaf = date(int(str(end_date).split('-')[0]),
                          int(str(end_date).split('-')[1]),
                          int(str(end_date).split('-')[2]))
            dias = 1
            if start_date != end_date:
                restaFechas = fechaf - fechai
                dias = float(str(restaFechas).split(' ')[0]) + 1
            dias_nomina = dias
            #Revisando si tiene 3 domingos
            dia_semana = fechai.weekday()
            for e in empleado.browse(cr, uid, empleado.search(cr, uid, ['|',  ('sec_company', '=', i.enterprise_id.id),  ('enterprise_id', '=', i.enterprise_id.id)])):
                if e.cnomina.id != i.oficina.id:
                    print("Saltando a " + str(e.name))
                    continue
                total_dias = dias
                dias_pago = 0
                vacaciones = 0
                inasistencias = 0
                incapacidad = 0
                monto = 0
                descuentos = 0
                lista_detalles = []
                if not e.tipo_pago:
                    #raise Warning('El empleado ' + e.name +
                    #    ' no tiene tipo de pago configurado')
                    print(("Saltando a " + e.name))
                    continue
                if not e.tipo_del_contrato:
                    #raise Warning("El empleado " + e.name +
                    #    " no tiene tipo de contrato configurdo")
                    print(("Saltando a " + e.name))
                    continue
                #Tipo de pago por honorarios
                if e.tipo_pago == "productividad":
                    #Buscamos las faltas
                    for h in holiday_obj.browse(cr, uid, holiday_obj.search(cr,
                        uid, [('employee_id', '=', e.id)])):
                        print("Encontre 1")
                        inicio = h.date_from
                        print("La fecha es")
                        print(inicio)
                        if not inicio:
                            continue
                        vinicio = date(int(str(inicio).split('-')[0]),
                          int(str(inicio).split('-')[1]),
                          int(str(inicio).split('-')[2][:2]))
                        fin = h.date_to
                        vfin = date(int(str(fin).split('-')[0]),
                          int(str(fin).split('-')[1]),
                          int(str(fin).split('-')[2][:2]))
                        dias = 0
                        print(fechai)
                        print(fechaf)
                        print(vinicio)
                        print(vfin)
                        if fechai <= vinicio and fechaf >= vfin:
                            print("En el peiodo")
                            dias = h.number_of_days_temp
                        elif fechai <= vinicio:
                            print("Inicia en el periodo")
                            restaFechas = fechaf - vinicio
                            dias = int(str(restaFechas).split(' ')[0]) + 1
                        elif fechaf >= vfin:
                            print("Termina en el periodo")
                            restaFechas = vfin - fechai
                            dias = int(str(restaFechas).split(' ')[0]) + 1
                        diasdiff = vinicio - fechai
                        diasd = float(str(diasdiff).split(' ')[0]) + 1
                        print((str(diasd)))
                        factor_dia = 1.1666
                        if (dia_semana == 6) and (diasd < 7):
                            factor_dia = 2.3333
                        print("Dias")
                        print(dias)
                        print("Dias con factor")
                        if h.holiday_status_id.name != "VACACIONES":
                            if dias > 0:
                                dias = dias * factor_dia
                                print(dias)
                                print("Tipo de ausencia")
                                print((h.holiday_status_id.name))
                        if h.holiday_status_id.name == "VACACIONES":
                            if dias > 0:
                                vacaciones += dias
                                dias = dias * factor_dia
                                monto_d = dias * e.salario_diario
                                monto += monto_d
                                #Prima
                                lista_detalles.append((str(vinicio),
                                    str("Vacaciones " + str(vinicio)
                                    + " a " + str(vfin)), "N/A",
                                    str(dias), str(monto_d)))
                                ''' prima = monto_d = dias * e.salario_diario *0.25
                                monto_d += prima
                                lista_detalles.append((str(vinicio),
                                    str("Prima " + str(vinicio)
                                    + " a " + str(vfin)), "N/A",
                                    str(dias), str(prima)))'''
                                
                #Buscamos las inasistencias del empleado solo para oficina
                if e.tipo_pago == "dia":
                    #Buscando faltas
                    for h in holiday_obj.browse(cr, uid, holiday_obj.search(cr,
                        uid, [('employee_id', '=', e.id)])):
                        print("Encontre 1")
                        inicio = h.date_from
                        print("La fecha es")
                        print(inicio)
                        if not inicio:
                            continue
                        vinicio = date(int(str(inicio).split('-')[0]),
                          int(str(inicio).split('-')[1]),
                          int(str(inicio).split('-')[2][:2]))
                        fin = h.date_to
                        vfin = date(int(str(fin).split('-')[0]),
                          int(str(fin).split('-')[1]),
                          int(str(fin).split('-')[2][:2]))
                        dias = 0
                        print(fechai)
                        print(fechaf)
                        print(vinicio)
                        print(vfin)
                        if fechai <= vinicio and fechaf >= vfin:
                            print("En el peiodo")
                            dias = h.number_of_days_temp
                        elif fechai <= vinicio:
                            print("Inicia en el periodo")
                            restaFechas = fechaf - vinicio
                            dias = int(str(restaFechas).split(' ')[0]) + 1
                        elif fechaf >= vfin:
                            print("Termina en el periodo")
                            restaFechas = vfin - fechai
                            dias = int(str(restaFechas).split(' ')[0]) + 1
                        diasdiff = vinicio - fechai
                        diasd = 0
                        try:
                            diasd = float(str(diasdiff).split(' ')[0]) + 1
                        except:
                            print("Vacaciones de 0 días")
                        print((str(diasd)))
                        factor_dia = 1.1666
                        if (dia_semana == 6) and (diasd < 7):
                            factor_dia = 2.3333
                        print("Dias")
                        print(dias)
                        print("Dias con factor")
                        dias = dias * factor_dia
                        print(dias)
                        print("Tipo de ausencia")
                        print((h.holiday_status_id.name))
                        if h.holiday_status_id.name == "VACACIONES":
                            if dias > 0:
                                vacaciones += dias
                                monto_d = dias * e.salario_diario
                                dias_pago += dias
                                lista_detalles.append((str(vinicio),
                                                       str("Vacaciones " + str(vinicio)
                                                           + " a " + str(vfin)), "N/A",
                                                       str(dias), str(monto_d)))
                            #Prima
                            ''' prima = monto_d = dias * e.salario_diario *0.25
                            monto_d += prima
                            lista_detalles.append((str(vinicio),
                                str("Prima " + str(vinicio)
                                + " a " + str(vfin)), "N/A",
                                str(dias), str(prima))) '''
                        elif h.holiday_status_id.name == "INCAPACIDAD":
                            incapacidad += dias
                            monto_d = dias * e.salario_diario
                            dias_pago += dias
                            lista_detalles.append((str(vinicio),
                                str("Incapacidad " +
                                str(vinicio) + " a " + str(vfin)), "N/A",
                                str(dias), str(monto_d)))
                        elif h.holiday_status_id.name == "FALTA":
                            print("Sumando la falta")
                            inasistencias += dias
                            monto_d = dias * e.salario_diario
                            lista_detalles.append((str(vinicio),
                                str("Falta " + str(vinicio)
                                + " a " + str(vfin)), "N/A",
                                str(dias), str(monto_d)))
                #Sumando todas las bonificaciones
                for b in bonos_obj.browse(cr, uid, bonos_obj.search(cr,
                    uid, [('empleado', '=', e.id)])):
                    if not b.fecha:
                        continue
                    fbono = date(int(str(b.fecha).split('-')[0]),
                    int(str(b.fecha).split('-')[1]),
                    int(str(b.fecha).split('-')[2][:2]))
                    if fbono >= fechai and fbono <= fechaf:
                        if b.tipo == 'dias':
                            print("Sumando dias")
                            print((str(b.dias)))
                            monto_d = b.dias * e.salario_diario
                            monto += monto_d
                            lista_detalles.append((str(fbono),
                                str("Pago en días " + b.name), "N/A",
                                str(str(b.dias)), str(monto_d)))

                        elif b.tipo == 'monto':
                            print("Sumando al monto")
                            print((str(b.monto)))
                            monto += b.monto
                            lista_detalles.append((str(fbono),
                                str("Pago en dinero " + str(b.name)),
                                str(b.monto), "N/A", str(b.monto)))

                print("Bonificaciones sumadas")
                #Restando los descuentos en dia
                for d in descuento_obj.browse(cr, uid, descuento_obj.search(cr,
                    uid, [('empleado', '=', e.id)])):
                    print("Fecha del descuento")
                    try:
                        print((d.fecha))
                    except:
                        continue

                    print((str(d.id)))
                    try:
                        fdesc = date(int(str(d.fecha).split('-')[0]),
                        int(str(d.fecha).split('-')[1]),
                        int(str(d.fecha).split('-')[2][:2]))
                    except:
                        continue
                    if fdesc > fechai and fdesc < fechaf:
                        if d.tipo == 'dias':
                            print("Restando dias")
                            print((d.dias))
                            monto_d = d.dias * e.salario_diario
                            monto -= monto_d
                            descuentos += monto_d
                            lista_detalles.append((str(fdesc),
                                str("Descuento en días "
                                + str(d.name)), "N/A", str(d.dias),
                                str(monto_d)))
                        elif d.tipo == 'monto' and not d.post:
                            monto -= d.monto
                            descuentos += d.monto
                            print("Restando el monto")
                            print((d.monto))
                            print("Queda")
                            print((str(monto)))
                            lista_detalles.append((str(fdesc),
                                str("Descuento en dinero "
                                + str(d.name)),
                                str(d.monto), "N/A", str(d.monto)))
                        elif d.tipo == 'monto' and d.post:
                            descuentos += d.monto
                #Sumando
                print("Por Sumar")
                print(("Vacaciones " + str(vacaciones)))
                print(("Faltas " + str(inasistencias)))
                print(("Incapacidad " + str(incapacidad)))
                print(("Dias de la nomina " + str(total_dias)))
                if e.tipo_pago == "dia":
                    dias_pago = total_dias - vacaciones - inasistencias\
                        - incapacidad
                print("Dias por pagar")
                print(dias_pago)
                print(("Salario Diario " + str(e.salario_diario)))
                #Monto = monto + dias pagados
                sueldos = dias_pago * e.salario_diario
                print (("Sueldos " + str(sueldos)))
                if dias_pago > 0:
                    lista_detalles.append(("N/A", 'Salario en días ',
                        "", str(dias_pago), str(sueldos)))
                nomina = monto + sueldos
                print(("Monto " + str(monto)))
                print(("Nomina " + str(nomina)))
                especial = 0
                dias = dias_nomina
                print(("Salario diario " + str(e.salario_diario)))
                print(("Dias de la nomina " + str(dias)))
                tope = e.salario_diario * dias
                print(("Tope a " + str(tope)))
                if nomina > tope and e.tipo_del_contrato == 'salarios':
                    especial = nomina - tope
                    nomina = tope
                factor = 1
                
                if e.tipo_del_contrato == 'salarios':
                    if (e.salario_diario > 0):
                        '''if (nomina % e.salario_diario) != 0:
                            especial = nomina % e.salario_diario
                            nomina = (nomina // e.salario_diario) * e.salario_diario'''
                        if e.is_sec:
                            if i.enterprise_id.id == e.sec_company:
                                factor = e.sec_salario / (e.sec_salario + e.salario_diario)
                        else:
                            factor = e.salario_diario / (e.sec_salario + e.salario_diario)
                print("El descuento fue de  -----------------  " + str(descuentos))                
                values = {
                    'empleado': e.id,
                    'relation': i.id,
                    'total_dias': dias_pago,
                    'vacaciones': vacaciones,
                    'incapacidad': incapacidad,
                    'faltas': inasistencias,
                    'empresa': e.enterprise_id.name,
                    'descuentos': descuentos,
                    'nomina': nomina * factor,
                    'dinero': monto * factor,
                    'especial': especial, 
                    }
                id_linea = None
                try:
                    id_linea = self.pool.get("hr.prenomina.linea").create(cr, uid, values, context)
                    print(("Id de la Linea " + str(id_linea)))
                except:
                    continue
                for de in lista_detalles:
                    print(de)
                    if(len(de) > 0):
                        print(("ID Linea " + str(id_linea)))
                        self.pool.get("hr.prenomina.linea.detalle").create(
                            cr, uid, {'name': de[1],
                            'fecha': de[0],
                            'monto': de[2],
                            'dias': de[3],
                            'total': de[4],
                            'linea_id': id_linea})
        return {}

    def delete_lines(self, cr, uid, ids, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            for j in i.lineas:
                self.pool.get("hr.prenomina.linea").unlink(cr, uid, [j.id])
        return ret

    _columns = {
            'name': fields.char(string="Nombre", size=80),
            'inicio': fields.date("Inicio"),
            'fin': fields.date("Fin"),
            'asistencias': fields.many2one("hr.asistencias",
                     "Registro de Asistencias"),
            'acumulada': fields.many2one("hr.prenomina", "Acumular con"),
            'acumulada2': fields.many2one("hr.prenomina", "Acumular con"),
            'lineas': fields.one2many("hr.prenomina.linea", "relation",
                string="Lineas de la prenómina"),
            'state': fields.selection([('borrador', 'Borrador'),
                ('aprobado', 'Aprobado')], "Estado", readonly=True),
            'tipo': fields.selection([("normal", "Normal"),
                ("especial", "Especial")], string="Tipo de nómina"),
            'enterprise_id': fields.many2one("ea.enterprise",
                string="Empresa"),
            'oficina': fields.many2one("ea.ciudadnomina",  string="Oficina")
        }


class jmdprenominalinea(osv.Model):
    _name = "hr.prenomina.linea"

    def get_departamento(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if not i.empleado or not i.empleado.department_id:
                ret[i.id] = "No definido"
            else:
                ret[i.id] = i.empleado.department_id.name
        return ret

    def get_oficina(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            if not i.empleado :
                ret[i.id] = "No definido"
            else:
                ret[i.id] = i.empleado.cnomina.name
        return ret

    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'nombre': fields.related("empleado", "nombre", type="char",
                string="Nombre", readonly=True),
            'departamento': fields.function(get_departamento,
                string="Departamento", type="char", store=True),
            'empleado': fields.many2one("hr.employee", 'Empleado'),
            'tipo_contrato': fields.related("empleado", "tipo_del_contrato",
                type="char", string="Tipo de Contrato", readonly=True,
                store=True),
            'tipo_pago': fields.related("empleado", "tipo_pago",
                type="char", string="Forma de Pago", readonly=True,
                store=True),
            'vacaciones': fields.integer("Vacaciones"),
            'faltas': fields.integer("Faltas"),
            'incapacidad': fields.integer("Incapacidad"),
            'relation': fields.many2one("hr.prenomina", string="Nómina"),
            'salario_diario': fields.related("empleado", "salario_diario",
                type="float", string="Salario Diario",
                realtion="res.partner", digits=(6, 2),
                readonly=True, store=True),
            'total_dias': fields.float(string="Total de días"),
            'dias_trabajados': fields.integer(string="Días Trabajados",
                type="integer"),
            'dias_acumulados': fields.float(string="Días Acumulados",
            digits=(9, 2)),
            'dinero': fields.float(string="Total de Pesos"),
            'nomina': fields.float("Nómina"),
            'especial': fields.float(string="Especial"),
            'empresa': fields.char("Empresa", readonly=True),
            'detalle_ids': fields.one2many("hr.prenomina.linea.detalle",
                "linea_id", string="Detalle"),
            'descuentos': fields.float("Descuentos"),
            'cnomina': fields.function(get_oficina,
                string="Oficina Nómina", type="char", store=True),
            'es_campo': fields.related("empleado", "es_campo",
                type="boolean", string="Es Campo", readonly=True,
                store=True),
        }


class myclass(osv.Model):
    _inherit = "mail.thread"
    _name = "hr.prenomina.linea.detalle"
    
    def get_persona(self, cr, uid, ids, fieldname, args, context="None"):
        ret = {}
        # @todo: finalizar de revisar el método
        #for j in self.browse(cr, uid, ids, context):
        #    for i in self.linea_id:
        #        if not i.empleado :
        #            ret[i.id] = "No definido"
        #        else:
        #            ret[i.id] = i.empleado.nombre
        return ret
    
    _columns = {
            'fecha': fields.char(string="Fecha"),
            'name': fields.char(string="Concepto"),
            'monto': fields.char("Importe"),
            'dias': fields.char("Días"),
            "total": fields.char("Total de la Nomina"),
            "dinero": fields.char("Total"),
            "cantidad": fields.integer("Número de Entrevistas"),
            "persona": fields.function(get_persona,
                string="Persona", type="char", store=True),
            "codigos_pago": fields.char("Codigos de Pago"),
            'linea_id': fields.many2one("hr.prenomina.linea", string="Linea")
        }
