@0xfff7299129556877;

struct ObjIndexType {
   index @0 : UInt64;
   type  @1 : UInt32;
}

struct UhdmRoot {
  designs @0 : List(Design);
  symbols @1 : List(Text);
  factoryProcess @2 :List(Process);
  factoryPropertydecl @3 :List(Propertydecl);
  factorySequencedecl @4 :List(Sequencedecl);
  factoryVirtualinterfacevar @5 :List(Virtualinterfacevar);
  factoryLetdecl @6 :List(Letdecl);
  factoryBegin @7 :List(Begin);
  factoryNamedbegin @8 :List(Namedbegin);
  factoryNamedfork @9 :List(Namedfork);
  factoryForkstmt @10 :List(Forkstmt);
  factoryForstmt @11 :List(Forstmt);
  factoryForeachstmt @12 :List(Foreachstmt);
  factoryGenscope @13 :List(Genscope);
  factoryDistribution @14 :List(Distribution);
  factoryOperation @15 :List(Operation);
  factoryPartselect @16 :List(Partselect);
  factoryRefobj @17 :List(Refobj);
  factoryTask @18 :List(Task);
  factoryFunction @19 :List(Function);
  factoryModport @20 :List(Modport);
  factoryInterfacetfdecl @21 :List(Interfacetfdecl);
  factoryContassign @22 :List(Contassign);
  factoryPort @23 :List(Port);
  factoryPortbit @24 :List(Portbit);
  factoryPrimitive @25 :List(Primitive);
  factoryModpath @26 :List(Modpath);
  factoryTchk @27 :List(Tchk);
  factoryDefparam @28 :List(Defparam);
  factoryRange @29 :List(Range);
  factoryUdpdefn @30 :List(Udpdefn);
  factoryIodecl @31 :List(Iodecl);
  factoryAliasstmt @32 :List(Aliasstmt);
  factoryClockingblock @33 :List(Clockingblock);
  factoryParamassign @34 :List(Paramassign);
  factoryInterfacearray @35 :List(Interfacearray);
  factoryProgramarray @36 :List(Programarray);
  factoryModulearray @37 :List(Modulearray);
  factoryGatearray @38 :List(Gatearray);
  factorySwitcharray @39 :List(Switcharray);
  factoryUdparray @40 :List(Udparray);
  factoryArraynet @41 :List(Arraynet);
  factoryLogicvar @42 :List(Logicvar);
  factoryArrayvar @43 :List(Arrayvar);
  factoryNamedevent @44 :List(Namedevent);
  factoryNamedeventarray @45 :List(Namedeventarray);
  factorySpecparam @46 :List(Specparam);
  factoryClassdefn @47 :List(Classdefn);
  factoryClasstypespec @48 :List(Classtypespec);
  factoryClassobj @49 :List(Classobj);
  factoryInterface @50 :List(Interface);
  factoryProgram @51 :List(Program);
  factoryPackage @52 :List(Package);
  factoryModule @53 :List(Module);
  factoryDesign @54 :List(Design);

}


