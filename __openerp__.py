##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################
{
    "name" : "Mrp Produzione Personalizzata",
    "version" : "1.0",
    "author" : "C.& G. Software",
    "category" : "mrp",
    "description":"""Quando conferma la produzione di un articolo visualizza l'elenco delle materie prime dando la possibilità di aggiungere articoli e modificare gli esistenti
    """,
    "depends" : ["mrp"],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : ['mrp_view.xml'],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

