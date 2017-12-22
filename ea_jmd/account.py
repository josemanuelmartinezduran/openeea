# -*- coding: utf-8 -*-
from osv import osv, fields

class jmdaccounts(osv.Model):
    _name= "account.sat"
    _columns = {
            'name': fields.char(string="Nombre"),
            'codigo': fields.char(string="Codigo"),
        }


class jmdaccount(osv.Model):
    _inherit = "account.account"

    def setParents(self, cr, uid, ids, context="None"):
        print("Here")
        ret = {}
        count = 0
        parent = "3963"
        for i in self.browse(cr, uid, self.search(cr, uid, []), context=None):
            count += 1
            if count >= 20:
                return ret
            print(("Modificando cuenta " + str(i.name) + str(i.code)))
            parent = 3963
            if i.id == parent:
                print("Skip")
                continue
            if i.name == "Estadistica":
                continue
            if len(i.code) >= 9:
                parent_code = i.code[:-5]
                for j in self.browse(cr, uid, self.search(cr, uid, [('code', '=', parent_code)]), context=None):
                    print("Encontrado " + str(j.code) + " pare de " + str(i.code) + " ID " +str(i.id) )
                    parent = j.id
                print("Id de la cuenta " + str(i.id))
                self.write(cr, uid, i.id, {'parent_id': parent})
                print("Nunca llega aqui")
        return ret

    _columns = {
            'balanza': fields.boolean(string="Balanza de Comprobación"),
            'resultados': fields.boolean(string="Estado de Resultados"),
            'balance_general': fields.boolean(string="Balance General"),
            'codigo_sat': fields.many2one("account.sat", string="Codigo SAT"),
            'sat': fields.char("Código Agrupador SAT")
        }


class jmdpoliza(osv.Model):
    _inherit = "account.move"

    def esta_cuadrada(self, cr, uid, ids, fieldname, args, context=None):
        ret = {}
        for i in self.browse(cr, uid, ids, context):
            ret[i.id] = False
            for j in i.line_id:
                if j.state is "valid":
                    ret[i.id] = True
        return ret

    _columns = {
            'field': fields.function(esta_cuadrada,
                string="Cuadrada", type="boolean")
        }

    _defaults = {
            'ref': lambda self, cr, uid, context={}: self.pool.get
                ('ir.sequence').get(cr, uid, 'ea.poliza')
        }
