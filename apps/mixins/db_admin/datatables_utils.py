from yatl.helpers import A, SPAN, XML

def query_as_dict(expression, field_type=None):
    """Seralizes gluon.dal.Query as dictionary.
    
    Converts a gluon.dal.Query or gluon.dal.Expression
    into a dictionary structure that can be pickled and
    stored in the session.
    
    Args:
        expression: gluon.dal.Query or gluon.dal.Expression
    
    Returns:
        Dictionary in the form {op:op, first:expression, second:expression}
        op: the query operation (eg, AND, EQ, GT)
        expression: either a dictionary (that expands a gluon Table,
            Field, Expression or Query object) or a base object such as
            a string or list.
    
    For example:
        >>>query = (db.comment.id.belongs((1,2,3))) & (db.webpage.title == 'FAQ')
        >>>print query_as_dict(query)
        "{'second': {'second': 'FAQ', 'first': {'table': 'webpage', 'fieldname': 'title',
        'tablename': 'webpage'}, 'op': 'EQ'}, 'first': {'second': (1, 2, 3), 'first':
        {'table': 'comment', 'fieldname': 'id', 'tablename': 'comment'}, 'op': 'BELONGS'},
        'op': 'AND'}"
    """
    from pydal.objects import Query, Expression, Table, Field
    if isinstance(expression, Field):
        tablename = expression._tablename
        return dict(tablename=expression._tablename,
                    table = str(expression._table),
                    fieldname = expression.name)
    elif isinstance(expression, (Expression, Query)):
        if not expression.second is None:
            return dict(op=expression.op.__func__.__name__, 
                        first=query_as_dict(expression.first), 
                        second=query_as_dict(expression.second))
        elif not expression.first is None:
            if not expression.op is None:
                return dict(op=expression.op.im_func.__name__,
                            first=query_as_dict(expression.first),
                            second=None) # eg '(person.title IS NULL)'
            else:
                return expression.first
        elif not isinstance(expression.op, str):
            return expression.op()
        else:
            return '(%s)' % expression.op
    elif field_type:
        return str(represent(expression,field_type))
    elif isinstance(expression,(list,tuple)):
        return expression
    elif isinstance(expression, Table):
        return dict(tablename=expression._tablename,
                    table = str(expression))
    elif expression==None:
        return None
    else:
        return str(expression)

#from ...auth.models import auth_db as db  #####JAB NEED TO SORT THIS OUT 
class QueryParser(object):
    """
    This class is intended as an interface for reading queries submitted
    via json or other client protocols
    """
       
    def __init__(self):
        self.dquery = None

    def parse(self, dquery):
        self.dquery = dquery
        return self.build(self.dquery)

    def build(self, d):
        op, first, second = (d["op"], d["first"],
                             d.get("second", None))
        built = None
        if op in ("_and", "_or"):
            if not (type(first), type(second)) == (dict, dict):
                raise SyntaxError("Invalid AND/OR query")
            if op == "_and":
                built = self.build(first) & self.build(second)
            else: built = self.build(first) | self.build(second)
 
        elif op == "NOT":
            if first is None:
                raise SyntaxError("Invalid NOT query")
            built = ~self.build(first)
        else:
            # normal operation (GT, EQ, LT, ...)
            if isinstance(second, dict) and "tablename" in second:
                right = db[second["tablename"]][second["fieldname"]]
            else:
                if second[0] == '{':
                    right = (second[1:])
                else:
                    right = second
            left = db[first["tablename"]][first["fieldname"]]
 
            if op == "EQ".lower(): built = left == right
            elif op == "NE".lower(): built = left != right
            elif op == "GT".lower(): built = left > right
            elif op == "GE".lower(): built = left >= right
            elif op == "LT".lower() : built = left < right
            elif op == "LE".lower() : built = left <= right
            elif op == "CONTAINS".lower() : built = left.contains(right)
            elif op == "BELONGS".lower() : 
                built = left.belongs(right)
            elif op == "STARTSWITH".lower() : built = left.startswith(right)
            else: raise SyntaxError("Operator not supported")
 
        return built

