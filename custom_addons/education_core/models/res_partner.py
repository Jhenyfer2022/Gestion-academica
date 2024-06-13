from odoo import fields, models


class ResPartner(models.Model):
    """Modelo heredado para agregar dos campos para determinar
                        si el socio es estudiante o padre"""
    _inherit = 'res.partner'

    is_student = fields.Boolean(string="Es Estudiante",
                                help="Habilita si el socio es un estudiante")
    is_parent = fields.Boolean(string="Es Padre",
                               help="Habilita si el socio es un padre")
