class Errors:
    class PMError(Exception):
        pass

    class ServerError(PMError):
        pass

    class UnidentifiedError(PMError):
        pass

    class VersionIsRequiredError(PMError):
        pass

    class PathError(PMError):
        pass

    class IsNotDir(PathError):
        pass

    class TarError(PMError):
        pass
