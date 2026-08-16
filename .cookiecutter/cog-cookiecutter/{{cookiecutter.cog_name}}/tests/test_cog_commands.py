"""The only tests that need the discord/redbot stubs installed by the
package-root conftest.py -- everything below the adapter layer is testable
without them (see test_domain_models.py / test_application_service.py)."""

from __future__ import annotations

import unittest

from corridor.domain import PermissionGroup

from ..{{cookiecutter.cog_name}} import {{ cookiecutter.cog_name.replace('-', '_').split('_') | map('capitalize') | join }}
from .conftest import FakeBot, FakeContext, FakeCorridor


class TestCommands(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.bot = FakeBot()
        self.cog = {{ cookiecutter.cog_name.replace('-', '_').split('_') | map('capitalize') | join }}(bot=self.bot)
        await self.cog.cog_load()
        self.ctx = FakeContext()

    async def test_count_reports_zero_initially(self) -> None:
        await self.cog.count.callback(self.cog, self.ctx)

        self.assertEqual(
            self.bot.corridor.replies, [{"title": "Count", "description": "0", "content": None}]
        )

    async def test_bump_increments_and_replies_through_corridor(self) -> None:
        await self.cog.bump.callback(self.cog, self.ctx)
        await self.cog.bump.callback(self.cog, self.ctx)

        descriptions = [reply["description"] for reply in self.bot.corridor.replies]
        self.assertEqual(descriptions, ["Now: 1", "Now: 2"])

    async def test_bump_checks_moderator_permission(self) -> None:
        await self.cog.bump.callback(self.cog, self.ctx)

        self.assertEqual(self.bot.corridor.permission_checks, [PermissionGroup.MODERATOR])

    async def test_bump_is_blocked_when_corridor_denies_permission(self) -> None:
        self.bot.corridor = FakeCorridor(allow_permission=False)
        await self.cog.cog_load()

        await self.cog.bump.callback(self.cog, self.ctx)

        self.assertEqual(self.bot.corridor.replies, [])
