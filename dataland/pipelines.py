'''

'''
from dataland.dataset import load_dataset

class Pipeline(object):
    def __init__(self, inputs, output, stages, *args, **kwargs):
        self.inputs = inputs
        self.output = output
        self.stages = stages

    def run(self):
        self.env = { input: load_dataset(input) for input in self.inputs }
        for stage in self.stages:
            import pdb; pdb.set_trace()
