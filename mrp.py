# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2008 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from tools.translate import _

from osv import fields, osv

#
# Dimensions Definition
#
class mrp_product_produce(osv.osv_memory):
    _inherit = "mrp.product.produce"
    _columns = {
                'product_id_produce': fields.many2one('product.product', 'Articolo', required=True, select=True, domain=[('type', '<>', 'service')]),
                'righe_in_consumo': fields.one2many('mrp.product.produce.consume', 'name', 'Righe Articoli in Consumo'),
                }
    
    def _get_product_id_produce(self, cr, uid, context=None):
        #import pdb;pdb.set_trace()
        ## è previsto che questo tipo di produzione sia per singolo articolo e non x + articoli sulla stessa produzione
        if context is None:
            context = {}
        prod = self.pool.get('mrp.production').browse(cr, uid, context['active_id'], context=context)
        return  prod.product_id.id
    
    
    def _get_consumi(self, cr, uid, context=None):
        # import pdb;pdb.set_trace()
        ## è previsto che questo tipo di produzione sia per singolo articolo e non x + articoli sulla stessa produzione
        if context is None:
            context = {}
        prod = self.pool.get('mrp.production').browse(cr, uid, context['active_id'], context=context)
        res = []
        
        for move in prod.move_lines:
           res.append(
                      {
                       'product_id_consume':move.product_id.id,
                       'product_qty_consume':move.product_qty,
                       'move_id':move.id,
                       }
                      )
        return res

    

    def do_produce(self, cr, uid, ids, context=None):
       
        # cicla si movimenti che ha se c'è già la riga per sicurezza la riscrive aggiornando la qta di scarico
        # se non c'è il movimento scrive la nuova riga con lo stato giusto di confermato
        for dati in self.browse(cr, uid, ids):
            for mov_sca in dati.righe_in_consumo:
                if mov_sca.move_id:
                    # così da la possibilità di modificare la qta di scarico
                    riga = {
                    'product_id': mov_sca.product_id_consume.id,
                    'product_qty':mov_sca.product_qty_consume,
                     }     
                    ok = self.pool.get('stock.move').write(cr, uid, [mov_sca.move_id.id], riga)                   
                else:
                   #import pdb;pdb.set_trace()
                   # nuova riga movimento di scarico da inserire
                   production_id = context.get('active_ids', [])[0]
                   production = self.pool.get('mrp.production').browse(cr, uid, [production_id])[0]
                   scarichi_obj = production.move_lines
                   scarichi = []
                   for sca in production.move_lines:
                       scarichi.append(sca.id)
                   #import pdb;pdb.set_trace() 
                   source = production.product_id.product_tmpl_id.property_stock_production.id
                   riga = {
                        'name':'PROD:' + production.name,
                        'picking_id':production.picking_id.id,
                        'product_id': mov_sca.product_id_consume.id,
                        'product_qty': mov_sca.product_qty_consume,
                        'product_uom': mov_sca.product_id_consume.uom_id.id,
                        'product_uos_qty': False,
                        'product_uos':  False,
                       # 'date': newdate,S
                     #   'move_dest_id': production.picking_idres_dest_id,
                        
                        'location_id': production.location_dest_id.id,
                        'location_dest_id': source,
                        
                        'state': 'assigned',
                        'company_id': production.company_id.id,

                     }     
                   id_mov_sca = self.pool.get('stock.move').create(cr, uid, riga)  
                   scarichi.append(id_mov_sca)                  
                   self.pool.get('mrp.production').write(cr, uid, [production_id], {'move_lines': [(6, 0, scarichi)]})    
                   riga = {
                            'name': mov_sca.product_id_consume.name,
                            'product_id': mov_sca.product_id_consume.id,
                            'product_qty': mov_sca.product_qty_consume,
                            'product_uom': mov_sca.product_id_consume.uom_id.id,
                            'product_uos_qty': False,
                            'product_uos': False,
                            'production_id': production.id
                            }       
                   id_sched_sca = self.pool.get('mrp.production.product.line').create(cr, uid, riga)  
        # import pdb;pdb.set_trace()
        # qui modifica il carico della qta prodotta
        production_order = self.pool.get('mrp.production').browse(cr, uid, context['active_id'], context=context)
        product_qty_planned = production_order.product_qty
        ok = self.pool.get('mrp.production').write(cr, uid, [production_order.id], {'product_qty':dati.product_qty, 'product_qty_planned':product_qty_planned})
        for mov_mag_id in production_order.move_created_ids:
            ok = self.pool.get('stock.move').write(cr, uid, [mov_mag_id.id], {'product_qty': dati.product_qty, })
        
        
        
       
        
        # qui fa lo standard
        if context is None:
            context = {}
        prod_obj = self.pool.get('mrp.production')
        move_ids = context.get('active_ids', [])
        for data in self.read(cr, uid, ids, context=context):
            for move_id in move_ids:
                prod_obj.action_produce(cr, uid, move_id,
                                    data['product_qty'], data['mode'], context=context)

        return {}

    _defaults = {
        'product_id_produce':_get_product_id_produce,
        'righe_in_consumo':_get_consumi,
    }
   
mrp_product_produce()

class mrp_product_produce_consume(osv.osv_memory):
    _name = "mrp.product.produce.consume"
    _columns = {
                'name':fields.many2one('mrp.product.produce', 'Articolo in Produzione', required=True, ondelete='cascade', select=True,),
                'move_id':fields.many2one('stock.move', 'Movimento di Scarico', required=False, readonly=False),
                'product_id_consume': fields.many2one('product.product', 'Articolo', required=True, select=True),
                'product_qty_consume': fields.float('Quantità da Scaricare', required=True),
                }
    
mrp_product_produce_consume()  

class mrp_production(osv.osv):
    _inherit = 'mrp.production' 
                #Do not touch _name it must be same as _inherit
                #_name = 'mrp.production' cr
    _columns = {
                'product_qty_planned': fields.float('Product Qty Planned', required=False, states={'draft':[('readonly', False)]}, readonly=True),
                                }
mrp_production()  

