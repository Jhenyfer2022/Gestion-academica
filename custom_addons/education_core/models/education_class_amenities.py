from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EducationClassAmenities(models.Model):
    """Para gestionar las comodidades de cada clase"""
    _name = 'education.class.amenities'
    _description = "Comodidades en la Clase"

    name = fields.Many2one('education.amenities', string="Comodidades",
                           help="Seleccione las comodidades en el aula")
    qty = fields.Float(string='Cantidad', help="La cantidad de las comodidades",
                       default=1.0)
    class_id = fields.Many2one('education.class.division',
                               string="Salón de Clases", help="Seleccione el salón de clases")

    @api.constrains('qty')
    def check_qty(self):
        """Devuelve un error de validación si la cantidad es 0 o negativa"""
        for rec in self:
            if rec.qty <= 0:
                raise ValidationError(_('La cantidad debe ser positiva'))
