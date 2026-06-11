## Custom screens for Evorath (§5.2, §5.9, §5.10).
## Visible-tabletop aesthetic: dice, DC, adv/disadv labels shown on every check.

## ─── Main Menu ──────────────────────────────────────────────────────────────

screen main_menu():
    tag menu
    style_prefix "main_menu"

    add Image("images/gui/main_menu.png")
    add Solid("#00000077")

    vbox:
        xalign 0.5
        yalign 0.35
        spacing 8

        add Image("images/gui/evorath_mark.png") xalign 0.5 ysize 120 fit "contain"
        null height 10
        text "EVORATH" xalign 0.5 color "#f0e0c0" size 64 bold True

    vbox:
        xalign 0.5
        yalign 0.72
        spacing 16

        textbutton _("New Game"):
            xsize 260
            xalign 0.5
            action Start()

        textbutton _("Load Game"):
            xsize 260
            xalign 0.5
            action ShowMenu("load")

        textbutton _("Quit"):
            xsize 260
            xalign 0.5
            action Quit(confirm=not main_menu)

style main_menu_button_text:
    idle_color "#ece0c6"        ## light cream — reads on the darkened coast
    hover_color "#ffe6b0"       ## brightens on hover (dark surface: highlight by lightening)
    selected_color "#ffe6b0"
    outlines [ (absolute(2), "#000000bb", absolute(0), absolute(0)) ]  ## halo so text survives the bright sand
    size 30                     ## tunable — gives the buttons menu presence

## ─── Game Menu (save / load / prefs) ────────────────────────────────────────

screen game_menu(title, scroll=None, yinitial=0.0):
    style_prefix "game_menu"
    add Image("images/gui/game_menu.png")
    add Solid("#00000055")

    frame:
        style "game_menu_outer_frame"

        hbox:
            frame:
                style "game_menu_navigation_frame"
                vbox:
                    textbutton _("History")    action ShowMenu("history")
                    textbutton _("Save")       action ShowMenu("save")
                    textbutton _("Load")       action ShowMenu("load")
                    textbutton _("Preferences")action ShowMenu("preferences")
                    textbutton _("Main Menu")  action MainMenu()
                    textbutton _("Quit")       action Quit(confirm=True)

            frame:
                style "game_menu_content_frame"
                if scroll == "viewport":
                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        transclude
                elif scroll == "vpgrid":
                    vpgrid:
                        cols 1
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        transclude
                else:
                    transclude

    label title:
        style "game_menu_label"

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")

style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_label is interface_label:
    xpos 75
    ysize 126
style game_menu_label_text is interface_label_text:
    size gui.title_text_size
    color gui.accent_color


## ─── Choices (menu) ──────────────────────────────────────────────────────────
## Plain menu: blocks route here. Long captions wrap; each option is a distinct
## dark card with light text, centered, that brightens on hover.

screen choice(items):
    style_prefix "choice"
    vbox:
        for i in items:
            textbutton i.caption action i.action

style choice_vbox:
    xalign 0.5
    yalign 0.5
    spacing 14

style choice_button:
    xsize 1000
    padding (30, 18)
    background "#1c1208e0"
    hover_background "#5a3a1af0"

style choice_button_text:
    color "#ece0c6"
    hover_color "#ffffff"
    size gui.text_size
    text_align 0.0
    layout "tear"


## ─── Save / Load ────────────────────────────────────────────────────────────

screen save():
    tag menu
    use game_menu(_("Save"), scroll="vpgrid"):
        use file_slots(_("Save"))

screen load():
    tag menu
    use game_menu(_("Load"), scroll="vpgrid"):
        use file_slots(_("Load"))

screen file_slots(title):
    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    hbox:
        for i in range(1, 13):
            $ slot = i
            button:
                action FileAction(slot)
                has vbox
                add FileScreenshot(slot) ysize 144
                text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                    size 16
                text FileSaveName(slot):
                    size 16


## ─── Preferences ────────────────────────────────────────────────────────────

