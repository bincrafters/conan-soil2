from conans import ConanFile, tools, AutoToolsBuildEnvironment, MSBuild
import os


class soil2Conan(ConanFile):
    name = "soil2"
    version = "1.11"
    description = "Simple OpenGL Image Library 2"
    topics = ("conan", "soil2", "opengl", "images")
    url = "https://github.com/bincrafters/conan-soil2"
    homepage = "https://github.com/SpartanJ/SOIL2"
    author = "Inexor <info@inexor.org>"
    license = "Unlicense"  # Public Domain
    settings = "os", "arch", "compiler", "build_type"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    generators = "premake"
    exports_sources = ["premake5.lua"]

    def config_options(self):
        # Visual Studio users: SOIL2 will need to be compiled as C++ source ( at least the file etc1_utils.c ), since VC compiler doesn't support C99
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def build_requirements(self):
        if not tools.which("premake"):
            self.build_requires("premake_installer/5.0.0-alpha14@bincrafters/stable")
    
    def requirements(self):
        if self.settings.os == "Linux" and tools.os_info.is_linux:
            self.requires("mesa/19.3.1@bincrafters/stable")

    def source(self):
        archive_url = "https://github.com/SpartanJ/SOIL2/archive/release-{}.tar.gz".format(self.version)
        tools.get(archive_url, sha256="104a2de5bb74b58b7b7cda7592b174d9aa0585eeb73d0bec4901f419321358bc")
        extracted_dir = "SOIL2-release-" + self.version 
        os.rename(extracted_dir, self._source_subfolder)
        # This is the upstream premake5.lua file which will be included in  a 1.11+ release
        # With additional support for 64bit via "platforms { .. } and filters .. architecture .."
        os.rename("premake5.lua", os.path.join(self._source_subfolder, "premake5.lua"))

    def system_requirements(self):
        if self.settings.os == "Macos":
            self.run("brew cask install xquartz")

    def build(self):
        config = "debug" if self.settings.build_type == "Debug" else "release"
        architecture = "x32" if self.settings.arch == "x86" else "x64"
        with tools.chdir(self._source_subfolder):
            if self.settings.compiler == "Visual Studio":
                self.run("premake5 --os=windows vs2015")
                with tools.chdir(os.path.join("make", "windows")):
                    msbuild = MSBuild(self)
                    msbuild.build("SOIL2.sln", targets=["soil2-static-lib"], platforms={"x86":"Win32"})
            else:
                the_os = "macosx" if self.settings.os == "Macos" else "linux"
                self.run("premake5 --os={} gmake".format(the_os))
                with tools.chdir(os.path.join("make", the_os)):
                    env_build = AutoToolsBuildEnvironment(self)
                    env_build.make(args=["soil2-static-lib", "config={}".format(config + "_" + architecture) ])

    def package(self):
        self.copy("*.h", dst="include/SOIL2", src="{}/src/SOIL2/".format(self._source_subfolder))
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["soil2-debug" if self.settings.build_type == "Debug" else "soil2"]
        if self.settings.os == "Windows":
            self.cpp_info.system_libs.extend(["glu32", "opengl32"])
        elif self.settings.os == "Macos":
            self.cpp_info.frameworks.extend(["OpenGL", "CoreFoundation"])
