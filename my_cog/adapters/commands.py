"""Discord-facing commands. Thin: translate ctx <-> service calls only."""

from __future__ import annotations

from redbot.core import commands

from ..application import CounterService


class CommandsMixin:
    """Requires `self._service: CounterService` (provided by CogBase)."""

    _service: CounterService

    @commands.hybrid_group(name="my_cog")
    async def my_cog_group(self, ctx: commands.Context) -> None:
        """A short one-line description of the cog."""

        if ctx.invoked_subcommand is None:
            await ctx.send_help()

    @my_cog_group.command(name="count")
    async def count(self, ctx: commands.Context) -> None:
        """Show this server's current count."""

        snapshot = await self._service.show(ctx.guild.id)
        await ctx.send(f"Count: {snapshot.count}")

    @my_cog_group.command(name="bump")
    async def bump(self, ctx: commands.Context) -> None:
        """Increment this server's count by one."""

        snapshot = await self._service.bump(ctx.guild.id)
        await ctx.send(f"Count is now: {snapshot.count}")
