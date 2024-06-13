from odoo import fields, models


class ResCompany(models.Model):
    """Herencia de res_company para agregar campo relacionado con una
        institución educativa"""
    _inherit = 'res.company'

    affiliation = fields.Char(string='Afiliación', help="Detalles de la Afiliación")
    register_num = fields.Char(string='Registro', help="Detalles del Registro")
    base_class_id = fields.Many2one('education.class',
                                    string="Clase Inferior",
                                    help="Clase más baja de la institución")
    higher_class_id = fields.Many2one('education.class',
                                      string="Clase Superior",
                                      help="Clase más alta de la institución")
