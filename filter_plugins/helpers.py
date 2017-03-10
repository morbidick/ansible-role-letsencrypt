def default_from_list(value, default_list):
    '''
    return the first array element or if its a string, the string itself
    '''
    from jinja2.runtime import Undefined

    if not isinstance(value, Undefined):
        return value
    if isinstance(default_list, basestring):
        return default_list
    elif isinstance(default_list, list):
        return default_list[0]
    else:
        raise ValueError('The list parameter is neither a string nor a list')

def pluck_key(input_list, key):
    '''
    extract input_list[key] for every item x in the list
    '''
    temp = {}

    for k,v in input_list.iteritems():
        if key in v:
            temp[k] = v[key]

    return temp

    #return {{k: v[key]} for k,v in input_list.iteritems()}

class FilterModule(object):
    '''
    custom jinja2 filters
    '''

    def filters(self):
        return {
            'default_from_list': default_from_list,
            'pluck_key': pluck_key
        }
