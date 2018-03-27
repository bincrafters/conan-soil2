from conans import ConanFile, CMake
from conans.tools import download, unzip
import shutil


class SOIL2Conan(ConanFile):
    name = "SOIL2"
    version = "387a4b1269e6"
    license = "Public Domain"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    url = "https://github.com/inexorgame/conan-soil2"
    build_policy = "missing"
    folder_name = "SpartanJ-soil2-{}".format(version)
    exports = "CMakeLists.txt"

#    def config_options(self):
 #       del self.settings.compiler.libcxx

    def source(self):
        # Download SOIL2
        zip_name = "default.tar.gz"
        download("https://bitbucket.org/SpartanJ/soil2/get/387a4b1269e6.tar.gz", zip_name)
        unzip(zip_name)
        # Copy CMakelists.txt
        shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.folder_name)


    def build(self):
        cmake = CMake(self)
        self.run("cmake {} {}".format(self.folder_name, cmake.command_line))
        self.run("cmake --build . {}".format(cmake.build_config))

    def package(self):
        self.copy("*.h", dst="include/SOIL2", src="{}/src/SOIL2/".format(self.folder_name))
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ['include']
        self.cpp_info.libs = ["SOIL2"]

