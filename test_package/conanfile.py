from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool
import os

class AceTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def system_requirements(self):
        pack_names = None
        if os_info.linux_distro == "ubuntu":
            pack_names = ["xutils-dev"]

        if pack_names:
            installer = SystemPackageTool()
            installer.update()
            installer.install(" ".join(pack_names))

    def build(self):
        cmake = CMake(self)

        if self.options["ace"].openssl or self.options["ace"].openssl11:
            cmake.definitions["WITH_SSL"] = "TRUE"

        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            self.run(".%sexample" % os.sep)
