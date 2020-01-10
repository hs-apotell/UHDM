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
 * File:   instance_array.h
 * Author:
 *
 * Created on December 14, 2019, 10:03 PM
 */

#ifndef INSTANCE_ARRAY_H
#define INSTANCE_ARRAY_H

namespace UHDM {

  class instance_array : public BaseClass {
  public:
    // Implicit constructor used to initialize all members,
    // comment: instance_array();
    ~instance_array()  {}
    
    std::string get_vpiName() const { return SymbolFactory::getSymbol(vpiName_); }

    bool set_vpiName(std::string data) { vpiName_ = SymbolFactory::make(data); return true; }

    std::string get_vpiFullName() const { return SymbolFactory::getSymbol(vpiFullName_); }

    bool set_vpiFullName(std::string data) { vpiFullName_ = SymbolFactory::make(data); return true; }

    int get_vpiSize() const { return vpiSize_; }

    bool set_vpiSize(int data) { vpiSize_ = data; return true;}

    expr* get_expr() const { return expr_; }

    bool set_expr(expr* data) { expr_ = data; return true;}

    expr* get_left_expr() const { return left_expr_; }

    bool set_left_expr(expr* data) { left_expr_ = data; return true;}

    expr* get_right_expr() const { return right_expr_; }

    bool set_right_expr(expr* data) { right_expr_ = data; return true;}

    VectorOfinstance* get_instances() const { return instances_; }

    bool set_instances(VectorOfinstance* data) { instances_ = data; return true;}

    range* get_range() const { return range_; }

    bool set_range(range* data) { range_ = data; return true;}

    VectorOfmodule* get_modules() const { return modules_; }

    bool set_modules(VectorOfmodule* data) { modules_ = data; return true;}

    virtual unsigned int getUhdmType() { return uhdminstance_array; }   
  private:
    
    unsigned int vpiName_;

    unsigned int vpiFullName_;

    int vpiSize_;

    expr* expr_;

    expr* left_expr_;

    expr* right_expr_;

    VectorOfinstance* instances_;

    range* range_;

    VectorOfmodule* modules_;

  };

  class instance_arrayFactory {
  friend Serializer;
  public:
  static instance_array* make() {
    instance_array* obj = new instance_array();
    objects_.push_back(obj);
    return obj;
  }
  private:
    static std::vector<instance_array*> objects_;
  };
 	      
  class VectorOfinstance_arrayFactory {
  friend Serializer;
  public:
  static std::vector<instance_array*>* make() {
    std::vector<instance_array*>* obj = new std::vector<instance_array*>();
    objects_.push_back(obj);
    return obj;
  }
  private:
  static std::vector<std::vector<instance_array*>*> objects_;
  };

};

#endif

