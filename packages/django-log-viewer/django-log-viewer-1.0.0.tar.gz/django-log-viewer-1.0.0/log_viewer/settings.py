# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf import settings

LOG_VIEWER_FILES = getattr(settings, 'LOG_VIEWER_FILES', [])
LOG_VIEWER_FILES_DIR = getattr(settings, 'LOG_VIEWER_FILES_DIR',
                               os.path.join(settings.BASE_DIR, 'logs'))
LOG_VIEWER_ITEMS_PER_PAGE = getattr(settings, 'LOG_VIEWER_ITEMS_PER_PAGE', 50)
LOG_VIEWER_FILE_LIST_TITLE = getattr(settings, 'LOG_VIEWER_FILE_LIST_TITLE', None)
LOG_VIEWER_FILE_LIST_STYLES = getattr(settings, 'LOG_VIEWER_FILE_LIST_STYLES', None)
