""" LilGit Parser """

import glob, json, re, os

import parser

from tornado import gen, web

from notebook.base.handlers import APIHandler


class ParseHandler(APIHandler):
    """
    A handler that runs a custom parser for lilGit on the server.
    """
    @web.authenticated
    @gen.coroutine
    def get(self, text = ''):
        #out = parse(text)
        self.finish('PARSER READY')
