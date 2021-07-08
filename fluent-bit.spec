%global install_prefix /

Name: fluent-bit
Version: 1.7.9
Release: 1%{?dist}
Summary: Fast data collector for Linux
License: Apache v2.0
URL: https://github.com/fluent/fluent-bit
Source0: https://github.com/fluent/%{name}/archive/refs/tags/v%{version}.tar.gz
Patch0: 0001-mbedtls-disable-Werror-in-prod-build.patch
Patch1: 0002-onigmo-add-fPIC-to-CFLAGS.patch
Patch2: 0003-CMake-fix-up-install-paths.patch

BuildRequires: pkgconfig
BuildRequires: make
BuildRequires: cmake
BuildRequires: systemd
BuildRequires: systemd-devel
BuildRequires: gcc-c++
BuildRequires: flex
BuildRequires: bison
BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: libpq-devel
BuildRequires: zlib-devel
BuildRequires: gnutls-devel
BuildRequires: openssl-devel
BuildRequires: cyrus-sasl-devel

%description
Fluent Bit is a high performance and multi-platform log forwarder.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
%{summary}

%prep
%autosetup -p1

%build
%cmake -DCMAKE_INSTALL_PREFIX=%{install_prefix}\
    -DFLB_EXAMPLES=Off\
    -DFLB_OUT_SLACK=Off\
    -DFLB_OUT_TD=Off\
    -DFLB_OUT_ES=Off\
    .
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc README.md MAINTAINERS.md CODE_OF_CONDUCT.md CONTRIBUTING.md GOLANG_OUTPUT_PLUGIN.md GOVERNANCE.md
%config %{_sysconfdir}/%{name}/*.conf
%{_bindir}/%{name}
%{_libdir}/libfluent-bit.so
%{_prefix}/lib/systemd/system/%{name}.service

%files devel
%{_includedir}/%{name}.h
%{_includedir}/%{name}/*.h

%changelog
* Wed Jul 8 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.9-1
- Update to 1.7.9

* Wed Jun 9 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.8-1
- Update to 1.7.8

* Sat May 23 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.6-1
- Update to 1.7.6

* Sat May 15 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.5-1
- Update to 1.7.5

* Fri Apr 16 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.4-1
- New release; use cmake macros

* Mon Sep 28 2020 Marcin Skarbek <rpm@skarbek.name> - 1.5.7-1
- Initial package
