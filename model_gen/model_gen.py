#!/usr/bin/tclsh
# -*- mode: python; c-basic-offset: 4; indent-tabs-mode: 4; -*-
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
import sys
import re
import pprint
from collections import OrderedDict

import file_utils


_cwd = os.path.dirname(os.path.realpath(__file__))

DEBUG = 0

OBJECTID = 2000 # Above sv_vpi_user.h and vhpi_user.h ranges.
ID = dict()
DEFINE_ID = dict()
DEFINE_NAME = dict()

SHORT_VISITOR_LIST = {
    "class_obj",
    "assertion",
    "immediate_assert",
    "tchk_term",
    "primitive",
    "clocked_property",
    "enum_const",
    "attribute",
    "task_call",
    "parameter",
    "program_array",
    "chandle_var",
    "return_stmt",
    "switch_array",
    "cont_assign",
    "while_stmt",
    "property_typespec",
    "fork_stmt",
    "repeat",
    "assert_stmt",
    "logic_typespec",
    "property_inst",
    "gen_var",
    "bit_typespec",
    "packed_array_net",
    "byte_var",
    "break_stmt",
    "sys_func_call",
    "typespec",
    "modport",
    "enum_var",
    "event_typespec",
    "named_event",
    "int_typespec",
    "forever_stmt",
    "interface_tf_decl",
    "final_stmt",
    "repeat_control",
    "packed_array_typespec",
    "port_bit",
    "short_real_var",
    "let_decl",
    "immediate_assume",
    "union_typespec",
    "param_assign",
    "integer_var",
    "method_func_call",
    "user_systf",
    "prim_term",
    "string_var",
    "property_spec",
    "delay_control",
    "expect_stmt",
    "operation",
    "class_typespec",
    "short_int_var",
    "event_control",
    "case_item",
    "gen_scope",
    "path_term",
    "property_decl",
    "assign_stmt",
    "tf_call",
    "sequence_typespec",
    "net_bit",
    "udp_defn",
    "short_int_typespec",
    "function",
    "sequence_inst",
    "delay_term",
    "named_fork",
    "time_var",
    "byte_typespec",
    "ports",
    "distribution",
    "initial",
    "string_typespec",
    "int_var",
    "do_while",
    "case_stmt",
    "sys_task_call",
    "package",
    "mod_path",
    "real_var",
    "atomic_stmt",
    "if_stmt",
    "virtual_interface_var",
    "if_else",
    "foreach_stmt",
    "alias_stmt",
    "release",
    "type_parameter",
    "class_defn",
    "null_stmt",
    "time_typespec",
    "enum_net",
    "module_array",
    "continue_stmt",
    "method_task_call",
    "task_func",
    "packed_array_var",
    "for_stmt",
    "func_call",
    "def_param",
    "array_var",
    "force",
    "scope",
    "typespecs",
    "sequence_decl",
    "named_begin",
    "spec_param",
    "instance_array",
    "integer_net",
    "reg_array",
    "constraint",
    "interface_typespec",
    "begin",
    "void_typespec",
    "cont_assign_bit",
    "class_var",
    "deassign",
    "udp_array",
    "gate_array",
    "unsupported_expr",
    "real_typespec",
    "program",
    "unsupported_stmt",
    "union_var",
    "always",
    "gen_scope_array",
    "integer_typespec",
    "tchk",
    "long_int_var",
    "array_typespec",
    "task",
    "named_event_array",
    "clocking_block",
    "time_net",
    "multiclock_sequence_expr",
    "concurrent_assertions",
    "immediate_cover",
    "long_int_typespec",
    "short_real_typespec",
    "primitive_array",
    "interface_array",
    "io_decl",
    "var_bit",
    "bit_var",
    "design"
}

def log(arg):
    if DEBUG == 1:
        print(arg)


def lognnl(arg):
    if DEBUG == 1:
        print(arg, end="")


def _format_headers(class_names):
    return '\n'.join([ f'#include "headers/{class_name}.h"' for class_name in class_names ])


def _parse_vpi_user_defines():
    dirpath = os.path.join(_cwd, 'include', 'vpi_user.h')
    with open(dirpath, "r") as fid:
        for line in fid:
            # Most defines are followed by comment on the same line and so the pattern
            # cannot terminate at EOL.
            # defines should be followed by either a space, a forward slash (start of comment) or newline (EOL).
            # This is done to avoid incorrectly parsing hexadecimal numbers with 0 value
            #   -- #define vpiABC 0 /* This should be valid */
            #   -- #define vpiDEF 0x123 /* This shouldn't be valid */
            m = re.match('^#\s*define\s+(?P<name>vpi\w+)\s+(?P<value>\d+)(\ |\/|$)', line)
            if m:
                ID[m.group('name')] = m.group('value')


def _define_type(name, vpiType, append=True):
    global ID, OBJECTID, DEFINE_ID, DEFINE_NAME
    id = ''
    define = None
    if name in ID:
        id = ID[name]
        if append:
            define = f'{name} = {id},'
            DEFINE_ID[id] = name
            DEFINE_NAME[name] = id
    elif vpiType and vpiType in ID:
        id = ID[vpiType]
    else:
        id = OBJECTID
        OBJECTID += 1
        ID[name] = id
        if append:
            define = f'{name} = {id},'
            DEFINE_ID[id] = name
            DEFINE_NAME[name] = id

    return (id, define)


def _parse_modeldefs(modeldef_list_filepath):
    modeldef_dirpath = os.path.dirname(modeldef_list_filepath)

    modeldefs = OrderedDict()
    uhdm_types = OrderedDict()
    with open(modeldef_list_filepath, 'r+t') as strm1:
        for modeldef_filename in strm1:
            modeldef_filename = modeldef_filename.strip()
            if modeldef_filename and not modeldef_filename.startswith('#'):
                modeldef_filepath = os.path.join(modeldef_dirpath, modeldef_filename)
                top_level_def = None
                with open(modeldef_filepath, 'r+t') as strm2:
                    lineNo = 0
                    current_def = None
                    for line in strm2:
                        lineNo += 1

                        # Strip out any comment
                        pos = line.find('#')
                        if pos >= 0:
                          line = line[:pos]

                        line = line.strip()
                        if not line or line.startswith('#'): # empty line or comment
                            continue

                        m = re.match('^[-]*\s*(?P<type>\w+)\s*:\s*(?P<name>.+)$', line)
                        if not m:
                          print(f'Failed to parse {modeldef_filename}:{lineNo}')
                          continue  # TODO(HS): This should be an error!

                        type = m.group('type').strip()
                        name = m.group('name').strip()
                        if type in [ 'obj_def', 'class_def', 'group_def' ]:
                            id, define = _define_type(name, None, False)

                            top_level_def = OrderedDict([
                              ('id', id),
                              ('name', name),
                              ('type', type),
                              ('extends', None),
                              ('card', None),
                              ('property', OrderedDict()),
                              ('class', OrderedDict()),
                              ('class_ref', OrderedDict()),
                              ('obj_ref', OrderedDict()),
                              ('group_ref', OrderedDict()),
                              ('subclasses', set()),
                            ])
                            current_def = top_level_def
                            modeldefs[name] = top_level_def

                        elif type == 'extends':
                            top_level_def['extends'] = name

                        elif type in ['property', 'class_ref', 'obj_ref', 'group_ref', 'class']:
                            if name not in top_level_def[type]:
                                top_level_def[type][name] = OrderedDict()
                            current_def = top_level_def[type][name]

                        elif type in ['type', 'card', 'vpi', 'vpi_obj', 'name']:
                            current_def[type] = name

                            if type == 'card':
                                id, define = _define_type(current_def.get('name'), current_def.get('vpi'), False)
                                current_def['id'] = id
                                if define:
                                    uhdm_types[define] = None

                        else:
                            print(f'Unknown type {type}')

    for name, value in modeldefs.items():
        baseclass = value['extends']
        while baseclass:
            modeldefs[baseclass]['subclasses'].add(name)
            baseclass = modeldefs[baseclass]['extends']

    return modeldefs, uhdm_types


