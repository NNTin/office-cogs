"""Install stubs before any my_cog module is imported.

The package __init__ imports redbot.core.bot.Red at module scope, so pytest
can't collect anything under this package without Red/discord.py installed
unless these modules exist in sys.modules first. Kept intentionally minimal:
only the surface adapters/infrastructure actually touch.
"""

from __future__ import annotations

import sys
import types
from typing import Any


def _make_stub_module(name: str, **attrs: object) -> types.ModuleType:
    module = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    return module


# --- discord ---
_discord = _make_stub_module("discord")
sys.modules["discord"] = _discord


# --- redbot.core.Config ---
class _FakeConfigValue:
    def __init__(self, data: dict[str, Any], key: str) -> None:
        self._data = data
        self._key = key

    async def __call__(self) -> Any:
        return self._data.get(self._key)

    async def set(self, value: Any) -> None:
        self._data[self._key] = value


class _FakeGuildConfig:
    def __init__(self, defaults: dict[str, Any]) -> None:
        self._data = dict(defaults)

    def __getattr__(self, name: str) -> _FakeConfigValue:
        return _FakeConfigValue(self._data, name)


class _FakeConfig:
    def __init__(self) -> None:
        self._guild_defaults: dict[str, Any] = {}
        self._guilds: dict[int, _FakeGuildConfig] = {}

    @classmethod
    def get_conf(
        cls, cog: object, identifier: int = 0, force_registration: bool = False
    ) -> _FakeConfig:
        return cls()

    def register_guild(self, **defaults: object) -> None:
        self._guild_defaults.update(defaults)

    def guild_from_id(self, guild_id: int) -> _FakeGuildConfig:
        if guild_id not in self._guilds:
            self._guilds[guild_id] = _FakeGuildConfig(self._guild_defaults)
        return self._guilds[guild_id]


# --- redbot.core.commands ---
class _FakeCommand:
    """Stub for a Red command -- callable, supports nested `.command()`."""

    def __init__(self, func: Any) -> None:
        self.callback = func
        self.__wrapped__ = func
        self.__name__ = getattr(func, "__name__", "command")
        self.__doc__ = getattr(func, "__doc__", "")

    async def __call__(self, *args: object, **kwargs: object) -> object:
        return await self.__wrapped__(*args, **kwargs)

    def command(self, **_kwargs: object) -> Any:
        def decorator(func: Any) -> _FakeCommand:
            return _FakeCommand(func)

        return decorator


class _FakeCog:
    @staticmethod
    def listener(func: Any = None) -> Any:
        if func is not None:
            return func

        def decorator(inner: Any) -> Any:
            return inner

        return decorator


class _FakeCommands:
    Cog = _FakeCog
    Context = object

    @staticmethod
    def hybrid_group(**_kwargs: object) -> Any:
        def decorator(func: Any) -> _FakeCommand:
            return _FakeCommand(func)

        return decorator


_redbot = _make_stub_module("redbot")
_redbot_core = _make_stub_module("redbot.core", Config=_FakeConfig, commands=_FakeCommands())
_redbot_core_bot = _make_stub_module("redbot.core.bot", Red=object)
_redbot_core_utils = _make_stub_module(
    "redbot.core.utils",
    get_end_user_data_statement_or_raise=lambda _file: "stubbed data statement",
)

sys.modules["redbot"] = _redbot
sys.modules["redbot.core"] = _redbot_core
sys.modules["redbot.core.bot"] = _redbot_core_bot
sys.modules["redbot.core.utils"] = _redbot_core_utils
