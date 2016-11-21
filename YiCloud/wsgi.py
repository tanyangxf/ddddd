"""
WSGI config for YiCloud project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from YiCloud import settings
from multiprocessing import Process

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "YiCloud.settings")

application = get_wsgi_application()

def worker():
    '''
        Multi process service VNC start
    '''

    dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'utils')

    websockify_path = os.path.join(dir_path, 'vnc', 'utils', 'websockify', 'websockify.py')
    web_path = os.path.join(dir_path, 'vnc')
    target_path = os.path.join(dir_path, 'vnc', 'vnc_tokens')

    cmd = u'python %s --web=%s --target-config=%s %s' %(websockify_path, web_path, target_path, settings.VNC_PROXY_PORT )

    os.system(cmd)

def start_websockify():
    '''
        Start the VNC agent service
        ./utils/websockify/websockify --web=. --target-config=vnc_tokens 6080
        {'target_cfg': '/home/xiaofei/work/noVNC/vnc_tokens', 'listen_port': 6080}
    '''

    print u'start vnc proxy..'

    t = Process(target=worker, args=())
    t.start()

    print u'vnc proxy started..'

start_websockify()
