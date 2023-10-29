from nicegui import ui, app

@ui.refreshable
def counter(name: str):
    s, sets = ui.state('drewes')
    app.config.dark=True
    app.config.add_run_config()
    with ui.card():
        myname , set_name = ui.state('drewes kooi')
        count, set_count = ui.state(0)
        color, set_color = ui.state('black')
        ui.label(f'{myname} = {count}').classes(f'text-{color}')
        ui.label(f'{name} = {count}').classes(f'text-{color}')
        ui.button(f'{name} += 1', on_click=lambda: set_count(count + 1))
        ui.button(f"{myname}", on_click=lambda e: set_name(myname.upper()))
        ui.select(['black', 'red', 'green', 'blue'],
                  value=color, on_change=lambda e: set_color(e.value))

with ui.row():
    counter('A')
    counter('B')

ui.run(port=7777)