def _print_method_declarations(classname, type, vpi, card, real_type=""):
    content = []
    if type in ['string', 'value', 'delay']:
        type = 'std::string'
    if vpi == 'uhdmType':
        type = 'UHDM_OBJECT_TYPE'

    final = ''
    virtual = ''
    if vpi in ['vpiParent', 'uhdmParentType', 'uhdmType', 'vpiLineNo', 'vpiFile']:
        final = ' final'
        virtual = 'virtual '

    check = ''
    if type == 'any':
        check = f'if (!{real_type}GroupCompliant(data)) return false;'

    Vpi_ = vpi[:1].upper() + vpi[1:]

    if card == '1':
        pointer = ''
        const = ''
        if type not in ['unsigned int', 'int', 'bool', 'std::string']:
            pointer = '*'
            const = 'const '

        if type == 'std::string':
            content.append(f'    {virtual}bool {Vpi_}(const {type}{pointer}& data){final};')
            if vpi == 'vpiFullName':
                content.append(f'    {virtual}const {type}{pointer}& {Vpi_}() const{final};')
            else:
                content.append(f'    {virtual}const {type}{pointer}& {Vpi_}() const{final};')
        else:
            content.append(f'    {virtual}{const}{type}{pointer} {Vpi_}() const {final} {{ return {vpi}_; }}')
            if vpi == 'vpiParent':
                content.append(f'    virtual bool {Vpi_}({type}{pointer} data) final {{ {check} {vpi}_ = data; if (data) uhdmParentType_ = data->UhdmType(); return true; }}')
            else:
                content.append(f'    {virtual}bool {Vpi_}({type}{pointer} data) {final} {{ {check} {vpi}_ = data; return true; }}')
    elif card == 'any':
        content.append(f'    VectorOf{type}* {Vpi_}() const {{ return {vpi}_; }}')
        content.append(f'    bool {Vpi_}(VectorOf{type}* data) {{ {check} {vpi}_ = data; return true; }}')

    return content


def _print_method_definitions(classname, type, vpi, card, real_type=""):
    content = []
    if type in ['string', 'value', 'delay']:
        type = 'std::string'
    if vpi == 'uhdmType':
        type = 'UHDM_OBJECT_TYPE'

    final = ''
    virtual = ''
    if vpi in ['vpiParent', 'uhdmParentType', 'uhdmType', 'vpiLineNo', 'vpiFile']:
        final = ' final'
        virtual = 'virtual '

    check = ''
    if type == 'any':
        check = f'if (!{real_type}GroupCompliant(data)) return false;'

    Vpi_ = vpi[:1].upper() + vpi[1:]

    if card == '1':
        pointer = ''
        const = ''
        if type not in ['unsigned int', 'int', 'bool', 'std::string']:
            pointer = '*'
            const = 'const '

        if type == 'std::string':
            if vpi == 'vpiFullName':
                content.append(f'const {type}{pointer} &{classname}::{Vpi_}() const {{')
                content.append(f'    if ({vpi}_) {{')
                content.append(f'        return serializer_->symbolMaker.GetSymbol({vpi}_);')
                content.append( '    } else {')
                content.append( '    std::vector<std::string> names;')
                content.append( '    const BaseClass* parent = this;')
                content.append( '    bool package = false;')
                content.append( '    while (parent) {')
                content.append( '        const BaseClass* actual_parent = parent->VpiParent();')
                content.append( '        if (parent->UhdmType() == uhdmdesign) break;')
                content.append( '        if (parent->UhdmType() == uhdmpackage) package = true;')
                content.append( '        const std::string &name = (!parent->VpiName().empty()) ? parent->VpiName() : parent->VpiDefName();')
                content.append( '        bool skip_name = (actual_parent != nullptr) && (actual_parent->UhdmType() == uhdmref_obj);')
                content.append( '        if ((!name.empty()) && (!skip_name))')
                content.append( '        names.push_back(name);')
                content.append( '        parent = parent->VpiParent();')
                content.append( '    }')
                content.append( '    std::string fullName;')
                content.append( '    if (names.size()) {')
                content.append( '        unsigned int index = names.size() - 1;')
                content.append( '        while (1) {{')
                content.append( '            fullName += names[index];')
                content.append( '            if (index > 0) fullName += (package) ? \'::\' : \'.\';')
                content.append( '            if (index == 0) break;')
                content.append( '            index--;')
                content.append( '        }')
                content.append( '    }')
                content.append(f'    (({classname}*)this)->VpiFullName(fullName);')
                content.append(f'    return serializer_->symbolMaker.GetSymbol({vpi}_);')
                content.append('    }')
                content.append('}')
            else:
                content.append(f'const {type}{pointer} &{classname}::{Vpi_}() const {{ return serializer_->symbolMaker.GetSymbol({vpi}_); }}')
            content.append(f'bool {classname}::{Vpi_}(const {type}{pointer} &data) {{ {vpi}_ = serializer_->symbolMaker.Make(data); return true; }}')

    return content


def _print_capnp_schema(type, vpi, card):
    mapping = {
      'string': 'UInt64',
      'unsigned int': 'UInt64',
      'int': 'Int64',
      'any': 'Int64',
      'bool': 'Bool',
      'value': 'UInt64',
      'delay': 'UInt64',
    }
    type = mapping.get(type, type)
    if card == '1':
        return (vpi, type)
    elif card == 'any':
        return (vpi, f'List({type})')
    else:
        return (None, None)


def _print_members(type, vpi, card):
    content = []

    if type in ['string', 'value', 'delay']:
        type = 'std::string'

    if card == '1':
        pointer = ''
        default_assignment = '0'
        if type not in ['unsigned int', 'int', 'bool', 'std::string']:
            pointer = '*'
            default_assignment = 'nullptr'

        if type == 'std::string':
            content.append(f'    SymbolFactory::ID {vpi}_ = 0;')
        else:
            content.append(f'    {type}{pointer} {vpi}_ = {default_assignment};')

    elif card == 'any':
        content.append(f'    VectorOf{type}* {vpi}_ = nullptr;')

    return content


def _print_iterate_body(name, classname, vpi, card):
    content = []
    if card == 'any':
        Name_ = name[:1].upper() + name[1:]
        content.append(f'if (handle->type == uhdm{classname} && type == {vpi}) {{')
        content.append(f'    if ((({classname}*)(object))->{Name_}())')
        content.append(f'        return NewHandle(uhdm{name}, (({classname}*)(object))->{Name_}());')
        content.append( '    else return 0;')
        content.append( '}')
        content.extend(_print_vpi_visitor(classname, vpi, card))
    return content


def _print_get_handle_by_name_body(name, classname, vpi, card):
    content = []
    Name_ = name[:1].upper() + name[1:]
    if card == '1':
        content.append(f'  if (handle->type == uhdm{classname}) {{')
        content.append(f'    const {classname}* const obj = (const {classname}*)(object);')
        content.append(f'    if (obj->{Name_}() && obj->{Name_}()->VpiName() == name) {{')
        content.append(f'      return NewVpiHandle(obj->{Name_}());')
        content.append( '    }')
        content.append( '  }')
    else:
        content.append(f'  if (handle->type == uhdm{classname}) {{')
        content.append(f'  const {classname}* const obj_parent = (const {classname}*)(object);')
        content.append(f'  if (obj_parent->{Name_}()) {{')
        content.append(f'    for (const BaseClass *obj : *obj_parent->{Name_}())')
        content.append(f'    if (obj->VpiName() == name) return NewVpiHandle(obj);')
        content.append( '    }')
        content.append( '  }')
    return content


def _print_get_body_prefix(classname):
    return [
      f'  if (handle->type == uhdm{classname}) {{',
       '      switch (property) {'
    ]


