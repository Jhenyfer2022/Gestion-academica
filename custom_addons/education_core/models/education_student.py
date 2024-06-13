from odoo import api, fields, models, _


class EducationStudent(models.Model):
    """Para gestionar los registros de estudiantes"""
    #_inherit = 'education.student'
    _name = 'education.student'
    _inherit = ['mail.thread']
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Registro de Estudiantes'


    def action_view_calendar(self):
        """Redirects the user to the Odoo calendar module."""
        self.ensure_one()
        calendar_model = self.env['calendar.event']
        return {
            'type': 'ir.actions.act_window',  
            'name': 'Calendar',
            'res_model': calendar_model._name,
            'view_mode': 'calendar,tree,form',
            'target': 'current',
        }
    
    def action_student_documents(self):
        """Devuelve los documentos que el estudiante presentó
        junto con la solicitud de admisión"""
        self.ensure_one()
        if self.application_id.id:
            documents = self.env['education.document'].search(
                [('application_ref_id', '=', self.application_id.id)])
            documents_list = documents.mapped('id')
            return {
                'domain': [('id', 'in', documents_list)],
                'name': _('Documentos'),
                'view_mode': 'tree,form',
                'res_model': 'education.document',
                'view_id': False,
                'context': {
                    'default_application_ref_id': self.application_id.id},
                'type': 'ir.actions.act_window'
            }

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            recs = self.search(
                [('name', operator, name)] + (args or []), limit=limit)
            if not recs:
                recs = self.search(
                    [('ad_no', operator, name)] + (args or []), limit=limit)
            return recs.name_get()
        return super(EducationStudent, self).name_search(
            name, args=args, operator=operator, limit=limit)

    @api.model
    def create(self, vals):
        """Sobrescribe el método create para asignar
        secuencia para el registro recién creado"""
        vals['ad_no'] = self.env['ir.sequence'].next_by_code(
            'education.student')
        res = super(EducationStudent, self).create(vals)
        return res

    partner_id = fields.Many2one(
        'res.partner', string='Socio', required=True,
        ondelete="cascade", help="Socio relacionado del estudiante")
    middle_name = fields.Char(string='Segundo Nombre', help="Ingrese el segundo nombre")
    last_name = fields.Char(string='Apellido', help="Ingrese el apellido")
    date_of_birth = fields.Date(string="Fecha de Nacimiento", requird=True,
                                help="Ingrese la fecha de nacimiento del estudiante")
    guardian_id = fields.Many2one('res.partner', string="Tutor",
                                  domain=[('is_parent', '=', True)],
                                  help="Selecciona el tutor del estudiante")
    father_name = fields.Char(string="Padre", help="Nombre del padre del estudiante")
    mother_name = fields.Char(string="Madre", help="Nombre de la madre del estudiante")
    class_division_id = fields.Many2one('education.class.division',
                                        string="Clase",
                                        help="Clase del estudiante")
    admission_class_id = fields.Many2one('education.class',
                                         string="Clase",
                                         help="Clase de admisión")
    ad_no = fields.Char(string="Número de Admisión", readonly=True,
                        help="Número de admisión del estudiante")
    gender = fields.Selection([('male', 'Masculino'), ('female', 'Femenino'),
                               ('other', 'Otro')], string='Género',
                              required=True, default='male',
                              track_visibility='onchange',
                              help="Detalles de género")
    blood_group = fields.Selection(
        [('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'),
         ('o-', 'O-'), ('ab-', 'AB-'), ('ab+', 'AB+')],
        string='Grupo Sanguíneo', required=True, help="Grupo sanguíneo del estudiante",
        default='a+', track_visibility='onchange')
    company_id = fields.Many2one('res.company', string='Compañía',
                                 help="Compañía actual")
    per_street = fields.Char(string="Calle", help="Ingrese la calle")
    per_street2 = fields.Char(string="Calle2", help="Ingrese la calle2")
    per_zip = fields.Char(change_default=True, string='Código postal',
                          help="Ingrese el Código Postal")
    per_city = fields.Char(string='Ciudad', help="Ingrese el nombre de la ciudad")
    per_state_id = fields.Many2one("res.country.state",
                                   string='Estado', ondelete='restrict',
                                   help="Selecciona el estado de origen")
    per_country_id = fields.Many2one('res.country',
                                     string='País', ondelete='restrict',
                                     help="Selecciona el País")
    medium_id = fields.Many2one('education.medium',
                                string="Medio", required=True,
                                help="Elige el medio de la clase,"
                                     " como inglés, hindi, etc.")
    sec_lang_id = fields.Many2one('education.subject',
                                  string="Segundo idioma",
                                  required=True,
                                  help="Elige el segundo idioma",
                                  domain=[('is_language', '=', True)])
    mother_tongue = fields.Char(string="Lengua Materna", required=True,
                                domain=[('is_language', '=', True)],
                                help="Ingresa la lengua materna del estudiante")
    caste = fields.Char(string="Casta", help="Mi casta es ")
    religion = fields.Char(string="Religión", help="Mi religión es ")
    is_same_address = fields.Boolean(string="¿Es la misma dirección?",
                                     help="Marca la casilla si la dirección actual y la permanente son iguales")
    nationality_id = fields.Many2one('res.country',
                                     string='Nacionalidad', ondelete='restrict',
                                     help="Selecciona la Nacionalidad")
    application_id = fields.Many2one('education.application',
                                     string="Número de Solicitud",
                                     help="Número de solicitud del estudiante")
    class_history_ids = fields.One2many('education.class.history',
                                        'student_id',
                                        string="Detalles de Clase",
                                        help="Detalles del historial de clases anteriores")

    _sql_constraints = [
        ('ad_no', 'unique(ad_no)',
         "¡Ya existe otro estudiante con este número de admisión!"),
    ]
