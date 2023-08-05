# -*- coding: utf-8 -*-
import logging
import os
import time

from pytils.translit import translify

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.validators import validate_email, ValidationError
from django.core.exceptions import ImproperlyConfigured

from commonstuff.str_utils import load_class_from_string, autocorrect_email

# пытаемся найти приложение с нашими моделями
for _app in settings.INSTALLED_APPS:
    try:
        WrongEmailLog = load_class_from_string(_app + '.models.WrongEmailLog')
        Digest = load_class_from_string(_app + '.models.Digest')
    except (ImportError, ImproperlyConfigured):
        pass


log_file = os.path.join(settings.BASE_DIR, 'log', 'checkemailautocorrection.log')
logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler(log_file))


class Command(BaseCommand):
    """Консольная команда для проверки автокоррекции e-mail адресов.
    
    Код автокоррекции e-mail может разрастись очень сильно, там неочевидные
    регэкспы и за результатами его работы надо следить на живых данных.
    """
    help = 'Checks e-mail address autocorrection algo on real data.'
    
    def handle(self, *args, **options):
        logger.info("cleansubscriptions started at %s.", time.asctime(time.localtime(time.time())))
        
        print(translify("1. Проверяем, не портит ли автоисправление " +
                        "нормальные e-mail (по базе активных)."))
        cnt = 0
        for s in Digest.objects.filter(is_active=True, errors=0):
            before = s.email.lower()
            after = autocorrect_email(before)
            if before != after:
                cnt += 1
                print("%s -> %s" % (before, after))
        if not cnt:
            print(translify("Нет, не портит."))
        print()
        
        print(translify("2. Проверяем, когда удалось исправить e-mail " +
                        "(по логу неправильных адресов)."))
        good = []
        bad = []
        cnt = 0
        for w in WrongEmailLog.objects.all():
            cnt += 1
            before = w.wrong_email.lower()
            after = autocorrect_email(before)
            try:
                validate_email(after)
                good.append( (before, after) )
            except ValidationError:
                if before != after:
                    bad.append( (before, after) )
        print(translify("Всего записей: %d" % cnt))
        print(translify("Исправлено успешно: %d" % len(good)))
        self._log_data(good, "SUCCESSFUL AUTOCCORRECTIONS")
        print(translify("Исправлено неудачно: %d" % len(bad)))
        self._log_data(bad, "FAILED AUTOCCORRECTIONS")
        print(translify("Никак не исправлено: %d" % (cnt - (len(good)+len(bad)))))
        print(translify("Все случаи, кроме никак, залогированы в %s" % log_file))
    
    def _log_data(self, data, title):
        if len(data):
            logger.info("%s - %d:" % (title, len(data)))
            for before, after in data:
                logger.info("%s -> %s" % (before, after))
            logger.info("")
    