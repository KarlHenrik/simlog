import os

import numpy

def ensurePathExists(fn):
    "Assumes that fn consists of a basepath (folder) and a filename, and ensures that the folder exists."
    path = os.path.split(fn)[0]

    if not os.path.exists(path):
        #oldMask = os.umask(0002)
        os.makedirs(path)

class HLogger:
    HIGH = 30
    MEDIUM = 20
    LOW = 10
    
    def __init__(self, base_context : list, output_level : int = 2):
        self._base_context = base_context
        self._output_level = self.MEDIUM
        self._extra_contexts = []

    def _get_context(self):
        list_of_strings = self._base_context + [item for sublist in self._extra_contexts for item in sublist]
        return list_of_strings

    def log_append(self, content, relative_context : list, level : int = MEDIUM):
        if level < self._output_level:
            return
        fn = self._get_fn(relative_context)
        
        with open(fn, 'a') as outF:
            outF.write(str(content) + ',')

    def log_histogram(self, content, relative_context : list, level : int = MEDIUM):
        if level < self._output_level:
            return
        #ignoring histogram for now..
        self.log_raw_numbers([x for x in content], relative_context, level)

    def log_raw_numbers(self, content, relative_context : list, level : int = MEDIUM):
        if level < self._output_level:
            return
        fn = self._get_fn(relative_context)
        
        assert isinstance(content,list), type(content) #just for now..
        with open(fn, 'w') as outF:
            for el in content:
                if isinstance(el, numpy.ndarray): #just for now
                    outF.write(','.join([str(x) for x in el]) + '\n')
                else:
                    outF.write(str(el) + ',')
                    
    def _get_fn(self, relative_context):
        context = self._get_context() + relative_context
        fn = '/'.join(context) + '.csv'
        ensurePathExists(fn)
        return fn
        
class InnerContext:
    def __init__(self, logger : HLogger, context : list):
        self._logger = logger
        self._context = context

    def __enter__(self):
        self._logger._extra_contexts.append(self._context)

    def __exit__(self, exception_type, exception_value, traceback):
        self._logger._extra_contexts.pop()
