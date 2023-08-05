from subprocess import run as subprocess_run


def run(command, **kwargs):
    try:
        subprocess_run(command, shell=True, **kwargs)
    except KeyboardInterrupt:
        print()


def shell(command, **kwargs):
    try:
        return subprocess_run(command, shell=True, capture_output=True, text=True, **kwargs)
    except KeyboardInterrupt:
        print()


def shell_list(command, **kwargs):
    try:
        return subprocess_run(
            command, shell=True, capture_output=True, text=True, **kwargs
        ).stdout.split("\n")
    except KeyboardInterrupt:
        print()
