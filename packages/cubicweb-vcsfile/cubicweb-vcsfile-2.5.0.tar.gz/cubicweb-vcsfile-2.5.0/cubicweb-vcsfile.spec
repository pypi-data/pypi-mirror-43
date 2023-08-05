# for el5, force use of python2.6
%if 0%{?el5}
%define python python26
%define __python /usr/bin/python2.6
%else
%define python python
%define __python /usr/bin/python
%endif
%{!?_python_sitelib: %define _python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           cubicweb-vcsfile
Version:        2.5.0
Release:        logilab.1%{?dist}
Summary:        component to integrate version control systems data into the CubicWeb framework
Group:          Applications/Internet
License:        LGPL
Source0:        cubicweb-vcsfile-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  %{python} %{python}-setuptools
Requires:       cubicweb >= 3.26.0
Requires:       cubicweb-localperms >= 0.1.0
Requires:       mercurial < 4.0.0
Requires:       %{python}-logilab-mtconverter >= 0.7.0
Requires:       %{python}-logilab-common >= 0.59.0
Requires:       %{python}-six
Requires:       %{python}-docutils
Requires:       %{python}-hglib >= 1.3
Requires:       %{python}-tzlocal

%description
component to integrate version control systems data into the CubicWeb framework

%prep
%setup -q -n cubicweb-vcsfile-%{version}
%if 0%{?el5}
# change the python version in shebangs
find . -name '*.py' -type f -print0 |  xargs -0 sed -i '1,3s;^#!.*python.*$;#! /usr/bin/python2.6;'
%endif

%install
NO_SETUPTOOLS=1 %{__python} setup.py --quiet install --no-compile --prefix=%{_prefix} --root="$RPM_BUILD_ROOT"
# remove generated .egg-info file
rm -rf $RPM_BUILD_ROOT/usr/lib/python*


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/*
