from odoo import fields, models


class DocumentDocument(models.Model):
    """Para gestionar tipos de documentos"""
    _name = 'document.document'
    _description = "Tipos de documentos"

    name = fields.Char(string='Nombre', required=True,
                       help="Nombre del tipo de documento")
    description = fields.Char(string='Descripción', help="Nota sobre el tipo de documento")
