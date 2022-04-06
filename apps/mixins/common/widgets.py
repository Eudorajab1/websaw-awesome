import os
from pydal import Field
from yatl.helpers import *

"""
ckeditor4: websaw plugin for CKEditor v4: http://ckeditor.com/
"""
class CKEditor(object):
    """
    Integrates CKEditor into websaw.
    """
    def __init__(self, field=None, vars=None):
        """
        Initializes the CKEditor module. Requires a DAL instance.
        """
        self.field = field
        self.vars = vars
        self.loaded=False
        
    def widget(self, field, vars, **attributes):
        """
        To be used with db.table.field.widget to set CKEditor as the desired
        widget for the field. Simply set
        db.table.field.widget = ckeditor.widget to use the CKEditor widget.
        """
        attributes['_class'] = 'text form-control ckeditor'
        attributes['_cols'] = 80
        attributes['_rows'] = 10
        attributes['_id'] = self.get_id(field)
        attributes['_name'] = field.name
        value = field.formatter(vars.get(field.name))
        textarea = TEXTAREA(value or '', **attributes)
        javascript = self.load('#' + textarea.attributes['_id'],
                               use_caching=False)
        result = CAT(textarea, javascript)
        return result
    
    def get_id(self, field):
        """create an identefier for a field"""
        return "%s_%s" % (getattr(field, "_tablename", "no_table"), field.name)
    
    def load(self, selector=None, use_caching=True):
        """
        Generates the required JavaScript for CKEditor. If selector is set,
        then immediately turns the selected HTML element(s) into CKEditor
        instances. Otherwise, a manual JavaScript call to plugin_ckeditor_init()
        is required with the desired selector.
        """
        if self.loaded and use_caching:
            return XML('')
        else:
            self.loaded = True

        jquery_js = URL('static', 'ckeditor/adapters/jquery.js')
        ckeditor_js = URL('static', 'ckeditor/ckeditor.js')
        contents_css = "['%s']" % URL('static', 'ckeditor/contents.css')
        return XML(
            """
            <script type="text/javascript" src="%(ckeditor_js)s"></script>
            <script type="text/javascript" src="%(jquery_js)s"></script>
            </script>
            """ % dict(
                ckeditor_js = ckeditor_js,
                jquery_js = jquery_js,
            )
        )

""" select2: Select2 widget for WebSaw: https://select2.org/ """
class Select2(object): #(field,vars):
    def __init__(self, field=None, vars=None):
        self.field=field
        self.vars=vars  
    
    def to_id(self, field):
        """get an identifier for a field"""
        return "%s_%s" % (getattr(field, "_tablename", "no_table"), field.name)

    def get_options(self, validators):
        """given a validator chain, if one has .options, return them"""
        options = None
        if validators:
            if not isinstance(validators, (list, tuple)):
                validators = [validators]
                print(validators)
            for item in validators:
                if hasattr(item, "options"):
                    options = item.options
                    break
            if callable(options):
                options = options()
        return options

    def widget(self, field, vars):
        multiple = field.type.startswith("list:")
        value = field.formatter(vars.get(field.name))
        value = list(map(str, value if isinstance(value, list) else [value]))
        div_id = self.to_id(field)
        field_options = [
            [k, v, (not k is None and k in value)]
            for k, v in self.get_options(field.requires)
        ]

        option_tags = [
            OPTION(v, _value=k, _selected=_selected)
            for (k, v, _selected) in field_options
        ]
        control = DIV()
        control.append ( SELECT(
         *option_tags,
         _id = self.to_id(field),
         _name = field.name,
         _class = "select2-multiple",
         _multiple = multiple,
              ))

        script = "$('#%s')" % (div_id)
        script += ".select2({placeholder:'Select an option',width:'50%'});"
        
        control.append(
            SCRIPT( script )
        )
        return control

""" dropify: Dropify widget for WebSaw"""
class Dropify(object): 
    def __init__(self, field=None, vars=None):
        self.field=field
        self.vars=vars
        
    def to_id(self, field):
        """get an identified for a field"""
        return "%s_%s" % (getattr(field, "_tablename", "no_table"), field.name)

    def widget(self, field, vars):
        value = field.formatter(vars.get(field.name))
        error = ''
        readonly = False
        title=''
        control = DIV()
        field_id = self.to_id(field)
        if value and not error:
            if not readonly:
                download_div = DIV()
                url = getattr(field, "download_url", lambda value: "#")(value)
                download_div.append(LABEL("Current Image", _class= "current has-text-primary has-text-centered is-size-5" ))
                
                #image_str = """<div class="has-text-primary has-text-centered is-size-5>Current Image</div>"""
                image_str = """<div class="container has-text-centered" style="width:100%;">"""
                image_str += """<figure class="image is-2by1"><img src="%s"alt="Placeholder image"></figure></div>""" % (url)
            download_div.append(XML(image_str))
            button_str = """<a class="new button is-success is-light is-small is-rounded" href=%s> Download </a>&nbsp""" % (url)
            download_div.append(XML(button_str))
            if not readonly:
                download_div.append(
                    INPUT(
                        _type="checkbox",
                        _value="ON",
                        _name="_delete_" + field.name,
                        _title=title,
                        _class="new"
                        
                        
                    )
                )
                test ="""&nbsp """
                download_div.append(XML(test))
                download_div.append(LABEL("Check to Remove", _class=" new has-text-danger"))
                download_div.append(XML("</div>"))
                

            control.append(download_div)
        upload_div = DIV()
        
        control.append(
                    LABEL(
                        "Select a New Image", _class="new has-text-primary is-size-5"
                    )
                )
        form_str = """<div class="new container">"""
        form_str += """<input class="dropify" type="file" id="%s" name="%s" data-height="320px">""" % (field_id, field.name)
    
        control.append(XML(form_str)) 
        control.append(
            SCRIPT(
                """ $('.dropify').dropify();
                """ )
        )    
        return control
