import time
from report import report_sxw
from openerp.osv import osv
from openerp import pooler


class orden(report_sxw.rml_parse):

    _description = "Plantilla para cotizacion"

    def __init__(self, cr, uid, name, context):
        super(orden, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            #'time': time,
            #'show_discount': self._show_discount,
            'compra': self.pool.get('sale.order').browse(cr, uid, context)
            })
        self.context = context

    #def _show_discount(self, uid, context=None):
        #cr = self.cr
        #try:
            #group_id = self.pool.get('ir.model.data').get_object_reference(cr,
                 #uid, 'sale', 'group_discount_per_so_line')[1]
        #except:
            #return False
        #return group_id in [x.id for x in self.pool.get('res.users').browse(cr,
             #uid, uid, context=context).groups_id]


report_sxw.report_sxw('report.tylus_alfa.reporte.ventas', 'sale.order',
      'addons/tylus_alfa/report/01_ventas/ventas_report.rml', parser=orden,
      header=False)