def _print_get_body_suffix():
    return [ '    }', '}' ]


def _print_get_body(classname, type, vpi, card):
    if vpi in ['vpiType', 'vpiLineNo']:  # These are already handled by base class
        return []

    content = []
    if (card == '1') and (type not in ['string', 'value', 'delay']):
        content.append(f'case {vpi}: return ((const {classname}*)(obj))->{vpi[:1].upper() + vpi[1:]}();')

    return content


def _print_get_value_body(classname, type, vpi, card):
    content = []
    if (card == '1') and (type == 'value'):
        content.append(f'if (handle->type == uhdm{classname}) {{')
        content.append(f'  const s_vpi_value* v = String2VpiValue((({classname}*)(obj))->VpiValue());')
        content.append(f'  if (v) {{')
        content.append(f'    *value_p = *v;')
        content.append( '  }')
        content.append( '}')

    return content


def _print_get_delay_body(classname, type, vpi, card):
    content = []
    if (card == '1') and (type == "delay"):
        content.append(f'  if (handle->type == uhdm{classname}) {{')
        content.append(f'    const s_vpi_delay* v = String2VpiDelays((({classname}*)(obj))->VpiDelay());')
        content.append( '    if (v) {')
        content.append( '      *delay_p = *v;')
        content.append( '    }}')
        content.append( '  }')
    return content


def _print_get_handle_body(classname, type, vpi, object, card):
    if type == 'BaseClass':
        type = f'(({classname}*)(object))->UhdmParentType()'

    content = []
    need_casting = not ((vpi == 'vpiParent') and (object == 'vpiParent'))

    if card == '1':
        Object_ = object[:1].upper() + object[1:]
        casted_object1 = f'((BaseClass*)(({classname}*)(object))' if need_casting else '(object'
        casted_object2 = f'(({classname}*)(object))' if need_casting else 'object'
        content.append(f'  if (handle->type == uhdm{classname} && type == {vpi}) {{')
        content.append(f'    if ({casted_object1}->{Object_}()))')
        content.append(f'      return NewHandle({casted_object1}->{Object_}())->UhdmType(), {casted_object2}->{Object_}());')
        content.append( '    else return 0;')
        content.append( '  }')
        content.extend(_print_vpi_visitor(classname, vpi, card))
    return content


def _print_get_str_visitor(classname, type, vpi, card):
    content = []
    if (card == '1') and (type == 'string') and (vpi != 'vpiFile'):
        content.append(f'    if (const char* s = vpi_get_str({vpi}, obj_h))')
        content.append(f'        stream_indent(out, indent) << "|{vpi}:" << s << std::endl;')
    return content


def _print_get_visitor(classname, type, vpi, card):
    content = []
    if vpi == "vpiValue":
        content.append('    s_vpi_value value;')
        content.append('    vpi_get_value(obj_h, &value);')
        content.append('    if (value.format) {')
        content.append('        std::string val = visit_value(&value);')
        content.append('        if (!val.empty()) {')
        content.append('            stream_indent(out, indent) << val;')
        content.append('        }')
        content.append('    }')
    elif vpi == "vpiDelay":
        content.append('    s_vpi_delay delay;')
        content.append('    vpi_get_delays(obj_h, &delay);')
        content.append('    if (delay.da != nullptr) {')
        content.append('        stream_indent(out, indent) << visit_delays(&delay);')
        content.append('    }}')
    elif (card == '1') and (type != "string") and (vpi != "vpiLineNo") and (vpi != "vpiType"):
        content.append(f'    if (const int n = vpi_get({vpi}, obj_h))')
        content.append( '        if (n != -1)')
        content.append(f'            stream_indent(out, indent) << \"|{vpi}:\" << n << std::endl;')
    return content


def _print_get_str_body(classname, type, vpi, card):
    # Already handled by the base class
    content = []
    if vpi in ['vpiFile', 'vpiName', 'vpiDefName']:
        return content

    Vpi_ = vpi[:1].upper() + vpi[1:]
    if (card == '1') and (type == 'string'):
        content.append(f'    if ((handle->type == uhdm{classname}) && (property == {vpi})) {{')
        content.append(f'        const {classname}* const o = (const {classname}*)(obj);')
        if vpi == 'vpiFullName':
            content.append(f'        return (o->{Vpi_}().empty() || o->{Vpi_}() == o->VpiName())')
            content.append( '            ? 0')
            content.append(f'            : (PLI_BYTE8*) o->{Vpi_}().c_str();')
        else:
            content.append(f'        return (PLI_BYTE8*) (o->{Vpi_}().empty() ? 0 : o->{Vpi_}().c_str());')
        content.append( '    }')
    return content


def _print_vpi_listener(classname, vpi, type, card):
    header = []
    any_listener = []
    listener = []

    Classname_ = classname[:1].upper() + classname[1:]
    if card == '0':
        header.append(f'void listen_{classname}(vpiHandle object, UHDM::VpiListener* listener);')

        any_listener.append(f'  case uhdm{classname}:')
        any_listener.append(f'    listen_{classname}(object, listener);')
        any_listener.append( '    break;')

        listener.append(f'void UHDM::listen_{classname}(vpiHandle object, VpiListener* listener) {{')
        listener.append(f'  {classname}* d = ({classname}*) ((const uhdm_handle*)object)->object;')
        listener.append( '  const BaseClass* parent = d->VpiParent();')
        listener.append( '  vpiHandle parent_h = parent ? NewVpiHandle(parent) : 0;')
        listener.append(f'  listener->enter{Classname_}(d, parent, object, parent_h);')
        return (header, any_listener, listener)

    if vpi in ['vpiParent', 'vpiInstance']:
        return  # To prevent infinite loops in visitors as these 2 relations are pointing upward in the tree

    if (vpi in ['vpiModule', 'vpiInterface']) and (card == '1'):
        return  # upward vpiModule, vpiInterface relation (when card == 1, pointing to the parent object) creates loops in visitors

    listener.append('  vpiHandle itr;')

    if card == '1':
        listener.append(f'  itr = vpi_handle({vpi}, object);')
        listener.append( '    if (itr) {')
        listener.append(f'      listen_{type}(itr, listener);')
        listener.append( '      vpi_free_object(itr);')
        listener.append( '    }')
    else:
        listener.append(f'  itr = vpi_iterate({vpi}, object);')
        listener.append( '  if (itr) {')
        listener.append( '    while (vpiHandle obj = vpi_scan(itr) ) {')
        listener.append(f'      listen_{type}(obj, listener);')
        listener.append( '      vpi_free_object(obj);')
        listener.append( '    }')
        listener.append( '    vpi_free_object(itr);')
        listener.append( '  }')

    return (header, any_listener, listener)


def _close_vpi_listener(classname):
    Classname_ = classname[:1].upper() + classname[1:]
    return [
        f'listener->leave{Classname_}(d, parent, object, parent_h);',
         'vpi_release_handle(parent_h);',
         '}'
    ]


def _print_vpi_visitor(classname, vpi, card):
    content = []
    if (vpi == "vpiParent") and (classname != "part_select"):
        return content

    content.append('  vpiHandle itr;')

    if card == '1':
        # Prevent loop in Standard VPI
        if (vpi != 'vpiModule') and (vpi != 'vpiInterface'):
            content.append(f'  itr = vpi_handle({vpi},obj_h);')
            content.append(f'  visit_object(itr, subobject_indent, "{vpi}", visited, out);')
            content.append( '  release_handle(itr);')
    else:
        if classname == 'design':
            content.append('  if (indent == 0) visited->clear();')
        # Prevent loop in Standard VPI
        if vpi != "vpiUse":
            content.append(f'  itr = vpi_iterate({vpi}, obj_h);')
            content.append( '  while (vpiHandle obj = vpi_scan(itr)) {')
            content.append(f'    visit_object(obj, subobject_indent, "{vpi}", visited, out);')
            content.append( '    release_handle(obj);')
            content.append( '  }')
            content.append( '  release_handle(itr);')

    return content


