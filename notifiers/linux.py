import subprocess

from .base import Notifier

class Linux(Notifier):
    def notify(self, to, msg):
        subprocess.Popen(['notify-send', msg])
