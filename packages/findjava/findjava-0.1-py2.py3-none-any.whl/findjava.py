"""
Find JAVA_HOME, and initialize by adding java_home to the os.envrion.

If JAVA_HOME is defined, validate that it is correct.
Otherwise, common locations for java will be searched.
"""

import os
import subprocess

__version__ = '0.1'


def _find_with_exec_java_home():
    """
    Use the `/usr/libexec/java_home` binary to find the java installation
    """
    out_paths = []
    try:
        path = subprocess.check_output(['/usr/libexec/java_home']).decode().strip()
        out_paths.append(path)
    except subprocess.CalledProcessError as err:
        # print("Got error: {}".format(err))
        pass
    return out_paths


def _find_with_bin_javac():
    """
    Use the location of `javac` in PATH to find the java_home.
    """
    out_paths = []
    try:
        # javac is present in JAVA_HOME/bin/javac
        path = os.path.dirname(os.path.dirname(
            subprocess.check_output(['which', 'javac']).decode().strip()))
        out_paths.append(path)
    except subprocess.CalledProcessError as err:
        # print("Got error: {}".format(err))
        pass
    return out_paths


def _find_with_bin_java():
    """
    Use the location of `java` in PATH to find the java_home.
    """
    out_paths = []
    try:
        # java is present in JAVA_HOME/bin/java
        path = os.path.dirname(os.path.dirname(
            subprocess.check_output(['which', 'java']).decode().strip()))
        out_paths.append(path)
    except subprocess.CalledProcessError as err:
        # print("Got error: {}".format(err))
        pass
    return out_paths


def find():
    """
    Find a java installation on the current computer.

    Will first check the JAVA_HOME env variable, and otherwise
    search common installation locations, e.g. from homebrew
    """
    java_home = os.environ.get('JAVA_HOME', None)

    if not java_home:
        possible_paths = ([
            '/etc/alternatives/java_sdk',  # yum in CentoOS for OpenJDK
            '/usr/java/default/'  # Oracle installer in CentoOS
            # Any other common places to look?
        ]
         + _find_with_exec_java_home()  # OS X
         + _find_with_bin_javac()  # If the PATH is set right
         + _find_with_bin_java()  # If the PATH is set right
        )
        for path in possible_paths:
            if os.path.exists(path):
                java_home = path
                break

    if not java_home:
        raise ValueError(
            "Couldn't find Java, make sure JAVA_HOME env is set "
            "or Java is in an expected location (e.g. from homebrew).")

    return java_home


def init(java_home=None):
    """
    :param java_home: str, optional, default = None
        Path to Java installation, check in default locations if not found.
    """

    if not java_home:
        java_home = find()

    # ensure JAVA_HOME is defined
    os.environ['JAVA_HOME'] = java_home


def main():
    java_home = find()
    print("JAVA_HOME detected at:", java_home)


if __name__ == '__main__':
    main()
