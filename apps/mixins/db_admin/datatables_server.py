import os
from websaw import redirect
import os 
from .controllers import app, Context
from ..common.form_1 import Form, FormStyleBulma
from datetime import datetime
from .datatables_utils import *
from PIL import Image

mygui=DtGui()
my_parser = QueryParser()

@app.route('del_rec', method=['GET','POST'])
@app.use('generic.html')
def del_rec(ctx: Context):
    my_dict = ctx.request.query.decode()
    cdb = my_dict.get('cdb', None)
    db = ctx.ask(cdb)
    
    if not my_dict.table:
        return dict(error = 'You need to select a table')
    if not my_dict.id:
        return dict(error = 'No ID')
    record = db[my_dict.table][my_dict.id]
    if record:
        record.delete_record()
        db.commit()
        #flash.set('Deleted record')
        redirect(ctx.URL(my_dict.caller, vars={"cdb":cdb, "table":my_dict.table}))
    return dict(s=my_dict)

@app.route('view_rec', method=['GET'])
@app.use('view_rec.html')
def view_rec(ctx: Context):
    page_title = 'View '
    my_dict = ctx.request.query.decode()
    if my_dict:
        if 'ktable' in my_dict:
            my_dict.table = my_dict.ktable
            my_dict.id = my_dict.kval
        s_dict = dict(cdb=my_dict.cdb, table=my_dict.table, id=my_dict.id, caller=my_dict.caller)
        ctx.session['s_dict'] = s_dict
    else:  # result of submit
        r_dict = ctx.session['s_dict']
        my_dict['cdb'] = r_dict['cdb']
        my_dict.table=r_dict['table']
        my_dict.id = r_dict['id']
        my_dict.caller = r_dict['caller']
    cdb = my_dict.get('cdb', None)
    db = ctx.ask(cdb)
    if 'ktable' in my_dict:
        b_button = mygui.get_button('back', ctx.URL(my_dict.caller, vars={"cdb":my_dict.cdb, "table":my_dict.b_table, "orig_query": 1}), "Back", 'Back')
    else:
        b_button = mygui.get_button('back', ctx.URL(my_dict.caller, vars={"cdb":cdb, "table":my_dict.table}), "Back", 'Back')
    db[my_dict.table]['id'].readable = db[my_dict.table]['id'].writable = False 
    form=Form(ctx, db[my_dict.table], record=my_dict.id, dbio=False, deletable=False, formstyle=FormStyleBulma)
    page_title += db[my_dict.table]._singular 

    if form.accepted:
        redirect(ctx.URL(my_dict.caller))
    return dict(form=form, page_title=page_title, back=b_button)

@app.route('edit_rec', method=['GET', 'POST'])
@app.use('edit_rec.html')
def edit_rec(ctx: Context):
    page_title = 'Edit '
    my_dict = ctx.request.query.decode()
    if my_dict:
        s_dict = dict(cdb=my_dict.cdb, table=my_dict.table, id=my_dict.id, caller=my_dict.caller)
        ctx.session['s_dict'] = s_dict
    else:
        r_dict = ctx.session['s_dict']
        my_dict['cdb'] = r_dict['cdb']
        my_dict.table=r_dict['table']
        my_dict.id = r_dict['id']
        my_dict.caller = r_dict['caller']
    
    my_params = list(ctx.request.params.items())
    rb = list(my_dict.items())
    post_vars = ctx.request.forms
    cdb = my_dict.get('cdb', None)
    db = ctx.ask(cdb)
    
    db[my_dict.table]['id'].readable = db[my_dict.table]['id'].writable = False 
    form=Form(ctx, db[my_dict.table], record=my_dict.id, deletable=False, formstyle=FormStyleBulma)
    page_title += db[my_dict.table]._singular 
    messages = []
    record = db[my_dict.table][my_dict.id]
    b_button = mygui.get_button('back', ctx.URL(my_dict.caller, vars={'cdb': cdb, "table":my_dict.table, "orig_query":1}), "Back", 'Back')
    url = ctx.request.url.split("?")[0]
    if form.accepted:
        if record:
            record.update_record(**form.vars)
            db.commit()
            #flash.set('Updated record')
            redirect(ctx.URL(my_dict.caller, vars={"cdb":my_dict.cdb, "table":my_dict.table}))
        else:
            # warning, should we really insert if record
            messages.append('trying to update form %s with no id as such: %s ' % (form.form_name, form.vars))
        messages.append('form %s accepted with: %s ' % (form.form_name, form.vars))
        #flash.set(messages)
    elif form.errors:
        messages.append('form %s has errors: %s ' % (form.form_name, form.errors))
        #flash.set(messages)
    return dict(form=form, page_title=page_title, back=b_button)


