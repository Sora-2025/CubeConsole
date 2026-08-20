import json
import os
from typing import cast

import flet as ft
from flet_color_pickers import BlockPicker

DEFAULT_CONFIG = {
    "accent": "#10B981",
    "language": "ru-RU",
    "theme": "system"
}

def main(page: ft.Page):
    page.padding = 0

    def reset_config():
        with open('config.json', "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=4)

        page.pop_dialog()

    def dump_config():
        with open('config.json', "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    if not os.path.exists('config.json'):
        reset_config()

    config = DEFAULT_CONFIG

    try:
        with open('config.json', "r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError:
            config = DEFAULT_CONFIG
            alert = ft.AlertDialog(
                        title='Oops!',
                        content=ft.Text('The configuration file was corrupted. Click Yes to reset the settings to their default values.'),
                        actions=[
                            ft.TextButton("Yes", on_click=lambda e: reset_config()),
                            ft.TextButton("No", on_click=lambda e: page.window.destroy()),
                        ],
                    )
            page.show_dialog(alert)
    except Exception as e:  # noqa: BLE001
        alert = ft.AlertDialog(
            title='Oops!',
            content=ft.Text(f'An error occurred while opening the configuration file. {e}')
        )
        page.show_dialog(alert)

    page.theme_mode = config['theme'] # type: ignore

    page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=config['accent']
            )
        )

    with open(f'assets/langs/{config['language']}.json', 'r', encoding='utf-8') as f:
        lang_codes = json.load(f)
    
    def on_nav_change(e):
        match e.data:
            case 0:
                content_area.content = main_page
            case 1:
                content_area.content = files_page
            case 2:
                content_area.content = settings_page
            case _:
                pass
        content_area.update()

    def on_color_change(e):
        page.theme = ft.Theme(
                color_scheme=ft.ColorScheme(
                    primary=e.data
                )
            )
        config['accent'] = e.data
        dump_config()

    def toggle_rail(e):
        if sidebar_container.width == 250:
            sidebar_container.width = 0
            toggle_btn.icon = ft.Icons.CHEVRON_RIGHT
        else:
            sidebar_container.width = 250
            toggle_btn.icon = ft.Icons.CHEVRON_LEFT
        
        sidebar_container.update()
        toggle_btn.update()

    def on_theme_change(e):
        match e.data:
            case ['dark']:
                page.theme_mode = ft.ThemeMode.DARK
                config['theme'] = "dark"
                dump_config()
            case ['light']:
                page.theme_mode = ft.ThemeMode.LIGHT
                config['theme'] = "light"
                dump_config()
            case ['system']:
                page.theme_mode = ft.ThemeMode.SYSTEM
                config['theme'] = "system"
                dump_config()

    async def destroy_app(e):
        await page.window.destroy()

    def on_lang_change(e):
        config['language'] = e.data
        dump_config()
        with open(f'assets/langs/{config['language']}.json', 'r', encoding='utf-8') as f:
                lang_codes = json.load(f)
                page.update()
        alert = ft.AlertDialog(
            title=lang_codes['restart_required_title'],
            content=ft.Text(lang_codes['restart_required_text']),
            actions=[
                ft.TextButton(lang_codes['OK'], on_click=destroy_app)
            ]
        )
        page.show_dialog(alert)

    toggle_btn = ft.IconButton(
        icon=ft.Icons.CHEVRON_LEFT,
        on_click=toggle_rail
    )

    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=True,          
        expand=True,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME,
                selected_icon=ft.Icons.HOME_OUTLINED,
                label="Главная",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.FOLDER,
                selected_icon=ft.Icons.FOLDER_OPEN_OUTLINED,
                label="Файлы",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS,
                selected_icon=ft.Icons.SETTINGS_OUTLINED,
                label="Настройки",
            ),
        ],
        on_change=on_nav_change
    )

    sidebar_container = ft.Container(
        content=nav_rail,
        width=250,
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        clip_behavior=ft.ClipBehavior.HARD_EDGE
    )


    main_page = ft.Container(
        content=ft.Row(
            controls=cast(list[ft.Control], [
                ft.Button(
                    content=lang_codes['home_launch'], 
                    icon=ft.Icons.POWER_SETTINGS_NEW, 
                    width=250,
                    height=60,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12)
                    )
                ),
                ft.Container(
                    margin=ft.Margin.only(left=12),
                    content=ft.Column([
                        ft.Button(
                            content="Остановить",
                            icon=ft.Icons.FLASH_OFF,
                            width=150,
                            height=26,
                            style=ft.ButtonStyle(
                                color=ft.Colors.RED_ACCENT,
                                shape=ft.RoundedRectangleBorder(radius=6),
                                padding=ft.Padding.symmetric(horizontal=10)
                            )
                        ),
                        ft.Button(
                            content="Перезагрузить",
                            icon=ft.Icons.RESTART_ALT,
                            width=150,
                            height=26,
                            style=ft.ButtonStyle(
                                color=ft.Colors.GREEN_200,
                                shape=ft.RoundedRectangleBorder(radius=6),
                                padding=ft.Padding.symmetric(horizontal=10)
                            )
                        ),
                    ], spacing=8)
                )
            ]),
            vertical_alignment=ft.CrossAxisAlignment.START
        ),
        alignment=ft.Alignment.TOP_LEFT,
        margin=ft.Margin.only(left=75, top=15),
        expand=True
    )

    files_page = ft.Container(
        ft.Text("Временно недоступно (Страница Файлы)"),
        alignment=ft.Alignment.CENTER
    )

    settings_page = ft.Container(
    ft.Tabs(
        length=2,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab("Оформление", ft.Icons.BRUSH),
                        ft.Tab("Запуск", ft.Icons.SETTINGS),
                    ]
                ),
                ft.TabBarView(
                    expand=True,
                    controls=cast(list[ft.Control], [
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=cast(list[ft.Control], [
                                            ft.Text(
                                                'Акцентный цвет',
                                                align=ft.Alignment.CENTER_LEFT
                                            ),
                                            BlockPicker(
                                                color=config['accent'],
                                                available_colors=[
                                                    "#10B981",
                                                    "#5865F2", 
                                                    "#00B4D8",
                                                    "#F59E0B", 
                                                    "#EF4444", 
                                                    "#8B5CF6"
                                                ],
                                                on_color_change=on_color_change,
                                                margin=ft.Margin.only(left=50),
                                                height=50
                                            )
                                        ]),
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                                    ),
                                    ft.Row(
                                        controls=cast(list[ft.Control], [
                                            ft.Text(
                                                'Тема',
                                                align=ft.Alignment.CENTER_LEFT
                                            ),
                                            ft.SegmentedButton(
                                                [
                                                    ft.Segment('dark', ft.Icons.DARK_MODE),
                                                    ft.Segment('light', ft.Icons.LIGHT_MODE),
                                                    ft.Segment('system', ft.Icons.SETTINGS)
                                                ],
                                                selected=['system'],
                                                margin=ft.Margin.only(left=50),
                                                on_change=on_theme_change
                                            )
                                        ])
                                    ),
                                    ft.Row(
                                        controls=cast(list[ft.Control], [
                                            ft.Text(
                                                'Язык',
                                                align=ft.Alignment.CENTER_LEFT
                                            ),
                                            ft.Dropdown(
                                                config['language'],
                                                [
                                                    ft.DropdownOption(
                                                        'ru-RU',
                                                        'Русский'
                                                    ),
                                                    ft.DropdownOption(
                                                        'en-US',
                                                        'English (US)'
                                                    )
                                                ],
                                                height=40,
                                                margin=ft.Margin.only(left=50),
                                                on_select=on_lang_change
                                            )
                                        ])
                                    )
                                ],
                                align=ft.Alignment.TOP_LEFT
                            ),
                            alignment=ft.Alignment.TOP_LEFT
                        ),
                        
                        ft.Container(
                            alignment=ft.Alignment.CENTER,
                            content=ft.Text("Settings content"),
                        ),
                    ]),
                )
            ],
        ),
    ),
    alignment=ft.Alignment.CENTER,
    margin=ft.Margin.only(left=75)
)

    content_area = ft.Container(
        content=main_page
    )

    page.add(
        ft.Row(
            [
                sidebar_container,
                ft.Stack(
                    [
                        content_area,
                        ft.Container(
                            content=toggle_btn,
                            left=10,
                            top=10,
                        )
                    ],
                    expand=True
                )
            ],
            expand=True,
            spacing=0
        )
    )

ft.run(main)