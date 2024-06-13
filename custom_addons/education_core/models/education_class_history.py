from odoo import fields, models


class EducationClassDivisionHistory(models.Model):
    """Gestiona detalles de clases anteriores de estudiantes"""
    _name = 'education.class.history'
    _description = "Historial de Salones de Clase"
    _rec_name = 'class_id'

    academic_year_id = fields.Many2one('education.academic.year',
                                       string='Año Académico',
                                       help="Selecciona el Año Académico")
    class_id = fields.Many2one('education.class.division',
                               string='Clase', help="Selecciona la clase")
    student_id = fields.Many2one('education.student',
                                 string='Estudiante',
                                 help="Selecciona Estudiante de la clase")

