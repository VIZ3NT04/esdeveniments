# -*- coding: utf-8 -*-
from sys import maxsize

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class esdeveniments(models.Model):
    _name = 'esdeveniments.esdeveniments'
    _description = 'esdeveniments.esdeveniments'

    nom = fields.Char(string='Nom',required=True)
    data_inici = fields.Date(string='Data inici',default=fields.Datetime.now)
    data_fi = fields.Date(string='Data final')
    duracion = fields.Integer(string='Duracion',compute='_compute_duracion',store=True)
    descripcio = fields.Char(string='Descripcio')
    foto = fields.Image(string='Foto',max_width=200)
    llista_participants = fields.Many2many('res.partner', string='Participantes')

    @api.depends('data_inici', 'data_fi')
    def _compute_duracion(self):
        for record in self:
            if record.data_inici and record.data_fi:
                # Calculamos la duración en días
                start_date = fields.Date.from_string(record.data_inici)
                end_date = fields.Date.from_string(record.data_fi)
                # Aseguramos que la fecha de fin es mayor o igual a la de inicio
                record.duracion = (end_date - start_date).days
            else:
                record.duracion = 0
    #Constrains per a fer els field en un rago predefinit
    @api.constrains('data_inici', 'data_fi')
    def _check_fechas(self):
        for record in self:
            print("Verificando fechas: ", record.data_inici, record.data_fi)
            if record.data_fi and record.data_inici:
                if record.data_fi <= record.data_inici:
                    raise ValidationError("La fecha de fin no puede ser menor que la fecha de inicio.")

    @api.constrains('llista_participants')
    def _check_llista(self):
        for record in self:
            if record.llista_participants:
                if len(record.llista_participants) > 2:
                    raise ValidationError("No puede hanbr mes de 2 participants per esdeveniment.")


