import os
import pandas as pd
import logging

from dataland.storage import storage, dataset_template

class Operation(object):
    def perform(self):
        raise NotImplemented

class AppendOperation(Operation):
    INPUT = ''
    IGNORE_DUPLICATES=False # requires full dataset to be read into memory

    def perform(self):
        storage.pull(self.__class__.INPUT)
        input = storage.local_path(self.__class__.INPUT)
        template = dataset_template(input)

        new_records = self.new_records()
        assert (set(new_records.columns.values) == set(template.columns)), 'new_records do not match existing data template'
        new_records = new_records.reindex(columns=template.columns.tolist())

        if self.__class__.IGNORE_DUPLICATES:
            old_records = pd.read_csv(input)
            new_records = pd.old_records.concat(new_records).drop_duplicates()

        with open(storage.local_path(self.__class__.INPUT), 'a') as input_file:
            new_records.to_csv(input_file, index=False, header=False)

        logging.info('{} updated {} records to {}'.format(self.__class__.__name__, len(new_records), self.__class__.INPUT))
        storage.push(self.__class__.INPUT)

    def new_records(self):
        raise NotImplemented
        '''
        returns a dataframe containing new records to be appended
        '''

class TransformOperation(Operation):
    INPUTS={}
    OUTPUT=''

    def perform(self):
        input_dataframes = {}
        for input, path in self.__class__.INPUTS.items():
            storage.pull(path)
            input_dataframes[input] = pd.read_csv(storage.local_path(path))

        output_dataframe = self.transform(**input_dataframes)

        with open(storage.local_path(self.__class__.OUTPUT), 'w+') as output_file:
            output_dataframe.to_csv(output_file, index=False)

        logging.info('{} transformed {} records into {}'.format(self.__class__.__name__, len(output_dataframe), self.__class__.OUTPUT))
        storage.push(self.__class__.OUTPUT)

    def transform(self, input_dataframe):
        raise NotImplemented
        '''
        returns new output dataframe
        '''

class UpdateOperation(TransformOperation):
    INPUT=''

    def __init__(self, *args, **kwargs):
        self.__class__.OUTPUT=self.__class__.INPUT
        self.transform = self.update
        super(UpdateOperation, self).__init__(*args, **kwargs)

    def update(self, input_dataframe):
        raise NotImplemented
        '''
        returns updated version of `input_dataframe`
        '''
