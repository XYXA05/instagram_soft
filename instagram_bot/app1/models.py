from django.db import models


class Instagram_acaunts(models.Model):
    
    mail = models.TextField(blank=False, null=False)
    password = models.TextField(blank=False, null=False)
    instagram_acaunts_for_get = models.TextField(null=False, blank=False)
    enter_count = models.PositiveIntegerField(default=0)

    
class acaunts_for_get(models.Model):

    class Meta:
        db_table = 'acaunts_for_get'

    filters = (('use','use'), ('not use','not use'))
    filter_massage = (('send_massage','send_massage'),('not_send_massage','not_send_massage'))

    acaunts_href = models.TextField(blank=True, null=True, unique=True)
    used = models.TextField(choices=filters, default='not use')
    send_massage_point = models.TextField(choices=filter_massage, default='not_send_massage')

class Potoci(models.Model):
    acaunts = models.ManyToManyField(Instagram_acaunts)
    chice = (('text', 'text'), ('text_with_gpt', 'text_with_gpt'))
    promt = models.TextField(null=True, blank=False)
    chice_answer = models.TextField(null=False, blank=False, choices=chice)