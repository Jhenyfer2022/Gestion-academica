from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StudentApplication(models.Model):
    """Gestiona la solicitud de estudiantes y su verificación"""
    _name = 'education.application'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Solicitudes de admisión'
    _order = 'id desc'

    @api.model
    def create(self, vals):
        """Anula el método create y asigna la secuencia para el registro recién creado"""
        if vals.get('name', _('Nuevo')) == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'education.application') or _('Nuevo')
        res = super(StudentApplication, self).create(vals)
        return res

    def unlink(self):
        """Devuelve una advertencia si la solicitud no está en estado de rechazo"""
        for rec in self:
            if rec.state != 'reject':
                raise ValidationError(
                    _("La solicitud solo puede ser eliminada después de ser rechazada"))

    def action_send_to_verify(self):
        """Acción del botón para enviar la solicitud para su verificación"""
        for rec in self:
            document_ids = self.env['education.document'].search(
                [('application_ref_id', '=', rec.id)])
            if not document_ids:
                raise ValidationError(_('No se proporcionaron documentos'))
            rec.write({
                'state': 'verification'
            })

    def action_create_student(self):
        """Crea un estudiante a partir de la solicitud y los datos y devuelve al estudiante"""
        for rec in self:
            values = {
                'name': rec.first_name,
                'last_name': rec.last_name,
                'middle_name': rec.middle_name,
                'application_id': rec.id,
                'father_name': rec.father_name,
                'mother_name': rec.mother_name,
                'guardian_id': rec.guardian_id.id,
                'street': rec.street,
                'street2': rec.street2,
                'city': rec.city,
                'state_id': rec.state_id.id,
                'country_id': rec.country_id.id,
                'zip': rec.zip,
                'is_same_address': rec.is_same_address,
                'per_street': rec.per_street,
                'per_street2': rec.per_street2,
                'per_city': rec.per_city,
                'per_state_id': rec.per_state_id.id,
                'per_country_id': rec.per_country_id.id,
                'per_zip': rec.per_zip,
                'gender': rec.gender,
                'date_of_birth': rec.date_of_birth,
                'blood_group': rec.blood_group,
                'nationality_id': rec.nationality_id.id,
                'email': rec.email,
                'mobile': rec.mobile,
                'phone': rec.phone,
                'image_1920': rec.image,
                'is_student': True,
                'medium_id': rec.medium_id.id,
                'religion': rec.religion,
                'caste': rec.caste,
                'sec_lang_id': rec.sec_lang_id.id,
                'mother_tongue': rec.mother_tongue,
                'admission_class_id': rec.admission_class_id.id,
                'company_id': rec.company_id.id,
            }
            if not rec.is_same_address:
                pass
            else:
                values.update({
                    'per_street': rec.street,
                    'per_street2': rec.street2,
                    'per_city': rec.city,
                    'per_state_id': rec.state_id.id,
                    'per_country_id': rec.country_id.id,
                    'per_zip': rec.zip,
                })

            student = self.env['education.student'].create(values)
            rec.write({
                'state': 'done'
            })
            return {
                'name': _('Estudiante'),
                'view_mode': 'form',
                'res_model': 'education.student',
                'type': 'ir.actions.act_window',
                'res_id': student.id,
                'context': self.env.context
            }

    def reject_application(self):
        """Rechaza la solicitud de estudiante para la admisión"""
        for rec in self:
            rec.write({
                'state': 'reject'
            })

    def action_application_verify(self):
        """Verifica la solicitud de estudiante. Devuelve una advertencia si no se proporcionan documentos o si los documentos proporcionados no están en estado completado"""
        for rec in self:
            document_ids = self.env['education.document'].search(
                [('application_ref_id', '=', rec.id)])
            if document_ids:
                doc_status = document_ids.mapped('state')
                if all(state in ('done', 'returned') for state in doc_status):
                    rec.write({
                        'verified_by_id': self.env.uid,
                        'state': 'approve'
                    })
                else:
                    raise ValidationError(
                        _('Todos los documentos aún no están verificados, '
                          'Por favor completa la verificación'))

            else:
                raise ValidationError(_('No se proporcionaron documentos'))

    def _compute_document_count(self):
        """Devuelve el recuento de los documentos proporcionados"""
        for rec in self:
            document_ids = self.env['education.document'].search(
                [('application_ref_id', '=', rec.id)])
            rec.document_count = len(document_ids)

    def action_document_view(self):
        """Devuelve la lista de documentos proporcionados junto con esta solicitud"""
        self.ensure_one()
        domain = [
            ('application_ref_id', '=', self.id)]
        return {
            'name': _('Documentos'),
            'domain': domain,
            'res_model': 'education.document',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'help': _('''<p class="oe_view_nocontent_create">
                               Haga clic para crear nuevos documentos
                            </p>'''),
            'limit': 80,
            'context': {'default_application_ref_id': self.id}
        }

    def action_re_request(self):
        """Vuelve a solicitar la solicitud de estudiante rechazada"""
        for rec in self:
            rec.write({
                'state': 'draft'
            })

    first_name = fields.Char(string='Nombre', required=True,
                             help="Ingrese el primer nombre del estudiante")
    middle_name = fields.Char(string='Segundo Nombre',
                              help="Ingrese el segundo nombre del estudiante")
    last_name = fields.Char(string='Apellido',
                            help="Ingrese el apellido del estudiante")
    prev_school_id = fields.Many2one('res.company',
                                     string='Institución Anterior',
                                     help="Ingrese el nombre de la institución anterior")
    image = fields.Binary(string='Imagen',
                          attachment=True,
                          help="Proporcione la imagen del estudiante")
    academic_year_id = fields.Many2one(
        'education.academic.year',
        string='Año Académico',
        help="Elija el año académico para el que se está solicitando la admisión")
    medium_id = fields.Many2one(
        'education.medium', string="Medio", required=True,
        help="Elija el medio de la clase, como inglés, hindi, etc.")
    sec_lang_id = fields.Many2one('education.subject',string="Segundo Idioma", required=True,
                                  domain=[('is_language', '=', True)],
                                  help="Elija el segundo idioma")
    mother_tongue = fields.Char(string="Lengua Materna",
                                required=True,
                                help="Ingrese la lengua materna del estudiante")
    admission_class_id = fields.Many2one(
        'education.class', string="Clase",
        required=True, help="Ingrese la clase a la que se está solicitando la admisión")
    admission_date = fields.Datetime(string='Fecha de Admisión',
                                     default=fields.Datetime.now,
                                     required=True, help="Fecha de admisión")
    name = fields.Char(string='Número de Solicitud', readonly=True,
                       default=lambda self: _('Nuevo'),
                       help="Número de solicitud de admisión")
    company_id = fields.Many2one('res.company', string='Compañía',
                                 default=lambda self: self.env.user.company_id,
                                 help="Empresa actual")
    email = fields.Char(string="Correo Electrónico", required=True,
                        help="Ingrese el correo electrónico para fines de contacto")
    phone = fields.Char(string="Teléfono",
                        help="Ingrese el número de teléfono para fines de contacto")
    mobile = fields.Char(string="Móvil", required=True,
                         help="Ingrese el número de móvil para fines de contacto")
    nationality_id = fields.Many2one('res.country',
                                     string='Nacionalidad', ondelete='restrict',
                                     help="Seleccione la nacionalidad")
    street = fields.Char(string='Calle', help="Ingrese la calle")
    street2 = fields.Char(string='Calle 2', help="Ingrese la calle 2")
    zip = fields.Char(change_default=True, string='Código Postal',
                      help="Ingrese el código postal")
    city = fields.Char(string='Ciudad', help="Ingrese el nombre de la ciudad")
    state_id = fields.Many2one("res.country.state", string='Estado',
                               ondelete='restrict',
                               help="Seleccione el estado de donde es")
    country_id = fields.Many2one('res.country', string='País',
                                 ondelete='restrict',
                                 help="Seleccione el país")
    is_same_address = fields.Boolean(
        string="Dirección Permanente igual a la anterior",
        default=True,
        help="Marque el campo si la dirección actual y permanente es la misma")
    per_street = fields.Char(string='Calle', help="Ingrese la calle")
    per_street2 = fields.Char(string='Calle 2', help="Ingrese la calle 2")
    per_zip = fields.Char(change_default=True, string='Código Postal',
                          help="Ingrese el código postal")
    per_city = fields.Char(string='Ciudad', help="Ingrese el nombre de la ciudad")
    per_state_id = fields.Many2one("res.country.state",
                                   string='Estado', ondelete='restrict',
                                   help="Seleccione el estado de donde es")
    per_country_id = fields.Many2one('res.country',
                                     string='País', ondelete='restrict',
                                     help="Seleccione el país")
    date_of_birth = fields.Date(string="Fecha de Nacimiento", required=True,
                                help="Ingrese su fecha de nacimiento")
    guardian_id = fields.Many2one('res.partner',
                                  string="Apoderado", required=True,
                                  domain=[('is_parent', '=', True)],
                                  help="Dinos quién se ocupará de ti")
    description = fields.Text(string="Nota",
                              help="Descripción sobre la admisión")
    father_name = fields.Char(string="Padre",
                              help="Orgulloso de decir que mi padre es")
    mother_name = fields.Char(string="Madre", help="El nombre de mi madre es")
    religion = fields.Char(string="Religión",
                           help="Mi religión es ")
    caste = fields.Char(string="Casta",
                        help="Mi casta es ")
    class_division_id = fields.Many2one('education.class.division',
                                        string="Clase",
                                        help="Clase de admisión")
    active = fields.Boolean(string='Activo', default=True,
                            help="Para archivar el formulario de admisión")
    document_count = fields.Integer(compute='_compute_document_count',
                                    string='# Documentos',
                                    help="Documentos del estudiante")
    verified_by_id = fields.Many2one('res.users',
                                     string='Verificado por',
                                     help="El documento está verificado por")
    reject_reason_id = fields.Many2one('application.reject.reason',
                                       string='Razón de Rechazo',
                                       help="La solicitud es rechazada debido a")
    gender = fields.Selection(
        [('male', 'Masculino'), ('female', 'Femenino'), ('other', 'Otro')],
        string='Género', required=True, default='male',
        track_visibility='onchange', help="Tu género es")
    blood_group = fields.Selection(
        [('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'),
         ('o-', 'O-'), ('ab-', 'AB-'), ('ab+', 'AB+')],
        string='Grupo Sanguíneo', required=True, default='a+',
        track_visibility='onchange', help="Tu grupo sanguíneo es")
    state = fields.Selection([('draft', 'Borrador'),
                              ('verification', 'Verificar'),
                              ('approve', 'Aprobar'),
                              ('reject', 'Rechazado'), ('done', 'Hecho')],
                             string='Estado', required=True, default='draft',
                             track_visibility='onchange',
                             help="Etapa de admisión")