screen preferences():
    tag menu
    use game_menu(_("Preferences")):
        vbox:
            xfill True
            label _("Text Speed")
            bar value Preference("text speed") xsize 420
            label _("Skip Unseen Text")
            textbutton _("Enable") action Preference("skip", "toggle")


## ─── History ────────────────────────────────────────────────────────────────

screen history():
    tag menu
    predict False
    use game_menu(_("History"), scroll="viewport", yinitial=1.0):
        style_prefix "history"
        for h in renpy.iter_history():
            window:
                has fixed:
                    yfit True
                if h.who:
                    label h.who style "history_name"
                    $ what = h.what
                    text what:
                        substitute False
                        xpos 220

style history_window is empty:
    ysize gui.history_height

style history_name is gui_label:
    xpos 233
    xanchor 1.0

style history_name_text is gui_label_text:
    textalign 1.0


## ─── Confirm / Yes-No ────────────────────────────────────────────────────────

screen confirm(message, yes_action, no_action):
    modal True
    add Solid("#00000088")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 440
        padding (20, 20)
        vbox:
            spacing 20
            text message xalign 0.5 textalign 0.5
            hbox:
                xalign 0.5
                spacing 30
                textbutton _("Yes") action yes_action
                textbutton _("No")  action no_action


## ─── Skip indicator ──────────────────────────────────────────────────────────

screen skip_indicator():
    zorder 100
    style_prefix "skip"
    frame:
        hbox:
            spacing 6
            text _("Skipping")
            text "▸▸"

style skip_frame is empty
style skip_text is gui_text:
    size 16
    color gui.accent_color


## ─── Notify ──────────────────────────────────────────────────────────────────

screen notify(message):
    zorder 100
    style_prefix "notify"
    frame at notify_appear:
        text message
    timer 3.25 action Hide("notify")

transform notify_appear:
    on show:
        alpha 0
        linear 0.25 alpha 1.0
    on hide:
        linear 0.5 alpha 0.0

style notify_frame is empty:
    ypos 68
    xpos 60

style notify_text is gui_text:
    size 16


## ─── NPC dialogue (say screen) — uses gui.rpy styles automatically ───────────

## Ren'Py uses the built-in say screen.  We only override styles in gui.rpy.
## No custom say screen needed; stock say screen works with the style overrides.


## ─── DICE RESULT SCREEN (visible-tabletop, §5.10) ────────────────────────────

screen dice_result(result):
    modal True
    add Solid("#000000aa")

    frame:
        xalign 0.5
        yalign 0.5
        xminimum 500
        xmaximum 680
        yminimum 300
        padding (30, 24)

        vbox:
            spacing 8
            xfill True

            ## Header
            $ _sk_label = (result.skill or result.attribute) + " CHECK"
            text _sk_label.upper() xalign 0.5 bold True color gui.accent_color size 20

            null height 4

            ## Dice / roll display
            hbox:
                xalign 0.5
                spacing 6
                text "d20 " color gui.text_color size 20
                text "[result.die_used]" bold True color gui.text_color size 26
                text "  +  " color gui.text_color size 20
                text "[result.attribute] [result.attr_value]" color gui.text_color size 20
                if result.skill_rank > 0:
                    text "  +  [result.skill] [result.skill_rank]" color gui.text_color size 20

            ## Advantage dice notation (if not straight roll)
            if result.net_adv != 0:
                $ _rolls = " and ".join(str(r) for r in result.die_rolls)
                $ _mode = "Took higher" if result.net_adv > 0 else "Took lower"
                text "(rolled [_rolls]; [_mode])" xalign 0.5 color "#998877" size 16

            ## DC line
            text "── vs DC [result.dc] ──" xalign 0.5 color "#776655" size 16

            null height 4

            ## Advantage / Disadvantage sources
            for source in result.adv_sources:
                if source[1] > 0:
                    text "✦ Advantage: [source[0]]" color gui.accent_color size 17 xpos 20
                else:
                    text "✦ Disadvantage: [source[0]]" color "#cc8844" size 17 xpos 20

            null height 8

            ## Result
            if result.nat20:
                text "✦ NATURAL 20 — AUTO-SUCCESS" xalign 0.5 bold True color "#b8860b" size 22
            elif result.nat1:
                text "✦ NATURAL 1 — AUTO-FAIL" xalign 0.5 bold True color "#cc4444" size 22
            elif result.passed:
                text "✓  SUCCESS" xalign 0.5 bold True color "#2e8b57" size 24
            else:
                text "✗  FAILURE" xalign 0.5 bold True color "#cc4444" size 24

            null height 12

            textbutton "Continue" xalign 0.5 action Return()


