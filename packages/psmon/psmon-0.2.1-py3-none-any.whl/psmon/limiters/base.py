class Limiter(object):
    def __init__(self, *args, **kwargs):
        pass

    def preexec(self):
        pass

    def tick(self, process_info):
        pass

    def update(self, state):
        return state

    def accumulate_reducer(self, a, b):
        return a + b

    def teardown(self)
        pass
