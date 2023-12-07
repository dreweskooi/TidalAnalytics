from  nicegui import ui, app 
#from sqlalchemy import create_engine
import asyncio
from typing import List
from tortoise import Tortoise
#import tortoise.backends.sqlite
#import models
import datetime 
import aioodbc
from timeit import default_timer as timer
import sys
import xmltodict
import json 
import pandas
import re
import tesrest
import shlex
import platform
import shlex
import sys
import os
import sqlite3
def try_parse_int(text):
  try:
    return int(text)
  except:
    return 1
class State:
    def __init__(self):
        self.x_axis = ''
        self.y_axis = ''
        self.value =''

#import pandas
loop = asyncio.get_event_loop()
try:
    with open('tidalanalytics.config.json') as f:
        cfg = tesrest.AttrDict(json.load(f))
except Exception as ex:
    print("Error in getting CONFIGURATION, check tidalanalytics.config.json. Exiting")
    sys.exit(1) 
try:
    with open('transport.selection.json') as f:
        transport_sel = tesrest.AttrDict(json.load(f))
except Exception as ex:
    print("Error in getting transport selection, check transport.selection.json. Exiting")
    sys.exit(1) 

dsn={
    'admiral':'Driver=ODBC Driver 17 for SQL Server;Server=localhost,1433;Database=AdmiralCHS_MN501;uid=sa;pwd=kooi',
    'reporting' : 'Driver=ODBC Driver 17 for SQL Server;Server=localhost,1433;Database=TidalReporting_US_DEV;uid=sa;pwd=kooi'
}
#TIDAL_CM = {
#        "DEV" : "http://localhost:8080/api/tes-6.5",
#        "TEST" : "http://localhost:8080/api/tes-6.5",
#        }
#TIDAL_CM_USER = "kooi\dkooi"
#TIDAL_CM_PASSWORD = "dkk"
"""
async def init_db():
    await Tortoise.init(db_url="sqlite://TidalReporting.db", modules={"models": ["models"]})
    await Tortoise.generate_schemas()

async def close_db() -> None:
    await Tortoise.close_connections()

app.on_startup(init_db)
app.on_shutdown(close_db)
"""

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
    category_list = sorted(set([i['category']  for i in query_dict['queries']['query'] if i['category'].lower() != 'hidden' and i['db'] in ['admiral','reporting','restapi']]))
    query_list = sorted(set([i['queryname']  for i in query_dict['queries']['query']]))
    """
    json_object = json.dumps(my_dict, indent=4)
    with open("queries.json", "w") as outfile:
        outfile.write(json_object)    
    """
    # Writing to sample.json
def showe(e):
    print(e)
def pagelayout():
    with ui.header(elevated=True).style('background-color: primary').classes('items-center justify-between'):
        with ui.row():
            ui.icon('analytics').classes('text-5xl top-0')
            ui.label('Synertech Tidal Reporting').classes('text-2xl')

            with ui.button(text='Job Activity'):    
                with ui.menu() as menu:
                    ui.menu_item('Job Activity', lambda: ui.open('/queries/715JobActivityNG'))
                    ui.menu_item('Job Activity in Error', lambda: ui.open('/queries/715JobActivityInError'))
            with ui.button(text='Audit'):    
                with ui.menu() as menu:
                    for q in query_dict['queries']['query']:
                        if q['category']=='audit':
                            ui.menu_item(q['queryname'], on_click= lambda q = q : ui.open(f'/queries/{q["queryname"]}'))
                            #ui.menu_item('Job Activity in Error', lambda: ui.open('/queries/JobactivityInError'))
            with ui.button(icon='menu',text='Analysis'):    
                with ui.menu() as menu:
                    for q in query_dict['queries']['query']:
                        if q['category'].lower()=='analysis':
                            with ui.element():
                                ui.menu_item(q['queryname'], on_click=lambda q = q : ui.open(f'/queries/{q["queryname"]}'))
            with ui.button(icon='menu',text='CM'):    
                with ui.menu() as menu:
                    for q in query_dict['queries']['query']:
                        if q['db']=='restapi':
                            ui.menu_item(q['queryname'], lambda q=q: ui.open(f'/queries/{q["queryname"]}'))
            ui.button(icon='menu',text='Transport', on_click=lambda q=q: ui.open(f'/transport/source'))
            ui.button(icon='menu',text='Test', on_click=lambda q=q: ui.open(f'/testpage'))
