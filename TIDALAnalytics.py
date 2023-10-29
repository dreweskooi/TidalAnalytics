from  nicegui import ui, app 
#from sqlalchemy import create_engine
import asyncio
import aioodbc
from timeit import default_timer as timer
import sys
import xmltodict
import json 
import re
#import pandas
loop = asyncio.get_event_loop()
dsn={
    'admiral':'Driver=ODBC Driver 17 for SQL Server;Server=localhost,1433;Database=AdmiralCHS_MN501;uid=sa;pwd=kooi',
    'reporting' : 'Driver=ODBC Driver 17 for SQL Server;Server=localhost,1433;Database=TidalReporting_US_DEV;uid=sa;pwd=kooi'
}
#admiral_dsn = 'Driver=ODBC Driver 17 for SQL Server;Server=localhost,1433;Database=AdmiralCHS_MN501;uid=sa;pwd=kooi'
#reporting_dsn = 'Driver=ODBC Driver 17 for SQL Server;Server=localhost,1433;Database=AdmiralCHS_MN501;uid=sa;pwd=kooi'
#conn_adm = create_engine('mssql+pyodbc://sa:kooi@localhost:1433/AdmiralCHS_MN501?driver=ODBC+Driver+17+for+SQL+Server')
job_status_list = [
"Scheduled",
"Waiting On Dependencies",
"Waiting On Operator",                                                                                                                                                                                     
"Held",                                                                                                                                                                                                    
"Timed Out For Day",                                                                                                                                                                                       
"Agent Unavailable",                                                                                                                                                                                       
"Agent Disabled",                                                                                                                                                                                          
"Waiting on Group",                                                                                                                                                                                        
"Waiting On Children",                                                                                                                                                                                     
"Waiting On Resource",                                                                                                                                                                                     
"Launched",                                                                                                                                                                                                
"Active",                                                                                                                                                                                                  
"Stopped",                                                                                                                                                                                                 
"Deferred",                                                                                                                                                                                                
"Error Occurred",                                                                                                                                                                                          
"Completed Normally",                                                                                                                                                                                      
"Completed Abnormally",                                                                                                                                                                                    
"Externally Defined",                                                                                                                                                                                      
"Completed Normally",                                                                                                                                                                                      
"Completed Abnormally",                                                                                                                                                                                    
"Skipped",                                                                                                                                                                                                 
"Orphaned",                                                                                                                                                                                                
"Aborted",                                                                                                                                                                                                 
"Externally Defined",                                                                                                                                                                                      
"Timed Out",                                                                                                                                                                                               
"Cancelled",                                                                                                                                                                                               
]
query_list={}
async def connect_db(db,sql):
    try:
        conn = await aioodbc.connect(dsn=dsn[db])
        cur = await conn.cursor()
        print(sql)
        await cur.execute(sql)
        rows = await cur.fetchall()
        await cur.close()
        await conn.close()
        return rows
    except Exception as ex:
        print(ex)
    
with open('queries.xml', 'r', encoding='utf-8') as file:
    my_xml = file.read()
    query_dict = xmltodict.parse(my_xml)
    category_list = sorted(set([i['category']  for i in query_dict['queries']['query'] if i['category'].lower() != 'hidden' and i['db'] in ['admiral','reporting']]))
    query_list = sorted(set([i['queryname']  for i in query_dict['queries']['query']]))
    """
    json_object = json.dumps(my_dict, indent=4)
    with open("queries.json", "w") as outfile:
        outfile.write(json_object)    
    """
    # Writing to sample.json
