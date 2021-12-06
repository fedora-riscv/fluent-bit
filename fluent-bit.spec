%global install_prefix /

Name: fluent-bit
Version: 1.8.10
Release: 5%{?dist}
Summary: Fast data collector for Linux
License: ASL 2.0
URL: https://github.com/fluent/fluent-bit
Source0: https://github.com/fluent/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
# Remove -Werror in mbedtls build. Not upstream
Patch0: 0001-mbedtls-disable-Werror-in-prod-build.patch
# Fix up some install paths in CMake. Not upstream
Patch1: 0002-CMake-fix-up-install-paths.patch
# Add -fPIC to onigomo build. Not upstream
Patch2: 0003-onigmo-add-fPIC-to-CFLAGS.patch
# Fix up a failing runtime test
# https://github.com/fluent/fluent-bit/issues/4274
Patch3: 0004-tests-runtime-in_proc-modify-absent-process-name-427.patch

BuildRequires: pkgconfig
BuildRequires: make
BuildRequires: cmake
BuildRequires: systemd-rpm-macros
# systemd-devel BR is needed for systemd input plugin
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

ExclusiveArch: x86_64 %{arm} aarch64

%description
Fluent Bit is a high performance and multi-platform log forwarder.

%prep
%autosetup -p1

%build
%cmake\
    -DCMAKE_BUILD_TYPE=RelWithDebInfo\
    -DFLB_EXAMPLES=Off\
    -DFLB_OUT_SLACK=Off\
    -DFLB_IN_SYSTEMD=On\
    -DFLB_OUT_TD=Off\
    -DFLB_OUT_ES=Off\
    -DFLB_SHARED_LIB=Off\
    -DFLB_TESTS_RUNTIME=On\
    -DFLB_TESTS_INTERNAL=Off\
    -DFLB_RELEASE=On\
    -DFLB_DEBUG=Off\
    -DFLB_TLS=On\
    .
%cmake_build

%install
%cmake_install
# We don't ship headers and shared library for plugins (yet)
rm -rvf %{buildroot}%{_includedir}

%check
%ctest

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md MAINTAINERS.md CODE_OF_CONDUCT.md CONTRIBUTING.md GOLANG_OUTPUT_PLUGIN.md GOVERNANCE.md
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%{_bindir}/%{name}
%{_unitdir}/%{name}.service

%changelog
* Sat Dec 4 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.10-5
- Do not set CMAKE_INSTALL_PREFIX explicitly

* Thu Nov 25 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.10-4
- Fix up source URL

* Wed Nov 24 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.10-3
- Re-add systemd-devel BR. Remove devel package

* Mon Nov 22 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.10-2
- Add systemd scriptlet macros, add patch status comments

* Sat Nov 20 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.10-1
- Update to 1.8.10, enable runtime tests

* Mon Nov 1 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.9-1
- Update to 1.8.9, remove shared library

* Thu Oct 28 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.8.8-1
- Update to 1.8.8, rebase patches

* Thu Jul 8 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.9-1
- Update to 1.7.9

* Wed Jun 9 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.8-1
- Update to 1.7.8

* Sun May 23 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.6-1
- Update to 1.7.6

* Sat May 15 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.5-1
- Update to 1.7.5

* Fri Apr 16 2021 Benjamin Kircher <bkircher@0xadd.de> - 1.7.4-1
- New release; use cmake macros

* Mon Sep 28 2020 Marcin Skarbek <rpm@skarbek.name> - 1.5.7-1
- Initial package
