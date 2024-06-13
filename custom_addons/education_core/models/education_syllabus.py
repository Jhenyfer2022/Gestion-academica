from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EducationSyllabus(models.Model):
    """Gestiona el plan de estudios de cada asignatura"""
    _name = 'education.syllabus'
    _description = 'Detalles del Plan de Estudios'

    name = fields.Char('Nombre', required=True, help="Nombre del plan de estudios")
    class_id = fields.Many2one('education.class', string='Clase',
                               help="Selecciona la clase para el plan de estudios")
    subject_id = fields.Many2one('education.subject',
                                 string='Asignatura', help="Selecciona las asignaturas")
    total_hours = fields.Float(string='Total de Horas',
                               help="Total de horas necesarias para la asignatura")
    description = fields.Text(string='Módulos del Plan de Estudios',
                              help="Nota sobre el plan de estudios")

    @api.constrains('total_hours')
    def validate_time(self):
        """Devuelve un error de validación si las horas no son un valor positivo"""
        for rec in self:
            if rec.total_hours <= 0:
                raise ValidationError(_('Las horas deben ser mayores que cero'))
