class CSVError(Exception):
    """Вызывается при неправильном формате CSV файла"""
    pass

class InvalidDataError(Exception):
    """Вызывается при критических ошибках валидации данных."""
    pass
