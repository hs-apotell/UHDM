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
from collections import OrderedDict

import config
import file_utils
import uhdm_types_h

SAVE = {}
RESTORE = {}

capnp_schema = {}
capnp_schema_all = []


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


def _write_capnp(capnp_schema_all, capnp_root_schema):
    template_filepath = os.path.join(_cwd, 'templates', 'UHDM.capnp')
    with open(template_filepath, 'r+t') as fid:
        capnp_content = fid.read()

    capnp_content = capnp_content.replace('<CAPNP_SCHEMA>', capnp_schema_all)
    capnp_content = capnp_content.replace('<CAPNP_ROOT_SCHEMA>', capnp_root_schema)

    generated_filepath = os.path.join(_cwd, 'src', 'UHDM.capnp')
    return file_utils.set_content_if_changed(generated_filepath, capnp_content)


def _process_baseclass(models, baseclass, classname, modeltype, capnpIndex):
    idx = capnpIndex
    Classname = (classname[:1].upper() + classname[1:]).replace('_', '')

    while baseclass:
        Baseclass = (baseclass[:1].upper() + baseclass[1:]).replace('_', '')

        # Capnp schema
        if modeltype != 'class_def':
            for name, type in capnp_schema[baseclass]:
                capnp_schema_all.append(f'{name} @{idx} :{type};')
                idx += 1

        # Save
        save = [ line.replace(f' {Baseclass}s', f' {Classname}s') for line in SAVE[baseclass] ]
        SAVE[classname].extend(save)

        # Restore
        restore = [ line.replace(f' {baseclass}Maker', f' {classname}Maker') for line in RESTORE[baseclass] ]
        RESTORE[classname].extend(restore)

        # Parent class
        baseclass = models[baseclass]['extends']

    return idx


def _print_methods(classname, type, vpi, card, real_type=''):
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
                content.append( '    if (!names.empty()) {')
                content.append( '        unsigned int index = names.size() - 1;')
                content.append( '        while (1) {')
                content.append( '            fullName += names[index];')
                content.append( '            if (index > 0) fullName += (package) ? "::" : ".";')
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
            content.append('')
            content.append(f'bool {classname}::{Vpi_}(const {type}{pointer} &data) {{ {vpi}_ = serializer_->symbolMaker.Make(data); return true; }}')
            content.append('')

    return content


