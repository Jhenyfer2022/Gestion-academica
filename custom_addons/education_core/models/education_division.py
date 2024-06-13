from odoo import fields, models


class EducationDivision(models.Model):
    """Gestiona divisiones de clase de la institución"""
    _name = 'education.division'
    _description = "División Cursos"

    name = fields.Char(string='Nombre', required=True,
                       help="Ingresa el Nombre de la División")
    strength = fields.Integer(string='Capacidad',
                              help="Capacidad total de la clase")
    faculty_id = fields.Many2one('education.faculty',
                                 string='Profesor de Clase',
                                 help="Profesor de Clase")
    class_id = fields.Many2one('education.class', string='Clase',
                               help="Clase de la división")
