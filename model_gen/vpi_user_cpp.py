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

import config
import file_utils


VISITOR = {}
VISITOR_RELATIONS = {}
vpi_iterator = {}
vpi_iterate_body = {}
vpi_iterate_body_all = []
vpi_get_str_body_inst = {}
vpi_get_body_inst = {}
vpi_scan_body = []
vpi_get_body = []
vpi_get_value_body = []
vpi_get_delay_body = []
vpi_get_str_body = []
vpi_handle_body = {}
vpi_handle_body_all = []
vpi_handle_by_name_body = {}
vpi_handle_by_name_body_all = []


def _classnames(models):
  return [ model['name'] for model in models.values() ]


def _format_headers(models):
    return '\n'.join([ f'#include "headers/{class_name}.h"' for class_name in _classnames(models) ])


def _print_vpi_visitor(classname, vpi, card):
    content = []
    if (vpi == 'vpiParent') and (classname != 'part_select'):
        return content

    if card == '1':
        # Prevent loop in Standard VPI
        if (vpi != 'vpiModule') and (vpi != 'vpiInterface'):
            content.append(f'    itr = vpi_handle({vpi},obj_h);')
            content.append(f'    visit_object(itr, subobject_indent, "{vpi}", visited, out);')
            content.append( '    release_handle(itr);')
    else:
        if classname == 'design':
            content.append('  if (indent == 0) visited->clear();')
        # Prevent loop in Standard VPI
        if vpi != 'vpiUse':
            content.append(f'    itr = vpi_iterate({vpi}, obj_h);')
            content.append( '    while (vpiHandle obj = vpi_scan(itr)) {')
            content.append(f'      visit_object(obj, subobject_indent, "{vpi}", visited, out);')
            content.append( '      release_handle(obj);')
            content.append( '    }')
            content.append( '    release_handle(itr);')

    VISITOR_RELATIONS[classname].extend(content)
    return content


def _print_iterate_body(name, classname, vpi, card):
    content = []
    if card == 'any':
        Name_ = name[:1].upper() + name[1:]
        content.append(f'  if ((handle->type == uhdm{classname}) && (type == {vpi})) {{')
        content.append(f'    if ((({classname}*)(object))->{Name_}())')
        content.append(f'      return NewHandle(uhdm{name}, (({classname}*)(object))->{Name_}());')
        content.append( '    else return 0;')
        content.append( '  }')
        _print_vpi_visitor(classname, vpi, card)
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
        content.append(f'    const {classname}* const obj_parent = (const {classname}*)(object);')
        content.append(f'    if (obj_parent->{Name_}()) {{')
        content.append(f'      for (const BaseClass *obj : *obj_parent->{Name_}())')
        content.append(f'        if (obj->VpiName() == name) return NewVpiHandle(obj);')
        content.append( '    }')
        content.append( '  }')
    return content


def _print_get_body_prefix(classname):
    return [
      f'  if (handle->type == uhdm{classname}) {{',
       '    switch (property) {'
    ]


def _print_get_body_suffix():
    return [ '    }', '  }' ]


def _print_get_body(classname, type, vpi, card):
    if vpi in ['vpiType', 'vpiLineNo']:  # These are already handled by base class
        return []

    content = []
    if (card == '1') and (type not in ['string', 'value', 'delay']):
        content.append(f'      case {vpi}: return ((const {classname}*)(obj))->{vpi[:1].upper() + vpi[1:]}();')

    return content


def _print_get_value_body(classname, type, vpi, card):
    content = []
    if (card == '1') and (type == 'value'):
        content.append(f'  if (handle->type == uhdm{classname}) {{')
        content.append(f'    const s_vpi_value* v = String2VpiValue((({classname}*)(obj))->VpiValue());')
        content.append( '    if (v) {')
        content.append( '      *value_p = *v;')
        content.append( '    }')
        content.append( '  }')

    return content


def _print_get_delay_body(classname, type, vpi, card):
    content = []
    if (card == '1') and (type == 'delay'):
        content.append(f'  if (handle->type == uhdm{classname}) {{')
        content.append(f'    const s_vpi_delay* v = String2VpiDelays((({classname}*)(obj))->VpiDelay());')
        content.append( '    if (v) {')
        content.append( '      *delay_p = *v;')
        content.append( '    }')
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
        content.append(f'  if ((handle->type == uhdm{classname}) && (type == {vpi})) {{')
        content.append(f'    if ({casted_object1}->{Object_}()))')
        content.append(f'      return NewHandle({casted_object1}->{Object_}())->UhdmType(), {casted_object2}->{Object_}());')
        content.append( '    else return 0;')
        content.append( '  }')
        _print_vpi_visitor(classname, vpi, card)
    return content


def _print_get_str_visitor(classname, type, vpi, card):
    content = []
    if (card == '1') and (type == 'string') and (vpi != 'vpiFile'):
        content.append(f'    if (const char* s = vpi_get_str({vpi}, obj_h))')
        content.append(f'        stream_indent(out, indent) << "|{vpi}:" << s << std::endl;')
    return content


