class EmptyResultSetException(Exception):
    def __init__(self):
        super().__init__("Returned result set is empty")
