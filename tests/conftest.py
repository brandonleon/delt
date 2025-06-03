import sys
import types
from datetime import datetime

# Stub for the ``arrow`` package used by ``delt.main``.
arrow_stub = types.ModuleType("arrow")


class Arrow:
    def __init__(self, dt: datetime) -> None:
        self.dt = dt

    def format(self, fmt: str) -> str:
        if fmt == "YYYY-MM-DD HH:mm:ss":
            return self.dt.strftime("%Y-%m-%d %H:%M:%S")
        raise NotImplementedError

    def __sub__(self, other: "Arrow"):
        return self.dt - other.dt


arrow_stub.Arrow = Arrow


def get(date_str: str) -> Arrow:
    return Arrow(datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S"))


def now() -> Arrow:
    return Arrow(datetime.utcnow())


arrow_stub.get = get
arrow_stub.now = now

parser = types.ModuleType("parser")


class ParserError(Exception):
    pass


parser.ParserError = ParserError
arrow_stub.parser = parser

sys.modules.setdefault("arrow", arrow_stub)
sys.modules.setdefault("arrow.parser", parser)

# Minimal stub for the ``typer`` package so that ``delt.main`` can be imported.
typer_stub = types.ModuleType("typer")


class Typer:
    def command(self, *args, **kwargs):
        def decorator(func):
            return func

        return decorator


typer_stub.Typer = Typer


def Option(*args, **kwargs):
    return None


def Argument(*args, **kwargs):
    return None


def echo(*args, **kwargs):
    pass


class Exit(Exception):
    pass


typer_stub.Option = Option
typer_stub.Argument = Argument
typer_stub.echo = echo
typer_stub.Exit = Exit

sys.modules.setdefault("typer", typer_stub)
