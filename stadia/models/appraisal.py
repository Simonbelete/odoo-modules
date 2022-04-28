from odoo import models, fields, api

knowledge = fields.Selection([
        ('A-1', '1 - Severely lacking in knowledge',), 
        ('B-2', '2 - Noticeable deficiencies in job knowledge',), 
        ('C-3', '3 - Understanding job routine. Some knowledge still to be acquired',), 
        ('D-4', '4 - Completely understands all aspects of the job',), 
        ('E-5', '5 - Understands why all job functions are performed and inter-relationship with other jobs. An expert',)])

quantity = fields.Selection([
    ('A-1', '1',), 
    ('B-2', '2',), 
    ('C-3', '3',), 
    ('D-4', '4',), 
    ('E-5', '5',)])

quantity = fields.Selection([
    ('A-1', '1 - Usually below acceptable standard',), 
    ('B-2', '2 - Barely acceptable level of output. A slow worker',), 
    ('C-3', '3 - Satisfactory. Meets expectations of average output',), 
    ('D-4', '4 - Usually exceeds the norm. A fast worker',), 
    ('E-5', '5 - Exceptional producer. Generates maximal output',)])

class Appraisal(models.Model):
    _name = 'stadia.appraisal.appraisal'

    employee_id = fields.Many2one('hr.employee', string = 'Employee')
    rated_by_id = fields.Many2one('hr.employee', string = 'Rated by')
    approved_by_id = fields.Many2one('hr.employee', string = 'Approved by')
    job_location = fields.Char()
    date = fields.Date()
    last_evaluation = fields.Date()
    strengths = fields.Text() # Comment on principal strengths:
    suggestion = fields.Text() # Comment on principal weaknesses and suggestions for improvement
    is_discussed_with_employee = fields.Boolean(required = True)
    recommendation = fields.Text() # Your recommendation for present and future job classification

    # Signatures
    employee_signature = fields.Char()
    employee_signature_date = fields.Date()

    ## Scores
    ## TODO: use reference with appraisal traits
    # appraisal_score_ids = fields.One2many('stadia.appraisal.score', 'appraisal_id')
    kn_1 = knowledge 
    kn_2 = knowledge
    kn_3 = knowledge
    kn_avg = fields.Float(compute="_compute_kn_avg")

    qu_1 = quantity
    qu_2 = quantity
    qu_3 = quantity
    qu_avg = fields.Float(compute="_compute_qu_avg")

    ac_1 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    ac_2 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    ac_3 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    ac_avg = fields.Float(compute="_compute_ac_avg")

    ju_1 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    ju_2 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    ju_3 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    ju_avg = fields.Float(compute="_compute_ju_avg")

    in_1 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    in_2 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    in_3 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    in_avg = fields.Float(compute="_compute_in_avg")

    flx_1 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    flx_2 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    flx_3 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    flx_avg = fields.Float(compute="_compute_flx_avg")

    coo_1 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    coo_2 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    coo_3 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    coo_avg = fields.Float(compute="_compute_coo_avg")

    init_1 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    init_2 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    init_3 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    init_avg = fields.Float(compute="_compute_init_avg")

    reli_1 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    reli_2 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    reli_3 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    reli_avg = fields.Float(compute="_compute_reli_avg")

    atd_1 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    atd_2 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    atd_3 = fields.Selection([('A-1', '1',), ('B-2', '2',), ('C-3', '3',), ('D-4', '4',), ('E-5', '5',)])
    atd_avg = fields.Float(compute="_compute_atd_avg")

    total_score = fields.Float(compute="_compute_total_score")

    def convert_to_score(self, v):
        switcher = {
            'A-1': 1,
            '1': 1,
            'B-2': 2,
            '2': 2,
            'C-3': 3,
            '3': 3,
            'D-4': 4,
            '4': 4
        }
        return switcher.get(v, 0)

    @api.depends('kn_1', 'kn_2', 'kn_3')
    def _compute_kn_avg(self):
        for record in self:
            record.kn_avg = (self.convert_to_score(record.kn_1) + self.convert_to_score(record.kn_2) + self.convert_to_score(record.kn_3)) /3

    @api.depends('qu_1', 'qu_2', 'qu_3')
    def _compute_qu_avg(self):
        for record in self:
            record.qu_avg = (self.convert_to_score(record.qu_1) + self.convert_to_score(record.qu_2) + self.convert_to_score(record.qu_3)) / 3

    @api.depends('ac_1', 'ac_2', 'ac_3')
    def _compute_ac_avg(self):
        for record in self:
            record.ac_avg = (self.convert_to_score(record.ac_1) + self.convert_to_score(record.ac_2) + self.convert_to_score(record.ac_3)) / 3

    @api.depends('ju_1', 'ju_2', 'ju_3')
    def _compute_ju_avg(self):
        for record in self:
            record.ju_avg = (self.convert_to_score(record.ju_1) + self.convert_to_score(record.ju_2) + self.convert_to_score(record.ju_3)) / 3

    @api.depends('in_1', 'in_2', 'in_3')
    def _compute_in_avg(self):
        for record in self:
            record.in_avg = (self.convert_to_score(record.in_1) + self.convert_to_score(record.in_2) + self.convert_to_score(record.in_3)) / 3

    @api.depends('flx_1', 'flx_2', 'flx_3')
    def _compute_flx_avg(self):
        for record in self:
            record.flx_avg = (self.convert_to_score(record.flx_1) + self.convert_to_score(record.flx_2) + self.convert_to_score(record.flx_3)) / 3

    @api.depends('coo_1', 'coo_2', 'coo_3')
    def _compute_coo_avg(self):
        for record in self:
            record.coo_avg = (self.convert_to_score(record.coo_1) + self.convert_to_score(record.coo_2) + self.convert_to_score(record.coo_3)) / 3

    @api.depends('init_1', 'init_2', 'init_3')
    def _compute_init_avg(self):
        for record in self:
            record.init_avg = (self.convert_to_score(record.init_1) + self.convert_to_score(record.init_2) + self.convert_to_score(record.init_3)) / 3

    @api.depends('reli_1', 'reli_2', 'reli_3')
    def _compute_reli_avg(self):
        for record in self:
            record.reli_avg = (self.convert_to_score(record.reli_1) + self.convert_to_score(record.reli_2) + self.convert_to_score(record.reli_3)) / 3

    @api.depends('atd_1', 'atd_2', 'atd_3')
    def _compute_atd_avg(self):
        for record in self:
            record.atd_avg = (self.convert_to_score(record.atd_1) + self.convert_to_score(record.atd_2) + self.convert_to_score(record.atd_3)) / 3

    @api.depends('kn_avg', 'qu_avg', 'ac_avg', 'ju_avg', 'in_avg', 'flx_avg', 'coo_avg', 'init_avg', 'reli_avg', 'atd_avg')
    def _compute_total_score(self):
        for record in self:
            record.total_score = record.kn_avg + record.qu_avg + record.ac_avg + record.ju_avg + record.in_avg + record.flx_avg + record.coo_avg + record.init_avg + record.reli_avg + record.atd_avg