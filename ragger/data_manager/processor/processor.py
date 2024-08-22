
class ProcessorManager:
    def __init__(self):
        self.pipeline = ProcessingPipeline()

    def process(self, literatures):
        for literature in literatures:
            literature = self.pipeline.process(literature)

        return literatures


class ProcessingPipeline:
    def __init__(self):
        self.pipeline = {}
