class Detect(object):
    id = 0
    type = 0

    def __init__(self, detect_id, detect_type):
        self.detect_type = detect_type
        self.detect_id = detect_id

    def return_tup(self):
        return (self.detect_id, self.detect_type)