def _make_vpi_name(classname):
    vpiclasstype = f'vpi{classname[:1].upper() + classname[1:]}'

    underscore = False
    vpict = vpiclasstype
    vpiclasstype = ''
    for ch in vpict:
        if ch == '_':
          underscore = True
        elif underscore:
            vpiclasstype += ch.upper()
            underscore = False
        else:
            vpiclasstype += ch

    overrides = {
      'vpiForkStmt': 'vpiFork',
      'vpiForStmt': 'vpiFor',
      'vpiIoDecl': 'vpiIODecl',
      'vpiClockingIoDecl': 'vpiClockingIODecl',
      'vpiTfCall': 'vpiSysTfCall',
      'vpiAtomicStmt': 'vpiStmt',
      'vpiAssertStmt': 'vpiAssert',
      'vpiClockedProperty': 'vpiClockedProp',
      'vpiIfStmt': 'vpiIf',
      'vpiWhileStmt': 'vpiWhile',
      'vpiCaseStmt': 'vpiCase',
      'vpiContinueStmt': 'vpiContinue',
      'vpiBreakStmt': 'vpiBreak',
      'vpiReturnStmt': 'vpiReturn',
      'vpiProcessStmt': 'vpiProcess',
      'vpiForeverStmt': 'vpiForever',
      'vpiConstrForeach': 'vpiConstrForEach',
      'vpiFinalStmt': 'vpiFinal',
      'vpiWaitStmt': 'vpiWait',
      'vpiThreadObj': 'vpiThread',
      'vpiSwitchTran': 'vpiSwitch',
    }

    return overrides.get(vpiclasstype, vpiclasstype)


def _print_scan_body(name, classname, type, card):
    content = []
    if card == 'any':
        content.append(f'  if (handle->type == uhdm{name}) {{')
        content.append(f'    VectorOf{type}* the_vec = (VectorOf{type}*)vect;')
        content.append( '    if (handle->index < the_vec->size()) {')
        content.append( '      uhdm_handle* h = new uhdm_handle(((BaseClass*)the_vec->at(handle->index))->UhdmType(), the_vec->at(handle->index));')
        content.append( '      handle->index++;')
        content.append( '      return (vpiHandle) h;')
        content.append( '    }')
        content.append( '  }')
    return content


members = {}
def _generate_group_checker(model, modeldefs):
    groupname = model.get('name')
    modeltype = model.get('type')

    files = {
        os.path.join(_cwd, 'templates', 'group_header.h'): os.path.join(_cwd, 'headers', f'{groupname}.h'),
        os.path.join(_cwd, 'templates', 'group_header.cpp'): os.path.join(_cwd, 'src', f'{groupname}.cpp'),
    }

    members[groupname] = set()
    for input, output in files.items():
      with open(input, 'r+t') as fid:
          template = fid.read()

      checktype = set()
      for key, value in model.items():
          if key in ['obj_ref', 'class_ref', 'group_ref'] and value:
              for name, content in value.items():
                  members[groupname].add(name)

                  if key == 'group_ref':
                      if name not in members:
                          print(f'ERROR: Group {name} unknown while processing group {groupname}')
                      else:
                          checktype.update([f'(uhdmtype != uhdm{member})' for member in members[name]])
                  else:
                      checktype.add(f'(uhdmtype != uhdm{name})')

                  if key == 'class_ref':
                      subclasses = modeldefs[name]['subclasses']
                      checktype.update([f'(uhdmtype != uhdm{subclass})' for subclass in subclasses])

      prefix = ' ' * 6
      checktype = ' &&\n'.join([ prefix + ct for ct in sorted(checktype) ])
      template = template.replace("<GROUPNAME>", groupname)
      template = template.replace("<UPPER_GROUPNAME>", groupname.upper())
      template = template.replace("<CHECKTYPE>", checktype)
      file_utils.set_content_if_changed(output, template)


def _write_vpi_listener_cpp(listeners, any_listeners):
    template_filepath = os.path.join(_cwd, 'templates', 'vpi_listener.cpp')
    with open(template_filepath, 'r+t') as fid:
        content = fid.read()

    vpi_listeners = '\n'.join([listener for _, class_listener in listeners.items() for listener in class_listener])
    vpi_any_listeners = '\n'.join([listener for _, class_listener in any_listeners.items() for listener in class_listener])

    content = content.replace("<VPI_LISTENERS>", vpi_listeners)
    content = content.replace("<VPI_ANY_LISTENERS>", vpi_any_listeners)

    generated_filepath = os.path.join(_cwd, 'src', 'vpi_listener.cpp')
    return file_utils.set_content_if_changed(generated_filepath, content)


def _write_vpi_listener_h(header):
    template_filepath = os.path.join(_cwd, 'templates', 'vpi_listener.h')
    with open(template_filepath, 'r+t') as fid:
        content = fid.read()

    vpi_listeners_header = '\n'.join([listener for _, class_listener in header.items() for listener in class_listener])
    content = content.replace("<VPI_LISTENERS_HEADER>", vpi_listeners_header)

    generated_filepath = os.path.join(_cwd, 'headers', 'vpi_listener.h')
    return file_utils.set_content_if_changed(generated_filepath, content)


def _write_uhdm_forward_decl(classnames):
    template_filepath = os.path.join(_cwd, 'templates', 'uhdm_forward_decl.h')
    with open(template_filepath, 'r+t') as fid:
        content = fid.read()

    uhdm_forward_decl = '\n'.join([f'class {classname};' for classname in classnames])
    content = content.replace("<UHDM_FORWARD_DECL>", uhdm_forward_decl)

    generated_filepath = os.path.join(_cwd, 'headers', 'uhdm_forward_decl.h')
    return file_utils.set_content_if_changed(generated_filepath, content)


def _write_VpiListener_h(modeldefs):
    methods = []
    for model in modeldefs.values():
        if model['type'] != 'group_def':
            classname = model['name']
            Classname_ = classname[:1].upper() + classname[1:]
            methods.append(f'    virtual void enter{Classname_}(const {classname}* object, const BaseClass* parent, vpiHandle handle, vpiHandle parentHandle) {{ }}')
            methods.append(f'    virtual void leave{Classname_}(const {classname}* object, const BaseClass* parent, vpiHandle handle, vpiHandle parentHandle) {{ }}')
            methods.append('')

    template_filepath = os.path.join(_cwd, 'templates', 'VpiListener.h')
    with open(template_filepath, 'r+t') as fid:
        content = fid.read()

    content = content.replace("<VPI_LISTENER_METHODS>", '\n'.join(methods))

    generated_filepath = os.path.join(_cwd, 'headers', 'VpiListener.h')
    return file_utils.set_content_if_changed(generated_filepath, content)


def _write_vpi_visitor_cpp():
    return

#    for item in SHORT_VISITOR_LIST:
#        filter[item] = 1
#
#    with open(f"{project_path()}/templates/vpi_visitor.cpp", "r") as fid:
#        visitor_cpp = fid.read()
#    vpi_visitor = ""
#    for classname in VISITOR:
#        if (classname in filter):
#            pass
#        vpiName = f"makeVpiName {classname}"
#        relations = ""
#        if classname in visitor_relations:
#            relations = visitor_relations[classname]
#
#        vpi_visitor = f"""  if (objectType == {vpiName}) {{
#            {VISITOR}({classname})
#            {relations}
#                return;
#                }}
#            """
#    visitor_cpp = visitor_cpp.replace("<OBJECT_VISITORS>", vpi_visitor)
#    set_content_if_change(f"{project_path()}/src/vpi_visitor.cpp", visitor_cpp)
#    #todo figureout the error.


