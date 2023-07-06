# -*- coding: utf-8 -*-
"""
This config file is inspired by DistroTube dotfiles
"""
import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401from typing import List  # noqa: F401

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"      # My terminal of choice
myBrowser = "brave"       # My browser of choice

# method to adjust the brightness.
def backlight(action):
    def f(qtile):
        brightness = int(subprocess.run(['xbacklight', '-get'],
                                        stdout=subprocess.PIPE).stdout)
        if brightness != 1 or action != 'dec':
            if (brightness > 49 and action == 'dec') \
                                or (brightness > 39 and action == 'inc'):
                subprocess.run(['xbacklight', f'-{action}', '10',
                                '-fps', '10'])
            else:
                subprocess.run(['xbacklight', f'-{action}', '1'])
    return f



keys = [
         ### The essentials
        Key([mod], "Return",
           lazy.spawn(myTerm ),
           desc='Launches My Terminal'
           ),
        Key([mod, "shift"], "Return",
            lazy.spawn("dmenu_run -p 'Run: '"),
            desc='Run Launcher'
            ),
        Key([mod], "b",
            lazy.spawn(myBrowser),
            desc='brave'
            ),
        Key([mod], "Tab",
            lazy.next_layout(),
            desc='Toggle through layouts'
            ),
        Key([mod, "shift"], "c",
            lazy.window.kill(),
            desc='Kill active window'
            ),
        Key([mod, "shift"], "r",
            lazy.restart(),
            desc='Restart Qtile'
            ),
        Key([mod, "shift"], "q",
            lazy.shutdown(),
            desc='Shutdown Qtile'
            ),
        Key(["control", "shift"], "e",
            lazy.spawn("emacsclient -c -a emacs"),
            desc='Doom Emacs'
            ),
        ### Treetab controls
         Key([mod, "shift"], "h",
            lazy.layout.move_left(),
            desc='Move up a section in treetab'
            ),
        Key([mod, "shift"], "l",
            lazy.layout.move_right(),
            desc='Move down a section in treetab'
            ),
        ### Window controls
        Key([mod], "j",
            lazy.layout.down(),
            desc='Move focus down in current stack pane'
            ),
        Key([mod], "k",
            lazy.layout.up(),
            desc='Move focus up in current stack pane'
            ),
        Key([mod, "shift"], "j",
            lazy.layout.shuffle_down(),
            lazy.layout.section_down(),
            desc='Move windows down in current stack'
            ),
        Key([mod, "shift"], "k",
            lazy.layout.shuffle_up(),
            lazy.layout.section_up(),
            desc='Move windows up in current stack'
            ),
        Key([mod], "h",
            lazy.layout.shrink(),
            lazy.layout.decrease_nmaster(),
            desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
            ),
        Key([mod], "l",
            lazy.layout.grow(),
            lazy.layout.increase_nmaster(),
            desc='Expand window (MonadTall), increase number in master pane (Tile)'
            ),
        Key([mod], "n",
            lazy.layout.normalize(),
            desc='normalize window size ratios'
            ),
        Key([mod], "m",
            lazy.layout.maximize(),
            desc='toggle window between minimum and maximum sizes'
            ),
        Key([mod, "shift"], "f",
            lazy.window.toggle_floating(),
            desc='toggle floating'
            ),
        Key([mod], "f",
            lazy.window.toggle_fullscreen(),
            desc='toggle fullscreen'
            ),
        Key(['mod1', 'control' ], 'x',
            lazy.spawn('xdotool getwindowfocus windowkill' ),
            desc='kill focused window'
            ),
        ### Stack controls
        Key([mod, "shift"], "Tab",
            lazy.layout.rotate(),
            lazy.layout.flip(),
            desc='Switch which side main pane occupies (XmonadTall)'
            ),
         Key([mod], "space",
            lazy.layout.next(),
            desc='Switch window focus to other pane(s) of stack'
            ),
        Key([mod, "shift"], "space",
            lazy.layout.toggle_split(),
            desc='Toggle between split and unsplit sides of stack'
            ),

        # Change the volume if your keyboard has special volume keys.
        Key(
            [], "XF86AudioRaiseVolume",
            lazy.spawn("amixer -c 0 -q set Master 2dB+"),
            desc='Raise volume'
        ),
        Key(
            [], "XF86AudioLowerVolume",
            lazy.spawn("amixer -c 0 -q set Master 2dB-"),
            desc='Lower volume'
        ),
        Key(
            [], "XF86AudioMute",
            lazy.spawn("amixer -c 0 -q set Master toggle"),
            desc='Mute volume'
        ),
        #flameshot screenshot
        Key(
            [mod], "s",
            lazy.spawn("flameshot gui"),
            desc='Take screenshot'
        ),

        # Screen brightness
        Key(
            [], "XF86ScreenSaver", 
            lazy.spawn("xset dpms force off"),
            desc='black out screen'
        ),
        Key(
            [], 'XF86MonBrightnessUp',   
            lazy.function(backlight('inc')),
            desc="increase brightness"
        ),
        Key(
            [], 'XF86MonBrightnessDown', 
            lazy.function(backlight('dec')),
            desc="Decrease brightness"    
        ),
        
        # redshift
        KeyChord([mod], "z", [
            Key([], "r",
            lazy.spawn("redshift -P -O 3000"),
            desc="redshift on at 3000K"),
            Key([], "t",
            lazy.spawn("redshift -P -O 6500"),
            desc="redshift on at 6500K")
        ])
]

