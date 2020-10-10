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

import config
import file_utils
import loader

import classes_h
import uhdm_h


def _main():
    config.set_cwd(r'D:\Projects\Davenche\UHDM')

    models = loader.load_models()
    classes_h.generate(models)
    uhdm_h.generate(models)

    # BaseClass.h
    file_utils.copy_file_if_changed(config.get_template_filepath('BaseClass.h'), config.get_header_filepath('BaseClass.h'))

    # SymbolFactory.h/cpp
    file_utils.copy_file_if_changed(config.get_template_filepath('SymbolFactory.h'), config.get_header_filepath('SymbolFactory.h'))
    file_utils.copy_file_if_changed(config.get_template_filepath('SymbolFactory.cpp'), config.get_source_filepath('SymbolFactory.cpp'))

    # vpi_uhdm.h
    file_utils.copy_file_if_changed(config.get_template_filepath('vpi_uhdm.h'), config.get_header_filepath('vpi_uhdm.h'))

    # vpi_visitor.h
    file_utils.copy_file_if_changed(config.get_template_filepath('vpi_visitor.h'), config.get_header_filepath('vpi_visitor.h'))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(_main())