def _write_capnp(capnp_schema_all, capnp_root_schema):
    template_filepath = os.path.join(_cwd, 'templates', 'UHDM.capnp')
    with open(template_filepath, 'r+t') as fid:
        capnp_content = fid.read()

    capnp_content = capnp_content.replace("<CAPNP_SCHEMA>", capnp_schema_all)
    capnp_content = capnp_content.replace("<CAPNP_ROOT_SCHEMA>", capnp_root_schema)

    generated_filepath = os.path.join(_cwd, 'src', 'UHDM.capnp')
    return file_utils.set_content_if_changed(generated_filepath, capnp_content)


def _write_uhdm_h(class_names):
    template_filepath = os.path.join(_cwd, 'templates', 'uhdm.h')
    with open(template_filepath, "r+t") as fid:
        content = fid.read()

    content = content.replace("<INCLUDE_FILES>", _format_headers(class_names))

    generated_filepath = os.path.join(_cwd, 'headers', 'uhdm.h')
    return file_utils.set_content_if_changed(generated_filepath, content)


def _write_uhdm_types_h(uhdm_types):
    template_filepath = os.path.join(_cwd, 'templates', 'uhdm_types.h')
    with open(template_filepath, 'r+t') as fid:
        content = fid.read()

    content = content.replace("<DEFINES>", '\n'.join(['  ' + t for t in uhdm_types.keys()]))

    generated_filepath = os.path.join(_cwd, 'headers', 'uhdm_types.h')
    return file_utils.set_content_if_changed(generated_filepath, content)


def _write_containers_h(containers):
    template_filepath = os.path.join(_cwd, 'templates', 'containers.h')
    with open(template_filepath, 'r+t') as fid:
        content = fid.read()

    unique = set()
    lines = []
    for type, card in containers:
        if card == 'any' and type not in unique:
            unique.add(type)
            if type != 'any':
                lines.append(f'  class {type};')
            lines.append(f'  typedef std::vector<{type}*> VectorOf{type};')
            lines.append(f'  typedef std::vector<{type}*>::iterator VectorOf{type}Itr;')
    content = content.replace("<CONTAINERS>", '\n'.join(lines))

    generated_filepath = os.path.join(_cwd, 'headers', 'containers.h')
    return file_utils.set_content_if_changed(generated_filepath, content)


def _update_vpi_inst(baseclass, classname, lvl):
    pass
#    global VISITOR
#    #todo figureout the below upvar code and convert it into python.
#    # upvar $lvl vpi_get_str_body_inst vpi_get_str_body_inst_l
#    # upvar $lvl vpi_get_body_inst vpi_get_body_inst_l
#    # upvar $lvl vpi_get_str_body vpi_get_str_body_l
#    # upvar $lvl vpi_get_body vpi_get_body_l vpi_get_value_body vpi_get_value_body_l vpi_get_delay_body vpi_get_delay_body_l
#
#    if (baseclass in vpi_get_str_body_inst_l):
#        for inst in vpi_get_str_body_inst_l[baseclass]:
#            pass
#            #todo figure out the below code and convert it into python.
#            # vpi_get_str_body_l += f"[printGetStrBody $classname [lindex $inst 1] [lindex $inst 2] [lindex $inst 3]]"
#            # VISITOR($classname) += f"[printGetStrVisitor $classname [lindex $inst 1] [lindex $inst 2] [lindex $inst 3]]"
#
#    if (baseclass in vpi_get_body_inst_l):
#        vpi_case_body = ""
#        for inst in vpi_get_body_inst_l[baseclass]:
#            pass
#            #todo figure out the below code and convert it into python.
#            # vpi_case_body += f"[printGetBody $classname [lindex $inst 1] [lindex $inst 2] [lindex $inst 3]]"
#
#
#        # The case body can be empty if all propeerties have been handled
#        # in the base class. So only if non-empty, add the if/switch
#        if (vpi_case_body != ""):
#            vpi_get_body_l += f"[printGetBodyPrefix $classname] $vpi_case_body [printGetBodySuffix]"
#
#        for inst in vpi_get_body_inst_l[baseclass]:
#            pass
#            #todo figure out the below code and convert it into python.
#            # vpi_get_value_body_l += f"[printGetValueBody $classname [lindex $inst 1] [lindex $inst 2] [lindex $inst 3]]"
#            # vpi_get_delay_body_l += f"[printGetDelayBody $classname [lindex $inst 1] [lindex $inst 2] [lindex $inst 3]]"
#            # VISITOR[classname] += f"[printGetVisitor $classname [lindex $inst 1] [lindex $inst 2] [lindex $inst 3]]"


def _process_baseclass(baseclass, classname, modeltype, capnpIndex):
    pass
#    global SAVE, RESTORE, BASECLASS, vpi_iterator, vpi_handle_body, vpi_iterate_body, vpi_handle_by_name_body
#    #todo figureout the below upvar code and convert it into python.
#    # upvar capnp_schema capnp_schema_l capnp_schema_all capnp_schema_all_l
#    # upvar vpi_iterate_body_all vpi_iterate_body_all_l vpi_handle_body_all vpi_handle_body_all_l
#    # upvar vpi_handle_by_name_body_all vpi_handle_by_name_body_all_l
#    idx = capnpIndex
#    Classname = classname[:1].upper() + classname[1:]
#    Classname = Classname.replace("_", "")
#
#    while (baseclass != ""):
#        # Capnp schema
#        if (modeltype != "class_def"):
#            for member in capnp_schema_l[baseclass]:
#                for (name, type) in member:
#                    capnp_schema_all_l += f"{name} @{idx} :{type};\n"
#                    idx += 1
#
#        # Save
#        save = ""
#        #todo convert the below commented out code in python.
#        for line in SAVE[baseclass].split('\n'):
#            base = baseclass
#            tmp = line
#            base = baseclass.replace("_", "")
#            tmp = line.replace(" [string toupper $base 0 0]s", f"{Classname}s")
#
#        SAVE[classname] += save
#
#        # Restore
#        restore = RESTORE[baseclass]
#        restore = RESTORE[baseclass].replace(f" {baseclass}Maker", f" {classname}Maker")
#
#        RESTORE[classname] += restore
#
#        # VPI
#        update_vpi_inst(baseclass, classname, 2)
#
#        if (baseclass in vpi_iterate_body):
#            vpi_iterate = vpi_iterate_body[baseclass]
#            vpi_iterate = vpi_iterate.replace(f"= uhdm{baseclass}", f"= uhdm{classname}")
#            vpi_iterate_body_all_l += vpi_iterate
#
#        if (baseclass in vpi_handle_body):
#            vpi_handle = vpi_handle_body[baseclass]
#            vpi_handle = vpi_handle.replace(f"= uhdm{baseclass}", f"= uhdm{classname}")
#            vpi_handle = vpi_handle.replace(f"{baseclass}\\*", f"{classname}\*")
#            vpi_handle_body_all_l += vpi_handle
#
#        if (baseclass in vpi_handle_by_name_body):
#            vpi_handle_by_name = vpi_handle_by_name_body[baseclass]
#            vpi_handle_by_name = vpi_handle_by_name.replace(f"= uhdm{baseclass}", f"= uhdm{classname}")
#            vpi_handle_by_name_body_all_l += vpi_handle_by_name
#
#        if (baseclass in vpi_iterator):
#            for (vpi, type, card) in vpi_iterator[baseclass]:
#                _print_vpi_visitor(classname, vpi, card) 
#                _print_vpi_listener(classname, vpi, type, card)
#
#        # Parent class
#        if (baseclass in BASECLASS):
#            baseclass = BASECLASS[baseclass]
#        else:
#            baseclass = ""
#
#    # return idx

