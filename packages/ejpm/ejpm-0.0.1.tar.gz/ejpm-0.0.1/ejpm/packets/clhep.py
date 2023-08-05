"""
https://github.com/JeffersonLab/JANA.git
export BMS_OSNAME=`./SBMS/osrelease.pl`

"""

import os

from ejpm.engine.commands import run, workdir
from ejpm.engine.env_gen import Set, Append
from ejpm.engine.installation import PacketInstallationInstruction


class ClhepInstallation(PacketInstallationInstruction):
    """Provides data for building and installing Genfit framework
    source_path  = {app_path}/src/{version}          # Where the sources for the current version are located
    build_path   = {app_path}/build/{version}        # Where sources are built. Kind of temporary dir
    install_path = {app_path}/root-{version}         # Where the binary installation is
    """

    fedora_required_packets = "boost-devel"         # Actually boost-devel it is needed for Rave but Genfit get error
    fedora_optional_packets = ""
    ubuntu_required_packets = "libboost-dev"
    ubuntu_optional_packets = ""

    def __init__(self, build_threads=8):
        """
        Installs Genfit track fitting framework
        """

        # Set initial values for parent class and self
        super(ClhepInstallation, self).__init__('clhep')
        self.build_threads = build_threads
        self.clone_command = ''             # will be set by self.set_app_path
        self.build_cmd = ''                 # will be set by self.set_app_path

    def setup(self, app_path):
        """Sets all variables like source dirs, build dirs, etc"""

        # What branch will we use? CLHEP has only one=)
        branch = 'master'

        #
        # use_common_dirs_scheme sets standard package variables:
        # source_path  = {app_path}/src/{version}          # Where the sources for the current version are located
        # build_path   = {app_path}/build/{version}        # Where sources are built. Kind of temporary dir
        # install_path = {app_path}/root-{version}         # Where the binary installation is
        self.use_common_dirs_scheme(app_path, branch)

        #
        # JANA download link. Clone with shallow copy
        # TODO accept version tuple to get exact branch
        self.clone_command = "git clone --depth 1 -b {branch} https://gitlab.cern.ch/CLHEP/CLHEP.git {source_path}"\
            .format(branch=branch, source_path=self.source_path)

        # cmake command:
        # the  -Wno-dev  flag is to ignore the project developers cmake warnings for policy CMP0075
        self.build_cmd = "cmake -Wno-dev -DCLHEP_SINGLE_THREAD=ON -DCMAKE_INSTALL_PREFIX={install_path} {source_path}" \
                         "&& cmake --build . -- -j {build_threads}" \
                         "&& cmake --build . --target install" \
                         .format(
                             source_path=self.source_path,    # cmake source
                             install_path=self.install_path,  # Installation path
                             build_threads=self.build_threads)     # make global options like '-j8'. Skip now

        # requirments  env var to locate
        # xerces-c     XERCESCROOT
        # ROOT         ROOTSYS
        # CCDB         CCDB_HOME
        # curl         CURL_HOME

    def step_install(self):
        self.step_clone()
        self.step_build()

    def step_clone(self):
        """Clones JANA from github mirror"""

        # Check the directory exists and not empty
        if os.path.exists(self.source_path) and os.path.isdir(self.source_path) and os.listdir(self.source_path):
            # The directory exists and is not empty. Nothing to do
            return
        else:
            # Create the directory
            run('mkdir -p {}'.format(self.source_path))

        # Execute git clone command
        run(self.clone_command)

    def step_build(self):
        """Builds JANA from the ground"""

        # Create build directory
        run('mkdir -p {}'.format(self.build_path))

        # go to our build directory
        workdir(self.build_path)

        # run scons && scons install
        run(self.build_cmd)

    def step_reinstall(self):
        """Delete everything and start over"""

        # clear sources directories if needed
        run('rm -rf {}'.format(self.app_path))

        # Now run build root
        self.step_install()

    @staticmethod
    def gen_env(data):
        """Generates environments to be set"""

        path = data['install_path']
        lib_path = os.path.join(path, 'lib')
        include_path = os.path.join(path, 'include')
        bin_path = os.path.join(path, 'bin')

        yield Set('CLHEP', path)
        yield Set('CLHEPPATH', path)                  # Some system look for CLHEP this way
        yield Set('CLHEP_INCLUDE_DIR', include_path)  # or /usr/include/CLHEP/
        yield Set('CLHEP_LIB_DIR', lib_path)

        yield Append('PATH', bin_path)  # to make available clhep-config and others
        yield Append('LD_LIBRARY_PATH', lib_path)

        # set DYLD_LIBRARY_PATH for mac
        import platform
        if platform.system() == 'Darwin':
            yield Append('DYLD_LIBRARY_PATH', lib_path)


