import os


DEFAULT_EPOCHS = 10
DEFAULT_EPOCH_STEPS = 5
DEFAULT_BATCH_SIZE = 256
TRAINING_DATA_KEY = 'TRAINING_DATA_PATH'
EXPORT_PATH_KEY = 'EXPORT_PATH'
START_FILE_NAME = 'START'


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
        self.rounds = 0
        self.round_steps = 0
        self.fitness_key = None
        self.minimum_score = None

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

        if not self.rounds:
            print('WARNING: Using default rounds of %d' % DEFAULT_EPOCHS)
            self.rounds = DEFAULT_EPOCHS

        if not self.round_steps:
            print('WARNING: Using default epoch steps of %d' % DEFAULT_EPOCH_STEPS)
            self.round_steps = DEFAULT_EPOCH_STEPS

        if not self.fitness_key:
            print('WARNING: No fitness key set, will not abort early')

        if not self.minimum_score:
            print('WARNING: minimum_score not set, will not abort early')

        if not isinstance(self.minimum_score, (int, float)):
            print('WARNING: minimum_score is not a number, will not abort early')
            self.minimum_score = None

    def do(self):
        model_name = self.name_model()
        (x_train, y_train), (x_test, y_test), nb_classes, input_shape = self.load_data(self.__training_data_path)
        model = self.model_func(nb_classes, input_shape)
        model = self.compile_model(model)

        with open(os.path.join(self.__export_path, START_FILE_NAME), 'w') as f:
            f.write(START_FILE_NAME)

        trained_rounds = 0
        fitness = {}
        while True:
            print(
                'Training model %s, rounds %d -> %d' % (
                    model_name,
                    trained_rounds,
                    trained_rounds + self.round_steps,
                )
            )

            model = self.train_epoch(model, x_train, y_train, self.batch_size, self.round_steps)
            fitness = self.evaluate_model(model, x_test, y_test)

            # Evaluate fitness
            if isinstance(fitness, dict) and self.fitness_key and self.minimum_score:
                score = fitness.get(self.fitness_key)
                if score < self.minimum_score:
                    print('Fitness: %.2f, Minimum: %.2f, aborting' % (score, self.minimum_score))
                    fitness['aborted'] = True
                    break

            if trained_rounds >= self.rounds:
                break

            trained_rounds += self.round_steps

        # Indent these lines to save per epoch set
        self.save_fitness(fitness, self.__export_path)
        self.save_model(model_name, model, self.__export_path, self.rounds)

    def name_model(self):
        raise NotImplementedError('name_model needs to be implemented')

    def load_data(self, file_path):
        raise NotImplementedError('load_data needs to be implemented')

    def get_model_map(self):
        raise NotImplementedError('get_model_map needs to be implemented')

    def build_model(self, model):
        raise NotImplementedError('build_model not implemented')

    def train_epoch(self, model, x_train, y_train, batch_size, rounds=1):
        raise NotImplementedError('train_epoch not implemented')

    def evaluate_model(self, model, x_test, y_test):
        raise NotImplementedError('evaluate_model not implemented')

    def save_model(self, model_name, model, epoch):
        raise NotImplementedError('save_model not implmeneted')

    def save_fitness(self, fitness, export_path):
        raise NotImplementedError('save_fitness not implmeneted')
