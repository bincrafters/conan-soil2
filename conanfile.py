from conans import ConanFile, tools, CMake ## MSBuild
import os


class soil2Conan(ConanFile):
    name = "soil2"
    version = "1.11"
    description = "Simple OpenGL Image Library 2"
    topics = ("conan", "soil2", "opengl", "images")
    url = "https://github.com/bincrafters/conan-soil2"
    homepage = "https://bitbucket.org/SpartanJ/soil2"
    author = "Inexor <info@inexor.org>"
    license = "Public Domain"
    settings = "os", "arch", "compiler", "build_type"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    generators = "cmake"
    # build_requires = "premake_installer/4.3@bincrafters/stable"

# SOIL2 seems to be C only mainly, but for some reason the premake file has a is_vs() -> language C++ switch, why?
#    def config_options(self):
 #       del self.settings.compiler.libcxx

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
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        cmake.build()
        # self.output.info("premake4 vs2013 --os=windows --file={}".format(os.path.join(self._source_subfolder, "premake4.lua")))
        # self.run("premake4 --help")
        # if self.settings.os == "Windows":
            # self.run("premake4 vs2010 --os=windows", cwd=self._source_subfolder)
            # msbuild = MSBuild(self)
            # msbuild.build("{}/make/windows/SOIL2.sln".format(self._source_subfolder), upgrade_project=True, arch="Win32", targets="soil2-static-lib")

    def package(self):
        self.copy("*.h", dst="include/SOIL2", src="{}/src/SOIL2/".format(self._source_subfolder))
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["SOIL2"]
        if self.settings.os == "Windows":
            self.cpp_info.libs.append("glu32")
            self.cpp_info.libs.append("opengl32")
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("GLU")
            self.cpp_info.libs.append("GL")
