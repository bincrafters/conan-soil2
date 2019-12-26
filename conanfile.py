from conans import ConanFile, tools, AutoToolsBuildEnvironment, MSBuild
import os


class soil2Conan(ConanFile):
    name = "soil2"
    version = "1.11"
    description = "Simple OpenGL Image Library 2"
    topics = ("conan", "soil2", "opengl", "images")
    url = "https://github.com/bincrafters/conan-soil2"
    homepage = "https://bitbucket.org/SpartanJ/soil2"
    author = "Inexor <info@inexor.org>"
    license = "Unlicense"  # Public Domain
    settings = "os", "arch", "compiler", "build_type"
    exports = ["LICENSE.md"]
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    generators = "premake"

    def config_options(self):
        # Visual Studio users: SOIL2 will need to be compiled as C++ source ( at least the file etc1_utils.c ), since VC compiler doesn't support C99
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def build_requirements(self):
        if not tools.which("premake"):
            self.build_requires("premake_installer/4.4-beta5@bincrafters/stable")
    
    def requirements(self):
        if self.settings.os == "Linux" and tools.os_info.is_linux:
            self.requires('mesa/19.3.1@bincrafters/stable')

    def source(self):
        archive_url = "https://bitbucket.org/SpartanJ/soil2/get/release-{}.tar.bz2".format(self.version)
        tools.get(archive_url, sha256="c6d729b0fb74540b40d461ed3520e507418b121ed81eed7b19569bfc02d7c5d0")
        extracted_dir = "SpartanJ-soil2-9e6974409740"
        os.rename(extracted_dir, self._source_subfolder)

    def system_requirements(self):
        if self.settings.os == "Macos":
            self.run("brew cask install xquartz")

    def build(self):
        config = "debug" if self.settings.build_type == "Debug" else "release"
        platform = "x32" if self.settings.arch == "x86" else "x64"
        with tools.chdir(self._source_subfolder):
            if self.settings.compiler == "Visual Studio":
                self.run("premake4 --os=windows --platform=%s vs2010" % platform)
                with tools.chdir(os.path.join("make", "windows")):
                    msbuild = MSBuild(self)
                    msbuild.build("SOIL2.sln", targets=["soil2-static-lib"], platforms={"x86":"Win32"})
            else:
                the_os = "macosx" if self.settings.os == "Macos" else "linux"
                self.run("premake4 --os=%s --platform=%s gmake" % (the_os, platform))
                with tools.chdir(os.path.join("make", the_os)):
                    env_build = AutoToolsBuildEnvironment(self)
                    env_build.make(args=["soil2-static-lib", "config=%s" % config])

    def package(self):
        self.copy("*.h", dst="include/SOIL2", src="{}/src/SOIL2/".format(self._source_subfolder))
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["soil2-debug" if self.settings.build_type == "Debug" else "soil2"]
        if self.settings.os == "Windows":
            self.cpp_info.libs.extend(["glu32", "opengl32"])
        elif self.settings.os == "Macos":
            frameworks = ["OpenGL", "CoreFoundation"]
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags

