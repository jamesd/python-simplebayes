# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?__python2: %global __python2 %__python}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global prjname simplebayes

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{prjname}
Version:        1.5.7
Release:        1%{?dist}
Summary:        A memory-based, optional-persistence naïve bayesian text classifier.

License:        MIT
URL:            https://github.com/hickeroar/%{prjname}
Source0:        https://github.com/hickeroar/%{prjname}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         Use-plain-ASCII-in-README.rst.patch

BuildArch:      noarch
BuildRequires:  python2-devel
%if %{with python3}
BuildRequires:  python3-devel
%endif # with python3

%description
This work is heavily inspired by the python "redisbayes" module found here:
[https://github.com/jart/redisbayes] and [https://pypi.python.org/pypi/redisbayes]

I've elected to write this to alleviate the network/time requirements when
using the bayesian classifier to classify large sets of text, or when
attempting to train with very large sets of sample data.

%if %{with python3}
%package -n python3-simplebayes
Summary:     %{summary} 

%description -n python3-simplebayes
%{summary}
%endif # with python3


%prep
%setup -c
pushd %{prjname}-%{version}
%patch0 -p1
popd
mv %{prjname}-%{version} python2

%if %{with python3}
cp -a python2 python3
%endif # with python3


%build
pushd python2
%{__python2} setup.py build
popd

%if %{with python3}
pushd python3
%{__python3} setup.py build
popd
%endif # with python3


%install
rm -rf $RPM_BUILD_ROOT
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if %{with python3}
pushd python3
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with python3

pushd python2
%{__python2} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd


%check
pushd python2
%{__python2} setup.py test
popd


%files
%license python2/LICENSE
%doc python2/README.rst
%{python2_sitelib}/*

%if %{with python3}
%files -n python3-simplebayes
%license python3/LICENSE
%doc python3/README.rst
%{python3_sitelib}/*
%endif # with python3


%changelog
* Sat Aug 27 2016 James Davidson <james@greycastle.net>
- Initial packaging