#                with ui.menu() as menu:
#                    ui.menu_item('Select Source ', lambda q=q: ui.open(f'/transport/source'))                    

@ui.page('/',response_timeout=99)
def index():
    pagelayout()
@ui.page('/edit_queries',response_timeout=99)
async def edit_queries():
    def handleRowSelection(event):
        ui.open(f"edit_query/{event.args['data']['name']}")
        """
        if event.args['colId']=='jobmst_id':
            with ui.dialog() as dialog , ui.card():
                with ui.grid(columns=4):
                    for r in event.args['data']:
                        ui.label(r).style('background-color: primary')
                        ui.label(event.args['data'][r])
            dialog.open()
        """

    pagelayout()
    rows= [{'name': q['queryname'],'edit': 'True'} for q in query_dict['queries']['query']]
    grid = ui.aggrid({
    'defaultColDef': {'flex': 1},
    'columnDefs': [
        {'headerName': 'Name', 'field': 'name','filter': 'agTextColumnFilter', 'floatingFilter': True},
        #{'headerName': 'Edit', 'field': ui.link('Edit', '/edit_query/{name}')},
        
    ],
    'rowData': rows
    ,
    'rowSelection': 'simgle',
    }).style('height: 500px').on('cellClicked', lambda event: handleRowSelection(event=event))

@ui.page('/edit_query/{queryname}',response_timeout=99)
async def edit_query(queryname):
    pagelayout()
    ui.label(f"Edit query {queryname}")

@ui.page('/transport/source',response_timeout=99,reconnect_timeout=10)

