import shutil


class ProwlerWrapper:

    @staticmethod
    def is_available():

        return (
            shutil.which("prowler")
            is not None
        )