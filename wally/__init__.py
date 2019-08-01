import logging
import os
import subprocess
import sys
import time
from providers import *
from wally.provider import Provider


class Wally:

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('wallyd')

        # Create data directory if doesn't exist
        try:
            os.stat(self.config['data_directory'])
        except FileNotFoundError:
            os.mkdir(self.config['data_directory'])


    def run(self, no_restore):
        cls = Provider.resolve(self.config['provider'])
        if not cls:
            self.logger.error("Provider `{}` not available".format(self.config['provider']))
            sys.exit(1)

        provider_obj = cls(self.config)

        try:
            if not no_restore:
                provider_obj.restore_state()
            else:
                self.logger.info("State override. Skipping state restore.")
            for f in provider_obj:
                ret_code, stderr = self.set_wallpaper(f)

                if ret_code == 0:
                    self.logger.info("Successfully set wallpaper: {}".format(f))
                else:
                    self.logger.error("Failed to set wallpaper {}: {}".format(f, stderr))

                self.logger.info("Sleeping for delay: {}".format(self.config['delay']))
                time.sleep(self.config['delay'])
        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal (SIGINT)...")
            self.logger.info("Storing provider state")
            provider_obj.save_state()
            self.logger.info("Exiting")
 
    def set_wallpaper(self, f):
        """
        Set provided image file as wallpaper using `feh`.
        This runs synchronously.
        """
        cmd = "DISPLAY=:0 feh --bg-scale '{}'".format(f)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, stderr = p.communicate()
        return p.returncode, stderr
