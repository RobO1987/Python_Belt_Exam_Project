from __future__ import unicode_literals
from django.db import models
# from datetime import datetime
# import datetime


class Userinfo (models.Model):
    name = models.CharField(max_length = 100)
    alias = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    # DOB = models.DateField(auto_now= False , auto_now_add = False)
    ###no idea how to get the DOB working with a datefield....

class Quotecontribute (models.Model):
    quoteauthor = models.CharField(max_length = 100)
    quotemessage = models.CharField(max_length = 500)
    user = models.ForeignKey(Userinfo, related_name = 'quote_contributions')

class Quotefavorites (models.Model):
    quoteauthorfav = models.CharField(max_length = 100)
    quotemessagefav = models.CharField(max_length = 500)
    quote = models.ForeignKey(Quotecontribute, related_name = 'quote_favorites')
    userfav = models.ForeignKey(Userinfo, related_name = 'user_quote_favorites')