def pagelayout():
    with ui.header(elevated=True).style('background-color: primary').classes('items-center justify-between'):
        with ui.row():
            ui.label('SYNERTECH TIDAL ANALYTICS').classes('text-2xl')
            with ui.button(text='Select Master'):    
                with ui.menu() as menu:
                    ui.menu_item('JobAudit', lambda: ui.open('/queries/JobAudit'))
                    ui.menu_item('ActionAudit', lambda: ui.open('/queries/ActionAudit'))
                    ui.menu_item('AlertAudit', lambda: ui.open('/queries/AlertAudit'))
            with ui.button(text='Job Activity'):    
                with ui.menu() as menu:
                    ui.menu_item('Job Activity', lambda: ui.open('/queries/715JobActivityNG'))
                    ui.menu_item('Job Activity in Error', lambda: ui.open('/queries/JobactivityInError'))

            with ui.button(icon='menu',text='Admin'):    
                with ui.menu() as menu:
                    category = 'Analysis'
                    ui.menu_item('Menu item 1', lambda: ui.link('',''))
                    ui.menu_item('Menu item 2', lambda: ui.link('',''))
                    with ui.button(icon='menu',text='SubAdmin'):                    
                        with ui.menu() as menu:
                            ui.menu_item('SubMenu item 1', lambda: lambda: ui.link('',''))
                            ui.menu_item('SubMenu item 2', lambda: lambda: ui.link('',''))

                    ui.menu_item('Menu item 3 (keep open)',
                                    lambda: result.set_text('Selected item 3'), auto_close=False)
                    ui.separator()
                    ui.menu_item('Close', on_click=menu.close)
            with ui.button(icon='menu',text='Audit'):    
                with ui.menu() as menu:
                    ui.menu_item('JobAudit', lambda: ui.open('/queries/JobAudit'))
                    ui.menu_item('ActionAudit', lambda: ui.open('/queries/ActionAudit'))
                    ui.menu_item('AlertAudit', lambda: ui.open('/queries/AlertAudit'))
                    with ui.button(icon='menu',text='SubAdmin'):                    
                        with ui.menu() as menu:
                            ui.menu_item('SubMenu item 1', lambda: lambda: ui.link('',''))
                            ui.menu_item('SubMenu item 2', lambda: lambda: ui.link('',''))

                    ui.menu_item('Menu item 2', lambda: ui.link('',''))
                    with ui.menu() as menu:
                        ui.menu_item('SubMenu item 1', lambda: lambda: ui.link('',''))
                        ui.menu_item('SubMenu item 2', lambda: lambda: ui.link('',''))

                    ui.menu_item('Menu item 3 (keep open)',
                                    lambda: result.set_text('Selected item 3'), auto_close=False)
                    ui.separator()
                    ui.menu_item('Close', on_click=menu.close)

@ui.page('/')
def index():
    pagelayout()

