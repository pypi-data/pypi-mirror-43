from django.conf import settings
from django.contrib.staticfiles.finders import FileSystemFinder
import os


class ThemeFileFinder(FileSystemFinder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        theme_dir = getattr(
            settings,
            'THEME_DIR',
            os.path.join(settings.BASE_DIR, 'themes')
        )

        self.locations.append(
            (
                'theme',
                os.path.join(
                    theme_dir,
                    getattr(settings, 'THEME', 'default'),
                    'static'
                )
            )
        )
