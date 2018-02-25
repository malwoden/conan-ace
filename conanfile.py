from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class AceConan(ConanFile):
    name = "ace"
    version = "6.4.6"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Ace here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    def source(self):
        tools.get("https://github.com/DOCGroup/ACE_TAO/releases/download/ACE+TAO-%s/ACE-src.tar.gz" % self.version.replace('.', '_'))

#     def source(self):
#         self.run("git clone https://github.com/memsharded/hello.git")
#         self.run("cd hello && git checkout static_shared")
#         # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
#         # if the packaged project doesn't have variables to set it properly
#         tools.replace_in_file("hello/CMakeLists.txt", "PROJECT(MyHello)", '''PROJECT(MyHello)
# include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
# conan_basic_setup()''')

    def build(self):
        ace_wrappers_path_abs = self.source_folder + "/ACE_wrappers"

        if self.settings.os == "Linux":
            env_build = AutoToolsBuildEnvironment(self)
            # for the scope of the 'with' add the autotools env vars to the current context
            with tools.environment_append(env_build.vars):
                with tools.environment_append({"ACE_ROOT": ace_wrappers_path_abs}):
                    with tools.chdir(ace_wrappers_path_abs):
                        install_location = ace_wrappers_path_abs + "/build_install"
                        tools.mkdir(install_location)

                        with open("%s/ace/config.h" % ace_wrappers_path_abs, "w+") as f:
                            f.write("#include \"ace/config-linux.h\"")

                        with open("%s/include/makeinclude/platform_macros.GNU" % ace_wrappers_path_abs, "w+") as f:
                            f.write("INSTALL_PREFIX = " + install_location)
                            f.write("\ninclude %s/include/makeinclude/platform_linux.GNU" % ace_wrappers_path_abs)

                        self.run("$ACE_ROOT/bin/mwc.pl -type gnuace ACE.mwc")
                        with tools.chdir("ace"):
                            self.run("make -j4 && make install")
        else:
            raise tools.ConanException("Build not setup for %s" % self.settings.os)

        # Explicit way:
        # self.run('cmake %s/hello %s' % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        install_src_abs = self.source_folder + "/ACE_wrappers/build_install"
        self.copy("*", dst="include", src=install_src_abs + "/include")
        self.copy("*", dst="lib", src=install_src_abs + "/lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Linux":
            self.cpp_info.libs = tools.collect_libs(self)
            # self.cpp_info.libs = ["libACE_Compression.so", "libACE_ETCL_Parser.so", "libACE_ETCL.so", "libACE_Monitor_Control", "libACE_RLECompression", "libACE.so"]
 