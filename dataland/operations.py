

class Operation(object):
    def perform(self):
        raise NotImplemented

class AppendOperation(Operation):
    INPUT = ''
    IGNORE_DUPLICATES=False # requires full dataset to be read into memory

    def perform(self):
        if not os.path.isfile(self.__class__.INPUT):
            raise ValueError('Operation INPUT "{}" is not a valid path'.format(INPUT))

        new_records = self.new_records()

        if self.__class__.IGNORE_DUPLICATES:
            # TODO this does not work as expected
            # it should read the old dataframe and only select new records
            old_records = pd.read_csv(self.__class__.INPUT)
            new_records = old_records.concat(new_records).drop_duplicates()

        assert (new_records.columns.values ==  self.get_template().columns.values).all(), 'new_records do not match existing data template'
        with open(self.__class__.INPUT, 'a') as input_file:
            new_records.to_csv(input_file, header=False, index=False)

        logging.info('{} updated {} records to {}'.format(self.__class__.__name__, len(new_records), self.__class__.INPUT))

    def new_records(self):
        raise NotImplemented
        '''
        returns a dataframe containing new records to be appended
        '''

    def get_template(self):
        return get_template(self.__class__.INPUT)

class TransformOperation(Operation):
    INPUT=''
    OUTPUT=''

    def perform(self):
        if not os.path.isfile(self.__class__.INPUT):
            raise ValueError('Operation INPUT "{}" is not a valid path'.format(INPUT))

        input_dataframe = pd.read_csv(self.__class__.INPUT)
        input_dataframe = self.update(input_dataframe)

        with open(self.__class__.INPUT, 'a') as input_file:
            input_dataframe.to_csv(self.__class__.OUTPUT, mode='w+', index=False, float_format='%.4f')

        logging.info('{} updated {} records to {}'.format(self.__class__.__name__, len(input_dataframe), self.__class__.OUTPUT))

    def transform(self, input_dataframe):
        raise NotImplemented
        '''
        returns new output dataframe
        '''

class UpdateOperation(TransformOperation):

    def __init__(self, *args, **kwargs):
        self.__class__.OUTPUT=self.__class__.INPUT
        self.transform = self.update
        super(UpdateOperation, self).__init__(*args, **kwargs)

    def update(self, input_dataframe):
        raise NotImplemented
        '''
        returns updated version of `input_dataframe`
        '''
