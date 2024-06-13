from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class EducationAcademicYear(models.Model):
    """For managing academic year of institution"""
    _name = 'education.academic.year'
    _description = 'Año académico'
    _order = 'sequence asc'

    @api.model
    def create(self, vals):
        """Anulando el método de creación y asignando el secuencia para el registro recién creado"""
        vals['sequence'] = self.env['ir.sequence'].next_by_code(
            'education.academic.year')
        res = super(EducationAcademicYear, self).create(vals)
        return res

    def unlink(self):
        """Error de validación de devolución al eliminar el curso académico"""
        for rec in self:
            raise ValidationError(
                _("El año académico no se puede eliminar, solo puedes"
                  "Archivarlo."))

    name = fields.Char(string='Nombre', required=True,
                       help='Nombre del año académico')
    sequence = fields.Integer(string='Secuencia', required=True,
                              help="Secuencia del año académico")
    ay_start_date = fields.Date(string='Fecha de inicio', required=True,
                                help='Fecha de inicio del año académico')
    ay_end_date = fields.Date(string='Fecha de finalización', required=True,
                              help='Fecha de finalización del año académico')
    ay_description = fields.Text(string='Descripción',
                                 help="Descripción sobre el año académico")
    active = fields.Boolean(
        'Activo', default=True,
        help="Si no está marcado, permitirá ocultar el Año Académico "
             "sin eliminarlo.")

    @api.constrains('ay_start_date', 'ay_end_date')
    def validate_date(self):
        """Consultar las fechas de inicio y finalización del plan de estudios, generar advertencia si la fecha de inicio no es anterior"""
        for rec in self:
            if rec.ay_start_date >= rec.ay_end_date:
                raise ValidationError(
                    _('La fecha de inicio debe ser anterior a la fecha de finalización'))
