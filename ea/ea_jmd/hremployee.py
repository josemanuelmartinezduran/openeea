# -*- coding: utf-8 -*-
from osv import osv, fields
import time


class jmdhremployee(osv.Model):
    _inherit = "hr.employee"

    # Employees can be searched by nombre or name
    def name_search(self, cr, uid, name, args=None, operator='ilike',
        context=None, limit=100):
        if not args:
            args = []
        args = args[:]
        ids = []
        if name:
            ids = self.search(cr, uid, ['|', ('nombre', 'like', name),
                ('name', 'like', name)] + args, limit=limit)
        return self.name_get(cr, uid, ids, context=context)
        
    
    def set_hollydas(self,  cr,  uid,  ids,  context=None):
        employee_obj = self.pool.get("hr.employee")
        hollyday_obj = self.pool.get("hr.holidays")
        print("Inside")
        for i in employee_obj.browse(cr,  uid,  employee_obj.search(cr,  uid,  [('seagea', '=', 'gea')])):
            print("Generando vacaciones empleado")
            print(i.name)
            hollyday_obj.create(cr,  uid,  {'name': "Asignación", 
                'employee_id': i.id, 
                'number_of_days_temp': 12, 
                'holiday_type': "employee", 
                'holiday_status_id': 13, 
                'type': "add", 
                },  context)

    #Display both names
    def name_get(self, cr, uid, ids, context=None):
        res = []
        reads = self.read(cr, uid, ids, ['nombre', 'name'])
        res = []
        for record in reads:
            name = record['name']
            if record['nombre']:
                name = name + ' ' + record['nombre']
            res.append((record['id'], name))
        return res

    def update_validation(self, cr, uid, ids, context=None):
        ret = {}
        validation_obj = self.pool.get("capacitacion.validacion")
        emp_obj = self.pool.get("hr.employee.valid")
        for i in self.browse(cr, uid, ids, context):
            for l in i.validaciones:
                emp_obj.unlink(cr, uid, [l.id], context)
            for j in validation_obj.browse(cr, uid,
                validation_obj.search(cr, uid, [(1, '=', 1)])):
                for k in j.empleado:
                    if str(k.name_related.name) == str(i.name) and k.validado:
                        emp_obj.create(cr, uid, {
                            'name': i.nombre,
                            'estudio': j.name.id,
                            'fecha': k.fecha_validacion,
                            'relation': i.id
                            })
        return ret

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

    def ve_bancos(self, cr, uid, ids, fieldname, args, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = False
            print("El usuario puede ver bancos?")
            print((self.pool.get('res.users').has_group(cr, uid,
                'ea_jmd.ver_bancos')))
            if self.pool.get('res.users').has_group(cr, uid,
                'ea_jmd.ver_bancos'):
                res[i.id] = True
        return res

    def _get_beneficiario(self, cr, uid, ids, context=None):
        value = ""
        for i in self.browse(cr, uid, ids, context):
            value = i.nombre
        return value

    def salir(self, cr, uid, ids, context=None):
        value = ""
        for i in self.browse(cr, uid, ids, context):
            for j in i.salida_ids:
                print("----------------")
                print(j.egreso)
                if j.egreso == False:
                    self.pool.get("ea.salida").write(cr, uid, [j.id], {
                        'egreso': time.strftime('%Y-%m-%d'),
                })
        return value

    def entrar(self, cr, uid, ids, context=None):
        value = ""
        for i in self.browse(cr, uid, ids, context):
            self.pool.get("ea.salida").create(cr, uid, {
                'employee_id': i.id,
                })
        return value


    def set_director(self, cr, uid, ids, departamento, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            dtp_obj = self.pool.get("hr.direccion")
            for j in dtp_obj.browse(cr, uid, dtp_obj.search(cr, uid, [('id', '=', departamento)])):
                res['parent_id'] = j.director_id.id
        return {'value': res}

    _columns = {
            'tipo_del_contrato': fields.selection([("salarios", "Nómina"),
                ("honorarios", "Honorarios")], string="Tipo de Contrato"),
            'tipo_pago': fields.selection([("dia", "Sueldo Fijo"),
                ("productividad", "Productividad")], string="Tipo de Pago"),
            'day_wage': fields.float(digits=(9, 2), string="Salario Diario"),
            'nombre': fields.char("Nombre Completo"),
            'seagea': fields.selection([('gea', 'GEA'), ('sea', 'SEA')],
                "GEA/SEA"),
            'nombre_oficina': fields.char("Nombre de Oficina"),
            'validaciones': fields.one2many("hr.employee.valid", "relation",
                string="Validaciones"),
            'beneficiario': fields.char("Beneficiario"),
            'banco': fields.char("Banco"),
            'cuenta': fields.char("Número de Cuenta"),
            'oficina': fields.char("Oficina"),
            'categoria': fields.char("Categoria"),
            'enterprise_id': fields.many2one("ea.enterprise",
                string="Empresa"),
            'adeudo_horas': fields.integer("Adeudo en Horas"),
            've_nomina': fields.function(ve_nomina, string="Ve Nómina",
                type="boolean", store=False),
            've_bancos': fields.function(ve_nomina, string="Ve Bancos",
                type="boolean", store=False),
            'calle': fields.char("Calle y Número"),
            'numero': fields.char("Número"),
            'tel_particular': fields.char("Teléfono Particular"),
            'colonia': fields.char("Colonia"),
            'colonia_id': fields.many2one("utils.colonia", string="Colonia"),
            'delegacion': fields.char("Delegación o Municipio"),
            'cp': fields.char("Código Postal"),
            'rfc': fields.char("RFC"),
            'curp': fields.char("CURP"),
            'homoclave': fields.char("Homoclave"),
            'nacimiento': fields.date("Fecha de Nacimiento"),
            'escolaridad': fields.selection([('Primaria', 'Primaria'), ('Secundaria', 'Secundaria'),
                ('Bachillerato','Bachillerato'), ('BachilleratoTrunco', 'Bachillerato Trunco'),
                ('Tecnico', 'Técnico'), ('LicenciaturaTrunca', 'Licenciatura Trunca'),
                ('Licenciatura', 'Licenciatura'), ('Maestria', 'Maestría'), ('Doctorado', 'Doctorado')],
                string="Escolaridad"),
            'particular': fields.boolean("Escuela Particular"),
            'sucursal': fields.many2one("hr.sucursal", "Sucursal"),
            'curso_ids': fields.one2many("hr.cursos", "employee_id", string="Cursos"),
            'contacto': fields.char("Contacto de Emergencia"),
            'tel_emergencia': fields.char("Teléfono de Emergencia"),
            'sangre': fields.selection([('O', 'O'), ('A', 'A'), ('B', 'B'), ('AB', 'AB')],
                "Tipo de Sangre"),
            'factor_rh': fields.selection([('Positivo', 'Positivo'), ('Negativo', 'Negativo')],
                "Factor RH"),
            'estado': fields.char("Estado"),
            'marital': fields.selection([("single", "Soltero"),("married", "Casado"),
                ("free", "Unión Libre")], string="Estado Civil"),
            'oficina_id': fields.many2one("ea.oficina", string="Oficina"),
            'es_foraneo': fields.boolean("Foraneo"),
            'provincia_id': fields.many2one("ea.provincia", string="Provincia"),
            'es_campo': fields.boolean("Pertenece a Campo"),
            'salida_ids': fields.one2many('ea.salida', 'employee_id'),
            'certificado': fields.char("Certificado Presentado"),
            'categoria_id': fields.many2one("ea.categoria", string="Categoría"),
            'direccion_id': fields.many2one("hr.direccion", string="Dirección"),
            'telefono_recados': fields.char("Teléfono de Recados"),
            'nacionalidad': fields.many2one('ea.nacionalidad', "Nacionalidad"),
            'cnomina': fields.many2one("ea.ciudadnomina", string="Oficina Nómina"), 
            'is_sec': fields.boolean("Empresa secundaria"), 
            'sec_company': fields.many2one("ea.enterprise",  string="Empresa Secundaria"), 
            'sec_salario': fields.float("Salario de Compañia Secundaria")
        }

    _sql_constraints = [
        ('unique_name', 'unique(name_related)', 'Ya existe ese empleado.'),
        ('unique_curp', 'unique(curp)', 'Ya existe ese empleado, CURP repetido.'),
        ]

    _defaults = {
            'seagea': 'gea',
            'banco': "Banamex",
            'nacionalidad': 1,
        }


class jmdnacionalidad(osv.Model):
    _name="ea.nacionalidad"
    _inherit="mail.thread"
    _columns = {
            'name': fields.char("Nacionalidad"),
        }


class jmddireccion(osv.Model):
    _name="hr.direccion"
    _inherit="mail.thread"
    _columns = {
            'name': fields.char("Nombre"),
            'director_id': fields.many2one("hr.employee", string="Director")
        }


class jmdcategoria(osv.Model):
    _name="ea.categoria"
    _inherit = "mail.thread"
    _columns = {
            'name': fields.char("Nombre"),
            'descripcion': fields.char("Descripción"),
            'job_id': fields.many2one("hr.job", string="Puesto")
        }


class jmdsalida(osv.Model):
    _name="ea.salida"
    _inherit="mail.thread"
    _columns = {
            'name': fields.date("Fecha de Reingreso"),
            'egreso': fields.date("Fecha de Baja"),
            'motivo': fields.char("Motivo"),
            'employee_id': fields.many2one("hr.employee", string="Empleado")
        }
    _defaults = {
        'name': lambda *a:time.strftime('%Y-%m-%d'),
        }


class jmdcursos(osv.Model):
    _name = "hr.cursos"
    _inherit = "mail.thread"
    _columns = {
        'name': fields.char("Nombre del Curso"),
        'evento': fields.many2one("event.event", string="Evento al que asistió"),
        'dh3': fields.boolean("DC3"),
        'fecha': fields.date("Fecha"),
        'employee_id': fields.many2one("hr.employee", string="Empleado")
        }

class jmddiploma(osv.Model):
    _name = "hr.diploma"
    _colums = {
        'name': fields.char("Nombre"),
        'entregado': fields.boolean("Entregado"),
        'empleado_id': fields.many2one("hr.employee", string="Empleado"),
        }

class jmdsucursal(osv.Model):
    _name = "hr.sucursal"
    _colums = {
        'name': fields.char("Nombre")
        }

class jmdvalidemployee(osv.Model):
    _name = "hr.employee.valid"
    _columns = {
            'name': fields.char(string="Nombre del Empleado", size=40),
            'estudio': fields.many2one("project.project",
                string="Clave del Estudio"),
            'diploma': fields.boolean("Diploma Entregado"),
            'nombre_corto': fields.related("estudio", "nombre_corto",
                type="char", string="Nombre Corto", readonly=True, store=True),
            'fecha': fields.date("Fecha"),
            'relation': fields.many2one("hr.employee")
        }


class jmdcontract(osv.Model):
    _inherit = "hr.contract"
    _columns = {
        'nombre': fields.related("employee_id", "nombre", type="char",
            string="Nombre", readonly=True, store=True)
        }


class jmdevaluation(osv.Model):
    _inherit = "hr.evaluation.interview"
    _columns = {
            'nombre': fields.related("user_to_review_id", "nombre",
                type="char", string="Nombre", readonly=True, store=True)
        }


class jmdevaluationl(osv.Model):
    _inherit = "hr_evaluation.evaluation"
    _columns = {
            'nombre': fields.related("employee_id", "nombre",
                type="char", string="Nombre", readonly=True, store=True)
        }


class jmdpayslip(osv.Model):
    _inherit = "hr.payslip"
    _columns = {
            'nombre': fields.related("employee_id", "nombre",
                type="char", string="Nombre", readonly=True, store=True)
        }
