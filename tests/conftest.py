import sys
import types
from datetime import datetime, timedelta

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

    def shift(self, *, seconds: int = 0) -> "Arrow":
        return Arrow(self.dt + timedelta(seconds=seconds))

    def humanize(self, other: "Arrow", *, only_distance: bool = False) -> str:
        seconds = int(abs((self.dt - other.dt).total_seconds()))
        units = [
            ("year", 31536000),
            ("month", 2592000),
            ("week", 604800),
            ("day", 86400),
            ("hour", 3600),
            ("minute", 60),
            ("second", 1),
        ]
        for name, count in units:
            if seconds >= count:
                value = seconds // count
                break
        else:
            value, name = 0, "second"
        if value == 1:
            article = "an" if name[0] in "aeiou" else "a"
            return f"{article} {name}"
        return f"{value} {name}{'s' if value != 1 else ''}"


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
