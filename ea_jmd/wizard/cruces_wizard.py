# -*- coding: utf-8 -*-
from osv import osv, fields


class jmdwizardcruces(osv.TransientModel):
    _name = "ea.wizard_cruces"

    def recur_count(self, var_count, dict_sofar, input_dict, total_encuestas):
        combinaciones = {}
        print(("Valor de var_count" + str(var_count)))
        if var_count == 0:
            print("Saliendo de la recursividad")
            for k, v in (list(dict_sofar.items())):
                combinaciones[k] = round(((v / 100) * total_encuestas))
            return combinaciones
        var_count -= 1
        for i in range(input_dict['countvars'][var_count]):
            print("ejecutnado el for")
            if dict_sofar == {}:
                print("Diccionario vacio")
                combo_name = input_dict['listvalor'][var_count][i]
                combinaciones[combo_name] = ((input_dict['arrayvars']
                    [var_count][i]))
            else:
                for j, k in (list(dict_sofar.items())):
                    print("Diccionario con datos")
                    combo_name = input_dict['listvalor'][var_count][i]\
                        + " X " + j
                    combinaciones[combo_name] = ((input_dict['arrayvars']
                        [var_count][i]
                        * k / 100))
        return self.recur_count(var_count,
            combinaciones, input_dict, total_encuestas)

    def generate_cruces(self, cr, uid, ids, context=None):
        plaza_id = context.get("current_plaza_id")
        total_encuestas = 0
        for i in self.browse(cr, uid, ids, context):
            total_encuestas = i.cantidad
        for j in self.pool.get("editor_encuestas").browse(cr, uid,
            [plaza_id], context):
            print(("nombre de la plaza" + str(j.place.name)))
        #Generando los cruces #IStandForFreedom
        #Paso 1 Leyendo las diferntes variables
        varlist = []
        countvars = []
        arrayvars = []
        listvalor = []
        combinaciones = {}
        for i in self.browse(cr, uid, ids):
            for j in i.variables:
                if j.variable not in varlist:
                    varlist.append(j.variable)
                    countvars.append(0)
                    arrayvars.append([])
                    listvalor.append([])
                for k in range(len(varlist)):
                    if j.variable == varlist[k]:
                        countvars[k] += 1
                        arrayvars[k].append(j.cantidad)
                        listvalor[k].append(j.valor)
        input_dict = {
            'varlist': varlist,
            'countvars': countvars,
            'arrayvars': arrayvars,
            'listvalor': listvalor
            }
        #Paso 2 Generando las combinaciones ejemplo 3 variables
        combinaciones = self.recur_count(len(varlist), combinaciones,
                        input_dict, total_encuestas)
        #Paso 3 Escribiendo en la base de datos
        for key, value in (list(combinaciones.items())):
            vals = {
                'name': str(key),
                'relation_id': plaza_id,
                'cantidad': value
                }
            self.pool.get("ea.cuota").create(cr, uid, vals)
            print(("La llave " + str(key) + " tiene el valor " + str(value)))
        return {}

    _columns = {
            'name': fields.char(string="Nombre", size=40, translate=True),
            'variables': fields.one2many("ea.wizard_cruces.variable",
                "relation", string="Cruces"),
            'cantidad': fields.integer("Número de encuestas"),
            'plaza': fields.many2one("res.country.state.city", "Plaza"),
        }


class jmdwizardvariable(osv.TransientModel):
    _name = "ea.wizard_cruces.variable"
    _columns = {
            'name': fields.char(string="Nombre", size=40),
            'variable': fields.char("Variable", size=80),
            'valor': fields.char("Valor", size=80),
            'cantidad': fields.float("Porcentaje", digits=(4, 2)),
            'relation': fields.many2one("ea.wizard_cruces")
        }