@app.route('add_rec', method=['GET','POST'])
@app.use('add_rec.html')
def add_rec(ctx: Context):
    page_title = 'New '
    my_dict = ctx.request.query.decode()
    cdb = my_dict.get('cdb', None)
    db=ctx.ask(cdb)
    ### make sure we have something here and decide what to do 
    
    post_vars = ctx.request.forms
    messages=[]
    back=''
    form=''
    stick = 0
    if ctx.session['orig_query']: #used for locking down specific fields
        fld = ctx.session['orig_query']['first']['fieldname']
        val = ctx.session['orig_query']['second']
        stick = 1
    if my_dict:
        s_dict = dict(table=my_dict.table, id=my_dict.id, caller=my_dict.caller)
        ctx.session['s_dict'] = s_dict
        
    if not my_dict: # result of submit
        r_dict = ctx.session['s_dict']
        my_dict.table=r_dict['table']
        my_dict.id = r_dict['id']
        my_dict.caller = r_dict['caller']
        #print('ADD RECORD r dict', r_dict)
    db[my_dict.table]['id'].readable = db[my_dict.table]['id'].writable = False 
    page_title += db[my_dict.table]._singular
    
    if stick==1:
        db[my_dict.table][fld].writable = False
        db[my_dict.table][fld].default = int(val)
        x=db[my_dict.table][fld].represent(val)
        page_title += ' For ' + x 
    form=Form(ctx, db[my_dict.table], dbio=False, formstyle=FormStyleBulma)
    
    b_button = mygui.get_button('back', ctx.URL(my_dict.caller, vars={'cdb': cdb, 'table': my_dict.table, "orig_query":1}), "Back", 'Back')
    messages=[]
    if form.accepted:
        db[my_dict.table].insert(**form.vars)
        #flash.set ('Added a record')
    elif form.errors:
        messages.append('form %s has errors: %s ' % (form.form_name, form.errors))
        #flash.set(messages)
    return dict(form=form, page_title=page_title, messages=messages, back=b_button)
  
def b_fields(flds):
    f_str=''
    for f in flds:
        f_str += '&nbsp;<span class="tag tag-info">%s</span>' % f
    return f_str


@app.route('dt_server')
def dt_server(ctx: Context):
    url = ctx.request.url.split("?")[0]
    call_header = ctx.request.headers.get('Referer')
    cal = call_header.split("/")
    my_dict = ctx.request.query.decode()
    columns= my_dict.cols.split(",")
    cdb = my_dict.get('cdb', None)
    if cdb:
        db = ctx.ask(cdb)
    else:
        print('We dont have a db') #### think about returning without doing anythign     
    row_buttons = my_dict.row_buttons.split(",")
    row_button = my_dict.row_button_list
    t = my_dict.table
    session=ctx.session    
    
    session['subquery'] = ''
    session['query'] = session['subquery']
    
    if ctx.session['orig_query'] != '':
        query_filter = my_parser.parse(session['orig_query'])
    elif session['query'] != '':
        query_filter = my_parser.parse(session['query'])
    else:
        query_filter = (db[t].id > 0)

    if ctx.request.query['start'] is not None:
        iDisplayStart = int(ctx.request.query['start'])
    else:
        iDisplayStart = 0

    if ctx.request.query['length'] is not None:
        iDisplayLength = int(ctx.request.query['length'])
    else:
        iDisplayLength = 10

    if ctx.request.query['draw'] is not None:
        sEcho = int(ctx.request.query['draw'])
    else:
        sEcho = 1

    cols=len(columns)
    if cols:
        origpos=[]
        newpos=[]
        fld = 'order[0][column]'            
        fld1 = 'order[0][dir]'            
        sortorder={}
        for i, column in enumerate(columns):
            origpos.append({'col':column, 'pos':i})
            if column in my_dict.hide:
                continue
            else:
                newpos.append({'col':column, 'pos':i})
               
        
        fd = ctx.request.query[fld]
        so = ctx.request.query.get(fld1, 'asc')
            
        for i, j in enumerate(origpos):
            op=origpos[i]['pos']
            if int(fd) == int(op):
                np = newpos[origpos[i]['pos']]
                nc = np['col'] 
                sortorder={'column': nc, 'direction': so}
                break
            else:
                continue
        if sortorder['direction'] == 'desc':
            colorder = ~db[t][sortorder['column']]
        else:
            colorder = db[t][sortorder['column']]
    
    if ctx.request.query['search[value]'] and ctx.request.query['search[value]'] != '':
        qf= ''
        sval=''
        qrytablelist=[]
        for i in range (int(cols)):
            if db[t][columns[i]].type == 'string':
                sval = (db[t][columns[i]].contains(ctx.request.query['search[value]']))
            elif db[t][columns[i]].type.startswith('reference'):
                try:
                    if db[t][columns[i]].requires.ktable:
                        reftable = db[t][columns[i]].requires.ktable
                        if not reftable in qrytablelist:
                            qrytablelist.append(reftable)
                            query_filter &= (db[reftable].id == db[t][columns[i]]) 
                        refname = db[t][columns[i]].requires.fieldnames[0]
                        sval = (db[reftable][refname].contains(ctx.request.query['search[value]']))
                except:
                    print('INSIDE REF EXCEPTION')
                
            elif db[t][columns[i]].type == 'text':
                sval = (db[t][columns[i]].contains(ctx.request.query['search[value]']))
            
            elif db[t][columns[i]].type == 'datetime':
                if not ctx.request.query['search[value]'].isdigit():
                    continue
                else:
                    print('Inside datetime')
                    sval = (db[t][columns[i]] >= (ctx.request.query['search[value]']))
            else:
                if not ctx.request.query['search[value]'].isdigit():
                    continue
                else:
                    sval = (db[t][columns[i]] == int(ctx.request.query['search[value]']))
            if qf == '':
                qf = sval
            else:
                qf |= sval
        query_filter &= qf
    
    query = db(query_filter).select(limitby=(iDisplayStart, iDisplayStart + iDisplayLength), orderby_on_limitby = False, orderby=colorder)

