from odoo import fields, models


class EducationClass(models.Model):
    """For managing classes"""
    _name = 'education.class'
    _description = "Cursos"

    name = fields.Char(string='Nombre', required=True,
                       help="Ingrese el nombre de la clase")
    syllabus_ids = fields.One2many('education.syllabus',
                                   'class_id',
                                   string="Plan de estudios",
                                   help="Plan de estudios de la clase")
    division_ids = fields.One2many('education.division',
                                   'class_id',
                                   string="Divisiones",
                                   help="Divisiones de la clase")
