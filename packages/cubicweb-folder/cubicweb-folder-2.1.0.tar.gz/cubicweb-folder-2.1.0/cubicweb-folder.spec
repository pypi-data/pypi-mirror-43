# for el5, force use of python2.6
%if 0%{?el5}
%define python python26
%define __python /usr/bin/python2.6
%else
%define python python
%define __python /usr/bin/python
%endif
%{!?_python_sitelib: %define _python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           cubicweb-folder
Version:        2.1.0
Release:        logilab.1%{?dist}
Summary:        folder component for the CubicWeb framework
Group:          Applications/Internet
License:        LGPL
Source0:        cubicweb-folder-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:  %{python} %{python}-setuptools
Requires:       cubicweb >= 3.19.0
Requires:       %{python}-six >= 1.4.0

%description
folder component for the CubicWeb framework

%prep
%setup -q -n cubicweb-folder-%{version}

%install
%{__python} setup.py --quiet install --no-compile --prefix=%{_prefix} --root="$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
/*