#    if query_filter == (db[t].id > 0):
#        #print('QF IS ', query_filter)
#        row = db(db.counters.table_name == t).select(db.counters.records).first()
#        if row:
#            iTotalRecords = row.records
#        else:    
#            iTotalRecords = db(query_filter).count()
#            x = db.counters.insert(table_name = t, records=iTotalRecords)
#    else:
    trecs = db(query_filter).count()
    iTotalRecords = trecs
    recs = query.as_list()
    aaData = []
    for row in recs:
        try:
            row=row[t]
        except:    
            pass
        datarow={}
        for col in row:
            if row[col] is not None:
                if col == t or '_record' in col:
                    # internal dal col names
                    continue
                elif db[t][col].type == 'date':
                    datarow[col] = row[col].strftime('%Y-%m-%d') # %H:%M:%S')
                elif db[t][col].type =='datetime':
                    datarow[col] = row[col].strftime('%Y-%m-%d %H:%M:%S')
                elif db[t][col].type.startswith('reference'):
                    try:
                        if db[t][col].requires.ktable:
                            href = ctx.URL('view_rec', vars={"caller":my_dict.caller, "cdb":cdb,
                                                             "orig_query":query_filter, "b_table": t,
                                                              "ktable":db[t][col].requires.ktable,
                                                              "kfield":db[t][col].requires.kfield,
                                                              "kval":row[col]})
                            datarow[col] = mygui.get_admin_button('view', db[t][col].represent(row[col], row), href)            
                    except:
                        datarow[col] = db[t][col].represent(row[col], row)
                    
                elif db[t][col].type.startswith('list:reference'):
                    datarow[col] = db[t][col].represent(row[col], row)
                elif db[t][col].type == 'upload':
                    x = str(db[t])
                    #### JAB this is a serious hack that needs to be sorted out !!!!!!!
                    if x == 'profile':
                        mixin_name = 'auth_mixin' #ctx.mixin_data.app_name
                        i_url = ctx.URL(f'static/mxn/{mixin_name}/images/{row[col]}')
                        img = '''<img src="%s" class="img-thumbnail" alt="Image" width="100">''' % i_url
                    else:
                        img = '''<img src="%s" class="img-thumbnail" alt="Image" width="100">''' % "images/%s" % row[col]
    
                    datarow[col] = img
                else:
                    datarow[col] = row[col]
            else:   
                datarow[col] = ''
        if row_buttons[0] != '': #empty list
            btns=""
            for i, j in enumerate(row_buttons):
                fk=''
                b_cdb = 'row_button_list[%d][cdb]'% (i)
                b = 'row_button_list[%d][name]'% (i)
                f = 'row_button_list[%d][func]'% (i)
                calr = 'row_button_list[%d][caller]' % (i)
                if j == 'link':
                    ffk = 'row_button_list[%d][fk]' % (i)
                    fk = my_dict[ffk]
                f_f = my_dict[f]
                b_name = my_dict[b]
                caller = my_dict[calr]
                href = ctx.URL(f_f, vars={"cdb": my_dict.cdb, "caller":caller, "table": t, "fk":fk, "id":row['id']})
                btns += " " + mygui.get_dtbutton_icon(j, b_name, href)
            datarow['btns'] = btns            
        aaData.append(datarow)
    return dict(draw=sEcho, recordsTotal=iTotalRecords, recordsFiltered=iTotalRecords, data=aaData)
