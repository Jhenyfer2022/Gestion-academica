from odoo import fields, models


class EducationAmenities(models.Model):
    """Used to manage amenities of institution"""
    _name = 'education.amenities'
    _description = 'Servicio en la Institución'
    

    name = fields.Char(string='Nombre', required=True, help='Nombre del servicio')
    description = fields.Char(string='Descripción', help='Descripción sobre el servicio')
    precio = fields.Integer(string='Precio', help='Precio del servicio')