@ui.page('/queries/{queryname}')
def queries(queryname):
    pagelayout()
    """
    content = {'Query and Selection': '', 'Results': 'Content 2', 'Chart': 'Content 3'}
    with ui.tabs() as tabs:
        for title in content:
            ui.tab(title)
    with ui.tab_panels(tabs).classes('w-full') as panels:
        for title, text in content.items():
            with ui.tab_panel(title):
                ui.label(text)

    """
    def update_query_list():
        app.storage.user['category'] = sel_category.value
        sel_query.options = sorted(set([i['queryname']  for i in query_dict['queries']['query'] if i['category'] == sel_category.value and i['db'].lower() in ['admiral','reporting']]))
        sel_query.update()
        #grid.options['rowdata']=None
        #grid.options['columndefs']=None
        #grid.update()

    def update_parameters_table():
        if not 'parameter_table' in locals():
            return
        #if not 'grid' in locals():
        #    return
        #grid.options['columndefs']=None
        #grid.options['rowdata']=None
        #grid.update()
        with parameter_table:
                parameter_table.clear()
                with ui.row():
                    if sel_query.value:
                        app.storage.user['query'] = sel_query.value
                        sqltext=[i['querytext_sqlserver']  for i in query_dict['queries']['query'] if i['queryname'] == sel_query.value][0]
                        sqltext = sql_expand_inherited_parameters(sqltext=sqltext)
                        matches = set(re.findall(r'<<.*?>>', sqltext))
                        parms_list = set()
                        for m in sorted(matches):
                            defaultvalue=''
                            parmname= m.lstrip('<<').rstrip('>>').split(':')[0]
                            if ':' in m.lstrip('<<').rstrip('>>'):
                                defaultvalue=m.lstrip('<<').rstrip('>>').split(':')[1]
                            if app.storage.user.get(m,None):
                                defaultvalue=app.storage.user[m]
                            if parmname.lower() == 'from_date':    
                                with ui.input('From Date') as from_date:
                                    from_date.value=defaultvalue
                                    with from_date.add_slot('append'):
                                        ui.icon('edit_calendar').on('click', lambda: from_menu.open()).classes('cursor-pointer')
                                    with ui.menu() as from_menu:
                                        ui.date().bind_value(from_date)
                                params[m]= from_date
                            elif parmname.lower() == 'prod_date':
                                with ui.input('Production Date') as prod_date:
                                    prod_date.value=defaultvalue
                                    with prod_date.add_slot('append'):
                                        ui.icon('edit_calendar').on('click', lambda: prod_menu.open()).classes('cursor-pointer')
                                    with ui.menu() as prod_menu:
                                        ui.date().bind_value(prod_date)
                                params[m]= prod_date
                                #ui.date(value='2023-09-01', on_change=lambda e: parms_list[parmname].set_value(e.value))
                            elif parmname.lower() == 'to_date':
                                with ui.input('To Date') as to_date:
                                    to_date.value=defaultvalue
                                    with to_date.add_slot('append'):
                                        ui.icon('edit_calendar').on('click', lambda: to_menu.open()).classes('cursor-pointer')
                                    with ui.menu() as to_menu:
                                        ui.date().bind_value(to_date)
                                params[m]= to_date
                            else:

                                params[m] = ui.input(label=parmname,value=defaultvalue, placeholder='')                    

    async def getData():
        #expansion.close()
        grid_expansion.open()
        expansion.update()
        grid_expansion.update()
        grid.options['rowData']=None
        grid.update()
        chart.visible=False
        sqltext, db =[(i['querytext_sqlserver'], i['db'] ) for i in query_dict['queries']['query'] if i['queryname'] == sel_query.value][0]
        sqltext = sql_expand_inherited_parameters(sqltext=sqltext)        

        for p in params:
            val = params[p].value
            app.storage.user[p] = val
            sqltext = sqltext.replace(p,val)
        if sqltext !='':
            try:
                start = timer()
                result = await connect_db(db=db, sql=sqltext)  
                end = timer()
                elapse_time= end - start
                lbl_elapsetime.text=f"{elapse_time:.01f} secs,"
                lbl_rows.text = f"{len(result)} rows."
                
                rows = []
                if len(result) >0:
                    columns = [column[0] for column in result[0].cursor_description]             
                    for r in result:
                        rows.append(dict(zip(columns, r)))
            except Exception as ex:
                print(ex)
                rows=[]
        else:
            rows=[]
        cols =[]
        if len(rows)>0:
            #cols = rows[0]._fields if len(rows) > 0 else []
            columnDefs = []
            for col in columns:
                columnDefs.append({'headerName': col, 'field': col, 'sortable': 'true', 'width':150, 'filter': 'agTextColumnFilter', 'floatingFilter': False} )
            grid.options['columnDefs'] =columnDefs
            grid.options['rowData'] = rows
            grid.update()
            cols=columns
            x_axis.options=list(cols)
            y1_axis.options=list(cols)
            seriesdata.options=list(cols)
        else:
            cols = []
            columnDefs = []
            for col in cols:
                columnDefs.append({'headerName': col, 'field': col, 'sortable': 'true', 'width': 100} )
            grid.options['columnDefs'] =columnDefs
            grid.options['rowData'] = rows
            #grid.call_column_api_method('sizeColumnsToFit', True)
            #grid.call_api_method('sizeColumnsToFit')
            grid.update()
            x_axis.options=list(cols)
            y1_axis.options=list(cols)
            seriesdata.options=list(cols)
        #series.options=list(cols)
        
        x_axis.update()
        y1_axis.update()
        seriesdata.update()

        
        return 
    
    def get_parameters(queryname):
        params ={}
        if queryname:
            sqltext=[i['querytext_sqlserver']  for i in query_dict['queries']['query'] if i['queryname'] == queryname][0]
            sqltext = sql_expand_inherited_parameters(sqltext=sqltext)
            matches = set(re.findall(r'<<.*?>>', sqltext))
            parms_list = set()
            for m in sorted(matches):
                ui.row()
                defaultvalue=''
                parmname= m.lstrip('<<').rstrip('>>').split(':')[0]
                if ':' in m.lstrip('<<').rstrip('>>'):
                    defaultvalue=m.lstrip('<<').rstrip('>>').split(':')[1]
                if app.storage.user.get(m,None):
                    defaultvalue=app.storage.user[m]
                params[parmname]= defaultvalue
        return params
    def sql_expand_inherited_parameters(sqltext):
        params ={}
        matches = set(re.findall(r'{{.*}}', sqltext))
        parms_list = set()
        for m in sorted(matches):
            inherited_sqltext=[i['querytext_sqlserver']  for i in query_dict['queries']['query'] if i['queryname'] == m.replace('{','').replace('}','')][0]
            #sqltext=sqltext.replace(m, inherited_sqltext)
            sqlparts = inherited_sqltext.split('order by')
            #fullSQL = ''
            sqltext = sqltext.replace(
                            m, ' ( ' + sqlparts[0] + ' ) sel1 ')

        return sqltext
        """
            if parmname.lower() == 'from_date':
                #parms_list[parmname] = ui.input(label='From date', placeholder='from_date')
                with ui.input('From Date') as from_date:
                    with from_date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
                    with ui.menu() as menu:
                        ui.date().bind_value(from_date)                    
                params[parmname]= to_date
                #ui.date(value='2023-09-01', on_change=lambda e: parms_list[parmname].set_value(e.value))
            elif parmname.lower() == 'to_date':
                with ui.input('To Date') as to_date:
                    with to_date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
                    with ui.menu() as menu:
                        ui.date().bind_value(to_date)                    
                params[parmname]= to_date
            else:
                params[parmname] = ui.input(label=parmname,value=defaultvalue, placeholder='')                    
            """
    def handleRowSelectedion(event):
        if event.args['colId']=='jobmst_id':
            with ui.dialog() as dialog , ui.card():
                with ui.grid(columns=4):
                    for r in event.args['data']:
                        ui.label(r).style('background-color: primary')
                        ui.label(event.args['data'][r])
            dialog.open()
        #print(event)

    def set_category_query(cat,query):
        pass

        #ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
    #with ui.left_drawer(top_corner=False, bottom_corner=False).style('background-color: #d7e3f4').classes('w-96'):
    if queryname != None:
        app.storage.user['query'] = queryname
        ui.open('/queries')
    params ={}
    rows=[]
    cols=[]
    with ui.expansion("Selection Query",value=True).classes('w-full') as expansion:
        with ui.row() as query_row:
            qry_button=ui.button('Get Data',icon='list', on_click=getData)
            sel_category = ui.select(label='Select Query Category',value=app.storage.user.get('category',None) ,options=category_list,on_change=lambda: update_query_list()).style('width:200px')
            sel_query = ui.select(label='Select Query',value=app.storage.user.get('query',None),options=sorted(set([i['queryname']  for i in query_dict['queries']['query'] if i.get('templatetype','') !='jinja' and i['db'].lower() in ['admiral','reporting']])), on_change=update_parameters_table)
            #ui.separator()
            parameter_table = ui.grid()
            if sel_query.value:
                update_parameters_table()
            lbl_elapsetime = ui.label()
            lbl_rows = ui.label()
    with ui.expansion("Query data").classes('w-full') as grid_expansion:
        with ui.aggrid({
        'defaultColDef': {'resizable': True},
        'pagination': False,
        'paginationPageSize': 100,        
        'columnDefs': [
            ],
            'rowData': [
            ],
        'rowSelection': 'single',
        },auto_size_columns=False).style('height: 500px').on('cellClicked', lambda event: handleRowSelectedion(event=event)).on('firstDataRendered', lambda: grid.call_column_api_method('autoSizeAllColumns')) as grid:
            with ui.context_menu() as cm1:
                ui.menu_item('Flip horizontally')
                ui.menu_item('Flip vertically')
                ui.separator()
                ui.menu_item('Reset')
        #ui.button('AutoSize Columns', on_click=lambda: grid.call_column_api_method('autoSizeAllColumns'))
    with ui.expansion("Chart").classes('w-full') as chart_expansion:        
        with ui.row():
            x_axis =  ui.select(list(cols), label='Select X axis ').style('width:200px')
            y1_axis = ui.select(list(cols), label='Select Y axis ').style('width:200px')
            seriesdata =  ui.select(list(cols), label='Select Group').style('width:200px')
            #series_data = ui.select(cols, label='Series')
        json = {
            'title': False,
            'chart': {'type': 'bar'},
            'xAxis': {'categories': ['A']},
            'series': [
                {'name': 'Alpha', 'data': []},
                ],
                }
        with ui.row() as r:
            chart = ui.highchart(json).style('height: 200px; width: 100%;') 
            chart.visible=False

        def update():
            rows=grid.options['rowData']
            if x_axis.value == None or y1_axis.value==None:
                ui.notify("Select x and y axis!")
                return
            if seriesdata.value:
                series= set([row[seriesdata.value] for row in rows])
            x1 = sorted(list(set([i[x_axis.value ] or '' for i in rows])))
            groups=[sorted(list(set([i[y1_axis.value ] or '' for i in rows])))]
            y =[]
            for g in series:
                y_temp = [{'name': g ,'data':   i[y1_axis.value] } for i in rows if g == i[seriesdata.value] ]
                y.append(y_temp)
            
            
            y1= [i[y1_axis.value] for i in rows]
            json1 ={
            'title': 'TIDAL Uptime and Planned/Unplanned Outages',
            'chart': {'type': 'column'},
            'barmode': 'stacked',
            'plotOptions': {
                'series': {
                    'stacking': 'normal',
                    'dataLabels': {
                        'enabled': True
                    }
                }
            },
            'xAxis': {'categories': x1},
            'yAxis': {'values': y1,'title' : {'text': 'Value'}},
            'series': [
                {'name': y1_axis.value, 'data': y1, 'color': 'blue'},
            ],
                }
            json1['series'] = y
            with r:
                r.clear()
                ui.chart(json1).style('height: 200px; width: 100%;') 
                #ui.json_editor({'content': {'json': json1}},  on_change=lambda e: ui.notify(f'Change: {e}'))                

        ui.button('Update Chart', on_click=update)
    with ui.footer().style('background-color: #3874c8'):
        ui.label('SYNERTECH TIDAL ANALYTICS')


ui.run(port=7777, reload=False, storage_secret='synertech')