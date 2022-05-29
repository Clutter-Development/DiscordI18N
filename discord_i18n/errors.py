__all__ = ("DiscordI18NError", "UnknownTranslationString", "NoFallback")


class DiscordI18NError(Exception):
    """The base exception class for this library."""


class UnknownTranslationString(DiscordI18NError):
    """Raised when a translation string doesn't exist."""


class NoFallback(DiscordI18NError):
    """Raised when the fallback language isn't in the provided languages."""
