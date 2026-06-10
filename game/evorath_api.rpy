## Sanctioned mechanics API bridge (§4, §5.9).
## Imports the pure-Python systems via game/api.py (not via systems.* directly)
## so the layer-contract check passes.  Narrative .rpy files call these wrapper
## functions, which inject player_state from the store at call time.

init -100 python:
    import api as _api_mod
    from api import GameState, CharacterBuilder

    # ── Sanctioned API wrappers ─────────────────────────────────────────────

    def check(attribute, skill, dc, adv_sources=None):
        """d20 + attr + skill vs DC. Returns CheckResult. (§5.9)"""
        return _api_mod.resolve_check(player_state, attribute, skill, dc, adv_sources)

    def adjust_stat(stat, delta):
        """Adjust an attribute or skill by delta. (§4)"""
        _api_mod.adjust_stat(player_state, stat, delta)

    def set_flag(name):
        """Record a story flag on player_state. (§4)"""
        _api_mod.set_flag(player_state, name)

    def has_flag(name):
        """Return True if the named flag is set. (§4)"""
        return _api_mod.has_flag(player_state, name)

    def add_item(item_id):
        """Add an item to player_state inventory. (§4)"""
        _api_mod.add_item(player_state, item_id)

    def has_item(item_id):
        """Return True if item_id is in inventory. (§4)"""
        return _api_mod.has_item(player_state, item_id)

