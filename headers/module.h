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
 * File:   module.h
 * Author:
 *
 * Created on December 14, 2019, 10:03 PM
 */

#ifndef MODULE_H
#define MODULE_H

namespace UHDM {

  class module : public BaseClass {
  public:
    module(){}
    ~module() final {}
    
    BaseClass* get_vpiParent() const { return vpiParent_; }

    void set_vpiParent(BaseClass* data) { vpiParent_ = data; }

    unsigned int get_uhdmParentType() const { return uhdmParentType_; }

    void set_uhdmParentType(unsigned int data) { uhdmParentType_ = data; }

    std::string get_vpiFile() const { return SymbolFactory::getSymbol(vpiFile_); }

    void set_vpiFile(std::string data) { vpiFile_ = SymbolFactory::make(data); }

    unsigned int get_vpiLineNo() const { return vpiLineNo_; }

    void set_vpiLineNo(unsigned int data) { vpiLineNo_ = data; }

    std::string get_vpiName() const { return SymbolFactory::getSymbol(vpiName_); }

    void set_vpiName(std::string data) { vpiName_ = SymbolFactory::make(data); }

    unsigned int get_vpiType() { return vpiModule; }

    bool get_vpiTopModule() const { return vpiTopModule_; }

    void set_vpiTopModule(bool data) { vpiTopModule_ = data; }

    int get_vpiDefDecayTime() const { return vpiDefDecayTime_; }

    void set_vpiDefDecayTime(int data) { vpiDefDecayTime_ = data; }

    instance_array* get_instance_array() const { return instance_array_; }

    void set_instance_array(instance_array* data) { instance_array_ = data; }

    const VectorOfscope* get_scope() const { return scope_; }

    void set_scope(VectorOfscope* data) { scope_ = data; }

    const VectorOfprocess* get_process() const { return process_; }

    void set_process(VectorOfprocess* data) { process_ = data; }

    const VectorOfprimitive* get_primitives() const { return primitives_; }

    void set_primitives(VectorOfprimitive* data) { primitives_ = data; }

    const VectorOfprimitive_array* get_primitive_arrays() const { return primitive_arrays_; }

    void set_primitive_arrays(VectorOfprimitive_array* data) { primitive_arrays_ = data; }

    clocking_block* get_global_clocking() const { return global_clocking_; }

    void set_global_clocking(clocking_block* data) { global_clocking_ = data; }

    clocking_block* get_default_clocking() const { return default_clocking_; }

    void set_default_clocking(clocking_block* data) { default_clocking_ = data; }

    const VectorOfport* get_ports() const { return ports_; }

    void set_ports(VectorOfport* data) { ports_ = data; }

    const VectorOfinterface* get_interfaces() const { return interfaces_; }

    void set_interfaces(VectorOfinterface* data) { interfaces_ = data; }

    const VectorOfinterface_array* get_interface_arrays() const { return interface_arrays_; }

    void set_interface_arrays(VectorOfinterface_array* data) { interface_arrays_ = data; }

    const VectorOfcont_assign* get_cont_assigns() const { return cont_assigns_; }

    void set_cont_assigns(VectorOfcont_assign* data) { cont_assigns_ = data; }

    const VectorOfmodule* get_modules() const { return modules_; }

    void set_modules(VectorOfmodule* data) { modules_ = data; }

    const VectorOfmodule_array* get_module_arrays() const { return module_arrays_; }

    void set_module_arrays(VectorOfmodule_array* data) { module_arrays_ = data; }

    const VectorOfmod_path* get_mod_paths() const { return mod_paths_; }

    void set_mod_paths(VectorOfmod_path* data) { mod_paths_ = data; }

    const VectorOftchk* get_tchks() const { return tchks_; }

    void set_tchks(VectorOftchk* data) { tchks_ = data; }

    const VectorOfdef_param* get_def_params() const { return def_params_; }

    void set_def_params(VectorOfdef_param* data) { def_params_ = data; }

    const VectorOfio_decl* get_io_decls() const { return io_decls_; }

    void set_io_decls(VectorOfio_decl* data) { io_decls_ = data; }

    const VectorOfalias_stmt* get_alias_stmts() const { return alias_stmts_; }

    void set_alias_stmts(VectorOfalias_stmt* data) { alias_stmts_ = data; }

    const VectorOfclocking_block* get_clocking_blocks() const { return clocking_blocks_; }

    void set_clocking_blocks(VectorOfclocking_block* data) { clocking_blocks_ = data; }

  private:
    
    BaseClass* vpiParent_;

    unsigned int uhdmParentType_;

    unsigned int vpiFile_;

    unsigned int vpiLineNo_;

    unsigned int vpiName_;

    bool vpiTopModule_;

    int vpiDefDecayTime_;

    instance_array* instance_array_;

    VectorOfscope* scope_;

    VectorOfprocess* process_;

    VectorOfprimitive* primitives_;

    VectorOfprimitive_array* primitive_arrays_;

    clocking_block* global_clocking_;

    clocking_block* default_clocking_;

    VectorOfport* ports_;

    VectorOfinterface* interfaces_;

    VectorOfinterface_array* interface_arrays_;

    VectorOfcont_assign* cont_assigns_;

    VectorOfmodule* modules_;

    VectorOfmodule_array* module_arrays_;

    VectorOfmod_path* mod_paths_;

    VectorOftchk* tchks_;

    VectorOfdef_param* def_params_;

    VectorOfio_decl* io_decls_;

    VectorOfalias_stmt* alias_stmts_;

    VectorOfclocking_block* clocking_blocks_;

  };

  class moduleFactory {
  friend Serializer;
  public:
  static module* make() {
    module* obj = new module();
    objects_.push_back(obj);
    return obj;
  }
  private:
    static std::vector<module*> objects_;
  };
 	      
  class VectorOfmoduleFactory {
  friend Serializer;
  public:
  static std::vector<module*>* make() {
    std::vector<module*>* obj = new std::vector<module*>();
    objects_.push_back(obj);
    return obj;
  }
  private:
  static std::vector<std::vector<module*>*> objects_;
  };

};

#endif

