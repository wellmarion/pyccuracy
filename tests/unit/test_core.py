#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from os.path import join, abspath, dirname
from pmock import *

from pyccuracy.core import PyccuracyCore
from pyccuracy.common import Settings

class SettingsMock(Mock):
    def __getattr__(self, attr):
        if attr == 'pages_dir':
            return '/pages/dir/'
        if attr == 'custom_actions_dir':
            return '/custom/actions/dir/'

        if attr == 'base_url':
            return "http://localhost"
        return super(SettingsMock, self).__getattribute__(attr)

def test_pyccuracy_core_instantiation():
    class MyParser:
        pass

    class MyRunner:
        pass

    pc = PyccuracyCore(MyParser(), MyRunner())
    assert isinstance(pc, PyccuracyCore)
    assert isinstance(pc.parser, MyParser)
    assert isinstance(pc.runner, MyRunner)

def test_pyccuracy_core_run_tests():
    context_mock = Mock()
    context_mock.browser_driver = Mock()
    context_mock.settings = SettingsMock()

    files = ["/some/weird/file.py"]
    fso_mock = Mock()
    fso_mock.expects(once()).add_to_import(eq(context_mock.settings.pages_dir))
    fso_mock.expects(once()).locate(eq(context_mock.settings.pages_dir), eq('*.py')).will(return_value(files))
    fso_mock.expects(once()).import_file(eq('file'))
    fso_mock.expects(once()).remove_from_import()

    context_mock.browser_driver.expects(once()).method('start_test')
    context_mock.browser_driver.expects(once()).method('stop_test')

    results_mock = Mock()
    suite_mock = Mock()

    runner_mock = Mock()
    parser_mock = Mock()

    parser_mock.expects(once()).method('get_stories').will(return_value(suite_mock))
    runner_mock.expects(once()).method('run_stories').will(return_value(results_mock))

    results_mock.expects(once()).summary_for(eq('en-us')).will(return_value('my results'))
    pc = PyccuracyCore(parser_mock, runner_mock)
    assert pc.run_tests(should_throw=False, context=context_mock, fso=fso_mock) == results_mock

    parser_mock.verify()
    runner_mock.verify()
    context_mock.verify()
    results_mock.verify()
    suite_mock.verify()
