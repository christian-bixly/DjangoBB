from optparse import make_option
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils import timezone
from djangobb_forum.models import Ban


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--all', action='store_true', dest='all', default=False, 
                    help=u'Unban all users'),
        make_option('--by-time', action='store_true', dest='by-time', default=False, 
                    help=u'Unban users by time'),
    )
    help = u'Unban users'

    def handle(self, *args, **options):
        if options['all']:
            bans = Ban.objects.all()
            user_ids = bans.values_list('user', flat=True)
            User.objects.filter(id__in=user_ids).update(is_active=True)
            bans.delete()
        elif options['by-time']:
            bans = Ban.objects.filter(ban_end__lte=timezone.now())
            user_ids = bans.values_list('user', flat=True)
            User.objects.filter(id__in=user_ids).update(is_active=True)
            bans.delete()
        else:
            raise CommandError('Invalid options')