## ─── CHARACTER SHEET CONFIRM (§5.2, §5.12) ───────────────────────────────────

screen charsheet_confirm(pre_attrs, skills, traits, pending_free):
    ## pre_attrs: {attr: value}  (after species+class bumps, before free points)
    ## skills:    {skill: source_label}
    ## traits:    [trait_id, ...]
    ## pending_free: int — free skill picks from overlap redirects (shown as info)

    modal True
    add Solid("#000000cc")

    ## Character sheet frame — the ornate set piece (sheet_frame.png, shown once)
    add Image("images/gui/sheet_frame.png") xalign 0.5 yalign 0.5

    ## Attribute trackers (screen-local)
    default alloc_STR = 0
    default alloc_DEX = 0
    default alloc_INT = 0
    default alloc_CHA = 0
    default alloc_SPR = 0
    default alloc_END = 0

    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        ysize 460
        background None
        padding (40, 36)

        vbox:
            spacing 4
            xfill True

            text "Distribute your 6 free points (max +2 per attribute, cap 10)." xalign 0.5 color gui.text_color size 16
            null height 8

            ## Pool indicator
            $ _used = alloc_STR + alloc_DEX + alloc_INT + alloc_CHA + alloc_SPR + alloc_END
            text "Points remaining: [6 - _used]" xalign 0.5 color ("#44cc88" if _used < 6 else "#cc4444") size 18

            null height 4

            ## Attribute grid
            for attr_name, alloc_var in [
                    ("STR", alloc_STR), ("DEX", alloc_DEX), ("INT", alloc_INT),
                    ("CHA", alloc_CHA), ("SPR", alloc_SPR), ("END", alloc_END)]:
                $ _base_val = pre_attrs.get(attr_name, 3)
                $ _final = _base_val + alloc_var
                $ _pool_ok = (_used < 6)

                hbox:
                    xfill True
                    spacing 8

                    text attr_name color gui.accent_color bold True size 20 xminimum 60
                    text "[_final]" color gui.text_color bold True size 20 xminimum 36 xalign 1.0

                    textbutton "−":
                        xsize 30
                        sensitive alloc_var > 0
                        action SetScreenVariable("alloc_" + attr_name, alloc_var - 1)

                    textbutton "+":
                        xsize 30
                        sensitive _pool_ok and alloc_var < 2 and _final < 10
                        action SetScreenVariable("alloc_" + attr_name, alloc_var + 1)

            null height 8

            ## Skills summary
            hbox:
                xfill True
                text "Skills: " color gui.accent_color size 17 bold True
                text (", ".join(skills.keys()) if skills else "—") color gui.text_color size 17

            ## Traits summary
            if traits:
                hbox:
                    xfill True
                    text "Traits: " color gui.accent_color size 17 bold True
                    $ _trait_names = ", ".join(t.replace("_", " ").title() for t in traits)
                    text _trait_names color gui.text_color size 17

            ## Pending free-skill note
            if pending_free > 0:
                text "[pending_free] free skill pick(s) — choose after confirming." color gui.accent_color size 15

            null height 12

            textbutton "Begin Your Story":
                xalign 0.5
                action Return({
                    "STR": alloc_STR, "DEX": alloc_DEX, "INT": alloc_INT,
                    "CHA": alloc_CHA, "SPR": alloc_SPR, "END": alloc_END,
                })
