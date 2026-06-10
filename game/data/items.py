"""Item registry (§5.6).

item_id:      canonical ID used in GameState.inventory.
display_name: shown on inventory/confirm screens.
description:  one line.
equipment_adv_label: if not None, this item grants advantage with this label
                     when "right tool for the job" triggers (§5.10).
"""

ITEMS: dict[str, dict] = {
    # Beach basic finds
    "rope_coil": {
        "display_name": "Coil of Rope",
        "description": "Salt-stiff but sound — always useful.",
        "equipment_adv_label": None,
    },
    "waterlogged_pack": {
        "display_name": "Waterlogged Pack",
        "description": "Soaked through, but the waxed inner pocket held: dried strips of meat and a waterskin.",
        "equipment_adv_label": None,
    },
    "salvage_knife": {
        "display_name": "Salvage Knife",
        "description": "A ship's knife, blade intact. Salt-pitted but still sharp.",
        "equipment_adv_label": "Advantage: proper tools",
    },
    # Thorough-find evidence item
    "device_fragment": {
        "display_name": "Strange Fragment",
        "description": (
            "A piece of something that doesn't belong to any ship's fitting you know. "
            "Warped metal, fused at one end as though by tremendous directed heat."
        ),
        "equipment_adv_label": None,
    },
    # Nat-20 bonus find
    "officers_compass": {
        "display_name": "Officer's Compass",
        "description": "A brass compass in a leather case, still true. Someone cared for this.",
        "equipment_adv_label": "Advantage: navigator's tool",
    },
}
