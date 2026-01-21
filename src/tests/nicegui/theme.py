from contextlib import contextmanager
from nicegui import ui


@contextmanager
def frame(navigation_title: str):
    with ui.row():
        with ui.column():
            ui.link('Home', '/')
            ui.link('Get structures', '/get-structures')
            ui.link('Get structure', '/get-structure')
            ui.link('Get forest', '/get-forest')
            ui.link('Get value', '/get-value')

        with ui.column():
            ui.label(navigation_title)
            yield
