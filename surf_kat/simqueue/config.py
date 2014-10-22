from django.template import loader, Context


def generate_config(simulation):
    """
    generate a config file from a simulation object
    """
    t = loader.get_template('simqueue/config.txt')
    return t.render(Context({'object': simulation}))