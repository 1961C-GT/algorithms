class Algorithm:
    def __init__(self, node_arr):
        self.node_arr = node_arr

    def _process(self, callback):
        self._callback = callback
        self.process(self._run_callback)

    def _run_callback(self):
        self._callback(self.node_arr)

    def process(self, callback):
        pass
