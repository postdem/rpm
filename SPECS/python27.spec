%global pybasever     	2.7
%global pylibdir      	%{_libdir}/python%{pybasever}
%global dynload_dir   	%{pylibdir}/lib-dynload
%global site_packages 	%{pylibdir}/site-packages

# ==================
# Top-level metadata
# ==================
Name:       python27
Version:    2.7.11
Release:    1%{?dist}
Summary:    An interpreted, interactive, object-oriented programming language
Group:      Development/Languages
License:    Python
URL:        http://www.python.org/

# =======================
# Build-time requirements
# =======================

BuildRequires: bzip2-devel
BuildRequires: db4-devel 
BuildRequires: expat-devel 
BuildRequires: gdbm-devel
BuildRequires: libffi-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: readline-devel
BuildRequires: sqlite-devel
BuildRequires: tcl-devel
BuildRequires: tix-devel
BuildRequires: tk-devel
BuildRequires: zlib-devel

%if 0%{?el7}
BuildRequires: libdb-devel
%endif


# =======================
# Source code and patches
# =======================
Source: https://www.python.org/ftp/python/%{version}/Python-%{version}.tgz

Patch0: python-2.7.1-config.patch
Patch1: 00001-pydocnogui.patch
Patch4: python-2.5-cflags.patch
Patch6: python-2.5.1-plural-fix.patch
Patch7: python-2.5.1-sqlite-encoding.patch
Patch102: python-2.7.3-lib64.patch
Patch103: python-2.7-lib64-sysconfig.patch
Patch104: 00104-lib64-fix-for-test_install.patch
Patch121: 00121-add-Modules-to-build-path.patch
Patch133: 00133-skip-test_dl.patch


# ======================================================
# Additional metadata, and subpackages
# ======================================================
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

%package libs
Summary: Runtime libraries for Python
Group: Applications/System
Requires: %{name} = %{version}-%{release}

Requires: expat

%description libs
This package contains runtime libraries for use by Python:
- the libpython dynamic library, for use by applications that embed Python as
a scripting language, and by the main "python" executable
- the Python standard library

%package devel
Summary: The libraries and header files needed for Python development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package tkinter
Summary: A graphical user interface for the Python scripting language
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description tkinter

The Tkinter (Tk interface) program is an graphical user interface for
the Python scripting language.

You should install the tkinter package if you'd like to use a graphical
user interface for Python programming.

%package test
Summary: The test modules from the main python package
Group: Development/Languages
Requires: %{name} = %{version}-%{release}

%description test

The test modules from the main python package: %{name}
These have been removed to save space, as they are never or almost
never used in production.

You might want to install the python-test package if you're developing python
code that uses more than just unittest and/or test_support.py.

# ======================================================
# Prep section
# ======================================================
%prep
%setup -q -n Python-%{version}

%patch0 -p1 -b .rhconfig
%patch1 -p1 -b .no_gui
%patch4 -p1 -b .cflags
%patch6 -p1 -b .plural
%patch7 -p1

%if "%{_lib}" == "lib64"
%patch102 -p1 -b .lib64
%patch103 -p1 -b .lib64-sysconfig
%patch104 -p1
%endif

%patch121 -p1


# ======================================================
# Building section
# ======================================================
%build
%configure \
  --enable-ipv6 \
  --enable-shared \
  --enable-unicode=ucs4 \
  --with-dbmliborder=gdbm:ndbm:bdb \
%if 0%{?el5}
%else
  --with-system-expat \
%endif
  --with-system-ffi

make %{?_smp_mflags}


# ======================================================
# Install section
# ======================================================
%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


# ======================================================
# Clean section
# ======================================================
%clean
rm -fr %{buildroot}


# ======================================================
# Files section
# ======================================================
%files
%defattr(-, root, root, -)
%{_bindir}/python*
%exclude %{_bindir}/2to3
%exclude %{_bindir}/idle
%exclude %{_bindir}/pydoc
%exclude %{_bindir}/smtpd.py
%{_mandir}/*/*

%files libs
%defattr(-,root,root,-)
%{_libdir}/libpython%{pybasever}.so.*
%{pylibdir}

%exclude %{dynload_dir}/_tkinter.so
%exclude %{pylibdir}/*/test
%exclude %{pylibdir}/config/*
%exclude %{pylibdir}/distutils/command/wininst-*.exe
%exclude %{pylibdir}/ensurepip/_bundled
%exclude %{pylibdir}/lib-tk
%exclude %{pylibdir}/LICENSE.txt

%files devel
%defattr(-,root,root,-)
%{_libdir}/libpython%{pybasever}.so
%{_libdir}/pkgconfig/python-%{pybasever}.pc
%{_libdir}/pkgconfig/python.pc
%{_libdir}/pkgconfig/python2.pc
%{_includedir}/python%{pybasever}/*.h
%{pylibdir}/config/*

%files tkinter
%defattr(-,root,root,-)
%{pylibdir}/lib-tk
%{dynload_dir}/_tkinter.so

%files test
%defattr(-, root, root, -)
%{pylibdir}/*/test
%{pylibdir}/test

%exclude %{pylibdir}/test/test_support.py*
%exclude %{pylibdir}/test/__init__.py*


# ======================================================
# Changelog section
# ======================================================
%changelog
* Fri Mar 25 2016 Dmitry Zakirdzhanov <postdem@gmail.com> - 2.7.11-1
- Python 2.7.11 builded on rhel5 rhel6 rhel7
