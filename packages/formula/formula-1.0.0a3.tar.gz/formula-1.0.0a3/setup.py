import glob
import os
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import setuptools

__version__ = "1.0.0a3"


class get_pybind_include(object):
    """Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked."""

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11

        return pybind11.get_include(self.user)


ext_modules = [
    Extension(
        "formula",
        ["src/main.cpp"],
        include_dirs=[
            # Paths to boost headers.
            # *set(map(
            #     os.path.dirname,
            #     glob.iglob(os.path.join("boost", "**", "*.hpp"), recursive=True),
            # )),
            "boost",
            "boost/boost/algorithm",
            "boost/boost/algorithm/cxx11",
            "boost/boost/algorithm/cxx14",
            "boost/boost/algorithm/cxx17",
            "boost/boost/algorithm/searching",
            "boost/boost/algorithm/searching/detail",
            "boost/boost/algorithm/string",
            "boost/boost/algorithm/string/detail",
            "boost/boost/algorithm/string/std",
            #####
            "boost/libs/math/include/boost",
            "boost/libs/math/include/boost/math",
            "boost/libs/math/include/boost/math/bindings",
            "boost/libs/math/include/boost/math/bindings/detail",
            "boost/libs/math/include/boost/math/complex",
            "boost/libs/math/include/boost/math/concepts",
            "boost/libs/math/include/boost/math/constants",
            "boost/libs/math/include/boost/math/cstdfloat",
            "boost/libs/math/include/boost/math/distributions",
            "boost/libs/math/include/boost/math/distributions/detail",
            "boost/libs/math/include/boost/math/interpolators",
            "boost/libs/math/include/boost/math/interpolators/detail",
            "boost/libs/math/include/boost/math/policies",
            "boost/libs/math/include/boost/math/quadrature",
            "boost/libs/math/include/boost/math/quadrature/detail",
            "boost/libs/math/include/boost/math/special_functions",
            "boost/libs/math/include/boost/math/special_functions/detail",
            "boost/libs/math/include/boost/math/tools",
            "boost/libs/math/include/boost/math/tools/detail",
            "boost/libs/math/minimax",
            "boost/libs/math/reporting/accuracy",
            "boost/libs/math/reporting/performance",
            "boost/libs/math/src/tr1",
            "boost/libs/math/tools",
            # Path to csformula headers.
            "src",
            # Path to pybind11 headers.
            get_pybind_include(),
            get_pybind_include(user=True),
        ],
        language="c++",
    )
]


# As of Python 3.6, CCompiler has a `has_flag` method.
# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile

    with tempfile.NamedTemporaryFile("w", suffix=".cpp") as f:
        f.write("int main (int argc, char **argv) { return 0; }")
        try:
            compiler.compile([f.name], extra_postargs=[flagname])
        except setuptools.distutils.errors.CompileError:
            return False
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14] compiler flag.

    The c++14 is preferred over c++11 (when it is available).
    """
    if has_flag(compiler, "-std=c++14"):
        return "-std=c++14"
    elif has_flag(compiler, "-std=c++11"):
        return "-std=c++11"
    else:
        raise RuntimeError(
            "Unsupported compiler -- at least C++11 support " "is needed!"
        )


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""

    c_opts = {"msvc": ["/EHsc"], "unix": []}

    if sys.platform == "darwin":
        c_opts["unix"] += ["-stdlib=libc++", "-mmacosx-version-min=10.7"]

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        if ct == "unix":
            opts.append('-DVERSION_INFO="%s"' % self.distribution.get_version())
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, "-fvisibility=hidden"):
                opts.append("-fvisibility=hidden")
        elif ct == "msvc":
            opts.append('/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args = opts
        build_ext.build_extensions(self)


setup(
    name="formula",
    version=__version__,
    author="Ivan Ergunov",
    author_email="hozblok@gmail.com",
    url="https://github.com/hozblok/formula",
    description="Arbitrary-precision formula solver.",  # TODO
    long_description="",
    ext_modules=ext_modules,
    install_requires=["pybind11>=2.2"],
    cmdclass={"build_ext": BuildExt},
    zip_safe=False,
    package_data={"": ["boost/libs/variant/include/boost/*.hpp"]},
)
