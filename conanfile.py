from conans import ConanFile, CMake, tools
import os


class SOIL2Conan(ConanFile):
    name = "SOIL2"
    version = "387a4b1269e6"
    license = "Public Domain"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/inexorgame/conan-soil2"
    homepage = "https://bitbucket.org/SpartanJ/soil2"
    author = "Inexor <info@inexor.org>"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

#    def config_options(self):
 #       del self.settings.compiler.libcxx

    def source(self):
        archive_url = "https://bitbucket.org/SpartanJ/soil2/get/{}.tar.gz".format(self.version)
        tools.get(archive_url, sha256="69e37f9c9f335a4cc2a546537dee5d556fc3fe97b185a914b0e63f90427b5353")
        extracted_dir = "SpartanJ-soil2-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include/SOIL2", src="{}/src/SOIL2/".format(self.source_subfolder))
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["SOIL2"]
