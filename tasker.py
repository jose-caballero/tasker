#!/usr/bin/env python 

from ConfigParser import SafeConfigParser
import jinja2

templatestr="""
#!/bin/bash 

# -----------------------------------------------

"""


class Function(object):
    def __init__(self, conf, sect):
        self.conf = conf
        self.sect = sect
        self.main_code = self._create_main_code()
        self.funct_code = self._create_funct_code()
        #print self.funct_code

    def _create_main_code(self):

        code = "f_%s\n" %self.sect
        code += "rc=$?\n"
        code += "if [ $rc -ne 0 ]; then\n"
        code += "   exit $rc\n"
        code += "fi\n"
        return code

    def _create_funct_code(self):

        code = "f_%s(){\n" %self.sect
        for line in self.conf.get(self.sect, 'code').split('\n'):
            if line.strip() != "":
                code += "   %s\n" %line
        code += "}\n"
        return code
    


class WholeCode(object):

    def __init__(self, conf):
        self.conf = conf
        self.main_list_functions = self._analyze_main()
        self.functions = self._create_list_functions()
        self.code = self._build()

    def _analyze_main(self):
        main = self.conf.get('main', 'next')
        return [x.strip() for x in main.split(',')]

    def _create_list_functions(self):
        l_functions = []
        for func in self.main_list_functions:
            f = self._create_function(func)
            l_functions.append(f)
        return l_functions

    def _create_function(self, func):
        fun = Function(self.conf, func)
        return fun

    def _build(self):
        template = jinja2.Template(templatestr)
        code = template.render()
        return code





conf = SafeConfigParser()
conf.readfp(open("conf"))
code = WholeCode(conf)
print code.code




