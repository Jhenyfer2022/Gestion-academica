from odoo import fields, models, _
from odoo.exceptions import UserError


class HRRecruitment(models.Model):
    """Herencia de hr_applicant para agregar un campo para el cuerpo docente y
    para crear un cuerpo docente desde la aplicación"""
    _inherit = 'hr.applicant'

    is_faculty = fields.Boolean(string="¿Cuerpo Docente?",
                                help="Marca Verdadero si esta es una contratación para el Cuerpo Docente")

    def create_employee_from_applicant(self):
        """ Crea un hr_employee desde los hr_applicants
            Sobrescribe la función existente para crear el cuerpo docente al crear
            el empleado"""
        employee = False
        for applicant in self:
            contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])[
                    'contact']
                contact_name = applicant.partner_id.name_get()[0][1]
            else:
                new_partner_id = self.env['res.partner'].create({
                    'is_company': False,
                    'name': applicant.partner_name,
                    'email': applicant.email_from,
                    'phone': applicant.partner_phone,
                    'mobile': applicant.partner_mobile
                })
                address_id = new_partner_id.address_get(['contact'])['contact']
            if applicant.job_id and (applicant.partner_name or contact_name):
                applicant.job_id.write({
                    'no_of_hired_employee': applicant.job_id.no_of_hired_employee + 1})
                employee = self.env['hr.employee'].create({
                    'name': applicant.partner_name or contact_name,
                    'job_id': applicant.job_id.id,
                    'address_home_id': address_id,
                    'department_id': applicant.department_id.id or False,
                    'address_id': applicant.company_id and applicant.company_id.partner_id
                                  and applicant.company_id.partner_id.id or False,
                    'work_email': applicant.department_id and applicant.department_id.company_id
                                  and applicant.department_id.company_id.email or False,
                    'work_phone': applicant.department_id and applicant.department_id.company_id
                                  and applicant.department_id.company_id.phone or False})
                applicant.write({'emp_id': employee.id})

                # creando el cuerpo docente
                if applicant.is_faculty:
                    values = {
                        'name': applicant.partner_name,
                        'email': applicant.email_from,
                        'phone': applicant.partner_phone,
                        'mobile': applicant.partner_mobile,
                        'degree_id': applicant.type_id.id,
                        'employee_id': employee.id
                    }
                    self.env['education.faculty'].create(values)
                applicant.job_id.message_post(
                    body=_(
                        'Nuevo Empleado %s Contratado') % applicant.partner_name if applicant.partner_name else applicant.name,
                    subtype_xmlid="hr_recruitment.mt_job_applicant_hired")
                # employee._broadcast_welcome()
            else:
                raise UserError(_(
                    'Debe definir un Trabajo Aplicado y un Nombre de Contacto '
                    'para este solicitante.'))

        employee_action = self.env.ref('hr.open_view_employee_list')
        dict_act_window = employee_action.read([])[0]
        if employee:
            dict_act_window['res_id'] = employee.id
        dict_act_window['view_mode'] = 'form,tree'
        return dict_act_window