struct Process {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Propertydecl {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Sequencedecl {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Virtualinterfacevar {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Letdecl {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Begin {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
stmts @4 :List(ObjIndexType);
vpiName @5 :UInt64;
vpiFullName @6 :UInt64;
concurrentassertions @7 :List(ObjIndexType);
variables @8 :List(ObjIndexType);
parameters @9 :List(ObjIndexType);
scopes @10 :List(ObjIndexType);
typespecs @11 :List(ObjIndexType);
propertydecls @12 :List(UInt64);
sequencedecls @13 :List(UInt64);
namedevents @14 :List(UInt64);
namedeventarrays @15 :List(UInt64);
virtualinterfacevars @16 :List(UInt64);
logicvar @17 :List(UInt64);
arrayvar @18 :List(UInt64);
arrayvarmem @19 :List(UInt64);
letdecls @20 :List(UInt64);
instanceitems @21 :List(ObjIndexType);
}
struct Namedbegin {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
stmts @4 :List(ObjIndexType);
vpiName @5 :UInt64;
vpiFullName @6 :UInt64;
concurrentassertions @7 :List(ObjIndexType);
variables @8 :List(ObjIndexType);
parameters @9 :List(ObjIndexType);
scopes @10 :List(ObjIndexType);
typespecs @11 :List(ObjIndexType);
propertydecls @12 :List(UInt64);
sequencedecls @13 :List(UInt64);
namedevents @14 :List(UInt64);
namedeventarrays @15 :List(UInt64);
virtualinterfacevars @16 :List(UInt64);
logicvar @17 :List(UInt64);
arrayvar @18 :List(UInt64);
arrayvarmem @19 :List(UInt64);
letdecls @20 :List(UInt64);
instanceitems @21 :List(ObjIndexType);
}
struct Namedfork {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiJoinType @4 :Int64;
stmts @5 :List(ObjIndexType);
vpiName @6 :UInt64;
vpiFullName @7 :UInt64;
concurrentassertions @8 :List(ObjIndexType);
variables @9 :List(ObjIndexType);
parameters @10 :List(ObjIndexType);
scopes @11 :List(ObjIndexType);
typespecs @12 :List(ObjIndexType);
propertydecls @13 :List(UInt64);
sequencedecls @14 :List(UInt64);
namedevents @15 :List(UInt64);
namedeventarrays @16 :List(UInt64);
virtualinterfacevars @17 :List(UInt64);
logicvar @18 :List(UInt64);
arrayvar @19 :List(UInt64);
arrayvarmem @20 :List(UInt64);
letdecls @21 :List(UInt64);
instanceitems @22 :List(ObjIndexType);
}
struct Forkstmt {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiJoinType @4 :Int64;
stmts @5 :List(ObjIndexType);
vpiName @6 :UInt64;
vpiFullName @7 :UInt64;
concurrentassertions @8 :List(ObjIndexType);
variables @9 :List(ObjIndexType);
parameters @10 :List(ObjIndexType);
scopes @11 :List(ObjIndexType);
typespecs @12 :List(ObjIndexType);
propertydecls @13 :List(UInt64);
sequencedecls @14 :List(UInt64);
namedevents @15 :List(UInt64);
namedeventarrays @16 :List(UInt64);
virtualinterfacevars @17 :List(UInt64);
logicvar @18 :List(UInt64);
arrayvar @19 :List(UInt64);
arrayvarmem @20 :List(UInt64);
letdecls @21 :List(UInt64);
instanceitems @22 :List(ObjIndexType);
}
struct Forstmt {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiName @4 :UInt64;
vpiFullName @5 :UInt64;
concurrentassertions @6 :List(ObjIndexType);
variables @7 :List(ObjIndexType);
parameters @8 :List(ObjIndexType);
scopes @9 :List(ObjIndexType);
typespecs @10 :List(ObjIndexType);
propertydecls @11 :List(UInt64);
sequencedecls @12 :List(UInt64);
namedevents @13 :List(UInt64);
namedeventarrays @14 :List(UInt64);
virtualinterfacevars @15 :List(UInt64);
logicvar @16 :List(UInt64);
arrayvar @17 :List(UInt64);
arrayvarmem @18 :List(UInt64);
letdecls @19 :List(UInt64);
instanceitems @20 :List(ObjIndexType);
}
struct Foreachstmt {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiName @4 :UInt64;
vpiFullName @5 :UInt64;
concurrentassertions @6 :List(ObjIndexType);
variables @7 :List(ObjIndexType);
parameters @8 :List(ObjIndexType);
scopes @9 :List(ObjIndexType);
typespecs @10 :List(ObjIndexType);
propertydecls @11 :List(UInt64);
sequencedecls @12 :List(UInt64);
namedevents @13 :List(UInt64);
namedeventarrays @14 :List(UInt64);
virtualinterfacevars @15 :List(UInt64);
logicvar @16 :List(UInt64);
arrayvar @17 :List(UInt64);
arrayvarmem @18 :List(UInt64);
letdecls @19 :List(UInt64);
instanceitems @20 :List(ObjIndexType);
}
struct Genscope {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiName @4 :UInt64;
vpiFullName @5 :UInt64;
concurrentassertions @6 :List(ObjIndexType);
variables @7 :List(ObjIndexType);
parameters @8 :List(ObjIndexType);
scopes @9 :List(ObjIndexType);
typespecs @10 :List(ObjIndexType);
propertydecls @11 :List(UInt64);
sequencedecls @12 :List(UInt64);
namedevents @13 :List(UInt64);
namedeventarrays @14 :List(UInt64);
virtualinterfacevars @15 :List(UInt64);
logicvar @16 :List(UInt64);
arrayvar @17 :List(UInt64);
arrayvarmem @18 :List(UInt64);
letdecls @19 :List(UInt64);
instanceitems @20 :List(ObjIndexType);
}
struct Distribution {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Operation {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiOpType @4 :Int64;
operands @5 :List(ObjIndexType);
vpiDecompile @6 :UInt64;
vpiSize @7 :Int64;
}
struct Partselect {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Refobj {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiName @4 :UInt64;
vpiFullName @5 :UInt64;
vpiDefName @6 :UInt64;
vpiGeneric @7 :Bool;
ports @8 :List(ObjIndexType);
typespec @9 :ObjIndexType;
instance @10 :ObjIndexType;
taskfunc @11 :ObjIndexType;
actualgroup @12 :ObjIndexType;
}
struct Task {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiMethod @4 :Bool;
vpiAccessType @5 :Int64;
vpiVisibility @6 :Int64;
vpiVirtual @7 :Bool;
vpiAutomatic @8 :Bool;
vpiDPIContext @9 :Bool;
vpiDPICStr @10 :Int64;
vpiDPICIdentifier @11 :UInt64;
leftexpr @12 :ObjIndexType;
rightexpr @13 :ObjIndexType;
stmt @14 :ObjIndexType;
classdefn @15 :UInt64;
refobj @16 :UInt64;
iodecl @17 :UInt64;
vpiName @18 :UInt64;
vpiFullName @19 :UInt64;
concurrentassertions @20 :List(ObjIndexType);
variables @21 :List(ObjIndexType);
parameters @22 :List(ObjIndexType);
scopes @23 :List(ObjIndexType);
typespecs @24 :List(ObjIndexType);
propertydecls @25 :List(UInt64);
sequencedecls @26 :List(UInt64);
namedevents @27 :List(UInt64);
namedeventarrays @28 :List(UInt64);
virtualinterfacevars @29 :List(UInt64);
logicvar @30 :List(UInt64);
arrayvar @31 :List(UInt64);
arrayvarmem @32 :List(UInt64);
letdecls @33 :List(UInt64);
instanceitems @34 :List(ObjIndexType);
}
struct Function {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiSigned @4 :Bool;
vpiSize @5 :Int64;
vpiFuncType @6 :Int64;
vpiMethod @7 :Bool;
vpiAccessType @8 :Int64;
vpiVisibility @9 :Int64;
vpiVirtual @10 :Bool;
vpiAutomatic @11 :Bool;
vpiDPIContext @12 :Bool;
vpiDPICStr @13 :Int64;
vpiDPICIdentifier @14 :UInt64;
leftexpr @15 :ObjIndexType;
rightexpr @16 :ObjIndexType;
stmt @17 :ObjIndexType;
classdefn @18 :UInt64;
refobj @19 :UInt64;
iodecl @20 :UInt64;
vpiName @21 :UInt64;
vpiFullName @22 :UInt64;
concurrentassertions @23 :List(ObjIndexType);
variables @24 :List(ObjIndexType);
parameters @25 :List(ObjIndexType);
scopes @26 :List(ObjIndexType);
typespecs @27 :List(ObjIndexType);
propertydecls @28 :List(UInt64);
sequencedecls @29 :List(UInt64);
namedevents @30 :List(UInt64);
namedeventarrays @31 :List(UInt64);
virtualinterfacevars @32 :List(UInt64);
logicvar @33 :List(UInt64);
arrayvar @34 :List(UInt64);
arrayvarmem @35 :List(UInt64);
letdecls @36 :List(UInt64);
instanceitems @37 :List(ObjIndexType);
}
struct Modport {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiName @4 :UInt64;
iodecls @5 :List(UInt64);
interface @6 :UInt64;
}
struct Interfacetfdecl {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiAccessType @4 :UInt64;
tasks @5 :List(UInt64);
functions @6 :List(UInt64);
}
struct Contassign {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Port {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
bits @4 :List(UInt64);
vpiPortIndex @5 :UInt64;
vpiName @6 :UInt64;
vpiPortType @7 :UInt64;
vpiScalar @8 :Bool;
vpiVector @9 :Bool;
vpiConnByName @10 :Bool;
vpiDirection @11 :UInt64;
vpiSize @12 :UInt64;
vpiExplicitName @13 :UInt64;
typespecs @14 :ObjIndexType;
instance @15 :ObjIndexType;
module @16 :UInt64;
highconn @17 :ObjIndexType;
lowconn @18 :ObjIndexType;
}
struct Portbit {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiPortIndex @4 :UInt64;
vpiName @5 :UInt64;
vpiPortType @6 :UInt64;
vpiScalar @7 :Bool;
vpiVector @8 :Bool;
vpiConnByName @9 :Bool;
vpiDirection @10 :UInt64;
vpiSize @11 :UInt64;
vpiExplicitName @12 :UInt64;
typespecs @13 :ObjIndexType;
instance @14 :ObjIndexType;
module @15 :UInt64;
highconn @16 :ObjIndexType;
lowconn @17 :ObjIndexType;
}
struct Primitive {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Modpath {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Tchk {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Defparam {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Range {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Udpdefn {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Iodecl {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiDirection @4 :Int64;
vpiName @5 :UInt64;
vpiScalar @6 :Bool;
vpiSigned @7 :Bool;
vpiSize @8 :Int64;
vpiVector @9 :Bool;
leftexpr @10 :ObjIndexType;
rightexpr @11 :ObjIndexType;
typespecs @12 :ObjIndexType;
instance @13 :ObjIndexType;
taskfunc @14 :ObjIndexType;
ranges @15 :List(UInt64);
udpdefn @16 :UInt64;
module @17 :UInt64;
expr @18 :ObjIndexType;
}
struct Aliasstmt {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Clockingblock {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiName @4 :UInt64;
vpiFullName @5 :UInt64;
concurrentassertions @6 :List(ObjIndexType);
variables @7 :List(ObjIndexType);
parameters @8 :List(ObjIndexType);
scopes @9 :List(ObjIndexType);
typespecs @10 :List(ObjIndexType);
propertydecls @11 :List(UInt64);
sequencedecls @12 :List(UInt64);
namedevents @13 :List(UInt64);
namedeventarrays @14 :List(UInt64);
virtualinterfacevars @15 :List(UInt64);
logicvar @16 :List(UInt64);
arrayvar @17 :List(UInt64);
arrayvarmem @18 :List(UInt64);
letdecls @19 :List(UInt64);
instanceitems @20 :List(ObjIndexType);
}
struct Paramassign {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Interfacearray {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
paramassigns @4 :List(UInt64);
vpiName @5 :UInt64;
vpiFullName @6 :UInt64;
vpiSize @7 :Int64;
expr @8 :ObjIndexType;
leftexpr @9 :ObjIndexType;
rightexpr @10 :ObjIndexType;
instances @11 :List(ObjIndexType);
range @12 :UInt64;
modules @13 :List(UInt64);
}
struct Programarray {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiName @4 :UInt64;
vpiFullName @5 :UInt64;
vpiSize @6 :Int64;
expr @7 :ObjIndexType;
leftexpr @8 :ObjIndexType;
rightexpr @9 :ObjIndexType;
instances @10 :List(ObjIndexType);
range @11 :UInt64;
modules @12 :List(UInt64);
}
struct Modulearray {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
paramassigns @4 :List(UInt64);
vpiName @5 :UInt64;
vpiFullName @6 :UInt64;
vpiSize @7 :Int64;
expr @8 :ObjIndexType;
leftexpr @9 :ObjIndexType;
rightexpr @10 :ObjIndexType;
instances @11 :List(ObjIndexType);
range @12 :UInt64;
modules @13 :List(UInt64);
}
struct Gatearray {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
delay @4 :ObjIndexType;
primitives @5 :List(ObjIndexType);
vpiName @6 :UInt64;
vpiFullName @7 :UInt64;
vpiSize @8 :Int64;
expr @9 :ObjIndexType;
leftexpr @10 :ObjIndexType;
rightexpr @11 :ObjIndexType;
instances @12 :List(ObjIndexType);
range @13 :UInt64;
modules @14 :List(UInt64);
}
struct Switcharray {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
delay @4 :ObjIndexType;
primitives @5 :List(ObjIndexType);
vpiName @6 :UInt64;
vpiFullName @7 :UInt64;
vpiSize @8 :Int64;
expr @9 :ObjIndexType;
leftexpr @10 :ObjIndexType;
rightexpr @11 :ObjIndexType;
instances @12 :List(ObjIndexType);
range @13 :UInt64;
modules @14 :List(UInt64);
}
struct Udparray {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
delay @4 :ObjIndexType;
primitives @5 :List(ObjIndexType);
vpiName @6 :UInt64;
vpiFullName @7 :UInt64;
vpiSize @8 :Int64;
expr @9 :ObjIndexType;
leftexpr @10 :ObjIndexType;
rightexpr @11 :ObjIndexType;
instances @12 :List(ObjIndexType);
range @13 :UInt64;
modules @14 :List(UInt64);
}
struct Arraynet {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Logicvar {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Arrayvar {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Namedevent {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Namedeventarray {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Specparam {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
}
struct Classdefn {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiName @4 :UInt64;
vpiFullName @5 :UInt64;
concurrentassertions @6 :List(ObjIndexType);
variables @7 :List(ObjIndexType);
parameters @8 :List(ObjIndexType);
scopes @9 :List(ObjIndexType);
typespecs @10 :List(ObjIndexType);
propertydecls @11 :List(UInt64);
sequencedecls @12 :List(UInt64);
namedevents @13 :List(UInt64);
namedeventarrays @14 :List(UInt64);
virtualinterfacevars @15 :List(UInt64);
logicvar @16 :List(UInt64);
arrayvar @17 :List(UInt64);
arrayvarmem @18 :List(UInt64);
letdecls @19 :List(UInt64);
instanceitems @20 :List(ObjIndexType);
}
struct Classtypespec {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiName @4 :UInt64;
vpiFullName @5 :UInt64;
concurrentassertions @6 :List(ObjIndexType);
variables @7 :List(ObjIndexType);
parameters @8 :List(ObjIndexType);
scopes @9 :List(ObjIndexType);
typespecs @10 :List(ObjIndexType);
propertydecls @11 :List(UInt64);
sequencedecls @12 :List(UInt64);
namedevents @13 :List(UInt64);
namedeventarrays @14 :List(UInt64);
virtualinterfacevars @15 :List(UInt64);
logicvar @16 :List(UInt64);
arrayvar @17 :List(UInt64);
arrayvarmem @18 :List(UInt64);
letdecls @19 :List(UInt64);
instanceitems @20 :List(ObjIndexType);
}
struct Classobj {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiName @4 :UInt64;
vpiFullName @5 :UInt64;
concurrentassertions @6 :List(ObjIndexType);
variables @7 :List(ObjIndexType);
parameters @8 :List(ObjIndexType);
scopes @9 :List(ObjIndexType);
typespecs @10 :List(ObjIndexType);
propertydecls @11 :List(UInt64);
sequencedecls @12 :List(UInt64);
namedevents @13 :List(UInt64);
namedeventarrays @14 :List(UInt64);
virtualinterfacevars @15 :List(UInt64);
logicvar @16 :List(UInt64);
arrayvar @17 :List(UInt64);
arrayvarmem @18 :List(UInt64);
letdecls @19 :List(UInt64);
instanceitems @20 :List(ObjIndexType);
}
struct Interface {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiIndex @4 :UInt64;
exprdist @5 :ObjIndexType;
instancearray @6 :ObjIndexType;
process @7 :List(ObjIndexType);
interfacetfdecls @8 :List(UInt64);
modports @9 :List(UInt64);
globalclocking @10 :UInt64;
defaultclocking @11 :UInt64;
modpaths @12 :List(UInt64);
contassigns @13 :List(UInt64);
interfaces @14 :List(UInt64);
interfacearrays @15 :List(UInt64);
vpiDefName @16 :UInt64;
vpiArrayMember @17 :Bool;
vpiCellInstance @18 :Bool;
vpiDefNetType @19 :Int64;
vpiDefFile @20 :UInt64;
vpiDefDelayMode @21 :Int64;
vpiProtected @22 :Bool;
vpiTimePrecision @23 :Int64;
vpiTimeUnit @24 :Int64;
vpiUnconnDrive @25 :Int64;
vpiLibrary @26 :UInt64;
vpiCell @27 :UInt64;
vpiConfig @28 :UInt64;
vpiAutomatic @29 :Bool;
vpiTop @30 :Bool;
taskfunc @31 :List(ObjIndexType);
net @32 :List(ObjIndexType);
arraynet @33 :List(ObjIndexType);
assertion @34 :List(ObjIndexType);
classdefn @35 :List(ObjIndexType);
instance @36 :ObjIndexType;
programs @37 :List(UInt64);
programarrays @38 :List(UInt64);
namedevent @39 :List(UInt64);
namedeventarray @40 :List(UInt64);
specparam @41 :List(UInt64);
module @42 :UInt64;
vpiName @43 :UInt64;
vpiFullName @44 :UInt64;
concurrentassertions @45 :List(ObjIndexType);
variables @46 :List(ObjIndexType);
parameters @47 :List(ObjIndexType);
scopes @48 :List(ObjIndexType);
typespecs @49 :List(ObjIndexType);
propertydecls @50 :List(UInt64);
sequencedecls @51 :List(UInt64);
namedevents @52 :List(UInt64);
namedeventarrays @53 :List(UInt64);
virtualinterfacevars @54 :List(UInt64);
logicvar @55 :List(UInt64);
arrayvar @56 :List(UInt64);
arrayvarmem @57 :List(UInt64);
letdecls @58 :List(UInt64);
instanceitems @59 :List(ObjIndexType);
}
struct Program {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiIndex @4 :UInt64;
instancearray @5 :ObjIndexType;
exprdist @6 :ObjIndexType;
process @7 :List(ObjIndexType);
defaultclocking @8 :UInt64;
interfaces @9 :List(UInt64);
interfacearrays @10 :List(UInt64);
contassigns @11 :List(UInt64);
clockingblocks @12 :List(UInt64);
vpiDefName @13 :UInt64;
vpiArrayMember @14 :Bool;
vpiCellInstance @15 :Bool;
vpiDefNetType @16 :Int64;
vpiDefFile @17 :UInt64;
vpiDefDelayMode @18 :Int64;
vpiProtected @19 :Bool;
vpiTimePrecision @20 :Int64;
vpiTimeUnit @21 :Int64;
vpiUnconnDrive @22 :Int64;
vpiLibrary @23 :UInt64;
vpiCell @24 :UInt64;
vpiConfig @25 :UInt64;
vpiAutomatic @26 :Bool;
vpiTop @27 :Bool;
taskfunc @28 :List(ObjIndexType);
net @29 :List(ObjIndexType);
arraynet @30 :List(ObjIndexType);
assertion @31 :List(ObjIndexType);
classdefn @32 :List(ObjIndexType);
instance @33 :ObjIndexType;
programs @34 :List(UInt64);
programarrays @35 :List(UInt64);
namedevent @36 :List(UInt64);
namedeventarray @37 :List(UInt64);
specparam @38 :List(UInt64);
module @39 :UInt64;
vpiName @40 :UInt64;
vpiFullName @41 :UInt64;
concurrentassertions @42 :List(ObjIndexType);
variables @43 :List(ObjIndexType);
parameters @44 :List(ObjIndexType);
scopes @45 :List(ObjIndexType);
typespecs @46 :List(ObjIndexType);
propertydecls @47 :List(UInt64);
sequencedecls @48 :List(UInt64);
namedevents @49 :List(UInt64);
namedeventarrays @50 :List(UInt64);
virtualinterfacevars @51 :List(UInt64);
logicvar @52 :List(UInt64);
arrayvar @53 :List(UInt64);
arrayvarmem @54 :List(UInt64);
letdecls @55 :List(UInt64);
instanceitems @56 :List(ObjIndexType);
}
struct Package {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiUnit @4 :Bool;
vpiDefName @5 :UInt64;
vpiArrayMember @6 :Bool;
vpiCellInstance @7 :Bool;
vpiDefNetType @8 :Int64;
vpiDefFile @9 :UInt64;
vpiDefDelayMode @10 :Int64;
vpiProtected @11 :Bool;
vpiTimePrecision @12 :Int64;
vpiTimeUnit @13 :Int64;
vpiUnconnDrive @14 :Int64;
vpiLibrary @15 :UInt64;
vpiCell @16 :UInt64;
vpiConfig @17 :UInt64;
vpiAutomatic @18 :Bool;
vpiTop @19 :Bool;
taskfunc @20 :List(ObjIndexType);
net @21 :List(ObjIndexType);
arraynet @22 :List(ObjIndexType);
assertion @23 :List(ObjIndexType);
classdefn @24 :List(ObjIndexType);
instance @25 :ObjIndexType;
programs @26 :List(UInt64);
programarrays @27 :List(UInt64);
namedevent @28 :List(UInt64);
namedeventarray @29 :List(UInt64);
specparam @30 :List(UInt64);
module @31 :UInt64;
vpiName @32 :UInt64;
vpiFullName @33 :UInt64;
concurrentassertions @34 :List(ObjIndexType);
variables @35 :List(ObjIndexType);
parameters @36 :List(ObjIndexType);
scopes @37 :List(ObjIndexType);
typespecs @38 :List(ObjIndexType);
propertydecls @39 :List(UInt64);
sequencedecls @40 :List(UInt64);
namedevents @41 :List(UInt64);
namedeventarrays @42 :List(UInt64);
virtualinterfacevars @43 :List(UInt64);
logicvar @44 :List(UInt64);
arrayvar @45 :List(UInt64);
arrayvarmem @46 :List(UInt64);
letdecls @47 :List(UInt64);
instanceitems @48 :List(ObjIndexType);
}
struct Module {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiIndex @4 :UInt64;
vpiTopModule @5 :Bool;
vpiDefDecayTime @6 :Int64;
exprdist @7 :ObjIndexType;
instancearray @8 :ObjIndexType;
process @9 :List(ObjIndexType);
primitives @10 :List(ObjIndexType);
primitivearrays @11 :List(ObjIndexType);
globalclocking @12 :UInt64;
defaultclocking @13 :UInt64;
modulearray @14 :UInt64;
ports @15 :List(UInt64);
interfaces @16 :List(UInt64);
interfacearrays @17 :List(UInt64);
contassigns @18 :List(UInt64);
modules @19 :List(UInt64);
modulearrays @20 :List(UInt64);
modpaths @21 :List(UInt64);
tchks @22 :List(UInt64);
defparams @23 :List(UInt64);
iodecls @24 :List(UInt64);
aliasstmts @25 :List(UInt64);
clockingblocks @26 :List(UInt64);
vpiDefName @27 :UInt64;
vpiArrayMember @28 :Bool;
vpiCellInstance @29 :Bool;
vpiDefNetType @30 :Int64;
vpiDefFile @31 :UInt64;
vpiDefDelayMode @32 :Int64;
vpiProtected @33 :Bool;
vpiTimePrecision @34 :Int64;
vpiTimeUnit @35 :Int64;
vpiUnconnDrive @36 :Int64;
vpiLibrary @37 :UInt64;
vpiCell @38 :UInt64;
vpiConfig @39 :UInt64;
vpiAutomatic @40 :Bool;
vpiTop @41 :Bool;
taskfunc @42 :List(ObjIndexType);
net @43 :List(ObjIndexType);
arraynet @44 :List(ObjIndexType);
assertion @45 :List(ObjIndexType);
classdefn @46 :List(ObjIndexType);
instance @47 :ObjIndexType;
programs @48 :List(UInt64);
programarrays @49 :List(UInt64);
namedevent @50 :List(UInt64);
namedeventarray @51 :List(UInt64);
specparam @52 :List(UInt64);
module @53 :UInt64;
vpiName @54 :UInt64;
vpiFullName @55 :UInt64;
concurrentassertions @56 :List(ObjIndexType);
variables @57 :List(ObjIndexType);
parameters @58 :List(ObjIndexType);
scopes @59 :List(ObjIndexType);
typespecs @60 :List(ObjIndexType);
propertydecls @61 :List(UInt64);
sequencedecls @62 :List(UInt64);
namedevents @63 :List(UInt64);
namedeventarrays @64 :List(UInt64);
virtualinterfacevars @65 :List(UInt64);
logicvar @66 :List(UInt64);
arrayvar @67 :List(UInt64);
arrayvarmem @68 :List(UInt64);
letdecls @69 :List(UInt64);
instanceitems @70 :List(ObjIndexType);
}
struct Design {
vpiParent @0 :UInt64;
uhdmParentType @1 :UInt64;
vpiFile @2 :UInt64;
vpiLineNo @3 :UInt32;
vpiName @4 :UInt64;
allModules @5 :List(UInt64);
topModules @6 :List(UInt64);
allPrograms @7 :List(UInt64);
allPackages @8 :List(UInt64);
}



