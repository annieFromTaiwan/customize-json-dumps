import json

# Shorten version of @martineau's answer
def test1():
    class NoIndent(object):
        def __init__(self, value):
            self.value = value
        def __repr__(self):
            return repr(self.value).strip('"')

    data_structure = { 
        'layer1': {
            'layer2': {
                'layer3_1': NoIndent([{"x":1,"y":7}, {"x":0,"y":4},
                                      {"x":5,"y":3}, {"x":6,"y":9}]),
                'layer3_2': 'string'
            }   
        }   
    }   

    return json.dumps(data_structure, default=repr, indent=2)


# Modified version of `test1`, to remove the human-add `NoIndent` when declaring data
def test2():
    class NoIndent(object):
        def __init__(self, value):
            self.value = value
        def __repr__(self):
            return repr(self.value)

    def list_to_noindent(json_obj):
        if isinstance(json_obj, list):
            after_process =  [ list_to_noindent(elem) for elem in json_obj ]
            return NoIndent(after_process)
        elif isinstance(json_obj, dict):
            after_process =  { key: list_to_noindent(json_obj[key]) for key in json_obj }
            return after_process
        else:
            return json_obj

    data_structure = { 
        'layer1': {
            'layer2': {
                'layer3_1': [{"x":1,"y":7}, {"x":0,"y":4},
                             {"x":5,"y":3}, {"x":6,"y":9}],
                'layer3_2': 'string'
            }   
        }   
    }   
    return json.dumps( list_to_noindent(data_structure), default=repr, indent=2 )


# J.F. Sebastian's solution
def test3():
    import uuid

    class NoIndent(object):
        def __init__(self, value):
            self.value = value

    class NoIndentEncoder(json.JSONEncoder):
        def __init__(self, *args, **kwargs):
            super(NoIndentEncoder, self).__init__(*args, **kwargs)
            self.kwargs = dict(kwargs)
            del self.kwargs['indent']   # for the `json.dumps` inside `default()`, see `test5()`
            self._replacement_map = {}

        def default(self, o): 
            if isinstance(o, NoIndent):
                key = uuid.uuid4().hex
                self._replacement_map[key] = json.dumps(o.value, **self.kwargs)
                return "@@%s@@" % (key,)
            else:
                return super(NoIndentEncoder, self).default(o)

        def encode(self, o):
            result = super(NoIndentEncoder, self).encode(o)
            for k, v in self._replacement_map.iteritems():
                result = result.replace('"@@%s@@"' % (k,), v)
            return result

    data_structure = {
        'layer1': {
            'layer2': {
                'layer3_1': NoIndent([{"x":1,"y":7}, {"x":0,"y":4},
                                      {"x":5,"y":3}, {"x":6,"y":9}]),
                'layer3_2': 'string'
            }
        }
    }

    return json.dumps(data_structure, cls=NoIndentEncoder, indent=2)


# playing with test3, comment out 2 lines
def test4():
    import uuid

    class NoIndent(object):
        def __init__(self, value):
            self.value = value

    class NoIndentEncoder(json.JSONEncoder):
        def __init__(self, *args, **kwargs):
            super(NoIndentEncoder, self).__init__(*args, **kwargs)
            self.kwargs = dict(kwargs)
            del self.kwargs['indent']
            self._replacement_map = {}

        def default(self, o):
            if isinstance(o, NoIndent):
                key = uuid.uuid4().hex
                self._replacement_map[key] = json.dumps(o.value, **self.kwargs)
                return "@@%s@@" % (key,)
            else:
                return super(NoIndentEncoder, self).default(o)

        def encode(self, o):
            result = super(NoIndentEncoder, self).encode(o)
            #for k, v in self._replacement_map.iteritems():
            #    result = result.replace('"@@%s@@"' % (k,), v)
            return result

    data_structure = {
        'layer1': {
            'layer2': {
                'layer3_1': NoIndent([{"x":1,"y":7}, {"x":0,"y":4},
                                      {"x":5,"y":3}, {"x":6,"y":9}]),
                'layer3_2': 'string'
            }
        }
    }

    return json.dumps(data_structure, cls=NoIndentEncoder, indent=2)


# playing with test3, comment out 1 lines
def test5():
    import uuid

    class NoIndent(object):
        def __init__(self, value):
            self.value = value

    class NoIndentEncoder(json.JSONEncoder):
        def __init__(self, *args, **kwargs):
            super(NoIndentEncoder, self).__init__(*args, **kwargs)
            self.kwargs = dict(kwargs)
            #del self.kwargs['indent']
            self._replacement_map = {}

        def default(self, o):
            if isinstance(o, NoIndent):
                key = uuid.uuid4().hex
                self._replacement_map[key] = json.dumps(o.value, **self.kwargs)
                return "@@%s@@" % (key,)
            else:
                return super(NoIndentEncoder, self).default(o)

        def encode(self, o):
            result = super(NoIndentEncoder, self).encode(o)
            for k, v in self._replacement_map.iteritems():
                result = result.replace('"@@%s@@"' % (k,), v)
            return result

    data_structure = {
        'layer1': {
            'layer2': {
                'layer3_1': NoIndent([{"x":1,"y":7}, {"x":0,"y":4},
                                      {"x":5,"y":3}, {"x":6,"y":9}]),
                'layer3_2': 'string'
            }
        }
    }

    return json.dumps(data_structure, cls=NoIndentEncoder, indent=2)


# J.F. Sebastian's solution + my recursive `list to NoIndent`
def test6():
    import uuid

    class NoIndent(object):
        def __init__(self, value):
            self.value = value

    class NoIndentEncoder(json.JSONEncoder):
        def __init__(self, *args, **kwargs):
            super(NoIndentEncoder, self).__init__(*args, **kwargs)
            self.kwargs = dict(kwargs)
            del self.kwargs['indent']   # for the `json.dumps` inside `default()`, see `test5()`
            self._replacement_map = {}

        def default(self, o):
            if isinstance(o, NoIndent):
                key = uuid.uuid4().hex
                self._replacement_map[key] = json.dumps(o.value, **self.kwargs)
                return "@@%s@@" % (key,)
            else:
                return super(NoIndentEncoder, self).default(o)

        def encode(self, o):
            result = super(NoIndentEncoder, self).encode(o)
            for k, v in self._replacement_map.iteritems():
                result = result.replace('"@@%s@@"' % (k,), v)
            return result

    def list_to_noindent(json_obj):
        if isinstance(json_obj, list):
            after_process =  [ list_to_noindent(elem) for elem in json_obj ]
            return NoIndent(after_process)
        elif isinstance(json_obj, dict):
            after_process =  { key: list_to_noindent(json_obj[key]) for key in json_obj }
            return after_process
        else:
            return json_obj

    data_structure = {
        'layer1': {
            'layer2': {
                'layer3_1': [{"x":1,"y":7}, {"x":0,"y":4},
                             {"x":5,"y":3}, {"x":6,"y":9}],
                'layer3_2': 'string'
            }
        }
    }

    data_structure = list_to_noindent(data_structure)

    return json.dumps(data_structure, cls=NoIndentEncoder, indent=2)


#############################

if __name__ == "__main__":

    orig_data_structure = {
        'layer1': {
            'layer2': {
                'layer3_1': [{"x":1,"y":7}, {"x":0,"y":4},
                             {"x":5,"y":3}, {"x":6,"y":9}],
                'layer3_2': 'string'
            }
        }
    }

    versions = [ test1, test2, test3, test4, test5, test6 ]

    for func in versions:
        print "\n" + func.__name__.center(50, "-")

        result = func()

        print result
        print "Check:", json.loads(result) == orig_data_structure


