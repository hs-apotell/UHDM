/*
 Do not modify, auto-generated by model_gen.tcl

 Copyright 2019 Alain Dargelas

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 */

/*
 * File:   instance.h
 * Author:
 *
 * Created on December 14, 2019, 10:03 PM
 */

#ifndef INSTANCE_H
#define INSTANCE_H

namespace UHDM {

  class instance : public scope {
  public:
    // Implicit constructor used to initialize all members,
    // comment: instance();
    ~instance()  {}
    
    std::string get_vpiDefName() const { return SymbolFactory::getSymbol(vpiDefName_); }

    bool set_vpiDefName(std::string data) { vpiDefName_ = SymbolFactory::make(data); return true; }

    bool get_vpiArrayMember() const { return vpiArrayMember_; }

    bool set_vpiArrayMember(bool data) { vpiArrayMember_ = data; return true;}

    bool get_vpiCellInstance() const { return vpiCellInstance_; }

    bool set_vpiCellInstance(bool data) { vpiCellInstance_ = data; return true;}

    int get_vpiDefNetType() const { return vpiDefNetType_; }

    bool set_vpiDefNetType(int data) { vpiDefNetType_ = data; return true;}

    std::string get_vpiDefFile() const { return SymbolFactory::getSymbol(vpiDefFile_); }

    bool set_vpiDefFile(std::string data) { vpiDefFile_ = SymbolFactory::make(data); return true; }

    int get_vpiDefDelayMode() const { return vpiDefDelayMode_; }

    bool set_vpiDefDelayMode(int data) { vpiDefDelayMode_ = data; return true;}

    bool get_vpiProtected() const { return vpiProtected_; }

    bool set_vpiProtected(bool data) { vpiProtected_ = data; return true;}

    int get_vpiTimePrecision() const { return vpiTimePrecision_; }

    bool set_vpiTimePrecision(int data) { vpiTimePrecision_ = data; return true;}

    int get_vpiTimeUnit() const { return vpiTimeUnit_; }

    bool set_vpiTimeUnit(int data) { vpiTimeUnit_ = data; return true;}

    int get_vpiUnconnDrive() const { return vpiUnconnDrive_; }

    bool set_vpiUnconnDrive(int data) { vpiUnconnDrive_ = data; return true;}

    std::string get_vpiLibrary() const { return SymbolFactory::getSymbol(vpiLibrary_); }

    bool set_vpiLibrary(std::string data) { vpiLibrary_ = SymbolFactory::make(data); return true; }

    std::string get_vpiCell() const { return SymbolFactory::getSymbol(vpiCell_); }

    bool set_vpiCell(std::string data) { vpiCell_ = SymbolFactory::make(data); return true; }

    std::string get_vpiConfig() const { return SymbolFactory::getSymbol(vpiConfig_); }

    bool set_vpiConfig(std::string data) { vpiConfig_ = SymbolFactory::make(data); return true; }

    bool get_vpiAutomatic() const { return vpiAutomatic_; }

    bool set_vpiAutomatic(bool data) { vpiAutomatic_ = data; return true;}

    bool get_vpiTop() const { return vpiTop_; }

    bool set_vpiTop(bool data) { vpiTop_ = data; return true;}

    VectorOftask_func* get_task_func() const { return task_func_; }

    bool set_task_func(VectorOftask_func* data) { task_func_ = data; return true;}

    VectorOfnet* get_net() const { return net_; }

    bool set_net(VectorOfnet* data) { net_ = data; return true;}

    VectorOfarray_net* get_array_net() const { return array_net_; }

    bool set_array_net(VectorOfarray_net* data) { array_net_ = data; return true;}

    VectorOfassertion* get_assertion() const { return assertion_; }

    bool set_assertion(VectorOfassertion* data) { assertion_ = data; return true;}

    VectorOfclass_defn* get_class_defn() const { return class_defn_; }

    bool set_class_defn(VectorOfclass_defn* data) { class_defn_ = data; return true;}

    instance* get_instance() const { return instance_; }

    bool set_instance(instance* data) { instance_ = data; return true;}

    VectorOfprogram* get_programs() const { return programs_; }

    bool set_programs(VectorOfprogram* data) { programs_ = data; return true;}

    VectorOfprogram* get_program_arrays() const { return program_arrays_; }

    bool set_program_arrays(VectorOfprogram* data) { program_arrays_ = data; return true;}

    VectorOfnamed_event* get_named_event() const { return named_event_; }

    bool set_named_event(VectorOfnamed_event* data) { named_event_ = data; return true;}

    VectorOfnamed_event* get_named_event_array() const { return named_event_array_; }

    bool set_named_event_array(VectorOfnamed_event* data) { named_event_array_ = data; return true;}

    VectorOfspec_param* get_spec_param() const { return spec_param_; }

    bool set_spec_param(VectorOfspec_param* data) { spec_param_ = data; return true;}

    module* get_module() const { return module_; }

    bool set_module(module* data) { module_ = data; return true;}

    virtual unsigned int getUhdmType() { return uhdminstance; }   
  private:
    
    unsigned int vpiDefName_;

    bool vpiArrayMember_;

    bool vpiCellInstance_;

    int vpiDefNetType_;

    unsigned int vpiDefFile_;

    int vpiDefDelayMode_;

    bool vpiProtected_;

    int vpiTimePrecision_;

    int vpiTimeUnit_;

    int vpiUnconnDrive_;

    unsigned int vpiLibrary_;

    unsigned int vpiCell_;

    unsigned int vpiConfig_;

    bool vpiAutomatic_;

    bool vpiTop_;

    VectorOftask_func* task_func_;

    VectorOfnet* net_;

    VectorOfarray_net* array_net_;

    VectorOfassertion* assertion_;

    VectorOfclass_defn* class_defn_;

    instance* instance_;

    VectorOfprogram* programs_;

    VectorOfprogram* program_arrays_;

    VectorOfnamed_event* named_event_;

    VectorOfnamed_event* named_event_array_;

    VectorOfspec_param* spec_param_;

    module* module_;

  };

  class instanceFactory {
  friend Serializer;
  public:
  static instance* make() {
    instance* obj = new instance();
    objects_.push_back(obj);
    return obj;
  }
  private:
    static std::vector<instance*> objects_;
  };
 	      
  class VectorOfinstanceFactory {
  friend Serializer;
  public:
  static std::vector<instance*>* make() {
    std::vector<instance*>* obj = new std::vector<instance*>();
    objects_.push_back(obj);
    return obj;
  }
  private:
  static std::vector<std::vector<instance*>*> objects_;
  };

};

#endif

