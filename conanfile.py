from conans import ConanFile, tools, AutoToolsBuildEnvironment
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

    def build_requirements(self):
        if not tools.which("premake"):
            self.build_requires("premake_installer/4.4-beta5@bincrafters/stable")

    def source(self):
        archive_url = "https://bitbucket.org/SpartanJ/soil2/get/release-{}.tar.bz2".format(self.version)
        tools.get(archive_url, sha256="c6d729b0fb74540b40d461ed3520e507418b121ed81eed7b19569bfc02d7c5d0")
        extracted_dir = "SpartanJ-soil2-9e6974409740"
        os.rename(extracted_dir, self._source_subfolder)

    def system_requirements(self):
        if self.settings.os == "Macos":
            self.run("brew cask install xquartz")

        if self.settings.os == "Linux" and tools.os_info.is_linux:
            installer = tools.SystemPackageTool()
            if tools.os_info.with_apt:
                if self.settings.arch == "x86":
                    arch_suffix = ':i386'
                elif self.settings.arch == "x86_64":
                    arch_suffix = ':amd64'
                packages = ['libgl1-mesa-dev%s' % arch_suffix]

            if tools.os_info.with_yum:
                if self.settings.arch == "x86":
                    arch_suffix = '.i686'
                elif self.settings.arch == 'x86_64':
                    arch_suffix = '.x86_64'
                packages = ['mesa-libGL-devel%s' % arch_suffix]


            for package in packages:
                installer.install(package)

    def build(self):
        config = "debug" if self.settings.build_type == "Debug" else "release"
        with tools.chdir(self._source_subfolder):
            if self.settings.compiler == "Visual Studio":
                raise Exception("TODO")
            else:
                self.run("premake4 gmake")
                platform = "macosx" if self.settings.os == "Macos" else "linux"
                with tools.chdir(os.path.join("make", platform)):
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
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend(["GLU", "GL"])
        elif self.settings.os == "Macos":
            frameworks = ["OpenGL", "CoreFoundation"]
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags

