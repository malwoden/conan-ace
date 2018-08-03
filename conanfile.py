from __future__ import print_function
from conans import ConanFile, AutoToolsBuildEnvironment, MSBuild, tools
from conans.tools import cpu_count
import re, glob

class AceConan(ConanFile):
    name = "ace"
    version = "6.4.6"
    license = "ACE has its own liberal license, somewhat like MIT or BSD"
    url = "https://github.com/malwoden/conan-ace"
    description = "ACE is a cpp utility framework focused on concurrent communication software"
    settings = "os", "compiler", "build_type", "arch"

    options = {"shared": [True, False],
               "openssl": [True, False],
               "openssl11": [True, False],
               "hasTokensLibrary": [True, False],
               "usesWchar": [True, False]}
    default_options = ("shared=False",
                       "openssl=False",
                       "openssl11=False",
                       "OpenSSL:shared=True",
                       "hasTokensLibrary=False",
                       "usesWchar=False")

    def configure(self):
        if self.options.openssl and self.options.openssl11:
            raise tools.ConanException("Cannot build with openssl and openssl11 flags")

        if self.options.usesWchar and self.settings.os != "Windows":
            self.options.usesWchar = False

    def build_requirements(self):
        if self.settings.os == "Windows":
            self.build_requires("strawberryperl/5.26.0@conan/stable")

    def requirements(self):
        if self.options.openssl:
            self.requires("OpenSSL/1.0.2n@conan/stable")
        if self.options.openssl11:
            self.requires("OpenSSL/1.1.0g@conan/stable")

    def source(self):
        extension = "zip" if self.settings.os == "Windows" else "tar.gz"

        tools.get("https://github.com/DOCGroup/ACE_TAO/releases/download/ACE+TAO-%s/ACE.%s" % (self.version.replace('.', '_'), extension))

    def build_config_file_for_options(self):
        contents = ""
        if self.options.hasTokensLibrary:
            contents += "#define ACE_HAS_TOKENS_LIBRARY\n"

        if self.options.usesWchar:
            contents += "#define ACE_USES_WCHAR\n"

        return contents

    def write_config_file(self, ace_wrappers_path, platform):
        with open(ace_wrappers_path + "/ace/config.h", "w+") as f:
            f.write(self.build_config_file_for_options())
            f.write("#include \"ace/config-%s.h\"" % platform)

    def build_unix(self, ace_wrappers_path_abs):
        env_build = AutoToolsBuildEnvironment(self)

        with tools.environment_append(env_build.vars):
            with tools.environment_append({"ACE_ROOT": ace_wrappers_path_abs}):
                with tools.chdir(ace_wrappers_path_abs):
                    install_location = ace_wrappers_path_abs + "/build_install"
                    tools.mkdir(install_location)

                    platform = "linux" if self.settings.os == "Linux" else "macosx"
                    self.write_config_file(ace_wrappers_path_abs, platform)

                    with open("%s/include/makeinclude/platform_macros.GNU" % ace_wrappers_path_abs, "w+") as f:
                        file_strings = []
                        file_strings.append("INSTALL_PREFIX = " + install_location)
                        file_strings.append("ssl=1" if self.options.openssl or self.options.openssl11 else "ssl=0")
                        file_strings.append("shared_libs_only=1" if self.options.shared else "static_libs_only=1")
                        file_strings.append("buildbits=32" if self.settings.arch == "x86" else "buildbits=64")
                        file_strings.append("debug=1" if self.settings.build_type == "Debug" else "optimize=1")
                        file_strings.append("include %s/include/makeinclude/platform_%s.GNU" % (ace_wrappers_path_abs, platform))
                        f.writelines(line + '\n' for line in file_strings)

                    openssl_include_path = ""
                    if self.options.openssl or self.options.openssl11:
                        openssl_include_path = self.deps_cpp_info["OpenSSL"].include_paths[0]

                    self.run("$ACE_ROOT/bin/mwc.pl -type gnuace ACE.mwc")
                    with tools.chdir("ace"):
                        if self.options.openssl or self.options.openssl11:
                            self.run("CFLAGS=\"-I%s\" make ACE SSL -j %s && make install" % (openssl_include_path, str(cpu_count())))
                        else:
                            self.run("make ACE -j %s && make install" % str(cpu_count()))

    def msvc_compiler_to_mwc_type(self):
        return {
            "10": "vc10",
            "11": "vc11",
            "12": "vc12",
            "14": "vc14",
            "15": "vs2017"
        }[str(self.settings.compiler.version)]

    def build_windows_msvc(self, ace_wrappers_path_abs):
        openssl_include_path = ""
        if self.options.openssl or self.options.openssl11:
            openssl_include_path = self.deps_cpp_info["OpenSSL"].rootpath

        with tools.environment_append(
                {"ACE_ROOT": ace_wrappers_path_abs,
                 "SSL_ROOT": openssl_include_path,
                 "CL": "/MP%s" % str(cpu_count())}):

            with tools.chdir(ace_wrappers_path_abs):
                self.write_config_file(ace_wrappers_path_abs, "win32")

                with open("%s/bin/MakeProjectCreator/config/default.features" % ace_wrappers_path_abs, "w+") as f:
                    file_strings = []
                    file_strings.append("ssl=1" if self.options.openssl or self.options.openssl11 else "ssl=0")
                    file_strings.append("openssl11=1" if self.options.openssl11 else "openssl11=0")
                    f.writelines(line + '\n' for line in file_strings)

                with tools.chdir("ace"):
                    self.run("perl %%ACE_ROOT%%/bin/mwc.pl -type %s %s ACE.mwc"
                        % (self.msvc_compiler_to_mwc_type(), "" if self.options.shared else "-static"))

                    build_targets = ["ACE"]

                    if self.options.openssl or self.options.openssl11:
                        build_targets.append("SSL")

                    msbuild = MSBuild(self)
                    msbuild.build("ACE.sln", targets=build_targets, upgrade_project=True,
                        platforms={'x86': 'Win32', 'x86_64': 'x64'}, parallel=False)

    def build(self):
        ace_wrappers_path_abs = self.source_folder + "/ACE_wrappers"

        if self.settings.os == "Linux" or self.settings.os == "Macos":
            self.build_unix(ace_wrappers_path_abs)
        elif self.settings.os == "Windows":
            self.build_windows_msvc(ace_wrappers_path_abs)

    # ACE includes cpp files from header files, so we need to find those files
    # and add them to the include path files
    def copy_include_cpp_files(self, ace_wrappers_path):
        pattern = re.compile(r"#pragma implementation \(\"(.*)\"\)$")

        for filename in glob.iglob(ace_wrappers_path + "/ace/*.h"):
            for _, line in enumerate(open(filename)):
                for match in re.finditer(pattern, line):
                    self.copy(match.groups()[0], dst="include/ace", src=ace_wrappers_path + "/ace")

    def package(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            install_src_abs = self.source_folder + "/ACE_wrappers/build_install"
            self.copy("*.h", dst="include", src=install_src_abs + "/include")
            # ace has template funcs in cpp files included in header files
            self.copy("*.cpp", dst="include", src=install_src_abs + "/include")
            self.copy("*.inl", dst="include", src=install_src_abs + "/include")
            self.copy("*.so*", dst="lib", src=install_src_abs + "/lib", keep_path=False)
            self.copy("*.dylib", dst="lib", keep_path=False)
            self.copy("*.a*", dst="lib",  src=install_src_abs + "/lib", keep_path=False)
        elif self.settings.os == "Windows":
            ace_src_path = self.source_folder + "/ACE_wrappers"
            ace_lib_path = ace_src_path + "/lib"

            static_lib_name = "ACEs.lib" if self.settings.build_type == "Release" else "ACEsd.lib"
            # No install target for windows builds, so we have to construct the package manually
            self.copy("*.h", dst="include/ace", src=ace_src_path + "/ace")
            self.copy("*.inl", dst="include/ace", src=ace_src_path + "/ace")
            self.copy("*.lib" if self.options.shared else static_lib_name, dst="lib", src=ace_lib_path, keep_path=False)
            self.copy("*.dll", dst="bin", src=ace_lib_path)
            self.copy_include_cpp_files(ace_src_path)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if not self.options.shared:
            self.cpp_info.defines = ["ACE_AS_STATIC_LIBS"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("dl")
            self.cpp_info.cppflags = ["-pthread"]