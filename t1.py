import asyncio
import aioodbc
loop = asyncio.get_event_loop()
dsn = 'Driver=ODBC Driver 17 for SQL Server;Server=localhost,1433;Database=Admiral;uid=sa;pwd=kooi'

async def connect_db(sql):
    conn = await aioodbc.connect(dsn=dsn)
    cur = await conn.cursor()
    await cur.execute(sql)
    rows = await cur.fetchall()
    await cur.close()
    await conn.close()
    results = []
    if len(rows) >0:
        columns = [column[0] for column in rows[0].cursor_description]             
        for row in rows:
            results.append(dict(zip(columns, row)))
    return results

rows = loop.run_until_complete(connect_db('select top 1 * from nodmst'))
    
for r in rows:
    print(r)