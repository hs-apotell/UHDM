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
 * File:   scope.h
 * Author:
 *
 * Created on December 14, 2019, 10:03 PM
 */

#ifndef SCOPE_H
#define SCOPE_H

namespace UHDM {

  class scope : public BaseClass {
  public:
    // Implicit constructor used to initialize all members,
    // comment: scope();
    ~scope()  {}
    
    std::string get_vpiName() const { return SymbolFactory::getSymbol(vpiName_); }

    bool set_vpiName(std::string data) { vpiName_ = SymbolFactory::make(data); return true; }

    std::string get_vpiFullName() const { return SymbolFactory::getSymbol(vpiFullName_); }

    bool set_vpiFullName(std::string data) { vpiFullName_ = SymbolFactory::make(data); return true; }

    VectorOfconcurrent_assertion* get_concurrent_assertions() const { return concurrent_assertions_; }

    bool set_concurrent_assertions(VectorOfconcurrent_assertion* data) { concurrent_assertions_ = data; return true;}

    VectorOfvariables* get_variables() const { return variables_; }

    bool set_variables(VectorOfvariables* data) { variables_ = data; return true;}

    VectorOfparameters* get_parameters() const { return parameters_; }

    bool set_parameters(VectorOfparameters* data) { parameters_ = data; return true;}

    VectorOfscope* get_scopes() const { return scopes_; }

    bool set_scopes(VectorOfscope* data) { scopes_ = data; return true;}

    VectorOftypespec* get_typespecs() const { return typespecs_; }

    bool set_typespecs(VectorOftypespec* data) { typespecs_ = data; return true;}

    VectorOfproperty_decl* get_property_decls() const { return property_decls_; }

    bool set_property_decls(VectorOfproperty_decl* data) { property_decls_ = data; return true;}

    VectorOfsequence_decl* get_sequence_decls() const { return sequence_decls_; }

    bool set_sequence_decls(VectorOfsequence_decl* data) { sequence_decls_ = data; return true;}

    VectorOfnamed_event* get_named_events() const { return named_events_; }

    bool set_named_events(VectorOfnamed_event* data) { named_events_ = data; return true;}

    VectorOfnamed_event_array* get_named_event_arrays() const { return named_event_arrays_; }

    bool set_named_event_arrays(VectorOfnamed_event_array* data) { named_event_arrays_ = data; return true;}

    VectorOfvirtual_interface_var* get_virtual_interface_vars() const { return virtual_interface_vars_; }

    bool set_virtual_interface_vars(VectorOfvirtual_interface_var* data) { virtual_interface_vars_ = data; return true;}

    VectorOflogic_var* get_logic_var() const { return logic_var_; }

    bool set_logic_var(VectorOflogic_var* data) { logic_var_ = data; return true;}

    VectorOfarray_var* get_array_var() const { return array_var_; }

    bool set_array_var(VectorOfarray_var* data) { array_var_ = data; return true;}

    VectorOfarray_var* get_array_var_mem() const { return array_var_mem_; }

    bool set_array_var_mem(VectorOfarray_var* data) { array_var_mem_ = data; return true;}

    VectorOflet_decl* get_let_decls() const { return let_decls_; }

    bool set_let_decls(VectorOflet_decl* data) { let_decls_ = data; return true;}

    VectorOfany* get_instance_items() const { return instance_items_; }

    bool set_instance_items(VectorOfany* data) {if (!instance_itemGroupCompliant(data)) return false; instance_items_ = data; return true;}

    virtual unsigned int getUhdmType() { return uhdmscope; }   
  private:
    
    unsigned int vpiName_;

    unsigned int vpiFullName_;

    VectorOfconcurrent_assertion* concurrent_assertions_;

    VectorOfvariables* variables_;

    VectorOfparameters* parameters_;

    VectorOfscope* scopes_;

    VectorOftypespec* typespecs_;

    VectorOfproperty_decl* property_decls_;

    VectorOfsequence_decl* sequence_decls_;

    VectorOfnamed_event* named_events_;

    VectorOfnamed_event_array* named_event_arrays_;

    VectorOfvirtual_interface_var* virtual_interface_vars_;

    VectorOflogic_var* logic_var_;

    VectorOfarray_var* array_var_;

    VectorOfarray_var* array_var_mem_;

    VectorOflet_decl* let_decls_;

    VectorOfany* instance_items_;

  };

  class scopeFactory {
  friend Serializer;
  public:
  static scope* make() {
    scope* obj = new scope();
    objects_.push_back(obj);
    return obj;
  }
  private:
    static std::vector<scope*> objects_;
  };
 	      
  class VectorOfscopeFactory {
  friend Serializer;
  public:
  static std::vector<scope*>* make() {
    std::vector<scope*>* obj = new std::vector<scope*>();
    objects_.push_back(obj);
    return obj;
  }
  private:
  static std::vector<std::vector<scope*>*> objects_;
  };

};

#endif

