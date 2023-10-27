#!/usr/bin/env python3
from nicegui import ui,app
"""
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
"""
with ui.row():
    ui.html("""
<template>
  <q-layout view="lHh Lpr lFf" class="bg-white">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          @click="toggleLeftDrawer"
          aria-label="Menu"
          icon="menu"
        />

        <q-toolbar-title>
          Quasar App
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      class="bg-grey-2"
    >
      <q-list>
        <q-item-label header>Essential Links</q-item-label>
        <q-item clickable target="_blank" rel="noopener" href="https://quasar.dev">
          <q-item-section avatar>
            <q-icon name="school" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Docs</q-item-label>
            <q-item-label caption>https://quasar.dev</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable target="_blank" rel="noopener" href="https://github.quasar.dev">
          <q-item-section avatar>
            <q-icon name="code" />
          </q-item-section>
          <q-item-section>
            <q-item-label>GitHub</q-item-label>
            <q-item-label caption>github.com/quasarframework</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable target="_blank" rel="noopener" href="http://chat.quasar.dev">
          <q-item-section avatar>
            <q-icon name="chat" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Discord Chat Channel</q-item-label>
            <q-item-label caption>https://chat.quasar.dev</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable target="_blank" rel="noopener" href="https://forum.quasar.dev">
          <q-item-section avatar>
            <q-icon name="record_voice_over" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Forum</q-item-label>
            <q-item-label caption>https://forum.quasar.dev</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable target="_blank" rel="noopener" href="https://twitter.quasar.dev">
          <q-item-section avatar>
            <q-icon name="rss_feed" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Twitter</q-item-label>
            <q-item-label caption>@quasarframework</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable target="_blank" rel="noopener" href="https://facebook.quasar.dev">
          <q-item-section avatar>
            <q-icon name="public" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Facebook</q-item-label>
            <q-item-label caption>@QuasarFramework</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>


""")



    ui.html("""
<div id="q-app" style="min-height: 100vh;">
<div class="q-pa-md">
    <q-btn-dropdown color="primary" label="Dropdown Button">
      <q-list>
        <q-item clickable v-close-popup @click="onItemClick">
          <q-item-section>
            <q-item-label>Photos</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable v-close-popup @click="onItemClick">
          <q-item-section>
            <q-item-label>Videos</q-item-label>
          </q-item-section>
        </q-item>

        <q-item clickable v-close-popup @click="onItemClick">
          <q-item-section>
            <q-item-label>Articles</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-btn-dropdown>
  </div>
</div>    
            
"""   ) 
    ui.html(
        """
<nav>
        <div class="flex flex-wrap items-center justify-between bg-slate-800 md:p-0">
            <div class="p-3 px-4 text-2xl text-white">Navbar</div>
            <div class="p-3 md:hidden">
                <img id="menu-button"
                    class="h-6 transition-opacity duration-500 ease-in-out cursor-pointer hover:opacity-[0.5]"
                    src="/static_files/svgs/bars-solid.svg" alt="list icon">
            </div>
            <div id="menu" class="hidden md:block">
                <ul class="items-center w-screen md:w-auto md:flex ">
                    <li class="p-4 text-gray-300 border-b border-gray-600 md:border-0 "><a href="#">Home</a></li>
                    <li class="p-4 text-gray-500 border-b border-gray-600 hover:text-gray-300 md:border-0"><a
                            href="#">Products</a></li>
                    <li class="p-4 text-gray-500 border-b border-gray-600 hover:text-gray-300 md:border-0"><a
                            href="#">Pricing</a></li>
                    <li id="drp-btn" class="text-gray-500 hover:text-gray-300">
                        <div class="relative inline-flex py-2">
                            <button type="button" class="inline-flex items-center px-4 py-2 font-semibold rounded ps-0">
                                <span class="pr-[0.25rem]">Company</span>
                                <img class="w-4 h-4 ml-2 fill-current" src="/static_files/svgs/caret-down-solid.svg"
                                    alt="caret-down">
                            </button>
                            <div id="drp-list" class="absolute z-10 hidden mt-2 bg-white rounded-md shadow-lg">
                                <a href="#" class="block px-4 py-2 text-gray-800 hover:rounded-t">Option
                                    1</a>
                                <a href="#" class="block px-4 py-2 text-gray-800">Option
                                    2</a>
                                <a href="#" class="block px-4 py-2 text-gray-800 hover:rounded-b">Option
                                    3</a>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </nav>"""


    )
    m1= ui.html(""" 
 <label for="cars">Choose a car:</label>

<select class="label bg-primary text-white" name="cars" id="cars">
<option  value="volvo">Volvo</option>
<option value="saab">Saab</option>
<option value="mercedes">Mercedes</option>
<option value="audi">Audi</option>
</select>     """
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
def runjs():
    ui.run_javascript("""
const app = Vue.createApp({})
app.use(Quasar, { config: {} })
app.mount('#q-app')
<script>
import { ref } from 'vue'

export default {
  name: 'MyLayout',

  setup () {
    const leftDrawerOpen = ref(false)

    function toggleLeftDrawer () {
      leftDrawerOpen.value = !leftDrawerOpen.value
    }

    return {
      leftDrawerOpen,
      toggleLeftDrawer
    }
  }
}
</script>

                      


""")
app.on_connect(runjs)    

ui.run(port=7777,reload=False, title='Tidal Reporting')