groups = [Group("work I\t", {'layout': 'monadtall'}),
            Group("work II\t", {'layout': 'monadtall'}),
            Group("work III\t", {'layout': 'monadtall'}),
            Group("office I\t", {'layout': 'monadtall'}),
            Group("office II\t", {'layout': 'monadtall'}),
            Group("music\t", {'layout': 'monadtall'}),
            Group("pass\t", {'layout': 'monadtall'}),
            Group("other", {'layout': 'monadtall'}),
            Group("fl", {'layout': 'floating'})]

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {"border_width": 4,
                "margin": 2,
                "border_focus": "D08770",
                "border_normal": "4C566A"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    #layout.Max(**layout_theme),
    layout.Max(
        border_width = 0,
        margin = 0),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    # layout.TreeTab(
    #     font = "Ubuntu",
    #     fontsize = 10,
    #     sections = ["FIRST", "SECOND", "THIRD", "FOURTH"],
    #     section_fontsize = 10,
    #     border_width = 2,
    #     bg_color = "1c1f24",
    #     active_bg = "c678dd",
    #     active_fg = "000000",
    #     inactive_bg = "a9a1e1",
    #     inactive_fg = "1c1f24",
    #     padding_left = 0,
    #     padding_x = 0,
    #     padding_y = 5,
    #     section_top = 10,
    #     section_bottom = 20,
    #     level_shift = 8,
    #     vspace = 3,
    #     panel_width = 200
    #     ),
    layout.Floating(**layout_theme)
]

colors = [["#2E3440", "#2E3440"], # panel background
            ["#D08770", "#D08770"], # background for current screen tab
            ["#ECEFF4", "#ECEFF4"], # font color for group names
            ["#5E81AC", "#5E81AC"], # border line color for current tab
            ["#4C566A", "#4C566A"], # border line color for 'other tabs' and color for 'odd widgets'
            ["#2E3440", "#2E3440"], # color for the 'even widgets'
            ["#ECEFF4", "#ECEFF4"], # window name
            ["#D8DEE9", "#D8DEE9"]] # backbround for inactive screens

