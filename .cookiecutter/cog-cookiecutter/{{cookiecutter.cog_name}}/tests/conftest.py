"""Shared fakes for the adapter-layer tests. Module stubbing lives in one
place (../conftest.py) and is not duplicated here -- this module only holds
the fake Discord-facing objects tests construct directly."""

from __future__ import annotations

from typing import Any


class FakeGuild:
    def __init__(self, guild_id: int) -> None:
        self.id = guild_id


class FakeContext:
    def __init__(self, guild_id: int = 12345) -> None:
        self.guild = FakeGuild(guild_id)
        self.sent: list[str] = []

    async def send(self, content: str = "") -> None:
        self.sent.append(content)

    async def send_help(self) -> None:
        self.sent.append("__help__")


class FakeCorridor:
    """Stands in for `bot.get_cog("Corridor")`. Tests here verify this cog
    *asks* corridor to reply/check permissions with the right arguments --
    what corridor actually renders/decides is covered by corridor's own
    test suite, not duplicated here."""

    def __init__(self, allow_permission: bool = True) -> None:
        self.allow_permission = allow_permission
        self.replies: list[dict[str, Any]] = []
        self.permission_checks: list[object] = []

    async def send_reply(
        self,
        ctx: object,
        *,
        title: str | None = None,
        description: str | None = None,
        content: str | None = None,
    ) -> None:
        self.replies.append({"title": title, "description": description, "content": content})

    async def require_permission(self, ctx: object, group: object) -> bool:
        self.permission_checks.append(group)
        return self.allow_permission


class FakeBot:
    def __init__(self, corridor: FakeCorridor | None = None) -> None:
        self.corridor = corridor or FakeCorridor()

    def get_cog(self, name: str) -> Any:
        if name == "Corridor":
            return self.corridor
        return None
