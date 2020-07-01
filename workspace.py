import os
import logging

from torch.utils.tensorboard import SummaryWriter


def get_logger(path, name='training'):

    filehandler = logging.FileHandler(os.path.join(path, '{}.logs'.format(name)), 'a')
    consolehandler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    filehandler.setFormatter(formatter)
    consolehandler.setFormatter(formatter)

    logger = logging.getLogger(name)

    for hdlr in logger.handlers[:]:  # remove all old handlers
        logger.removeHandler(hdlr)

    logger.addHandler(filehandler)  # set the new handler
    logger.addHandler(consolehandler)

    logger.setLevel(logging.DEBUG)

    return logger


def save_tsdf(filename, data):
    with h5py.File(filename, 'w') as file:
        file.create_dataset('TSDF',
                            shape=data.shape,
                            data=data)

def save_weights(filename, data):
    with h5py.File(filename, 'w') as file:
        file.create_dataset('weights',
                            shape=data.shape,
                            data=data)

class Workspace(object):

    def __init__(self, path):

        self.workspace_path = path
        self.model_path = os.path.join(path, 'model')
        self.log_path = os.path.join(path, 'logs')
        self.output_path = os.path.join(path, 'output')

        os.makedirs(self.workspace_path)
        os.makedirs(self.model_path)
        os.makedirs(self.log_path)
        os.makedirs(self.output_path)

        self.writer = SummaryWriter(self.log_path)

        self._init_logger()

    def _init_logger(self):
        self.train_logger = get_logger(self.log_path, 'training')
        self.val_logger = get_logger(self.log_path, 'validation')

    def save_config(self, config):
        print('Saving config to ', self.workspace_path)
        save_config_to_json(self.workspace_path, config)

    def save_model_state(self, state, is_best=False):
        save_checkpoint(state, is_best, self.model_path)

    def save_tsdf_data(self, file, data):
        tsdf_file = os.path.join(self.output_path, file)
        save_tsdf(tsdf_file, data)

    def save_weigths_data(self, file, data):
        weight_files = os.path.join(self.output_path, file)
        save_weights(weight_files, data)

    def log(self, message, mode='train'):
        if mode == 'train':
            self.train_logger.info(message)
        elif mode == 'val':
            self.val_logger.info(message)


