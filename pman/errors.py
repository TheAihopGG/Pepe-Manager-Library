class Errors:
    class PMError(Exception):
        pass

    class ServerError(PMError):
        pass

    class UnidentifiedError(PMError):
        pass
