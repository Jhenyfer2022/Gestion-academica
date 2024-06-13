from odoo import fields, models


class StandardMedium(models.Model):
    """Gestiona los detalles del medio de clase del estudiante"""
    _name = "education.medium"
    _description = "Medio Estándar"

    name = fields.Char(string='Nombre', required=True,
                       help="Ingresa el Nombre del Medio")
    code = fields.Char(string='Código', help="Ingresa el Código del Medio")
    description = fields.Text(string='Descripción', help="Nota sobre el medio")