def _generate_code(modeldefs, uhdm_types):
    with open(os.path.join(_cwd, 'templates', 'class_header.h'), 'r+t') as fid:
        template_content = fid.read()
    
    class_names = []
    factories = []
    factories_methods = []

    methods = {}
    members = {}
    SAVE = {}
    RESTORE = {}
    capnp_schema = {}
    vpi_iterate_body = {}
    vpi_iterator = {}
    vpi_get_str_body_inst = {}
    vpi_handle_body = {}
    visitor_relations = {}
    vpi_get_body_inst = {}
    vpi_handle_by_name_body = {}

    vpi_iterate_body_all = []
    vpi_handle_by_name_body_all = []
    vpi_scan_body = []
    vpi_handle_body_all = []
    vpi_get_body = []
    vpi_get_value_body = []
    vpi_get_delay_body = []
    vpi_get_str_body = []
    typedefs = []
    containers = []
    capnp_save = []
    capnpRootSchemaIndex = 2
    factory_object_type_map = []
    capnp_schema_all = []
    capnp_root_schema = []

    for model in modeldefs.values():
        classname = model["name"]
        modeltype = model["type"]
        template = template_content
        baseclass = ''
        methods[classname] = []
        members[classname] = []
        SAVE[classname] = []
        RESTORE[classname] = []
        capnp_schema[classname] = []
        vpi_iterate_body[classname] = []
        vpi_iterator[classname] = []
        vpi_handle_body[classname] = []
        vpi_get_str_body_inst[classname] = []
        visitor_relations[classname] = []
        vpi_get_body_inst[classname] = []
        vpi_handle_by_name_body[classname] = []

        Classname_ = classname[:1].upper() + classname[1:]
        Classname = Classname_.replace('_', '')
        class_names.append(classname)

        template = template.replace("<CLASSNAME>", classname)
        template = template.replace("<UPPER_CLASSNAME>", classname.upper())
        if modeltype == 'class_def':
            template = template.replace('<FINAL_DESTRUCTOR>', '')
            template = template.replace('<VIRTUAL>', 'virtual ')
            template = template.replace('<OVERRIDE_OR_FINAL>', 'override')
            template = template.replace('<DISABLE_OBJECT_FACTORY>', '#if 0 // This class cannot be instantiated')
            template = template.replace('<END_DISABLE_OBJECT_FACTORY>', '#endif')
        else:
            template = template.replace('<FINAL_DESTRUCTOR>', 'final')
            template = template.replace('<VIRTUAL>', 'virtual ')
            template = template.replace('<OVERRIDE_OR_FINAL>', 'final')
            template = template.replace('<DISABLE_OBJECT_FACTORY>', '')
            template = template.replace('<END_DISABLE_OBJECT_FACTORY>', '')

        id, define = _define_type(f"uhdm{classname}", None, True)
        if define:
            uhdm_types[define] = None

        if modeltype == 'group_def':
            _generate_group_checker(model, modeldefs)
            continue

        log(f'Generating headers/{classname}.h')
        if modeltype != 'class_def':
            factories.append(f'    {classname}Factory {classname}Maker;')
            factories_methods.append(f'    {classname}* Make{Classname_}() {{ {classname}* tmp = {classname}Maker.Make(); tmp->SetSerializer(this); tmp->UhdmId(objId_++); return tmp; }}')
            factory_object_type_map.append(f'  case uhdm{classname}: return {classname}Maker.objects_[index];')

        factories.append(f'    VectorOf{classname}Factory {classname}VectMaker;')
        factories_methods.append(f'    std::vector<{classname}*>* Make{Classname_}Vec() {{ return {classname}VectMaker.Make();}}')

        _print_vpi_listener(classname, classname, classname, '0')

        if modeltype == 'class_def':
            # DeepClone() not implemented for class_def; just declare to narrow the covariant return type.
            methods[classname].append(f'  {classname}* DeepClone(Serializer* serializer, ElaboratorListener* elab_listener, BaseClass* parent) const override = 0;')
        else:
            # Builtin properties do not need to be specified in each models
            # Builtins: "vpiParent, Parent type, vpiFile, Id" method and field
            methods[classname].extend(_print_method_declarations(classname, 'BaseClass', 'vpiParent', '1'))
            members[classname].extend(_print_members('BaseClass', 'vpiParent', '1'))
            vpi_handle_body[classname] += _print_get_handle_body(classname, 'BaseClass', 'vpiParent', 'vpiParent', '1')

            methods[classname].extend(_print_method_declarations(classname, 'unsigned int', 'uhdmParentType', '1'))
            members[classname].extend(_print_members('unsigned int', 'uhdmParentType', '1'))

            methods[classname].extend(_print_method_declarations(classname,'string','vpiFile', '1'))
            members[classname].extend(_print_members('string', 'vpiFile', '1'))
            vpi_get_str_body_inst[classname].extend(f'{classname} string vpiFile 1')

            methods[classname].extend(_print_method_declarations(classname, 'unsigned int', 'uhdmId', '1'))
            members[classname].extend(_print_members('unsigned int', 'uhdmId', '1'))

            methods[classname].append(f'    {classname}* DeepClone(Serializer* serializer, ElaboratorListener* elab_listener, BaseClass* parent) const override;')

            capnp_schema[classname].append(('vpiParent', 'UInt64'))
            capnp_schema[classname].append(('uhdmParentType', 'UInt64'))
            capnp_schema[classname].append(('vpiFile', 'UInt64'))
            capnp_schema[classname].append(('vpiLineNo', 'UInt32'))
            capnp_schema[classname].append(('uhdmId', 'UInt64'))

            capnp_root_schema.append(f'  factory{Classname} @{capnpRootSchemaIndex} :List({Classname});')
            capnpRootSchemaIndex += 1

            SAVE[classname].append(f'    {Classname}s[index].setVpiParent(GetId(obj->VpiParent()));')
            SAVE[classname].append(f'    {Classname}s[index].setUhdmParentType(obj->UhdmParentType());')
            SAVE[classname].append(f'    {Classname}s[index].setVpiFile(obj->GetSerializer()->symbolMaker.Make(obj->VpiFile()));')
            SAVE[classname].append(f'    {Classname}s[index].setVpiLineNo(obj->VpiLineNo());')
            SAVE[classname].append(f'    {Classname}s[index].setUhdmId(obj->UhdmId());')

            RESTORE[classname].append(f'   {classname}Maker.objects_[index]->UhdmParentType(obj.getUhdmParentType());')
            RESTORE[classname].append(f'   {classname}Maker.objects_[index]->VpiParent(GetObject(obj.getUhdmParentType(),obj.getVpiParent()-1));')
            RESTORE[classname].append(f'   {classname}Maker.objects_[index]->VpiFile(symbolMaker.GetSymbol(obj.getVpiFile()));')
            RESTORE[classname].append(f'   {classname}Maker.objects_[index]->VpiLineNo(obj.getVpiLineNo());')
            RESTORE[classname].append(f'   {classname}Maker.objects_[index]->UhdmId(obj.getUhdmId());')

        indTmp = 0
        type_specified = False
        for key, value in model.items():
            if key == 'property':
                for prop, conf in value.items():
                    name = conf.get('name')
                    vpi = conf.get('vpi')
                    type = conf.get('type')
                    card = conf.get('card')

                    if prop == 'type':
                        type_specified = True
                        methods[classname].append(f'    {type} {vpi[:1].upper() + vpi[1:]}() const final {{ return {name}; }}')
                        vpi_get_body_inst[classname].append(f'{classname} {type} {vpi} {card}')
                        continue

                    if type != 'any':
                        containers.append((type, card))

                    # properties are already defined in vpi_user.h, no need to redefine them
                    methods[classname].extend(_print_method_declarations(classname, type, vpi, card))
                    members[classname].extend(_print_members(type, vpi, card))
                    vpi_get_body_inst[classname].append(f'{classname} {type} {vpi} {card}')
                    vpi_get_str_body_inst[classname].append(f'{classname} {type} {vpi} {card}')
                    capnp_schema[classname].append(_print_capnp_schema(type, vpi, card))

                    Vpi_ = vpi[:1].upper() + vpi[1:]
                    Vpi = Vpi_.replace("_", "")

                    if type in ['string', 'value', 'delay']:
                        if Vpi != 'VpiFullName':
                            SAVE[classname].append(f'    {Classname}s[index].set{Vpi}(obj->GetSerializer()->symbolMaker.Make(obj->{Vpi_}()));')
                            RESTORE[classname].append(f'    {classname}Maker.objects_[index]->{Vpi_}(symbolMaker.GetSymbol(obj.get{Vpi}()));')
                    else:
                        SAVE[classname].append(f'    {Classname}s[index].set{Vpi}(obj->{Vpi_}());')
                        RESTORE[classname].append(f'    {classname}Maker.objects_[index]->{Vpi_}(obj.get{Vpi}());')
            
            elif key == 'extends' and value:
                template = template.replace("<EXTENDS>", value)

            elif key in ['class', 'obj_ref', 'class_ref', 'group_ref']:
                for name, content in value.items():
                    if not content:
                      continue

                    vpi  = content.get('vpi')
                    type = content.get('type')
                    card = content.get('card')
                    id   = content.get('id')

                    Type_ = type[:1].upper() + type[1:]
                    Type = Type_.replace("_", "")
                    Name_ = name
                    Name = name.replace("_", "")

                    if (card == 'any') and not name.endswith('s'):
                        name += 's'
                    real_type = type

                    if key == 'group_ref':
                        type = 'any'

                    containers.append((type, card))
                    # define access properties (allModules...)
                    id, define = _define_type(f'uhdm{name}', None, True)
                    if define:
                        uhdm_types[define] = None

                    methods[classname].extend(_print_method_declarations(classname, type, name, card, real_type))
                    _print_vpi_listener(classname, vpi, type, card)
                    members[classname].extend(_print_members(type, name, card))
                    vpi_iterate_body[classname].extend(_print_iterate_body(name, classname, vpi, card))
                    vpi_handle_by_name_body[classname].extend(_print_get_handle_by_name_body(name, classname, vpi, card))
                    vpi_iterator[classname].append(f'{vpi} {type} {card}')
                    vpi_scan_body.extend(_print_scan_body(name, classname, type, card))
                    vpi_handle_body[classname].extend(_print_get_handle_body(classname, f'uhdm{type}', vpi, name, card))

                    obj_key = 'ObjIndexType' if key in ['class_ref', 'group_ref'] else 'UInt64'

                    capnp_schema[classname].append(_print_capnp_schema(obj_key, Name, card))
                    if card == '1':
                        if key in ['class_ref', 'group_ref']:
                            SAVE[classname].append(f'  if (obj->{name[:1].upper() + name[1:]}()) {{')
                            SAVE[classname].append(f'    ::ObjIndexType::Builder tmp$indTmp = {Classname}s[index].get{Name_}();')
                            SAVE[classname].append(f'    tmp{indTmp}.setIndex(GetId(((BaseClass*) obj->{Name_}())));')
                            SAVE[classname].append(f'    tmp{indTmp}.setType(((BaseClass*)obj->{Name_}())->UhdmType());  }}')
                            RESTORE[classname].append(f'     {classname}Maker.objects_[index]->{Name_}(({type}*)GetObject(obj.get{Name_}().getType(),obj.get{Name_}().getIndex()-1));')
                            indTmp += 1
                        else:
                            SAVE[classname].append(f'    {Classname}s[index].set{Name_}(GetId(obj->{Name_}()));')
                            RESTORE[classname].append(f'    if (obj.get{Name_}())')
                            RESTORE[classname].append(f'        {classname}Maker.objects_[index]->{Name_}({type}Maker.objects_[obj.get{Name_}()-1\]);')

                    else:
                        obj_key = '::ObjIndexType' if key in ['class_ref', 'group_ref'] else '::uint64_t'

                        SAVE[classname].append(f'if (obj->{Name_}()) {{')
                        SAVE[classname].append(f'    ::capnp::List<{obj_key}>::Builder {Name_}s = {Classname}s[index].init{Name_}(obj->{Name_}()->size());')
                        SAVE[classname].append(f'    for (unsigned int ind = 0; ind < obj->{Name_}()->size(); ind++) {{\n')
                        
                        if key in ['class_ref', 'group_ref']:
                            SAVE[classname].append(f'        ::ObjIndexType::Builder tmp = {Name_}s[ind];')
                            SAVE[classname].append(f'        tmp.setIndex(GetId(((BaseClass*) (*obj->{Name_}())[ind])));')
                            SAVE[classname].append(f'        tmp.setType(((BaseClass*)((*obj->{Name_}())[ind]))->UhdmType());')
                        else:
                            SAVE[classname].append(f'        {Name_}s.set(ind, GetId((*obj->{Name_}())[ind]));')
                        
                        SAVE[classname].append('      }}')
                        SAVE[classname].append('    }}')

                        RESTORE[classname].append(f'if (obj.get{Name_}().size()) {{')
                        RESTORE[classname].append(f'std::vector<{type}*>* vect = {type}VectMaker.Make();')
                        RESTORE[classname].append(f'for (unsigned int ind = 0; ind < obj.get{Name_}().size(); ind++) {{')

                        if key in ['class_ref', 'group_ref']:
                            RESTORE[classname].append(f'        vect->push_back(({type}*)GetObject(obj.get{Name_}()[ind].getType(), obj.get{Name_}()[ind].getIndex()-1));')
                        else:
                            RESTORE[classname].append(f'        vect->push_back({type}Maker.objects_[obj.get{Name_}()[ind]-1]);')
                        
                        RESTORE[classname].append(f'      }}')
                        RESTORE[classname].append(f'{classname}Maker.objects_[index]->{Name_}(vect);')
                        RESTORE[classname].append('    }}')

        if not type_specified and (modeltype == 'obj_def'):
            vpiclasstype = _make_vpi_name(classname)
            methods[classname].append(f'    unsigned int VpiType() const final {{ return {vpiclasstype}; }}')
            vpi_get_body_inst[classname].append(f'{classname} "unsigned int" vpiType 1')

        template = template.replace('<EXTENDS>', 'BaseClass')
        template = template.replace('<METHODS>', '\n\n'.join(methods[classname]))
        template = template.replace('<MEMBERS>', '\n\n'.join(members[classname]))

        file_utils.set_content_if_changed(os.path.join(_cwd, 'headers', f'{classname}.h'), template)

        # VPI
        _update_vpi_inst(classname, classname, 1)

        capnpIndex = 0
        if modeltype not in [ 'class_def', 'group_def']:
            capnp_schema_all.append('struct $Classname \{')
            for (name, type) in capnp_schema[classname]:
                capnp_schema_all.append(f'{name} {capnpIndex} :{type};')
                capnpIndex += 1

        vpi_iterate_body_all.extend(vpi_iterate_body[classname])
        vpi_handle_body_all.extend(vpi_handle_body[classname])
        vpi_handle_by_name_body_all.extend(vpi_handle_by_name_body[classname])

        # process baseclass recursively
        capnpIndex = _process_baseclass(baseclass, classname, modeltype, capnpIndex)

        if modeltype != 'class_def':
            capnp_schema_all.append('}')

        _close_vpi_listener(classname)

    # uhdm.h
    _write_uhdm_h(class_names)

    # uhdm_types.h
    _write_uhdm_types_h(uhdm_types)

    # containers.h
    _write_containers_h(containers)

    # vpi_user.cpp
    with open(os.path.join(_cwd, 'templates', 'vpi_user.cpp'), 'r+t') as fid:
        vpi_user = fid.read()

    vpi_user = vpi_user.replace('<HEADERS>', _format_headers(class_names))
    vpi_user = vpi_user.replace('<VPI_HANDLE_BY_NAME_BODY>', '\n'.join(vpi_handle_by_name_body_all))
    vpi_user = vpi_user.replace('<VPI_ITERATE_BODY>', '\n'.join(vpi_iterate_body_all))
    vpi_user = vpi_user.replace('<VPI_SCAN_BODY>', '\n'.join(vpi_scan_body))
    vpi_user = vpi_user.replace('<VPI_HANDLE_BODY>', '\n'.join(vpi_handle_body_all))
    vpi_user = vpi_user.replace('<VPI_GET_BODY>', '\n'.join(vpi_get_body))
    vpi_user = vpi_user.replace('<VPI_GET_VALUE_BODY>', '\n'.join(vpi_get_value_body))
    vpi_user = vpi_user.replace('<VPI_GET_DELAY_BODY>', '\n'.join(vpi_get_delay_body))
    vpi_user = vpi_user.replace('<VPI_GET_STR_BODY>', '\n'.join(vpi_get_str_body))
    file_utils.set_content_if_changed(os.path.join(_cwd, 'src', 'vpi_user.cpp'), vpi_user)

    # UHDM.capnp