def _print_get_visitor(classname, type, vpi, card):
    content = []
    if vpi == 'vpiValue':
        content.append('    s_vpi_value value;')
        content.append('    vpi_get_value(obj_h, &value);')
        content.append('    if (value.format) {')
        content.append('        std::string val = visit_value(&value);')
        content.append('        if (!val.empty()) {')
        content.append('            stream_indent(out, indent) << val;')
        content.append('        }')
        content.append('    }')
    elif vpi == 'vpiDelay':
        content.append('    s_vpi_delay delay;')
        content.append('    vpi_get_delays(obj_h, &delay);')
        content.append('    if (delay.da != nullptr) {')
        content.append('        stream_indent(out, indent) << visit_delays(&delay);')
        content.append('    }}')
    elif (card == '1') and (type != 'string') and (vpi != 'vpiLineNo') and (vpi != 'vpiType'):
        content.append(f'    if (const int n = vpi_get({vpi}, obj_h))')
        content.append( '      if (n != -1)')
        content.append(f'        stream_indent(out, indent) << "|{vpi}:" << n << std::endl;')
    return content


def _print_get_str_body(classname, type, vpi, card):
    # Already handled by the base class
    content = []
    if vpi in ['vpiFile', 'vpiName', 'vpiDefName']:
        return content

    Vpi_ = vpi[:1].upper() + vpi[1:]
    if (card == '1') and (type == 'string'):
        content.append(f'  if ((handle->type == uhdm{classname}) && (property == {vpi})) {{')
        content.append(f'    const {classname}* const o = (const {classname}*)(obj);')
        if vpi == 'vpiFullName':
            content.append(f'    return (o->{Vpi_}().empty() || o->{Vpi_}() == o->VpiName())')
            content.append( '      ? 0')
            content.append(f'      : (PLI_BYTE8*) o->{Vpi_}().c_str();')
        else:
            content.append(f'    return (PLI_BYTE8*) (o->{Vpi_}().empty() ? 0 : o->{Vpi_}().c_str());')
        content.append( '  }')
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


def _update_vpi_inst(baseclass, classname):
    if baseclass in vpi_get_str_body_inst:
        for _, type, vpi, card in vpi_get_str_body_inst[baseclass]:
            vpi_get_str_body.extend(_print_get_str_body(classname, type, vpi, card))
            VISITOR[classname].extend(_print_get_str_visitor(classname, type, vpi, card))

    if baseclass in vpi_get_body_inst:
        vpi_case_body = []
        for _, type, vpi, card in vpi_get_body_inst[baseclass]:
            vpi_case_body.extend(_print_get_body(classname, type, vpi, card))
           
        # The case body can be empty if all propeerties have been handled
        # in the base class. So only if non-empty, add the if/switch
        if vpi_case_body:
            vpi_get_body.extend(_print_get_body_prefix(classname))
            vpi_get_body.extend(vpi_case_body)
            vpi_get_body.extend(_print_get_body_suffix())

        for _, type, vpi, card in vpi_get_body_inst[baseclass]:
            vpi_get_value_body.extend(_print_get_value_body(classname, type, vpi, card))
            vpi_get_delay_body.extend(_print_get_delay_body(classname, type, vpi, card))
            VISITOR[classname].extend(_print_get_visitor(classname, type, vpi, card))


def _process_baseclass(models, baseclass, classname, modeltype):
    Classname = (classname[:1].upper() + classname[1:]).replace('_', '')

    while baseclass:
        Baseclass = (baseclass[:1].upper() + baseclass[1:]).replace('_', '')

        # VPI
        _update_vpi_inst(baseclass, classname)

        if baseclass in vpi_iterate_body:
            vpi_iterate_body_all.extend([line.replace(f'= uhdm{baseclass}', f'= uhdm{classname}') for line in vpi_iterate_body[baseclass]])

        if baseclass in vpi_handle_body:
            vpi_handle_body_all.extend([
              line.replace(f'= uhdm{baseclass}', f'= uhdm{classname}').replace(f'{baseclass}*', f'{classname}*')
              for line in vpi_handle_body[baseclass]
            ])

        if baseclass in vpi_handle_by_name_body:
            vpi_handle_by_name_body_all.extend([line.replace(f'= uhdm{baseclass}', f'= uhdm{classname}') for line in vpi_handle_by_name_body[baseclass]])

        if baseclass in vpi_iterator:
            for vpi, type, card in vpi_iterator[baseclass]:
                _print_vpi_visitor(classname, vpi, card) 

        # Parent class
        baseclass = models[baseclass]['extends']


