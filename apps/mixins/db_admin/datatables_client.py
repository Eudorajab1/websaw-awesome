from websaw.core import Fixture
from yatl.helpers import INPUT, H1, A, DIV, SPAN, XML
from .datatables_utils import DtGui
mygui=DtGui()
from pprint import pprint
import json
# ################################################################
# Grid object (replaced SQLFORM.grid) using Datatables 
# ################################################################

class Grid(object):
    """
    Usage in websaw controller:

       def index():
           grid = Grid(db.thing, record=1)
           return dict(grid=grid)

    Arguments:
    - ctx current context
    - db name we are using as defined in DBRegistry
    - table: a DAL table or a list of fields (equivalent to old SQLFORM.factory)
    - fields: a list of fields to display
    - create: set to False to disable creation of new record
    - editable: set to False to disallow editing of recordrsd seletion
    - deletable: set to False to disallow deleting of recordrsd seletion
    - links: list of addtional links to other tables
    - form_name: the optional name for this grid
    - serverside: set to False for client side processing
    """

    def __init__(self,
                 ctx = None,
                 cdb = None,
                 table = None,
                 fields=None,
                 create=True,
                 editable=True,
                 deletable=True,
                 viewable=True,
                 upload=False,
                 download=False,
                 back=None,
                 links=None,
                 page_title=None,
                 formstyle='',
                 form_name=False,
                 serverside=True,
                 show_id=True,
                 hide=[],
                 order=['0', 'asc'],
                 extended_search=False):

        self.ctx = ctx
        self.cdb = cdb
        self.table = table
        self.create=create
        self.editable=editable
        self.deletable=deletable
        self.viewable=viewable
        self.back=back
        self.links=links
        self.readonly = False
        self.upload=upload
        self.download=download
        self.page_title=page_title
        self.formstyle=formstyle
        self.serverside=serverside
        self.form_name = form_name or table._tablename
        self.hidden = False
        self.formkey = None
        self.cached_helper = None
        self.show_id = show_id
        self.hide=hide
        self.order=order
        self.extended_search=extended_search
        self.db = self.ctx.ask(self.cdb)
               
        self.ctx.session['query'] = self.ctx.session.get('query', '')
        if self.ctx.session['query'] :
            print(self.ctx.session['query'])
        else:
            self.ctx.session['query'] = ''
        
        if isinstance(table, list):
            dbio = False
            # mimic a table from a list of fields without calling define_table
            form_name = form_name or 'none'
            for field in table: 
                field.tablename = getattr(field,'tablename',form_name)

        if isinstance(fields, list):
            self.fields=fields
        else:
            self.fields=table.fields
        cal = self.ctx.request.url.split("/")
        #print('CAL is ', cal)
        scal = cal[4].split("?")
        self.app = cal[3]
        self.func = scal[0]
    
    def build_headers(self):
        #call_header = ctx.request.headers.get('Referer')
        headers= ''
        db = self.db
        hide = self.hide
        t = self.table
        self.col =  ",".join(self.fields)
        self.cols=[]
        self.hdrs=[]
        for f in self.fields:
            if f in hide:
                continue
            if f == 'id':
                if self.show_id:
                    self.cols.append({'data': f})
                    self.hdrs.append(db[t][f].label)
                    continue
                else:
                    continue
            self.cols.append({'data': f})
            self.hdrs.append(db[t][f].label)
            
        self.hdrs.append('Action')
        self.cols.append({'data': 'btns'})
        headers = self.hdrs
        return headers
    
    def get_fields(self):
        return self.fields
        
    def form_buttons(self):
        btns = []
        #a="""
        #<button id="btToggleDisplay" class="btn btn-outline-info btn-sm"><i class="fa fa-table" aria-hidden="true"></i> 
	#<i class="fas fa-arrows-alt-h " aria-hidden="true"></i> <i class="far fa-address-card " aria-hidden="true"></i></button>
    #"""
        
        if self.download:
            d_button = mygui.get_dt_button('download', self.ctx.URL('index', vars={"caller": self.func, "table" : self.table._tablename}), "Export", 'Export')
            btns.append(d_button)
        if self.upload:
            u_button = mygui.get_dt_button('upload_csv', self.ctx.URL('index', vars={"caller": self.func, "table" : self.table._tablename}), "Import", "Import")
            btns.append(u_button)
        if self.create:
            a_button = mygui.get_dt_button('add', self.ctx.URL('add_rec', vars={"cdb":self.cdb, "caller": self.func, "table" : self.table._tablename}), "Add", 'Add')
            btns.append(a_button)
        if self.back:
            btns.append(self.back)
        #btns.append(a)
        if not self.page_title:
            if not self.table._plural:
                b_str='<span class="subtitle">&nbsp;%s</span>' % self.table
            else:
                b_str='<span class="subtitle">&nbsp;%s</span>' % self.table._plural
        else:
            b_str='<span class="subtitle">&nbsp;%s</span>' % self.page_title
        
        for b in btns:
            b_str += '<span class="is-pulled-right">&nbsp;%s</span>' % XML(b)
        return b_str
        
    def row_buttons(self):
        r_btns = []
        row_buttons=[]
        if self.links:
            for l in self.links:
                #print('LINK IS', l)
                r_btns.append('link')
                row_buttons.append({'name': l['name'], 'cdb':self.cdb, 'caller': self.func, 'func':l['func'], 'fk':l['fk'],'id':'id'}) 
        if self.viewable:
            r_btns.append('view')
            row_buttons.append({"name":"View", 'cdb':self.cdb, "caller": self.func, "func":"view_rec", "id": "id"})
        if self.editable:
            r_btns.append('edit')
            row_buttons.append({"name":"Edit",'cdb':self.cdb,"caller": self.func, "func":"edit_rec", "id": "id"})
        if self.deletable:
            r_btns.append('delete')
            row_buttons.append({"name":"Delete",'cdb':self.cdb,"caller": self.func, "func":"del_rec", "id": "id"})
            
        self.r_buts = ",".join(r_btns)
        return row_buttons

    def build_j_script(self):
        row_buttons = self.row_buttons()
        name = self.table
        js="""
        <script>
            $(document).ready(function() {
                var table = $('#%s').DataTable( {
                "processing": true,
                "serverSide": true,
                "autoWidth": false,
                "scrollX": true,
                "ajax": {
                    "url": "%s",
                    "data": function ( d ) {
                        d.table = "%s"
                        d.cols = "%s"
                        d.row_buttons = "%s"
                        d.row_button_list = %s
                        d.caller = "%s"
                        d.hide = "%s"
                        d.cdb = "%s"
                        
                    },
                },
                "columns": %s,
                "order" : [%s]
                
            });
            	 	$('#btToggleDisplay').on('click', function () {
			$("#generic thead").toggle()

			$("#generic").toggleClass('cards')
			if($("#generic").hasClass("cards")){
				// Create an array of labels containing all table headers
				var labels = [];
				$("#generic").find("thead th").each(function() {
					labels.push($(this).text());
				});

				// Add data-label attribute to each cell
				$("#generic").find("tbody tr").each(function() {
					$(this).find("td").each(function(column) {
						$(this).attr("data-label", labels[column]);
					});
				});

				var max = 0;
				$("#generic tr").each(function() {
					max = Math.max($(this).height(), max);
				}).height(max);

			} else {

				// Remove data-label attribute from each cell
				$("#generic").find("td").each(function() {
					$(this).removeAttr("data-label");
				});

				$("#generic tr").each(function(){
					$(this).height("auto");
				});
                        
				}	
                
            });

        });
        </script>""" % (self.table, self.ctx.URL('dt_server'), self.table, self.col, self.r_buts, 
                        row_buttons,self.func, self.hide, self.cdb, self.cols,self.order)
        return js
        
    def dt_grid(self):
        f_buttons = self.form_buttons()
        hdrs = self.build_headers()
        hd = ''
        for h in hdrs:
            hd += '<th>%s</th>' % h
        frm = self.build_j_script()
        frm += """
        <div class="column is-12 is-centered">
			%s
        </div>
        <div class="table-responsive">
            <table id=%s class="table is-narrow is-striped is-bordered">
                <thead>
                    <tr>
                        %s
                    </tr>
                </thead>
            </table>
        </div>""" % (f_buttons, self.table, hd)
        return frm
                
    def __str__(self):
        return self.dt_grid()
