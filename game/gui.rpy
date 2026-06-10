## Evorath GUI configuration (§5.7)
## 1280×720, parchment-and-rope visual register.
## Custom assets live in game/images/gui/ (not the stock game/gui/ folder).

init python:
    gui.init(1280, 720)

## ─── Colours ──────────────────────────────────────────────────────────────

define gui.accent_color            = "#c8a96e"   ## warm gold
define gui.idle_color              = "#c8b89a"   ## pale parchment text
define gui.hover_color             = "#f0e0c0"   ## highlight
define gui.selected_color          = "#f0e0c0"
define gui.insensitive_color       = "#776655"
define gui.muted_color             = "#886644"
define gui.hover_muted_color       = "#aa8855"

define gui.text_color              = "#2a1f14"   ## dark ink on light background
define gui.interface_text_color    = "#c8b89a"
define gui.name_text_color         = "#c8a96e"

## ─── Fonts ────────────────────────────────────────────────────────────────
## Using Ren'Py built-in fonts; a custom font can be added post-MVP.

define gui.text_font               = "DejaVuSans.ttf"
define gui.name_font               = "DejaVuSans.ttf"
define gui.interface_font          = "DejaVuSans.ttf"

define gui.text_size               = 24
define gui.name_size               = 22
define gui.interface_size          = 24
define gui.label_text_size         = 28
define gui.notify_text_size        = 20
define gui.title_text_size         = 60

## ─── Window / Textbox ─────────────────────────────────────────────────────

define gui.textbox_height          = 185
define gui.textbox_yalign          = 1.0

define gui.name_xpos               = 310
define gui.name_ypos               = 6
define gui.name_xalign             = 0.0

define gui.dialogue_xpos           = 210
define gui.dialogue_ypos           = 45
define gui.dialogue_width          = 868

## ─── Dialogue / Say screen ────────────────────────────────────────────────

define gui.say_thought_size        = gui.text_size

## ─── Menu / Choices ───────────────────────────────────────────────────────

define gui.choice_button_width     = 790
define gui.choice_button_height    = 54
define gui.choice_button_text_size = gui.text_size

## ─── Scrollbars / Sliders ─────────────────────────────────────────────────

define gui.scrollbar_size          = 14
define gui.slider_size             = 30
define gui.vscrollbar_size         = 14
define gui.vslider_size            = 30

## ─── History screen ────────────────────────────────────────────────────────

define gui.history_height          = 210
define gui.history_text_width      = 900

## ─── NVL mode ─────────────────────────────────────────────────────────────

define gui.nvl_height              = None
define gui.nvl_text_size           = gui.text_size
define gui.nvl_name_size           = gui.name_size

## ─── Transition ────────────────────────────────────────────────────────────

define config.enter_transition     = dissolve
define config.exit_transition      = dissolve
define config.after_load_transition = None
define config.end_game_transition  = None
define config.game_main_transition = dissolve

## ─── Styles ────────────────────────────────────────────────────────────────

style default:
    font gui.text_font
    size gui.text_size
    color gui.text_color

style window:
    xalign 0.5
    xsize 1280
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background Image("images/gui/textbox.png")

style say_label:
    color gui.name_text_color
    bold True

style say_dialogue:
    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

style frame:
    background Frame(Image("images/gui/frame.png"), 20, 20, 20, 20)
    padding (20, 20)

style button_text:
    color gui.idle_color
    hover_color gui.hover_color
    selected_color gui.selected_color
    insensitive_color gui.insensitive_color
    font gui.interface_font
    size gui.interface_size

style choice_button:
    background Frame("#00000066", 5, 5)
    hover_background Frame("#3d2b1a99", 5, 5)
    xsize gui.choice_button_width
    ysize gui.choice_button_height

style choice_button_text is button_text:
    xalign 0.5
    yalign 0.5
    color gui.idle_color
    hover_color gui.hover_color

style interface_label_text:
    color gui.accent_color
    bold True
    size gui.label_text_size

## ─── Notify ────────────────────────────────────────────────────────────────

define gui.skip_transition         = Dissolve(0.25)
define gui.fast_skip_used          = False