def generate(models):
    for model in models.values():
        modeltype = model['type']
        if modeltype == 'group_def':
            continue

        classname = model['name']
        baseclass = model['extends']

        VISITOR[classname] = []
        VISITOR_RELATIONS[classname] = []

        vpi_iterate_body[classname] = []
        vpi_iterator[classname] = []
        vpi_handle_body[classname] = []
        vpi_get_str_body_inst[classname] = []
        vpi_get_body_inst[classname] = []
        vpi_handle_by_name_body[classname] = []

        Classname_ = classname[:1].upper() + classname[1:]
        Classname = Classname_.replace('_', '')

        if modeltype != 'class_def':
            # Builtin properties do not need to be specified in each models
            # Builtins: "vpiParent, Parent type, vpiFile, Id" method and field
            vpi_handle_body[classname] += _print_get_handle_body(classname, 'BaseClass', 'vpiParent', 'vpiParent', '1')
            vpi_get_str_body_inst[classname].append((classname, 'string', 'vpiFile', '1'))

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
                        vpi_get_body_inst[classname].append((classname, type, vpi, card))
                        continue

                    # properties are already defined in vpi_user.h, no need to redefine them
                    vpi_get_body_inst[classname].append((classname, type, vpi, card))
                    vpi_get_str_body_inst[classname].append((classname, type, vpi, card))

                    Vpi_ = vpi[:1].upper() + vpi[1:]
                    Vpi = Vpi_.replace('_', '')

            elif key in ['class', 'obj_ref', 'class_ref', 'group_ref']:
                for name, content in value.items():
                    if not content:
                      continue

                    vpi  = content.get('vpi')
                    type = content.get('type')
                    card = content.get('card')
                    id   = content.get('id')

                    Type_ = type[:1].upper() + type[1:]
                    Type = Type_.replace('_', '')
                    Name_ = name
                    Name = name.replace('_', '')

                    if (card == 'any') and not name.endswith('s'):
                        name += 's'
                    real_type = type

                    if key == 'group_ref':
                        type = 'any'

                    vpi_iterate_body[classname].extend(_print_iterate_body(name, classname, vpi, card))
                    vpi_handle_by_name_body[classname].extend(_print_get_handle_by_name_body(name, classname, vpi, card))
                    vpi_iterator[classname].append((vpi, type, card))
                    vpi_scan_body.extend(_print_scan_body(name, classname, type, card))
                    vpi_handle_body[classname].extend(_print_get_handle_body(classname, f'uhdm{type}', vpi, name, card))

        if not type_specified and (modeltype == 'obj_def'):
            vpiclasstype = _make_vpi_name(classname)
            vpi_get_body_inst[classname].append((classname, 'unsigned int', 'vpiType', '1'))

        # VPI
        _update_vpi_inst(classname, classname)

        vpi_iterate_body_all.extend(vpi_iterate_body[classname])
        vpi_handle_body_all.extend(vpi_handle_body[classname])
        vpi_handle_by_name_body_all.extend(vpi_handle_by_name_body[classname])

        # process baseclass recursively
        _process_baseclass(models, baseclass, classname, modeltype)

    # vpi_user.cpp
    with open(config.get_template_filepath('vpi_user.cpp'), 'r+t') as strm:
        file_content = strm.read()

    file_content = file_content.replace('<HEADERS>', _format_headers(models))
    file_content = file_content.replace('<VPI_HANDLE_BY_NAME_BODY>', '\n'.join(vpi_handle_by_name_body_all))
    file_content = file_content.replace('<VPI_ITERATE_BODY>', '\n'.join(vpi_iterate_body_all))
    file_content = file_content.replace('<VPI_SCAN_BODY>', '\n'.join(vpi_scan_body))
    file_content = file_content.replace('<VPI_HANDLE_BODY>', '\n'.join(vpi_handle_body_all))
    file_content = file_content.replace('<VPI_GET_BODY>', '\n'.join(vpi_get_body))
    file_content = file_content.replace('<VPI_GET_VALUE_BODY>', '\n'.join(vpi_get_value_body))
    file_content = file_content.replace('<VPI_GET_DELAY_BODY>', '\n'.join(vpi_get_delay_body))
    file_content = file_content.replace('<VPI_GET_STR_BODY>', '\n'.join(vpi_get_str_body))
    file_utils.set_content_if_changed(config.get_source_filepath('vpi_user.cpp'), file_content)


    ########################################################################

    # vpi_visitor.cpp
    visitors = []
    for model in models.values():
        modeltype = model['type']
        if modeltype == 'group_def':
            continue

        classname = model['name']
        # if classname not in _whitelist:
        #     continue

        vpi_name = _make_vpi_name(classname)
        visitors.append(f'  if (objectType == {vpi_name}) {{')
        visitors.extend(VISITOR[classname])
        visitors.extend(VISITOR_RELATIONS[classname])
        visitors.append( '    return;')
        visitors.append( '  }')

    with open(config.get_template_filepath('vpi_visitor.cpp'), 'r+t') as strm:
        file_content = strm.read()

    file_content = file_content.replace('<OBJECT_VISITORS>', '\n'.join(visitors))
    file_utils.set_content_if_changed(config.get_source_filepath('vpi_visitor.cpp'), file_content)

    return True


def _main():
    import loader

    config.set_cwd(r'D:\Projects\Davenche\UHDM')

    models = loader.load_models()
    return generate(models)


if __name__ == '__main__':
    import sys
    sys.exit(0 if _main() else 1)
