from odoo import api, fields, models


class EducationFaculty(models.Model):
    """Gestiona los detalles de la facultad de la institución"""
    _name = 'education.faculty'
    _inherit = ['mail.thread']
    _description = 'Registro de Maestro'

    def action_create_employee(self):
        """Creando el empleado por Maestro"""
        for rec in self:
            values = {
                'name': rec.name + rec.last_name,
                'gender': rec.gender,
                'birthday': rec.date_of_birth,
                'image_1920': rec.image,
                'work_phone': rec.phone,
                'work_email': rec.email,
            }
            emp_id = self.env['hr.employee'].create(values)
            rec.employee_id = emp_id.id

    @api.model
    def create(self, vals):
        """Sobrescribe el método create para asignar
        la secuencia para los registros recién creados"""
        vals['faculty_id'] = self.env['ir.sequence'].next_by_code(
            'education.faculty')
        res = super(EducationFaculty, self).create(vals)
        return res

    name = fields.Char(string='Nombre', required=True,
                       help="Ingresa el primer nombre")
    faculty_id = fields.Char(string="ID", readonly=True,
                             help="Número de identificación del Maestro")
    last_name = fields.Char(string='Apellido', help="Ingresa el apellido")
    image = fields.Binary(string="Imagen", attachment=True,
                          help="Imagen de la facultad")
    email = fields.Char(string="Correo Electrónico",
                        help="Ingresa el correo electrónico para contacto")
    phone = fields.Char(string="Teléfono",
                        help="Ingresa el teléfono para contacto")
    mobile = fields.Char(string="Móvil",
                         help="Ingresa el móvil para contacto")
    date_of_birth = fields.Date(string="Fecha de Nacimiento", help="Ingresa la fecha de nacimiento")
    guardian_name = fields.Char(string="Guardián", help="Tu guardián es ")
    father_name = fields.Char(string="Padre", help="El nombre de tu padre es ")
    mother_name = fields.Char(string="Madre", help="El nombre de tu madre es ")
    subject_lines_ids = fields.Many2many('education.subject',
                                         string='Líneas de Asignaturas',
                                         help="Asignaturas de la facultad")
    employee_id = fields.Many2one('hr.employee',
                                  string="Empleado Relacionado",
                                  help="Detalles del empleado relacionado")
    degree_id = fields.Many2one('hr.recruitment.degree',
                                string="Grado",
                                Help="Selecciona tu grado más alto")
    gender = fields.Selection(
        [('male', 'Masculino'), ('female', 'Femenino'), ('other', 'Otro')],
        string='Género', required=True, default='male',
        help="Género de la facultad", track_visibility='onchange')
    blood_group = fields.Selection(
        [('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'),
         ('o-', 'O-'), ('ab-', 'AB-'), ('ab+', 'AB+')], string='Grupo Sanguíneo',
        required=True, default='a+',
        track_visibility='onchange', help="Grupo sanguíneo del Maestro")