#    if {[write_capnp $capnp_schema_all $capnp_root_schema] || ![file exists "[project_path]/src/UHDM.capnp.h"]} {
#        log "Generating Capnp schema..."
#        file delete -force [project_path]/src/UHDM.capnp.*
#        set capnp_path [find_file $working_dir "capnpc-c++$exeext"]
#        puts "capnp_path = $capnp_path"
#        set capnp_path [file dirname $capnp_path]
#
#        if { $tcl_platform(platform) == "windows" } {
#            exec -ignorestderr cmd /c "set PATH=$capnp_path;%PATH%; && cd /d [project_path]/src && $capnp_path/capnp.exe compile -oc++ UHDM.capnp"
#        } else {
#            exec -ignorestderr sh -c "export PATH=$capnp_path; $capnp_path/capnp compile -oc++:. [project_path]/src/UHDM.capnp"
#        }
#    }

    # BaseClass.h
    file_utils.copy_file_if_changed(os.path.join(_cwd, 'templates', 'BaseClass.h'), os.path.join(_cwd, 'headers', 'BaseClass.h'))

    # SymbolFactory.h/cpp
    file_utils.copy_file_if_changed(os.path.join(_cwd, 'templates', 'SymbolFactory.h'), os.path.join(_cwd, 'headers', 'SymbolFactory.h'))
    file_utils.copy_file_if_changed(os.path.join(_cwd, 'templates', 'SymbolFactory.cpp'), os.path.join(_cwd, 'src', 'SymbolFactory.cpp'))

    # Serializer.cpp
    serializer_filepaths = {
      os.path.join(_cwd, 'templates', 'vpi_uhdm.h'): os.path.join(_cwd, 'headers', 'vpi_uhdm.h'),
      os.path.join(_cwd, 'templates', 'Serializer.h'): os.path.join(_cwd, 'headers', 'Serializer.h'),
      os.path.join(_cwd, 'templates', 'Serializer_save.cpp'): os.path.join(_cwd, 'src', 'Serializer_save.cpp'),
      os.path.join(_cwd, 'templates', 'Serializer_restore.cpp'): os.path.join(_cwd, 'src', 'Serializer_restore.cpp'),
    }
    
    for template_filepath, generated_filepath in serializer_filepaths.items():
        capnp_init_factories = []
        capnp_restore_factories = []
        capnp_save = []
        capnp_id = []
        factory_purge = []

        for model in modeldefs.values():
            modeltype = model['type']
            classname = model['name']
            Classname_ = classname[:1].upper() + classname[1:]
            Classname = Classname_.replace('_', '')

            if modeltype not in ['class_def', 'group_def'] and SAVE[classname]:
                capnp_save.append(f'::capnp::List<{Classname}>::Builder {Classname}s = cap_root.initFactory{Classname}({classname}Maker.objects_.size());')
                capnp_save.append( 'index = 0;')
                capnp_save.append(f'for (auto obj : {classname}Maker.objects_) {{')
                capnp_save.extend(SAVE[classname])
                capnp_save.append('  index++;')
                capnp_save.append( '}')

                capnp_init_factories.append(f'::capnp::List<{Classname}>::Reader {Classname}s = cap_root.getFactory{Classname}();')
                capnp_init_factories.append(f'for (unsigned ind = 0; ind < {Classname}s.size(); ind++) {{')
                capnp_init_factories.append(f'SetId(Make{Classname_}(), ind);')
                capnp_init_factories.append( '}')

                capnp_restore_factories.append( 'index = 0;')
                capnp_restore_factories.append(f'for ({Classname}::Reader obj : {Classname}s) {{')
                capnp_restore_factories.extend(RESTORE[classname])
                capnp_restore_factories.append( 'index++;')
                capnp_restore_factories.append( '}')

            if modeltype != 'class_def':
                capnp_id.append( 'index = 1;')
                capnp_id.append(f'for (auto obj : ${classname}Maker.objects_) {{')
                capnp_id.append( '  SetId(obj, index);')
                capnp_id.append( '  index++;')
                capnp_id.append( '}')

                factory_purge.append(f'for (auto obj : ${classname}Maker.objects_) {{')
                factory_purge.append( '  delete obj;')
                factory_purge.append( '}')
                factory_purge.append(f'{classname}Maker.objects_.clear();')

        with open(template_filepath, 'r+t') as fid:
            serializer_content = fid.read()

        serializer_content = serializer_content.replace('<FACTORIES>', '\n'.join(factories))
        serializer_content = serializer_content.replace('<FACTORIES_METHODS>', '\n'.join(factories_methods))
