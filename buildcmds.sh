#!/bin/bash

INSTALL_SUFFIX=$UHDM_INSTALL_PREFIX

if [ -z "$INSTALL_SUFFIX" ] ; then
   echo "INSTALL_SUFFIX is unset. Setting it to default 'install'"
   INSTALL_SUFFIX="install"
fi

INSTALL_PREFIX=`realpath $INSTALL_SUFFIX`
echo "INSTALL_PREFIX = $INSTALL_PREFIX"

uhdm_build_debug() {
  mkdir -p builds/Debug
  pushd builds/Debug
  cmake ../../ -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX/Debug"
  cmake --build .
  popd
}

uhdm_build_release() {
  mkdir -p builds/Release
  pushd builds/Release
  cmake ../../ -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX/Release"
  cmake --build .
  popd
}

uhdm_build_all() {
  uhdm_build_debug
  uhdm_build_release
}

uhdm_clean_debug() {
  rm -rf builds/Debug
}

uhdm_clean_release() {
  rm -rf builds/Release
}

uhdm_clean_all() {
  uhdm_clean_debug
  uhdm_clean_release
  rm -f src/*
  rm -rf headers/*
}

uhdm_install_debug() {
  mkdir -p builds/Debug
  pushd builds/Debug
  cmake ../../ -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX/Debug"
  cmake --build . --target install
  popd
}

uhdm_install_release() {
  mkdir -p builds/Release
  pushd builds/Release
  cmake ../../ -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX/Release"
  cmake --build . --target install
  popd
}

uhdm_install_all() {
  uhdm_install_debug
  uhdm_install_release
}

uhdm_uninstall_debug() {
  rm -rf "${INSTALL_PREFIX}/Debug"
}

uhdm_uninstall_release() {
  rm -rf "${INSTALL_PREFIX}/Release"
}

uhdm_uninstall_all() {
  uhdm_uninstall_debug
  uhdm_uninstall_release
}

uhdm_test_debug_unix() {
  mkdir -p builds/Debug
  pushd builds/Debug
  cmake ../../ -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX/Debug"
  cmake --build . --target UnitTests
  ctest --output-on-failure
  popd
}

uhdm_test_release_unix() {
  mkdir -p builds/Release
  pushd builds/Release
  cmake ../../ -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX/Release"
  cmake --build . --target UnitTests
  ctest --output-on-failure
  popd
}

uhdm_test_debug_windows() {
  mkdir -p builds/Debug
  pushd builds/Debug
  cmake ../../ -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX/Debug"
  cmake --build . --target UnitTests
  popd
}

uhdm_test_release_windows() {
  mkdir -p builds/Release
  pushd builds/Release
  cmake ../../ -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$INSTALL_PREFIX/Release"
  cmake --build . --target UnitTests
  popd
}

uhdm_test_junit_debug() {
  uhdm_build_debug
  pushd builds/Debug
  ctest --no-compress-output -T Test -C RelWithDebInfo --output-on-failure
  xsltproc .github/kokoro/ctest2junit.xsl builds/Debug/Testing/*/Test.xml > builds/Debug/test_results.xml
  popd
}

uhdm_test_junit_release() {
  uhdm_build_release
  pushd builds/Release
  ctest --no-compress-output -T Test -C RelWithDebInfo --output-on-failure
  xsltproc .github/kokoro/ctest2junit.xsl builds/Release/Testing/*/Test.xml > builds/Release/test_results.xml
  popd
}

uhdm_test_install_debug() {
  uhdm_build_debug
  pushd builds/Debug
  ${CXX} -std=c++14 -g ../../tests/test1.cpp \
    -I${INSTALL_PREFIX}/Debug/include/uhdm \
    -I${INSTALL_PREFIX}/Debug/include/uhdm/include \
    ${INSTALL_PREFIX}/Debug/lib/uhdm/libuhdm.a \
    ${INSTALL_PREFIX}/Debug/lib/uhdm/libcapnp.a \
    ${INSTALL_PREFIX}/Debug/lib/uhdm/libkj.a \
    -ldl -lutil -lm -lrt -lpthread -o test_inst
  ./test_inst
  popd
}

uhdm_test_install_release() {
  uhdm_build_release
  pushd builds/Release
  ${CXX} -std=c++14 -g ../../tests/test1.cpp \
    -I${INSTALL_PREFIX}/Release/include/uhdm \
    -I${INSTALL_PREFIX}/Release/include/uhdm/include \
    ${INSTALL_PREFIX}/Release/lib/uhdm/libuhdm.a \
    ${INSTALL_PREFIX}/Release/lib/uhdm/libcapnp.a \
    ${INSTALL_PREFIX}/Release/lib/uhdm/libkj.a \
    -ldl -lutil -lm -lrt -lpthread -o test_inst
  ./test_inst
  popd
}

"$@"
