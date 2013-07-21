import os.path
import sass
from django.conf import settings
from django.contrib.staticfiles.management.commands import collectstatic


class Command(collectstatic.Command):
    
    def collect(self):
        # before collecting static files we should make the CSS
        with open(
                os.path.join(
                    settings.BASE_DIR,
                    'static',
                    'css',
                    'base.css'
                ),
                'wb'
        ) as w:
            w.write(
                sass.compile(
                    filename=os.path.join(
                        settings.BASE_DIR,
                        'sass',
                        'base.scss'
                    ),
                )
            )
        return super(Command, self).collect()