class DtGui:
    """
        This class contains all helper functions for datatables
    """
    def get_dtbutton_icon(self, button_type,
                                    button_text = '',
                                    href=''):
        
        if button_type == 'edit':
            href = href
            button = '<a class="tag is-info" href="%s"><i class="fas fa-user-edit text-warning"></i>&nbsp;%s</a>' %(href, button_text)
            return XML(button)
        if button_type == 'view':
            href = href
            button = '<a class="tag is-info" href="%s"><i class="fa fa-search-plus text-info"></i>&nbsp;%s</a>' %(href, button_text)
            return XML(button)
        
        if button_type == 'delete':
            href = href
            onc="return confirm('Are you sure?');"
            button = '<a class="tag is-info" href="%s" onclick=%s><i class="fa fa-trash text-danger"></i>&nbsp;%s</a>' %(href, onc, button_text)
            return XML(button)
        
        if button_type == 'link':
            href = href
            button = '<a class="tag is-link" href="%s"><i class="fa fa-list text-info"></i>&nbsp;%s</a>' %(href, button_text)
            return XML(button)

        return XML(button)
        
    def get_admin_button(self, button_type,
                                    button_text = '',
                                    href=''):
        
        if button_type == 'table':
            href = href
            button = '<a class="tag is-link" href="%s"><i class="fas fa-list text-info"></i>&nbsp;%s</a>' %(href, button_text)
            return button
            
        if button_type == 'view':
            href = href
            button = '<a class="tag is-link" href="%s"><i class="fas fa-search-location text-info"></i>&nbsp;%s</a>' %(href, button_text)
            return button
        
        if button_type == 'edit':
            href = href
            button = '<a class="tag is-link" href="%s"><i class="fas fa-cog"></i>&nbsp;%s</a>' %(href, button_text)
            return button
        if button_type == 'delete':
            href = href
            button = '<a class="tag is-link" href="%s"><i class="fa fa-trash"></i>&nbsp;%s</a>' %(href, button_text)
            return XML(button)

        return XML(button)
    
    def b_buttons(self, buttons,table):
        b_str='<h4><span class="float-left text-info">&nbsp;%s Admin</span></h4>' % db[table]._plural
        for b in buttons:
            b_str += '<span class="float-right">&nbsp;%s</span>' % XML(b)
        return b_str
                    
    def get_button(self,
                   button_type,
                   url,
                   tooltip="",
                   title='',
                   _class='',
                   _id='',
                   _style='',
                   _target='',
                   _disabled=False,
                   onclick=None,
                   cid=None,
                   btn_size='',
                   btn_class="button is-outlined is-small is-link"):
        """
            This function returns a button of type "button_type" and redirects to url "url".
            See below for supported button types
            The tooltip argument can be used to specify text shown when the mouse hovers over the button
        """
        if button_type == 'add':
            title = title or 'New Record'
            icon = "fa fa-plus"
        elif button_type == 'register':
            title = title or "Register"
            icon = "fa fa-registered"
        elif button_type == 'accept':
            title = title
            icon = 'fa fa-check'
        elif button_type == 'barcode':
            icon = 'fa fa-barcode'
        elif button_type == 'delete':
            title = title
            icon = "fa fa-trash"
            onclick = "return confirm('Are you sure?');"
        elif button_type == 'delete_notext':
            title = ""
            icon = "fa fa-times"
        elif button_type == 'cancel':
            title = title
            icon = 'fa fa-ban'
        elif button_type == 'cancel_notext':
            title = ''
            icon = 'fa fa-ban'
        elif button_type == 'calendar_notext':
            title = ''
            icon = 'fa fa-calendar-o'
        elif button_type == 'ok_notext':
            title = ''
            icon = 'fa fa-check'
        elif button_type == 'list_notext':
            title = ''
            icon = 'fa fa-list'
        elif button_type == 'pending':
            title = title
            icon = 'fa fa-hourglass2'
        elif button_type == 'user_notext':
            title = ''
            icon = 'fa fa-user'
        elif button_type == 'user':
            title = title
            icon = 'fa fa-user'
        elif button_type == 'back':
            title = " Back" if not title else title
            icon = "fas fa-arrow-left"
            #btn_class = 'btn-back'
        elif button_type == 'back_bs':
            title = "Back" if not title else title
            icon = "fa fa-arrow-left"
        elif button_type == 'duplicate':
            title = title
            tooltip = "Duplicate"
            icon = 'fa fa-clone'
        elif button_type == 'next_no_text':
            title = ''
            icon = 'fa fa-arrow-right'
        elif button_type == 'previous_no_text':
            title = ''
            icon = 'fa fa-arrow-left'
        elif button_type == 'list':
            title = title
            icon = 'fa fa-list'
        elif button_type == 'download':
            title = title
            icon = 'fa fa-download'
        elif button_type == 'credit-card':
            title = title
            icon = 'fa fa-credit-card'
        elif button_type == 'file':
            title = title
            icon  = 'fa fa-file-o'
        elif button_type == 'print':
            title = title
            icon  = 'fa fa-print'
        elif button_type == 'repeat':
            title = title
            icon = 'fa fa-refresh'
        elif button_type == 'search':
            title = title
            icon  = 'fa fa-search'
        elif button_type == 'shopping-cart':
            title = title
            icon = self.get_icon('shopping-cart')
        elif button_type == 'noicon':
            title = title
            icon = ''

        else:
            title = "Invalid button type, please check..."
            icon = ''

        if _class:
            _class = "btn" + ' ' + btn_class + ' ' + btn_size + ' ' + _class
        else:
            _class = "btn" + ' ' + btn_class + ' ' +  btn_size

        if not cid:
            button = A(SPAN(_class=icon), ' ',
                       title,
                       _class=_class,
                       _id=_id,
                       _href=url,
                       _onclick=onclick,
                       _title=tooltip,
                       _style=_style,
                       _target="#myModal"
                       )
        else:
            button = A(SPAN(_class=icon), '',
                       title,
                       _class=_class,
                       _id=_id,
                       _href=url,
                       _onclick=onclick,
                       _title=tooltip,
                       _style=_style,
                       _target=_target,
                       cid=cid)

        if _disabled:
            button['_disabled'] = 'disabled'
            button['_href'] = '#'
            button['_onclick'] = ''

        return button

    def get_dt_button(self,
                   button_type,
                   url,
                   tooltip="",
                   title='',
                   _class='',
                   _id='',
                   _style='',
                   _target='',
                   _disabled=False,
                   onclick=None,
                   cid=None,
                   btn_size='',
                   btn_class='tag tag-info' ):
        """
            This function returns a button of type "button_type" and redirects to url "url".
            See below for supported button types
            The tooltip argument can be used to specify text shown when the mouse hovers over the button
        """
        if button_type == 'add':
            title = title or 'New Record'
            icon = "fas fa-plus"
        elif button_type == 'back':
            title = "Back" if not title else title
            icon = "fas fa-arrow-left"
        elif button_type == 'upload_csv':
            title = title or "Upload CSV"
            icon = "fas fa-upload"
        elif button_type == 'delete':
            title = title
            icon = "fas fa-trash"
            onclick = "return confirm('Are you sure?');"
        elif button_type == 'download':
            title = title
            icon = 'fas fa-download'
        elif button_type == 'file':
            title = title
            icon  = 'fas fa-file-o'
        elif button_type == 'print':
            title = title
            icon  = 'fas fa-print'
        elif button_type == 'repeat':
            title = title
            icon = 'fas fa-refresh'
        elif button_type == 'search':
            title = title
            icon  = 'fas fa-search'
        elif button_type == 'shopping-cart':
            title = title
            icon = self.get_icon('shopping-cart')
        elif button_type == 'noicon':
            title = title
            icon = ''

        else:
            title = "Invalid button type, please check..."
            icon = ''

        if _class:
            _class = "btn" + ' ' + btn_class + ' ' + btn_size + ' ' + _class
        else:
            _class = "btn" + ' ' + btn_class + ' ' +  btn_size

        button = '<a class="%s" href="%s"><i class="%s"></i>&nbsp;%s</a>' %(btn_class, url, icon, title)
        
        return button
