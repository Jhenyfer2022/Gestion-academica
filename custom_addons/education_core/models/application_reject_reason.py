from odoo import fields, models


class ApplicationRejectReason(models.Model):
    """Se utiliza para gestionar los motivos de rechazo de las solicitudes"""
    _name = 'application.reject.reason'
    _description = 'Motivos del rechazo'

    name = fields.Char(string="Motivo", required=True,
                       help="Posible motivo para rechazar las solicitudes")

