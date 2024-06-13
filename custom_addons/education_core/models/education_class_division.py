from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EducationClassDivision(models.Model):
    """Gestiona los detalles de la división de clases"""
    _name = 'education.class.division'
    _description = "Salón de Clases"
    _inherit = ['mail.thread']

    @api.model
    def create(self, vals):
        if 'class_id' in vals and 'division_id' in vals:
            class_id = self.env['education.class'].browse(vals['class_id'])
            division_id = self.env['education.division'].browse(
                vals['division_id'])
            name = str(class_id.name + '-' + division_id.name)
            vals['name'] = name
        return super(EducationClassDivision, self).create(vals)

    def action_view_students(self):
        """Devuelve la lista de estudiantes actuales en esta clase"""
        self.ensure_one()
        students = self.env['education.student'].search(
            [('class_division_id', '=', self.id)])
        students_list = students.mapped('id')
        return {
            'domain': [('id', 'in', students_list)],
            'name': _('Estudiantes'),
            'view_mode': 'tree,form',
            'res_model': 'education.student',
            'view_id': False,
            'context': {'default_class_id': self.id},
            'type': 'ir.actions.act_window'
        }

    def _compute_student_count(self):
        """Devuelve el número de estudiantes en la clase"""
        for rec in self:
            students = self.env['education.student'].search(
                [('class_division_id', '=', rec.id)])
            student_count = len(students) if students else 0
            rec.update({
                'student_count': student_count
            })

    name = fields.Char(string='Nombre', readonly=True,
                       help="Nombre de la división de la clase")
    actual_strength = fields.Integer(string='Cantida de estudiantes de la clase',
                                     help="Cantidad total de estudiantes de la clase")
    faculty_id = fields.Many2one('education.faculty',
                                 string='Tutor de Clase', required=True,
                                 help="Tutor de Clase/Facultad")
    academic_year_id = fields.Many2one('education.academic.year',
                                       string='Año Académico',
                                       help="Selecciona el Año Académico",
                                       required=True)
    class_id = fields.Many2one('education.class', string='Clase',
                               required=True, help="Selecciona la Clase")
    division_id = fields.Many2one('education.division',
                                  string='División', required=True,
                                  help="Selecciona la División")
    student_ids = fields.One2many('education.student',
                                  'class_division_id',
                                  string='Estudiantes',
                                  help="Estudiantes bajo esta división")
    amenities_ids = fields.One2many('education.class.amenities',
                                    'class_id', string='Comodidades',
                                    help="Comodidades de esta división")
    student_count = fields.Integer(string='Cantidad de Estudiantes',
                                   help="Conteo de los estudiantes en la "
                                        "división",
                                   compute='_compute_student_count')

    @api.constrains('actual_strength')
    def validate_strength(self):
        """Devuelve un error de validación si
            la fortaleza de los estudiantes no es un número distinto de cero"""
        for rec in self:
            if rec.actual_strength <= 0:
                raise ValidationError(_('La fortaleza debe ser un valor distinto de cero'))
