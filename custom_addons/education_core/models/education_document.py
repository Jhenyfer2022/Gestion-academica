import datetime
from odoo import api, fields, models, _


class EducationDocument(models.Model):
    """Para gestionar detalles y verificación de documentos de estudiantes"""
    _name = 'education.document'
    _description = "Documentos del Estudiante"
    _inherit = ['mail.thread']

    @api.model
    def create(self, vals):
        """Sobrescribe el método create para asignar
        la secuencia para los registros recién creados"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'education.document') or _('New')
        res = super(EducationDocument, self).create(vals)
        return res

    def action_verify_document(self):
        """Devuelve el estado a 'hecho' si los documentos son perfectos"""
        for rec in self:
            rec.write({
                'verified_by_id': self.env.uid,
                'verified_date': datetime.datetime.now().strftime("%Y-%m-%d"),
                'state': 'done'
            })

    def action_need_correction(self):
        """Devuelve el estado a 'corrección' si los documentos no son perfectos"""
        for rec in self:
            rec.write({
                'state': 'correction'
            })

    def action_hard_copy_returned(self):
        """Registra quién devuelve los documentos y cuándo se devuelven"""
        for rec in self:
            if rec.state == 'done':
                rec.write({
                    'state': 'returned',
                    'returned_by_id': self.env.uid,
                    'returned_date': datetime.datetime.now().strftime(
                        "%Y-%m-%d")
                })

    name = fields.Char(string='Número de Serie', copy=False,
                       help="Número de serie del documento",
                       default=lambda self: _('New'))
    document_type_id = fields.Many2one('document.document',
                                       string='Tipo de Documento', required=True,
                                       help="Selecciona el tipo de documento")
    description = fields.Text(string='Descripción', copy=False,
                              help="Ingresa una descripción sobre el documento")
    has_hard_copy = fields.Boolean(
        string="Copia Física Recibida",
        help="Marca este campo si se ha recibido la copia física")
    location_id = fields.Many2one(
        'stock.location', 'Ubicación',
        domain="[('usage', '=', 'internal')]",
        help="Ubicación donde se almacena la copia física")
    location_note = fields.Char(string="Nota de Ubicación",
                                help="Ingresa algunas notas sobre la ubicación")
    submitted_date = fields.Date(string="Fecha de Envío",
                                 default=fields.Date.today(),
                                 help="Documentos son enviados en")
    received_by_id = fields.Many2one('hr.employee',
                                     string="Recibido Por",
                                     help="Los Documentos son recibidos por")
    returned_by_id = fields.Many2one('hr.employee',
                                     string="Devuelto Por",
                                     help="Los Documentos son devueltos por")
    verified_date = fields.Date(string="Fecha de Verificación",
                                help="Fecha en que se realiza la verificación")
    returned_date = fields.Date(string="Fecha de Devolución", help="Fecha de Devolución")
    responsible_verified_id = fields.Many2one('hr.employee',
                                              string="Responsable",
                                              help="Persona responsable de verificar el documento")
    responsible_returned_id = fields.Many2one('hr.employee',
                                              string="Responsable",
                                              help="Persona responsable de verificar el documento devuelto")
    verified_by_id = fields.Many2one('res.users',
                                     string='Verificado por',
                                     help="Documento es verificado por el usuario")
    application_ref_id = fields.Many2one('education.application',
                                         copy=False, string="Referencia de Solicitud",
                                         help="Referencia de solicitud del documento")
    doc_attachment_ids = fields.Many2many(
        'ir.attachment', 'education_doc_attach_rel',
        'doc_id', 'attach_id3', string="Adjunto", copy=False,
        help='Puedes adjuntar una copia de tu documento')
    state = fields.Selection(
        [('draft', 'Borrador'), ('correction', 'Corrección'),
         ('done', 'Hecho'), ('returned', 'Devuelto')], string='Estado',
        required=True, default='draft',
        track_visibility='onchange', help="Etapas del documento ")
