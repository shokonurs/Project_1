from django.template.defaulttags import register
from django import template



class SetVarNode(template.Node):
    def __init__(self, var_name, var_value):
        self.var_name=var_name
        self.var_value=var_value

    def render(self, context):
        try:
            value=template.Variable(self.var_value).resolve(context)
       
        except template.VariableDoesNotExist:
            value=""
        context[self.var_name]=value


@register.tag(name='set')
def set_var(parser, token):

    parts=token.split_contents()
    if len(parts) <3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments")
   
    return SetVarNode(parts[1], parts[3])