def generate(models):
    # Serializer.cpp
    serializer_filepaths = {
      # config.get_template_filepath('vpi_uhdm.h'): config.get_header_filepath('vpi_uhdm.h'),
      # config.get_template_filepath('Serializer.h'): config.get_header_filepath('Serializer.h'),
      # config.get_template_filepath('Serializer_save.cpp'): config.get_source_filepath('Serializer_save.cpp'),
      config.get_template_filepath('Serializer_restore.cpp'): config.get_source_filepath('Serializer_restore.cpp'),
    }

    factories = []
    factories_methods = []

    methods = []
    capnp_save = []
    capnpRootSchemaIndex = 2
    factory_object_type_map = []
    capnp_root_schema = []

    for model in models.values():
        classname = model['name']
        modeltype = model['type']
        baseclass = model['extends']

        if modeltype == 'group_def':
            continue

        SAVE[classname] = []
        RESTORE[classname] = []
        capnp_schema[classname] = []

        Classname_ = classname[:1].upper() + classname[1:]
        Classname = Classname_.replace('_', '')

        if modeltype != 'class_def':
            factories.append(f'    {classname}Factory {classname}Maker;')
            factories_methods.append(f'    {classname}* Make{Classname_}() {{ {classname}* tmp = {classname}Maker.Make(); tmp->SetSerializer(this); tmp->UhdmId(objId_++); return tmp; }}')
            factory_object_type_map.append(f'  case uhdm{classname}: return {classname}Maker.objects_[index];')

        factories.append(f'    VectorOf{classname}Factory {classname}VectMaker;')
        factories_methods.append(f'    std::vector<{classname}*>* Make{Classname_}Vec() {{ return {classname}VectMaker.Make();}}')

        if modeltype != 'class_def':
            methods.extend(_print_methods(classname, 'BaseClass', 'vpiParent', '1'))
            methods.extend(_print_methods(classname, 'unsigned int', 'uhdmParentType', '1'))
            methods.extend(_print_methods(classname, 'string','vpiFile', '1'))
            methods.extend(_print_methods(classname, 'unsigned int', 'uhdmId', '1'))

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

            RESTORE[classname].append(f'  {classname}Maker.objects_[index]->UhdmParentType(obj.getUhdmParentType());')
            RESTORE[classname].append(f'  {classname}Maker.objects_[index]->VpiParent(GetObject(obj.getUhdmParentType(), obj.getVpiParent()-1));')
            RESTORE[classname].append(f'  {classname}Maker.objects_[index]->VpiFile(symbolMaker.GetSymbol(obj.getVpiFile()));')
            RESTORE[classname].append(f'  {classname}Maker.objects_[index]->VpiLineNo(obj.getVpiLineNo());')
            RESTORE[classname].append(f'  {classname}Maker.objects_[index]->UhdmId(obj.getUhdmId());')

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
                        continue

                    methods.extend(_print_methods(classname, type, vpi, card))
                    capnp_schema[classname].append(_print_capnp_schema(type, vpi, card))

                    Vpi_ = vpi[:1].upper() + vpi[1:]
                    Vpi = Vpi_.replace('_', '')

                    if type in ['string', 'value', 'delay']:
                        if Vpi != 'VpiFullName':
                            SAVE[classname].append(f'    {Classname}s[index].set{Vpi}(obj->GetSerializer()->symbolMaker.Make(obj->{Vpi_}()));')
                            RESTORE[classname].append(f'  {classname}Maker.objects_[index]->{Vpi_}(symbolMaker.GetSymbol(obj.get{Vpi}()));')
                    else:
                        SAVE[classname].append(f'    {Classname}s[index].set{Vpi}(obj->{Vpi_}());')
                        RESTORE[classname].append(f'  {classname}Maker.objects_[index]->{Vpi_}(obj.get{Vpi}());')
            
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

                    if (card == 'any') and not name.endswith('s'):
                        name += 's'

                    Name_ = name[:1].upper() + name[1:]
                    Name = Name_.replace('_', '')

                    real_type = type
                    if key == 'group_ref':
                        type = 'any'

                    methods.extend(_print_methods(classname, type, name, card, real_type))

                    obj_key = 'ObjIndexType' if key in ['class_ref', 'group_ref'] else 'UInt64'

                    capnp_schema[classname].append(_print_capnp_schema(obj_key, Name, card))
                    if card == '1':
                        if key in ['class_ref', 'group_ref']:
                            SAVE[classname].append(f'    if (obj->{Name_}()) {{')
                            SAVE[classname].append(f'      ::ObjIndexType::Builder tmp{indTmp} = {Classname}s[index].get{Name}();')
                            SAVE[classname].append(f'      tmp{indTmp}.setIndex(GetId(((BaseClass*) obj->{Name_}())));')
                            SAVE[classname].append(f'      tmp{indTmp}.setType(((BaseClass*)obj->{Name_}())->UhdmType());')
                            SAVE[classname].append( '    }')
                            RESTORE[classname].append(f'  {classname}Maker.objects_[index]->{Name_}(({type}*)GetObject(obj.get{Name}().getType(), obj.get{Name}().getIndex()-1));')
                            indTmp += 1
                        else:
                            SAVE[classname].append(f'    {Classname}s[index].set{Name}(GetId(obj->{Name_}()));')
                            RESTORE[classname].append(f'  if (obj.get{Name}()) {{')
                            RESTORE[classname].append(f'    {classname}Maker.objects_[index]->{Name_}({type}Maker.objects_[obj.get{Name}()-1]);')
                            RESTORE[classname].append( '  }')

                    else:
                        obj_key = '::ObjIndexType' if key in ['class_ref', 'group_ref'] else '::uint64_t'

                        SAVE[classname].append(f'    if (obj->{Name_}()) {{')
                        SAVE[classname].append(f'      ::capnp::List<{obj_key}>::Builder {Name}s = {Classname}s[index].init{Name}(obj->{Name_}()->size());')
                        SAVE[classname].append(f'      for (unsigned int ind = 0; ind < obj->{Name_}()->size(); ind++) {{')
                        
                        if key in ['class_ref', 'group_ref']:
                            SAVE[classname].append(f'        ::ObjIndexType::Builder tmp = {Name}s[ind];')
                            SAVE[classname].append(f'        tmp.setIndex(GetId(((BaseClass*) (*obj->{Name_}())[ind])));')
                            SAVE[classname].append(f'        tmp.setType(((BaseClass*)((*obj->{Name_}())[ind]))->UhdmType());')
                        else:
                            SAVE[classname].append(f'        {Name}s.set(ind, GetId((*obj->{Name_}())[ind]));')
                        
                        SAVE[classname].append('      }')
                        SAVE[classname].append('    }')

                        RESTORE[classname].append(f'  if (!obj.get{Name}().empty()) {{')
                        RESTORE[classname].append(f'    std::vector<{type}*>* vect = {type}VectMaker.Make();')
                        RESTORE[classname].append(f'    for (unsigned int ind = 0; ind < obj.get{Name}().size(); ind++) {{')

                        if key in ['class_ref', 'group_ref']:
                            RESTORE[classname].append(f'      vect->push_back(({type}*)GetObject(obj.get{Name}()[ind].getType(), obj.get{Name}()[ind].getIndex()-1));')
                        else:
                            RESTORE[classname].append(f'      vect->push_back({type}Maker.objects_[obj.get{Name}()[ind]-1]);')
                        
                        RESTORE[classname].append( '    }')
                        RESTORE[classname].append(f'    {classname}Maker.objects_[index]->{Name_}(vect);')
                        RESTORE[classname].append( '  }')
                    SAVE[classname].append('')

        capnpIndex = 0
        if modeltype not in [ 'class_def', 'group_def']:
            capnp_schema_all.append('struct {Classname} \{')
            for (name, type) in capnp_schema[classname]:
                capnp_schema_all.append(f'{name} {capnpIndex} :{type};')
                capnpIndex += 1

        # process baseclass recursively
        capnpIndex = _process_baseclass(models, baseclass, classname, modeltype, capnpIndex)

        if modeltype != 'class_def':
            capnp_schema_all.append('}')

    uhdm_name_map = [
        'std::string UHDM::UhdmName(UHDM_OBJECT_TYPE type) {',
        '  switch (type) {'
    ]
    uhdm_name_map.extend([ f'  case {id}: return "{name[4:]};' for name, id in uhdm_types_h.get_type_map(models).items() ])
    uhdm_name_map.append('default: return "NO TYPE";')
    uhdm_name_map.append('}')
    uhdm_name_map.append('}')
    uhdm_name_map.append('')

    for template_filepath, generated_filepath in serializer_filepaths.items():
        capnp_init_factories = []
        capnp_restore_factories = []
        capnp_save = []
        capnp_id = []
        factory_purge = []

        for model in models.values():
            modeltype = model['type']

            if modeltype in [ 'class_def', 'group_def' ]:
              continue

            classname = model['name']
            Classname_ = classname[:1].upper() + classname[1:]
            Classname = Classname_.replace('_', '')

            if modeltype not in ['class_def', 'group_def'] and SAVE[classname]:
                capnp_save.append(f'  ::capnp::List<{Classname}>::Builder {Classname}s = cap_root.initFactory{Classname}({classname}Maker.objects_.size());')
                capnp_save.append( '  index = 0;')
                capnp_save.append(f'  for (auto obj : {classname}Maker.objects_) {{')
                capnp_save.extend(SAVE[classname])
                capnp_save.append( '    index++;')
                capnp_save.append( '  }')

                capnp_init_factories.append(f'::capnp::List<{Classname}>::Reader {Classname}s = cap_root.getFactory{Classname}();')
                capnp_init_factories.append(f'for (unsigned ind = 0; ind < {Classname}s.size(); ind++) {{')
                capnp_init_factories.append(f'  SetId(Make{Classname_}(), ind);')
                capnp_init_factories.append( '}')
                capnp_init_factories.append( '')

                capnp_restore_factories.append( 'index = 0;')
                capnp_restore_factories.append(f'for ({Classname}::Reader obj : {Classname}s) {{')
                capnp_restore_factories.extend(RESTORE[classname])
                capnp_restore_factories.append( '  index++;')
                capnp_restore_factories.append( '}')
                capnp_restore_factories.append( '')

            if modeltype != 'class_def':
                capnp_id.append( '  index = 1;')
                capnp_id.append(f'  for (auto obj : {classname}Maker.objects_) {{')
                capnp_id.append( '    SetId(obj, index);')
                capnp_id.append( '    index++;')
                capnp_id.append( '  }')

                factory_purge.append(f'  for (auto obj : {classname}Maker.objects_) {{')
                factory_purge.append( '    delete obj;')
                factory_purge.append( '  }')
                factory_purge.append(f'  {classname}Maker.objects_.clear();')
                factory_purge.append('')

        with open(template_filepath, 'r+t') as fid:
            serializer_content = fid.read()

        # Serializer.h
        serializer_content = serializer_content.replace('<FACTORIES>', '\n'.join(factories))
        serializer_content = serializer_content.replace('<FACTORIES_METHODS>', '\n'.join(factories_methods))

        # Serializer_save.cpp
        serializer_content = serializer_content.replace('<METHODS_CPP>', '\n'.join(methods))
        serializer_content = serializer_content.replace('<UHDM_NAME_MAP>', '\n'.join(uhdm_name_map))
        serializer_content = serializer_content.replace('<FACTORY_PURGE>', '\n'.join(factory_purge))
        serializer_content = serializer_content.replace('<FACTORY_OBJECT_TYPE_MAP>', '\n'.join(factory_object_type_map))
        serializer_content = serializer_content.replace('<CAPNP_ID>', '\n'.join(capnp_id))
        serializer_content = serializer_content.replace('<CAPNP_SAVE>', '\n'.join(capnp_save))

        # Serializer_restore.cpp
        serializer_content = serializer_content.replace('<CAPNP_INIT_FACTORIES>', '\n'.join(capnp_init_factories))
        serializer_content = serializer_content.replace('<CAPNP_RESTORE_FACTORIES>', '\n'.join(capnp_restore_factories))

        file_utils.set_content_if_changed(generated_filepath, serializer_content)


    # UHDM.capnp
#    if {[_write_capnp $capnp_schema_all $capnp_root_schema] || ![file exists '[project_path]/src/UHDM.capnp.h']} {
#        log 'Generating Capnp schema...'
#        file delete -force [project_path]/src/UHDM.capnp.*
#        set capnp_path [find_file $working_dir 'capnpc-c++$exeext']
#        puts 'capnp_path = $capnp_path'
#        set capnp_path [file dirname $capnp_path]
#
#        if { $tcl_platform(platform) == 'windows' } {
#            exec -ignorestderr cmd /c 'set PATH=$capnp_path;%PATH%; && cd /d [project_path]/src && $capnp_path/capnp.exe compile -oc++ UHDM.capnp'
#        } else {
#            exec -ignorestderr sh -c 'export PATH=$capnp_path; $capnp_path/capnp compile -oc++:. [project_path]/src/UHDM.capnp'
#        }
#    }

    return True


def _main():
    import loader

    config.set_cwd(r'D:\Projects\Davenche\UHDM')

    models = loader.load_models()
    return generate(models)


if __name__ == '__main__':
    import sys
    sys.exit(0 if _main() else 1)
