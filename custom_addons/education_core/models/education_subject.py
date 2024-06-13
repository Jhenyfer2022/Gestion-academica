from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EducationSubject(models.Model):
    """Gestiona las asignaturas del instituto"""
    _name = 'education.subject'
    _description = 'Detalles de Asignaturas'

    name = fields.Char(string='Nombre', required=True,
                       help="Nombre de la Asignatura")
    is_language = fields.Boolean(string="Idioma",
                                 help="Marca si esta asignatura es un idioma")
    is_lab = fields.Boolean(string="Laboratorio", help="Marca si esta asignatura es un laboratorio")
    code = fields.Char(string="Código", help="Ingresa el Código de la Asignatura")
    type = fields.Selection(
        [('compulsory', 'Obligatoria'), ('elective', 'Optativa')],
        string='Tipo', default="compulsory",
        help="Elige el tipo de asignatura")
    weightage = fields.Float(string='Ponderación', default=1.0,
                             help="Ingresa la ponderación para esta asignatura")
    description = fields.Text(string='Descripción',
                              help="Nota sobre la asignatura")

    _sql_constraints = [
        ('code', 'unique(code)',
         "¡Otra Asignatura ya existe con este código!"),
    ]

    @api.constrains('weightage')
    def check_weightage(self):
        """Devuelve una advertencia si la ponderación dada no es un valor positivo"""
        for rec in self:
            if rec.weightage <= 0:
                raise ValidationError(_('La ponderación debe ser positiva'))
