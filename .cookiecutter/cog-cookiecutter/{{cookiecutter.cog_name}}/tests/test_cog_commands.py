"""The only test that needs the discord/redbot stubs installed by the
package-root conftest.py -- everything below the adapter layer is testable
without them (see test_domain_models.py / test_application_service.py)."""

from __future__ import annotations

import unittest

from ..{{cookiecutter.cog_name}} import {{ cookiecutter.cog_name.replace('-', '_').split('_') | map('capitalize') | join }}
from .conftest import FakeContext


class TestCommands(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.cog = {{ cookiecutter.cog_name.replace('-', '_').split('_') | map('capitalize') | join }}(bot=object())
        self.ctx = FakeContext()

    async def test_count_reports_zero_initially(self) -> None:
        await self.cog.count.callback(self.cog, self.ctx)

        self.assertEqual(self.ctx.sent, ["Count: 0"])

    async def test_bump_increments_and_replies(self) -> None:
        await self.cog.bump.callback(self.cog, self.ctx)
        await self.cog.bump.callback(self.cog, self.ctx)

        self.assertEqual(self.ctx.sent, ["Count is now: 1", "Count is now: 2"])
