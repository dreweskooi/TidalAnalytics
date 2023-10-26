#!/usr/bin/env python3
from nicegui import ui
ui.header()
with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
    ui.label('SYNERTECH TIDAL ANALYTICS').classes('text-2xl items-center')
    with ui.button(icon='menu',text='Admin'):    
        with ui.menu() as menu:
            category = 'Analysis'
            ui.menu_item('Menu item 1', lambda: ui.link('',''))
            ui.menu_item('Menu item 2', lambda: ui.link('',''))
            with ui.menu() as menu:
                ui.menu_item('SubMenu item 1', lambda: lambda: ui.link('',''))
                ui.menu_item('SubMenu item 2', lambda: lambda: ui.link('',''))

            ui.menu_item('Menu item 3 (keep open)',
                            lambda: result.set_text('Selected item 3'), auto_close=False)
            ui.separator()
            ui.menu_item('Close', on_click=menu.close)
    with ui.button(icon='menu',text='Audit'):    
        with ui.menu() as menu:
            category = 'Analysis'
            ui.menu_item('Menu item 1', lambda: ui.link('',''))
            ui.menu_item('Menu item 2', lambda: ui.link('',''))
            with ui.menu() as menu:
                ui.menu_item('SubMenu item 1', lambda: lambda: ui.link('',''))
                ui.menu_item('SubMenu item 2', lambda: lambda: ui.link('',''))

            ui.menu_item('Menu item 3 (keep open)',
                            lambda: result.set_text('Selected item 3'), auto_close=False)
            ui.separator()
            ui.menu_item('Close', on_click=menu.close)

m1= ui.html(""" 
<div id="q-app" style="min-height: 100vh;">
<div class="q-pa-md">
    <div class="q-gutter-md">

<q-btn color="primary" label="Basic Menu">
        <q-menu>
          <q-list style="min-width: 100px">
            <q-item clickable v-close-popup>
              <q-item-section>New tab</q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section>New incognito tab</q-item-section>
            </q-item>
            <q-separator></q-separator>
            <q-item clickable v-close-popup>
              <q-item-section>Recent tabs</q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section>History</q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section>Downloads</q-item-section>
            </q-item>
            <q-separator></q-separator>
            <q-item clickable v-close-popup>
              <q-item-section>Settings</q-item-section>
            </q-item>
            <q-separator></q-separator>
            <q-item clickable v-close-popup>
              <q-item-section>Help &amp; Feedback</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>
    </div>
  </div>
</div>      
      """
            )


"""
with ui.header().classes(replace='row items-center') as header:
    ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
    with ui.tabs() as tabs:
        ui.tab('A')
        ui.tab('B')
        ui.tab('C')

with ui.footer(value=False) as footer:
    ui.label('Footer')

with ui.left_drawer().classes('bg-blue-100') as left_drawer:
    ui.label('Side menu')

with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
    ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

with ui.tab_panels(tabs, value='A').classes('w-full'):
    with ui.tab_panel('A'):
        ui.label('Content of A')
    with ui.tab_panel('B'):
        ui.label('Content of B')
    with ui.tab_panel('C'):
        ui.label('Content of C')
"""

ui.run(port=7777,reload=False, title='Tidal Reporting')