#        serializer_content = serializer_content.replace('<METHODS_CPP>', '\n'.join(methods_cpp))

#        serializer_content = serializer_content.replace('<UHDM_NAME_MAP>', '\n'.join(uhdm_name_map))
        serializer_content = serializer_content.replace('<FACTORY_PURGE>', '\n'.join(factory_purge))
        serializer_content = serializer_content.replace('<FACTORY_OBJECT_TYPE_MAP>', '\n'.join(factory_object_type_map))
        serializer_content = serializer_content.replace('<CAPNP_ID>', '\n'.join(capnp_id))
        serializer_content = serializer_content.replace('<CAPNP_SAVE>', '\n'.join(capnp_save))
        serializer_content = serializer_content.replace('<CAPNP_INIT_FACTORIES>', '\n'.join(capnp_init_factories))
        serializer_content = serializer_content.replace('<CAPNP_RESTORE_FACTORIES>', '\n'.join(capnp_restore_factories))

        file_utils.set_content_if_changed(generated_filepath, serializer_content)

    # vpi_visitor.h
    file_utils.copy_file_if_changed(os.path.join(_cwd, 'templates', 'vpi_visitor.h'), os.path.join(_cwd, 'headers', 'vpi_visitor.h'))

    # vpi_visitor.cpp
    _write_vpi_visitor_cpp()

    # VpiListener.h
    _write_VpiListener_h(modeldefs)

    # vpi_listener.h
    _write_vpi_listener_h()

    # vpi_listener.cpp
#    _write_vpi_listener_cpp()

    # uhdm_forward_decl.h
    _write_uhdm_forward_decl(class_names)


def _main():
    global _cwd

    modeldef_list_filepath = r'D:\Projects\Davenche\UHDM\model\models.lst'
    _cwd = r'D:\Projects\Davenche\UHDM'

    print("UHDM MODEL GENERATION")
    print("Model definition filepath: {}".format(modeldef_list_filepath))
    print("Working dir: {}".format(_cwd))

    src_dir = os.path.join(_cwd, "src")
    if not os.path.exists(src_dir):
        os.mkdir(src_dir)

    headers_dir = os.path.join(_cwd, "headers")
    if not os.path.exists(headers_dir):
        os.mkdir(headers_dir)

    _parse_vpi_user_defines()
    modeldefs, uhdm_types = _parse_modeldefs(modeldef_list_filepath)
#    with open('model_gen.log', 'w+t') as outstrm:
#        pprint.pprint(modeldefs, stream=outstrm)
    _generate_code(modeldefs, uhdm_types)

    #generate_elaborator(models)

    print("UHDM MODEL GENERATION DONE.")
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(_main())
