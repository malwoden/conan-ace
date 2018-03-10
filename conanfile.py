from __future__ import print_function
from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.tools import cpu_count

class AceConan(ConanFile):
    name = "ace"
    version = "6.4.6"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Ace here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "openssl": [True, False], "openssl11": [True, False]}
    default_options = "shared=False", "openssl=False", "openssl11=False", "OpenSSL:shared=True"

    def configure(self):
        if self.options.openssl and self.options.openssl11:
            raise tools.ConanException("Cannot build with openssl and openssl11 flags")

    def requirements(self):
        if self.options.openssl:
            self.requires("OpenSSL/1.0.2n@conan/stable")
        if self.options.openssl11:
            self.requires("OpenSSL/1.1.0g@conan/stable")

    def source(self):
        tools.get("https://github.com/DOCGroup/ACE_TAO/releases/download/ACE+TAO-%s/ACE-src.tar.gz" % self.version.replace('.', '_'))

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
                            file_strings = []
                            file_strings.append("INSTALL_PREFIX = " + install_location)
                            file_strings.append("ssl=1" if self.options.openssl else "ssl=0")
                            file_strings.append("shared_libs_only=1" if self.options.shared else "static_libs_only=1")
                            file_strings.append("buildbits=32" if self.settings.arch == "x86" else "buildbits=64")
                            file_strings.append("debug=1" if self.settings.build_type == "Debug" else "optimize=1")
                            file_strings.append("include %s/include/makeinclude/platform_linux.GNU" % ace_wrappers_path_abs)
                            f.writelines(line + '\n' for line in file_strings)

                        openssl_include_path = ""
                        if self.options.openssl or self.options.openssl11:
                            openssl_include_path = self.deps_cpp_info["OpenSSL"].include_paths[0]

                        self.run("$ACE_ROOT/bin/mwc.pl -type gnuace ACE.mwc")
                        with tools.chdir("ace"):
                            if self.options.openssl or self.options.openssl11:
                                self.run("CFLAGS=\"-I%s\" make -j %s && make install" % (openssl_include_path, str(cpu_count())))
                            else:
                                self.run("make -j %s && make install" % str(cpu_count()))
        else:
            # add openssl11=1 for windows ace builds
            raise tools.ConanException("Build not setup for %s" % self.settings.os)

    def package(self):
        install_src_abs = self.source_folder + "/ACE_wrappers/build_install"
        self.copy("*.h", dst="include", src=install_src_abs + "/include")
        # ace has template funcs in cpp files included in header files
        self.copy("*.cpp", dst="include", src=install_src_abs + "/include")
        self.copy("*.inl", dst="include", src=install_src_abs + "/include")
        self.copy("*.so*", dst="lib", src=install_src_abs + "/lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a*", dst="lib",  src=install_src_abs + "/lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Linux":
            self.cpp_info.libs = tools.collect_libs(self)
            self.cpp_info.cppflags = ["-pthread"]
            self.cpp_info.exelinkflags.append("-ldl")
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags