import os


DEFAULT_EPOCHS = 10
DEFAULT_EPOCH_STEPS = 5
DEFAULT_BATCH_SIZE = 256
TRAINING_DATA_KEY = 'TRAINING_DATA_PATH'
EXPORT_PATH_KEY = 'EXPORT_PATH'


class Model(object):
    def __init__(self, **kwargs):
        # Check for data environment variables
        self.__training_data_path = os.environ.get(TRAINING_DATA_KEY)
        if not self.__training_data_path:
            raise SystemExit('%s not found' % TRAINING_DATA_KEY)

        self.__export_path = os.environ.get(EXPORT_PATH_KEY)
        if not self.__export_path:
            raise SystemExit('%s not found' % EXPORT_PATH_KEY)

        self.batch_size = 0
        self.epochs = 0
        self.epoch_steps = 0

        self.__dict__.update(kwargs)

        # Check for required arguments
        if not hasattr(self, 'architecture'):
            raise SystemExit('architecture not set')

        models = self.get_model_map()
        if not isinstance(models, dict):
            raise SystemExit('model map is not a dictionary')

        self.model_func = models.get(self.architecture)
        if not self.model_func:
            raise SystemExit('Unknown architecture')

        if not self.batch_size:
            print('WARNING: Using default batch_size of %d' % DEFAULT_BATCH_SIZE)
            self.batch_size = DEFAULT_BATCH_SIZE

        if not self.epochs:
            print('WARNING: Using default epochs of %d' % DEFAULT_EPOCHS)
            self.epochs = DEFAULT_EPOCHS

        if not self.epoch_steps:
            print('WARNING: Using default epoch steps of %d' % DEFAULT_EPOCH_STEPS)
            self.epoch_steps = DEFAULT_EPOCH_STEPS

    def do(self):
        model_name = self.name_model()
        (x_train, y_train), (x_test, y_test), nb_classes, input_shape = self.load_data(self.__training_data_path)
        model = self.model_func(nb_classes, input_shape)
        model = self.compile_model(model)

        trained_epochs = 0
        fitness = {}
        while True:
            print(
                'Training model %s, epochs %d -> %d' % (
                    model_name,
                    trained_epochs,
                    trained_epochs + self.epoch_steps,
                )
            )

            model = self.train_epoch(model, x_train, y_train, self.batch_size, self.epoch_steps)
            fitness = self.evaluate_model(model, x_test, y_test)

            trained_epochs += self.epoch_steps
            if trained_epochs >= self.epochs:
                break

        # Indent these lines to save per epoch set
        self.save_fitness(fitness, self.__export_path)
        self.save_model(model_name, model, self.__export_path, self.epochs)

    def name_model(self):
        raise NotImplementedError('name_model needs to be implemented')

    def load_data(self, file_path):
        raise NotImplementedError('load_data needs to be implemented')

    def get_model_map(self):
        raise NotImplementedError('get_model_map needs to be implemented')

    def build_model(self, model):
        raise NotImplementedError('build_model not implemented')

    def train_epoch(self, model, x_train, y_train, batch_size, epochs=1):
        raise NotImplementedError('train_epoch not implemented')

    def evaluate_model(self, model, x_test, y_test):
        raise NotImplementedError('evaluate_model not implemented')

    def save_model(self, model_name, model, epoch):
        raise NotImplementedError('save_model not implmeneted')

    def save_fitness(self, fitness, export_path):
        raise NotImplementedError('save_fitness not implmeneted')