## no idea what this does.
# prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize = 12,
    padding = 2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
            widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    foreground = colors[2],
                    background = colors[0]
                    ),
            #   widget.Image(
            #            filename = "~/.config/qtile/icons/python-white.png",
            #            scale = "False",
            #            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm)}
            #            ),
            widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    foreground = colors[2],
                    background = colors[0]
                    ),
            widget.GroupBox(
                    font = "Ubuntu Bold",
                    fontsize = 9,
                    margin_y = 3,
                    margin_x = 0,
                    padding_y = 5,
                    padding_x = 3,
                    borderwidth = 3,
                    active = colors[2],
                    inactive = colors[7],
                    rounded = False,
                    highlight_color = colors[1],
                    highlight_method = "line",
                    #    this_current_screen_border = colors[6],
                    this_screen_border = colors [4],
                    #    other_current_screen_border = colors[6],
                    other_screen_border = colors[4],
                    foreground = colors[2],
                    background = colors[0]
                    ),
            #   widget.Prompt(
            #            prompt = prompt,
            #            font = "Ubuntu Mono",
            #            padding = 10,
            #            foreground = colors[3],
            #            background = colors[1]
            #            ),
            widget.Sep(
                    linewidth = 0,
                    padding = 40,
                    foreground = colors[2],
                    background = colors[0]
                    ),
            widget.WindowName(
                    foreground = colors[6],
                    background = colors[0],
                    padding = 0
                    ),
            widget.Systray(
                    background = colors[0],
                    padding = 5
                    ),
            widget.Sep(
                    linewidth = 0,
                    padding = 6,
                    foreground = colors[0],
                    background = colors[0]
                    ),
            widget.TextBox(
                    text = '',
                    background = colors[0],
                    foreground = colors[5],
                    padding = 0,
                    fontsize = 37
                    ),
            #   widget.TextBox(
            #            text = '',
            #            background = colors[2],
            #            foreground = colors[5],
            #            padding = 0,
            #            fontsize = 37
            #            ),
            widget.Net(
                    interface = "wlan0",
                    format = '{down} ↓↑ {up}',
                    foreground = colors[2],
                    background = colors[5],
                    padding = 5
                    ),
             widget.TextBox(
                    text = '',
                    background = colors[5],
                    foreground = colors[4],
                    padding = 0,
                    fontsize = 37
                    ),
            widget.TextBox(
                   #    text = " 🌡",
                    padding = 2,
                    foreground = colors[2],
                    background = colors[4],
                    fontsize = 11
                    ),
            widget.ThermalSensor(
                    foreground = colors[2],
                    background = colors[4],
                    threshold = 90,
                    padding = 5
                    ),
            widget.TextBox(
                    text='',
                    background = colors[4],
                    foreground = colors[5],
                    padding = 0,
                    fontsize = 37
                    ),
            widget.Battery(
                    font="Noto Sans",
                    update_interval = 10,
                    fontsize = 12,
                    foreground = colors[2],
                    background = colors[5],
	                ),
            #   widget.TextBox(
            #            text = " ⟳",
            #            padding = 2,
            #            foreground = colors[2],
            #            background = colors[5],
            #            fontsize = 14
            #            ),
            # widget.CheckUpdates(
            #         update_interval = 1800,
            #         distro = "Arch_checkupdates",
            #         display_format = "{updates} Updates",
            #         foreground = colors[2],
            #         mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
            #         background = colors[5]
            #         ),
            widget.TextBox(
                    text = '',
                    background = colors[5],
                    foreground = colors[4],
                    padding = 0,
                    fontsize = 37
                    ),
            widget.TextBox(
                  #    text = " 🖬",
                    foreground = colors[2],
                    background = colors[4],
                    padding = 0,
                    fontsize = 14
                    ),
            widget.Memory(
                    foreground = colors[2],
                    background = colors[4],
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                    padding = 5
                    ),
            widget.TextBox(
                    text = '',
                    background = colors[4],
                    foreground = colors[5],
                    padding = 0,
                    fontsize = 37
                    ),
            widget.TextBox(
                    text = " Vol:",
                    foreground = colors[2],
                    background = colors[5],
                    padding = 0
                    ),
            widget.Volume(
                    foreground = colors[2],
                    background = colors[5],
                    padding = 5
                    ),
            widget.TextBox(
                    text = '',
                    background = colors[5],
                    foreground = colors[4],
                    padding = 0,
                    fontsize = 37
                    ),
            widget.CurrentLayoutIcon(
                    custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                    foreground = colors[0],
                    background = colors[4],
                    padding = 0,
                    scale = 0.7
                    ),
            widget.CurrentLayout(
                    foreground = colors[2],
                    background = colors[4],
                    padding = 5
                    ),
            widget.TextBox(
                    text = '',
                    background = colors[4],
                    foreground = colors[5],
                    padding = 0,
                    fontsize = 37
                    ),
            widget.Clock(
                    foreground = colors[2],
                    background = colors[5],
                    format = "%A, %B %d - %H:%M "
                    ),
            ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[7:8]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

# def init_widgets_screen2():
#     widgets_screen2 = init_widgets_list()
#     return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]
    # return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
    #         Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
    #         Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    # widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

# def window_to_previous_screen(qtile):
#     i = qtile.screens.index(qtile.current_screen)
#     if i != 0:
#         group = qtile.screens[i - 1].group.name
#         qtile.current_window.togroup(group)

# def window_to_next_screen(qtile):
#     i = qtile.screens.index(qtile.current_screen)
#     if i + 1 != len(qtile.screens):
#         group = qtile.screens[i + 1].group.name
#         qtile.current_window.togroup(group)

# def switch_screens(qtile):
#     i = qtile.screens.index(qtile.current_screen)
#     group = qtile.screens[i - 1].group
#     qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_app_rules = []  # type: List
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
    Match(wm_class='wnr'),            # wnr pomodoro timer
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# @hook.subscribe.startup_once
# def start_once():
#     home = os.path.expanduser('~')
#     subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


processes = [
    "feh --bg-scale /home/victor/pictures/wallpapers/foggy_forest.jpg",
    # "picom --no-vsync &",
    "/usr/bin/dropbox &"
]

for p in processes:
    os.system(p)