async def transportSelectSource():
    data ={
        'table' : {},
        'selected':{},
        'selection':{}
    }
    selected = []
    job_or_jobgroup ='JobGroup'
    table1 ={}
    table2={}
    ENV = app.storage.user['transport_source']
    if ENV == None:
        ENV=list(cfg['CM'].keys())[0]
    tesconn = tesrest.TESREST(cfg.CM[ENV], cfg.CM_USER[ENV], cfg.CM_PASSWORD[ENV])

    pagelayout()
    try:
        with open('transport.selection.json') as f:
            transport_sel = tesrest.AttrDict(json.load(f))
    except Exception as ex:
        print("Error in getting transport selection, check transport.selection.json. Exiting")
        sys.exit(1) 

    async def getJobData(tesobject, criteria, columns,rows):
        result, msg = await tesconn.getTESList(tesobject,criteria=criteria,columns="id,parentid,name,type,fullpath")
        rows=[]
        if len(result) >0:
            columns = [column for column in result[0]._attrs]             
            for r in result:
                nr  ={}
                for c in columns:
                    nr[c] = r[c]
                rows.append(nr)

        tabdata.update()

    def set_source():
        app.storage.user['transport_source'] = sel_source.value
        ui.notify(f'Connecting to {sel_source.value}')
        tesconn = tesrest.TESREST(cfg.CM[sel_source.value], cfg.CM_USER[sel_source.value], cfg.CM_PASSWORD[sel_source.value])
        table1.rows.clear()
        table1.update()
        rows=[]
        if sel_object.value in ['Job','JobGroup']:
            filter=''
            columns='id,parentid,name,type,fullpath'
            ui.notify(f'Getting data to {tesconn.url}')
            result,_ = tesconn.getTESListSorted('Job',filter,columns=columns) 
            if len(result) >0:
                columns = [column for column in result[0]._attrs]             
                for r in result:
                    nr  ={}
                    for c in columns:
                        nr[c] = r[c]
                    table1.rows.append(nr)
        #table1.rows.clear()
        #table1.rows.append(rows)
        table1.update()
            

    def set_dest():
        app.storage.user['transport_dest'] = sel_dest.value
    def set_object():
        app.storage.user['transport_object'] = sel_object.value
    def add_to_selected():
        for r in table1.selected:
            if not r['fullpath'] in [t['name'] for t in table2.rows]:
                table2.add_rows({'name': r['fullpath'], 'job_or_jobgroup' : job_or_jobgroup.value})
        table1.selected.clear()
        table2.update()
        table1.update()
        #selection.clear()
        selected.clear()
        #selection.update()

    async def run_command(command: str) -> None:
        """Run a command in the background and display the output in the pre-created dialog."""
        dialog.open()
        result.content = ''
        command = command.replace('python3', sys.executable)  # NOTE replace with machine-independent Python path (#1240)
        process = await asyncio.create_subprocess_exec(
            *shlex.split(command, posix="win" not in sys.platform.lower()),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        # NOTE we need to read the output in chunks, otherwise the process will block
        output = ''
        while True:
            new = await process.stdout.read(512)
            if not new:
                break
            output += new.decode()
            # NOTE the content of the markdown element is replaced every time we have new output
            result.content = f'```\n{output}\n```'
    
    async def start_command(command: str) -> None:
        """Run a command in the background"""
        command = command.replace('python3', sys.executable)  # NOTE replace with machine-independent Python path (#1240)
        process = await asyncio.create_subprocess_exec(
            *shlex.split(command, posix="win" not in sys.platform.lower()),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

    def get_transport_log():
        #ui.notify(f'Checking transportlog') 
        if app.storage.user['ts']=='':
            #ui.notify('No Transport active')
            app.storage.user['processid'] = ''
            return
        else:
            if app.storage.user['processid']!='':
                #ui.notify(f'Active processid {app.storage.user["processid"]}')
                #app.storage.user['processid'] = cfgsel['processid']
                sql= f"SELECT pid,created_date, message FROM messagelog where env_from='{app.storage.user['transport_source']}' and env_to='{app.storage.user['transport_dest']}' and pid ={app.storage.user['processid']} order by created_date"
                #ui.notify(sql)
                con = sqlite3.connect("db/transport.db")
                cur = con.cursor()
                # Return all results of query
                rows =cur.execute(sql).fetchall()
                con.close()
                logarea.value=''
                for r in rows:
                    logarea.value += r[2] + '\n'
                logarea.update()
                return
            else:
                with open(f'transport_selection_{app.storage.user["ts"]}.json') as f:
                    cfgsel = tesrest.AttrDict(json.load(f))
                    if cfgsel.get('processid',None) != None:
                        app.storage.user['processid'] = cfgsel['processid']
                    else:
                        app.storage.user['processid'] = ''
                pass


    async def save_selection():
        transport_sel.Job =[]
        transport_sel.Jobgroup= []
        for r in table2.rows:
            if r['job_or_jobgroup'] =='Job':
                transport_sel['Job'].append(r['name'])
                if not 'Job' in transport_sel['TRANSPORT']:
                    transport_sel['TRANSPORT'].append('Job')
                transport_sel['Job'].append(r['name'])
            elif r['job_or_jobgroup'] =='JobGroup':
                if not 'JobGroup' in transport_sel['TRANSPORT']:
                    transport_sel['TRANSPORT'].append('JobGroup')
                transport_sel['JobGroup'].append(r['name'])
        ts = datetime.datetime.now().strftime("%m%d%Y_%H%M%S")
        transport_sel['FROM']= sel_source.value
        transport_sel['TO']= sel_dest.value
        with open(f"transport_selection_{ts}.json", "w") as outfile:
            json.dump(transport_sel, outfile)
            save_ts.set_text(ts)
            save_ts.update()
        ui.notify(f'Start transport.exe transport_selection_{ts}.json')
        app.storage.user['processid']=''
        app.storage.user['ts']=ts
        await start_command(f'transport.exe transport_selection_{ts}.json')
        ui.notify("Transport complete!")

        
    with ui.row():
        sel_source = ui.select(label='Select Source',value=app.storage.user.get('transport_source',None) ,options=list(cfg['CM'].keys()),on_change= set_source).style('width:300px')
        sel_dest   = ui.select(label='Select destination',value=app.storage.user.get('transport_dest',None) ,options=list(cfg['CM'].keys()),on_change= set_dest).style('width:300px')
        rows=[]
#    with ui.row():
        sel_object   = ui.select(label='Select Object',value=app.storage.user.get('transport_object',None) ,options=transport_sel['TRANSPORT_OBJECT'],on_change= set_object).style('width:300px')
        sel_filter = ui.input(label='Enter filter:').style('width:300px')
        columns1 = [

            {'name': 'name', 'label': 'Name', 'field': 'fullpath','sortable': True, 'align': 'left'},
            {'name': 'type', 'label': 'Type', 'field': 'type','sortable': True, 'align': 'left'},
                ]

        columns2 = [

            {'name': 'name', 'label': 'Name', 'field': 'name','sortable': True, 'align': 'left'},
            {'name': 'job_or_jobgroup', 'label': 'Job or Group', 'field': 'job_or_jobgroup','sortable': True, 'align': 'left'},
                ]

        get_data = ui.button(text="GET DATA",on_click=lambda rows=rows : getData("Job", f"name like '{sel_filter.value}'","",rows))
    sel_rows=[]        
    if sel_object.value in ['Job','JobGroup']:
        filter=''
        columns='id,parentid,name,type,fullpath'
        rows=[]

        result,_ = tesconn.getTESListSorted('Job',filter,columns=columns) 
        if len(result) >0:
            columns = [column for column in result[0]._attrs]             
            for r in result:
                nr  ={}
                for c in columns:
                    nr[c] = r[c]
                rows.append(nr)
        with ui.row():
            job_or_jobgroup =ui.toggle({'Job': 'Select as Job', 'JobGroup': 'Select as JobGroup'},value='JobGroup')#.bind_value(globals(),'job_or_jobgroup')
            ui.button(text='Add to selection',on_click=add_to_selected)
        with ui.splitter().classes('w-full text-left') as splitter:
            with splitter.before:
                #selection = ui.select(options=[r['fullpath'] for r in teslist], with_input=True,multiple=True,clearable=True, on_change=lambda e: ui.notify(e.value)).classes('w-1/2')#.bind_value(globals(),'selected')
                with ui.table(title='Selection', columns=columns1, row_key='name', rows=rows, selection='multiple', pagination=10).classes('w-full text-left') as table1:
                    with table1.add_slot('top-right'):
                        with ui.input(placeholder='Search').props('type=search').bind_value(table1, 'filter').add_slot('append'):
                            ui.icon('search')
            with splitter.after:
                ui.label().bind_text_from(table2, 'selected', lambda val: f'Current selection: {val}')
                ui.button('Remove', on_click=lambda: table2.remove_rows(*table2.selected)).bind_visibility_from(table2, 'selected', backward=lambda val: bool(val))
                #table =  ui.table(columns=columns, rows=[], row_key='name',selection='multiple', pagination=10).classes('w-full')
                with ui.table(title='Transport Selection', columns=columns2, row_key='name', rows=sel_rows, selection='multiple', pagination=10).classes('w-full') as table2:
                    with table2.add_slot('top-right'):
                        with ui.input(placeholder='Search').props('type=search').bind_value(table2, 'filter').add_slot('append'):
                            ui.icon('search')
                with ui.row():
                    ui.button('Start Transport', on_click=save_selection)
                    ui.label('TimeStamp:')
                    save_ts = ui.label()
                    logarea = ui.textarea().classes('w-full text-left')
                    ui.timer(1, lambda: get_transport_log())
            #with ui.dialog() as dialog, ui.card():
            #    result = ui.markdown()                    
                


@ui.page('/queries/{queryname}',response_timeout=99,reconnect_timeout=10)
async def queries(queryname):
    #print(queryname)
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
        sel_query.options = sorted(set([i['queryname']  for i in query_dict['queries']['query'] if i['category'] == sel_category.value and i['db'].lower() in ['admiral','reporting','restapi']]))
        sel_query.update()
        #grid.options['rowdata']=None
        #grid.options['columndefs']=None
        #grid.update()

    def update_parameters_table():
        if not 'parameter_table' in locals():
            return
        def get_Params_and_re_execute():
            for m in matches:
                print(params[m].value)
                app.storage.user[m] = params[m].value
            ui.open(f'/queries/{sel_query.value}')
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
                                if defaultvalue=='':
                                    if m =='prod_date':
                                        defaultvalue=  datetime.now.strftime("%Y-%m-%d")
                                    if m =='from_date':
                                        defaultvalue=  datetime.now - datetime.timedelta(days=8).strftime("%Y-%m-%d")
                                    if m =='to_date':
                                        defaultvalue=  datetime.now - datetime.timedelta(days=1).strftime("%Y-%m-%d")

                            else:
                                app.storage.user[m]=''
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
        if 'sel_query' in locals() and sel_query.value:                                
            ui.button('Get Data', on_click=lambda: get_Params_and_re_execute())                                                  
        #ui.button('Get Data', on_click=lambda: ui.open(f'/queries/{sel_query.value}'))
    async def getData(queryname):
        #expansion.close()
        grid_expansion.open()
        #expansion.update()
        grid_expansion.update()
        grid.options['rowData']=None
        grid.update()
        chart.visible=False
        columns =[]
        sqltext, db =[(i['querytext_sqlserver'], i['db'] ) for i in query_dict['queries']['query'] if i['queryname'] == sel_query.value][0]
        sqltext = sql_expand_inherited_parameters(sqltext=sqltext)        

        for p in params:
            val = params[p].value
            app.storage.user[p] = val
            sqltext = sqltext.replace(p,val)
        if sqltext !='':
            try:
                rows = []
                start = timer()
                if db=='restapi':
                    result, msg = await tesconn.getTESList(sqltext.split(':')[0],sqltext.split(':')[1],sqltext.split(':')[2])
                    if len(result) >0:
                        columns = [column for column in result[0]._attrs]             
                        for r in result:
                            nr  ={}
                            for c in columns:
                                nr[c] = r[c]
                            rows.append(nr)
                            #rows.append(dict(zip(columns, r)))
                else:
                    result = await connect_db(db=db, sql=sqltext)  
                    if len(result) >0:
                        columns = [column[0] for column in result[0].cursor_description]             
                        for r in result:
                            rows.append(dict(zip(columns, r)))
                end = timer()
                elapse_time= end - start
                print(f"{elapse_time:.01f} secs,{len(result)} rows.")
                #df = pandas.DataFrame.from_dict(rows)
            except Exception as ex:
                print(ex)
                rows=[]

        else:
            rows=[]
            df = pandas.DataFrame()
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
            x_axis.set_value(app.storage.user.get(f'{sel_query.value}:x-axis',''))
            chart_function.options=['Sum', 'Count']
            chart_function.set_value(app.storage.user.get(f'{sel_query.value}:chart-function',''))
            y1_axis.options=list(cols)
            y1_axis.set_value(app.storage.user.get(f'{sel_query.value}:y-axis',''))
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
            x_axis.set_value(app.storage.user.get(f'{sel_query.value}:x-axis',''))
            chart_function.options=['Sum', 'Count']
            chart_function.set_value(app.storage.user.get(f'{sel_query.value}:chart-function',''))
            y1_axis.options=list(cols)
            y1_axis.set_value(app.storage.user.get(f'{sel_query.value}:y-axis',''))
            seriesdata.options=list(cols)
        #series.options=list(cols)
        
        x_axis.update()
        y1_axis.update()
        seriesdata.update()
        if 'lbl_count' in locals():
            lbl_count.text= f'Rows:'
        
        return 
    async def get_specified_parameters():
        row = await models.UserQuery.filter(queryname=sql_query.value)

        for row in reversed(rows):
            with ui.card():
                with ui.row().classes('items-center'):
                    ui.input('Description', on_change=row.save) \
                        .bind_value(row, 'description').on('blur', list_of_outages.refresh)

        pass 
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

    async def set_category_query(cat,query):
        pass

        #ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
    #with ui1.left_drawer(top_corner=False, bottom_corner=False).style('background-color: #d7e3f4').classes('w-96'):
    """
    if queryname != None:
        app.storage.user['query'] = queryname
        ui.open('/queries')
    """
    params ={}
    rows=[]
    cols=[]
    #with ui.expansion("Selection Query",value=True).classes('w-full') as expansion:
    #    pass
    with ui.row() as query_row:
        if 'sel_query' in locals():
            qry_button=ui.button('Get Data', on_click=getData(sel_query.value))
            lbl_count= ui.label('Rows: 0')
        sel_category = ui.select(label='Select Query Category',value=app.storage.user.get('category',None) ,options=category_list,on_change=lambda: update_query_list()).style('width:100px')
        sel_query = ui.select(label='Select Query',value=queryname,options=sorted(set([i['queryname']  for i in query_dict['queries']['query'] if i.get('templatetype','') !='jinja' and i['db'].lower() in ['admiral','reporting','restapi']])), on_change=update_parameters_table)
        #ui.separator()
        parameter_table = ui.grid()
        if sel_query.value:
            update_parameters_table()
        #qry_button=ui.button('Get Data', on_click=getData(sel_query.value))            
        lbl_elapsetime = ui.label()
        lbl_rows = ui.label()
    with ui.expansion("Query data").classes('w-full') as grid_expansion:
        grid = ui.aggrid({
        'defaultColDef': {'resizable': True},
        'pagination': False,
        'paginationPageSize': 100,        
        'columnDefs': [
            ],
            'rowData': [
            ],
        'rowSelection': 'single',
        },auto_size_columns=False).classes("h-screen").on('cellClicked', lambda event: handleRowSelectedion(event=event)).on('firstDataRendered', lambda: grid.call_column_api_method('autoSizeAllColumns'))
        #ui.button('AutoSize Columns', on_click=lambda: grid.call_column_api_method('autoSizeAllColumns'))
    #with ui.expansion("Chart",value=True).classes('w-full') as chart_expansion:        
    #    chart_expansion.open()

    with ui.row():
        val =app.storage.user.get(f'{sel_query.value}:x-axis','')
        x_axis =  ui.select(list(cols),value=val,label='Select X axis ').style('width:200px')
        chart_function = ui.select(['Sum','Count'])
        x_axis.value=val
        x_axis.update()
        y1_axis = ui.select(list(cols), label='Select Y axis ').style('width:200px')
        if app.storage.user.get(f'{sel_query.value}:y-axis',None) != None:
            val = app.storage.user[f'{sel_query.value}:y-axis']
            y1_axis.set_value(val)

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
        app.storage.user[f'{sel_query.value}:x-axis'] = x_axis.value
        app.storage.user[f'{sel_query.value}:chart-function'] = chart_function.value
        app.storage.user[f'{sel_query.value}:y-axis'] = y1_axis.value
        #pivot_df = pandas.pivot_table(rows, index=x_axis.value, columns=y1_axis.value, values=None, aggfunc='sum')
        if seriesdata.value:
            series= set([row[seriesdata.value] for row in rows])
        x1 = sorted(list(set([i[x_axis.value ] or '' for i in rows])))
        groups=[sorted(list(set([try_parse_int(i[y1_axis.value]) for i in rows])))]
        y =[]
        if seriesdata.value:
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
        #json1['series'] = y1
        with r:
            r.clear()
            chart = ui.highchart(json1).style('height: 500px; width: 1000px;') 
            chart.update()
            #ui.json_editor({'content': {'json': json1}},  on_change=lambda e: ui.notify(f'Change: {e}'))                

    ui.button('Update Chart', on_click=update)
    with ui.footer().style('background-color: #3874c8'):
        ui.label('SYNERTECH TIDAL ANALYTICS')
    await getData(queryname)
    update()


@ui.page('/testpage',response_timeout=999,reconnect_timeout=10)
async def testpage():
    pagelayout()
    async def run_command(command: str) -> None:
        """Run a command in the background and display the output in the pre-created dialog."""
        import shlex
        import os
        dialog.open()
        result.content = ''
        command = command.replace('python3', sys.executable)  # NOTE replace with machine-independent Python path (#1240)
        process = await asyncio.create_subprocess_exec(
            *shlex.split(command, posix="win" not in sys.platform.lower()),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        # NOTE we need to read the output in chunks, otherwise the process will block
        output = ''
        while True:
            new = await process.stdout.read(1024)
            if not new:
                break
            output += new.decode()
            # NOTE the content of the markdown element is replaced every time we have new output
            result.content = f'```\n{output}\n```'

    with ui.dialog() as dialog, ui.card():
        result = ui.markdown()

    ui.button('python3 hello.py', on_click=lambda: run_command('python3 hello.py')).props('no-caps')


ui.run(port=7777, reload=False, storage_secret='synertech2')