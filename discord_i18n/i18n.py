from __future__ import annotations

import os
from typing import TYPE_CHECKING, Literal

import discord
import json5
from discord.ext import commands

from .errors import NoFallback, UnknownTranslationString
from .misc import find_in_nested_dict

if TYPE_CHECKING:
    from mongo_manager import MongoManager

__all__ = ("DiscordI18N",)


class DiscordI18N:
    def __init__(self, lang_file_dir: str, /, *, db: MongoManager, fallback: str) -> None:
        self._db = db
        self.languages = {}
        self.fallback = fallback

        files = os.listdir(lang_file_dir)

        for fn in files:
            if fn.endswith(("json", "json5")):
                with open(os.path.join(lang_file_dir, fn)) as f:
                    self.languages[fn[: -len(fn.rsplit(".", 1)[-1])]] = json5.load(f)

        if fallback not in self.languages:
            raise NoFallback(
                f"The fallback language ({fallback}) does not exist in the languages directory ({lang_file_dir})."
            )

    async def translate_with_id(
        self, id: int, text: str, /, *, type: Literal["guild", "user"]
    ) -> str:
        """Fetches the preferred language for the user with an id. Then gets the translation with the language. If the translation is not found, the fallback translation is used. If the fallback translation is not found, an error is raised.

        Args:
            id (int): The target id.
            text (str): The translation code to get translation of.
            type ("guild" | "user"): The id's type.

        Raises:
            UnknownTranslaionString: If the fallback translation is not found.

        Returns:
            str: The translated string.
        """
        translated = find_in_nested_dict(
            self.languages.get(
                await self._db.get(f"{f'{type}s'}.{id}.language", default=self.fallback),
                self.fallback,
            ),
            text,
            default=find_in_nested_dict(
                self.languages[self.fallback],
                text,
            ),
        )
        if not translated:
            raise UnknownTranslationString(f"Unknown translation string: {text}")

        return translated

    async def __call__(
        self,
        ctx: discord.Message | discord.Interaction | commands.Context,
        text: str,
        /,
        *,
        use_guild: bool = False,
    ) -> str:
        """Translates a translation code to human-readable text.

        Args:
            ctx (discord.Message | discord.Interaction | commands.Context): The context to get the language from.
            text (str): The translation code to get translation of.
            use_guild (bool, optional): Whether to use the guild's language or the user's language. Defaults to False.

        Raises:
            UnknownTranslaionString: If the fallback translation is not found.

        Returns:
            str: The translated string.
        """
        is_interaction = isinstance(ctx, discord.Interaction)

        target_id = (ctx.guild_id if is_interaction else ctx.guild.id) if use_guild else (ctx.user.id if is_interaction else ctx.author.id)  # type: ignore
        translated = await self.translate_with_id(target_id, text, type="guild" if use_guild else "user")  # type: ignore

        return translated
