#!/usr/bin/env python3
# encoding: utf-8


class HachiModel():
    """Hachi Model for query checking

    :arg plugins (list): list of plugins this Hachi Model has, each element should be a Plugin instance

    """
    def __init__(self, plugins=[]):
        self.plugins = plugins
        self.res = {}

    def check(self, query):
        """check method for a Hachi Model instance

        :arg query (str): query
        :return dict: {plugin_name: plugin_res}

        """
        for plugin in self.plugins:
            self.res[plugin.name] = plugin.check(query)

        return self.res

