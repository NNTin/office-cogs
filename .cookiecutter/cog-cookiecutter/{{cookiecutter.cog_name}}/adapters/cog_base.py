"""Dependency composition and lifecycle for the {{ cookiecutter.cog_name.replace('-', '_').split('_') | map('capitalize') | join }} Cog."""

from __future__ import annotations

from typing import Any

from redbot.core.bot import Red

from ..application import CounterService
from ..infrastructure import RedCounterRepository


class CogBase:
    """Wire services once and own resources spanning the Cog lifetime."""

    bot: Red
    config: Any

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self._repository = RedCounterRepository.create(self)
        self.config = self._repository.config
        self._service = CounterService(self._repository)
        self._corridor: Any = None

    async def cog_load(self) -> None:
        """Extension point for start-up work (background tasks, sessions, ...).

        corridor is declared in required_cogs, so Red loads it first -- but
        fetch defensively rather than assuming load order is guaranteed.
        """

        self._corridor = self.bot.get_cog("Corridor")
        if self._corridor is None:
            raise RuntimeError(
                "corridor is not loaded. It's declared in required_cogs -- "
                "install/load it before this cog."
            )

    async def cog_unload(self) -> None:
        """Extension point for teardown work."""
