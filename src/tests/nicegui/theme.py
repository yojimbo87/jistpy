from contextlib import contextmanager
from nicegui import ui


@contextmanager
def frame(navigation_title: str):
    with ui.row():
        with ui.column():
            ui.link('Home', '/')

            ui.label("REST API:")
            with ui.list():
                with ui.item():
                    ui.link('Get config', '/rest-get-config')
                with ui.item():
                    ui.link('Get structures', '/rest-get-structures')
                with ui.item():
                    ui.link('Get structure', '/rest-get-structure')
                with ui.item():
                    ui.link('Get forest', '/rest-get-forest')
                with ui.item():
                    ui.link('Get value', '/rest-get-value')
                with ui.item():
                    ui.link('Get default view', '/rest-get-default-view')
                with ui.item():
                    ui.link('Get view', '/rest-get-view')

            ui.label("Client API:")
            with ui.list():
                with ui.item():
                    ui.link('Load structure', '/client-load-structure')
                with ui.item():
                    ui.link(
                        'Load structure view',
                        '/client-load-structure-view'
                    )

        with ui.column():
            ui.label(navigation_title)
            yield
