import os
import logging
from wally.provider import Provider, BaseProvider


@Provider.register
class Local(BaseProvider):

    def __init__(self, config):
        self.folder = config['local']['folder']
        self.recurse = config['local']['recurse']
        self.wallpapers = []
        self.ix = 0
        self.data_dir = os.path.join(config['data_directory'], "local")
        self.state_file = os.path.join(self.data_dir, 'state')

        try:
            os.stat(self.data_dir)
        except FileNotFoundError:
            logging.info("Missing data directory. Creating...")
            os.mkdir(os.path.join(self.data_dir))
            logging.info('done')

        try:
            os.stat(self.state_file)
        except FileNotFoundError:
            logging.info("Missing state file. Creating...")
            open(self.state_file, 'a').close()
            logging.info('done')

        if self.recurse:
            self.populate_recursive()
        else:
            self.populate()

    def __iter__(self):
        return self

    def __next__(self):
        return self._next_wallpaper()

    def populate(self):
        for file in os.listdir(self.folder):
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                self.wallpapers.append(os.path.join(self.folder, file))

    def populate_recursive(self):
        for root, _, files in os.walk(self.folder):
            for file in files:
                if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                    self.wallpapers.append(os.path.join(root, file))

    def _next_wallpaper(self):
        if self.ix == len(self.wallpapers) - 1:
            self.ix = 0
        else:
            self.ix += 1
        return self.wallpapers[self.ix]

    def save_state(self):
        try:
            with open(self.state_file, 'w') as fp:
                fp.write(str(self.ix))
                logging.info('Successfully saved current state')
            return True
        except Exception as e:
            logging.error(f"Exception while opening file {self.state_file}: {e}")

        return False

    def restore_state(self):
        # Restore index of wallpaper array
        try:
            with open(self.state_file, 'r') as fp:
                data = fp.read()
                if data:
                    self.ix = int(data.strip())
                    logging.info("Successfully restored previous state")
                    return True
                else:
                    logging.error("No previous state found")
        except Exception as e:
            logging.error(f"Failed to restore state: {e}")

        return False
