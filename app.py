from typing import cast

import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    def on_nav_change(e):
        match e.data:
            case 0:
                content_area.content = main_page
            case 1:
                content_area.content = files_page
            case 2:
                content_area.content = settings_page
            case _:
                print("недоступно")
        content_area.update()

    def toggle_rail(e):
        if sidebar_container.width == 250:
            sidebar_container.width = 0
            toggle_btn.icon = ft.Icons.CHEVRON_RIGHT
        else:
            sidebar_container.width = 250
            toggle_btn.icon = ft.Icons.CHEVRON_LEFT
        
        sidebar_container.update()
        toggle_btn.update()

    toggle_btn = ft.IconButton(
        icon=ft.Icons.CHEVRON_LEFT, 
        icon_color=ft.Colors.BLUE,
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
                    content="Запустить", 
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
        ft.Text("Временно недоступно (Страница Настройки)"),
        alignment=ft.Alignment.CENTER
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