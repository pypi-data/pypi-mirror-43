#!/usr/bin/env python3
# encoding: utf-8

import thulac
import tempfile
from cnprep import Extractor
from collections import Counter
from .utils import plugin_name_generator


class BlacklistPlugin():
    """
    Initialize blacklist plugin parameters:

    :arg words_list (list): word list
    :arg name (str): plugin name, default is blacklist_xxxx(will be generated randomly)

    """
    def __init__(self, words_list=[], name="blacklist_"):
        self.sensitive_words = words_list
        self.name = name + plugin_name_generator()
        self.res = {
            "nigger_word":{},
            "nigger_char":{},
        }
        self.segmentor = self._build_segmentor(self.sensitive_words)


    def _build_segmentor(self, dict_words):
        """
        Build user dict from dict words(sensitive_words) for thulac instance
        """
        user_dict_str = "\n".join(dict_words)
        t = tempfile.TemporaryFile()
        t.write(bytes(user_dict_str, "utf-8"))
        t.seek(0)
        segmentor = thulac.thulac(seg_only=True, user_dict=t.name, deli="\t")
        return segmentor



    def __str__(self):
        """
        Simple summary

        :return (str): simple summary of plugin instance
        """
        summary = ("<PLUGIN>: {},\n<TYPE>: {},\n<WORD COUNT>: {}".format(
            self.name,
            self.__class__.__name__,
            len(self.sensitive_words)))
        return summary


    def check(self, query):
        """
        Blacklist plugin check method

        :arg query (str): input string for nigger checking

        :return (dict): blacklist check result, basicly it contains two dict on word level and char level separately
        """
        self._nigger_check(query)
        return self.res


    def _nigger_check(self, query):
        nigger_word = []
        query_words = self.segmentor.cut(query, text=True).split()
        for word in query_words:
            if word in self.sensitive_words:
                nigger_word.append(word)
        self.res["nigger_word"] = dict(Counter(nigger_word))

        nigger_char = {}
        for word in self.sensitive_words:
            if query.count(word) != 0:
                nigger_char[word] = query.count(word)
        self.res["nigger_char"] = nigger_char


class PatternPlugin():
    """Pattern Plugin implemented with powerful regex

    :arg cnprep_args (list): pattern will be extracted, default is ["email", "telephone", "url", "QQ", "wechat"]
    :arg name (str): plugin name, default is pattern_xxxx(will be generated randomly)
    """

    def __init__(self,
                 cnprep_args=["email", "telephone", "url", "QQ", "wechat"],
                 name="pattern_"):
        self.cnprep_args = cnprep_args
        self.cnprep_extractor = Extractor(args=cnprep_args,
                                          limit=5)
        self.name = name + plugin_name_generator()
        self.res = {}

    def __str__(self):
        summary = ("<PLUGIN>: {},\n<TYPE>: {},\n<PATTERN>: {}".format(
            self.name,
            self.__class__.__name__,
            ",".join(self.cnprep_args)))
        return summary

    def check(self, query):
        """
        pattern plugin check method

        :arg query (str): input string for pattern checking

        :return dict: pattern check result
        """
        self._cnprep_check(query)
        return self.res

    def _cnprep_check(self, query):
        self.res["special_pattern"] = self.cnprep_extractor.extract(query)

