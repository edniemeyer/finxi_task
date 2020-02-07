from django.db import models
from django.utils.html import escape
from django.utils.safestring import mark_safe


class Demand(models.Model):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    ]

    description = models.TextField()
    address = models.TextField()
    info = models.TextField()
    advertiser = models.ForeignKey(
        'auth.User', related_name='demands', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=OPEN,
        editable=False
    )

    def __str__(self):
        ret = self.description + ',' + self.address
        return ret

    def image_tag(self):
        if self.status == Demand.CLOSED:
            return mark_safe('<img src="%s" width="25" height="25" />' % ('/static/shop/img/baseline-highlight_off.svg'))
        else:
            return mark_safe('<img src="%s" width="25" height="25" />' % ('/static/shop/img/baseline-check_circle_outline.svg'))

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
