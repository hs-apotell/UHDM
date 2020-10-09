# Copyright 2019-2020 Alain Dargelas
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os


_cwd = os.path.dirname(os.path.realpath(__file__))

_models_dirname = 'model'
_template_dirname = 'templates'
_sources_dirname = 'src.py'
_headers_dirname = 'headers.py'
_debug = False


def debug_enabled():
    return _debug


def set_cwd(dirpath):
    global _cwd
    _cwd = dirpath

    headers_dirpath = os.path.join(_cwd, _headers_dirname)
    if not os.path.exists(headers_dirpath):
        os.mkdir(headers_dirpath)

    sources_dirpath = os.path.join(_cwd, _sources_dirname)
    if not os.path.exists(sources_dirpath):
        os.mkdir(sources_dirpath)


def get_template_filepath(filename):
    return os.path.join(_cwd, _template_dirname, filename)


def get_header_filepath(filename):
    return os.path.join(_cwd, _headers_dirname, filename)


def get_source_filepath(filename):
    return os.path.join(_cwd, _sources_dirname, filename)


def get_modellist_filepath():
    return os.path.join(_cwd, _models_dirname, 'models.lst')