%global release_prefix          100

Name:                           brotli
Version:                        1.0.9
Release:                        %{release_prefix}%{?dist}
Summary:                        Lossless compression algorithm
License:                        MIT
URL:                            https://github.com/google/brotli

Source0:                        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Patch0:                         09b0992b6acb7faa6fd3b23f9bc036ea117230fc.patch

%if 0%{?rhel} == 7
BuildRequires:                  devtoolset-7-toolchain, devtoolset-7-libatomic-devel
%endif
BuildRequires:                  gcc
BuildRequires:                  gcc-c++
BuildRequires:                  cmake
BuildRequires:                  python3-devel
BuildRequires:                  python3-setuptools

Requires:                       lib%{name}%{?_isa} = %{version}-%{release}

%description
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods.
It is similar in speed with deflate but offers more dense compression.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: libbrotli
# -------------------------------------------------------------------------------------------------------------------- #

%package -n libbrotli
Summary:                        Library for brotli lossless compression algorithm

%description -n libbrotli
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods.
It is similar in speed with deflate but offers more dense compression.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: python3-brotli
# -------------------------------------------------------------------------------------------------------------------- #

%package -n python3-%{name}
Summary:                        Lossless compression algorithm (python 3)
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods.
It is similar in speed with deflate but offers more dense compression.
This package installs a Python 3 module.

# -------------------------------------------------------------------------------------------------------------------- #
# Package: brotli-devel
# -------------------------------------------------------------------------------------------------------------------- #

%package devel
Summary:                        Lossless compression algorithm (development files)
Requires:                       %{name}%{?_isa} = %{version}-%{release}
Requires:                       lib%{name}%{?_isa} = %{version}-%{release}

%description devel
Brotli is a generic-purpose lossless compression algorithm that compresses
data using a combination of a modern variant of the LZ77 algorithm, Huffman
coding and 2nd order context modeling, with a compression ratio comparable
to the best currently available general-purpose compression methods.
It is similar in speed with deflate but offers more dense compression.
This package installs the development files

# -------------------------------------------------------------------------------------------------------------------- #
# -----------------------------------------------------< SCRIPT >----------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------------- #

%prep
%autosetup -p1
# fix permissions for -debuginfo
# rpmlint will complain if I create an extra %%files section for
# -debuginfo for this so we'll put it here instead
%{__chmod} 644 c/enc/*.[ch]
%{__chmod} 644 c/include/brotli/*.h
%{__chmod} 644 c/tools/brotli.c


%build
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-7/enable
%endif
%cmake \
    -DCMAKE_INSTALL_PREFIX="%{_prefix}" \
  -DCMAKE_INSTALL_LIBDIR="%{_libdir}"
%cmake_build
%py3_build


%install
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-7/enable
%endif
%cmake_install

# I couldn't find the option to not build the static libraries
%{__rm} "%{buildroot}%{_libdir}/"*.a

%py3_install
%{__install} -dm755 "%{buildroot}%{_mandir}/man3"
cd docs
for i in *.3;do
  %{__install} -m644 "${i}" "%{buildroot}%{_mandir}/man3/${i}brotli"
done

%ldconfig_scriptlets


%check
%if 0%{?rhel} == 7
. /opt/rh/devtoolset-7/enable
%endif
%ctest

%files
%{_bindir}/brotli


%files -n libbrotli
%license LICENSE
%{_libdir}/libbrotlicommon.so.1*
%{_libdir}/libbrotlidec.so.1*
%{_libdir}/libbrotlienc.so.1*


# Note that there is no %%files section for the unversioned python module
# if we are building for several python runtimes
%files -n python3-%{name}
%license LICENSE
%{python3_sitearch}/brotli.py
%{python3_sitearch}/_brotli.cpython-%{python3_version_nodots}*.so
%{python3_sitearch}/__pycache__/brotli.cpython-%{python3_version_nodots}*.py*
%{python3_sitearch}/Brotli-%{version}-py%{python3_version}.egg-info


%files devel
%{_includedir}/brotli
%{_libdir}/libbrotlicommon.so
%{_libdir}/libbrotlidec.so
%{_libdir}/libbrotlienc.so
%{_libdir}/pkgconfig/libbrotlicommon.pc
%{_libdir}/pkgconfig/libbrotlidec.pc
%{_libdir}/pkgconfig/libbrotlienc.pc
%{_mandir}/man3/constants.h.3brotli*
%{_mandir}/man3/decode.h.3brotli*
%{_mandir}/man3/encode.h.3brotli*
%{_mandir}/man3/types.h.3brotli*


%changelog
* Thu Jun 17 2021 Package Store <kitsune.solar@gmail.com> - 1.0.9-100
- UPD: Move to GitHub.
- UPD: License.

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.0.9-5
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 01 2020 Travis Kendrick <pouar@pouar.net> - 1.0.9-3
- Apparently %%autosetup calls %%patch on its own

* Thu Oct 01 2020 Travis Kendrick <pouar@pouar.net> - 1.0.9-2
- Fix pc file (#1884364)

* Wed Sep 30 2020 Travis Kendrick <pouar@pouar.net> - 1.0.9-1
- Update to 1.0.9 (#1872932)

* Wed Aug 12 2020 Carl George <carl@george.computer> - 1.0.7-14
- Update cmake invocation rhbz#1863298

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-13
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.7-11
- Rebuilt for Python 3.9

* Fri Mar 13 2020 Package Store <kitsune.solar@gmail.com> - 1.0.7-104
- UPD: master-0786c4.

* Sun Jun 23 2019 Package Store <kitsune.solar@gmail.com> - 1.0.7-103
- FIX: SPEC-file.

* Sun Jun 23 2019 Package Store <kitsune.solar@gmail.com> - 1.0.7-102
- FIX: SPEC-file.

* Sun Jun 23 2019 Package Store <kitsune.solar@gmail.com> - 1.0.7-101
- FIX: SPEC-file.

* Sun Jun 23 2019 Kitsune Solar <kitsune.solar@gmail.com> - 1.0.7-100
- Remove last python2 bits.
- EPEL compatibility.
- Build with devtoolset-7 on EPEL7 to fix aarch64 builds.
- Update from MARKETPLACE.

* Sat Dec 15 2018 Kitsune Solar <kitsune.solar@gmail.com> - 1.0.7-2
- Update from MARKETPLACE.

* Wed Nov 28 2018 Travis Kendrick <pouar@pouar.net> - 1.0.7-1
- Update to 1.0.7

* Wed Nov 28 2018 Travis Kendrick <pouar@pouar.net> - 1.0.5-2
- remove Python 2 support https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Jul 13 2018 Travis Kendrick <pouar@pouar.net> - 1.0.5-1
- update to 1.0.5

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.0.4-3
- Rebuilt for Python 3.7

* Wed Apr 18 2018 Travis Kendrick <pouar@pouar.net> - 1.0.4-2
- update to 1.0.4

* Sat Mar 03 2018 Travis Kendrick <pouar@pouar.net> - 1.0.3-1
- update to 1.0.3

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.1-2
- Switch to %%ldconfig_scriptlets

* Fri Sep 22 2017 Travis Kendrick <pouar@pouar.net> - 1.0.1-1
- update to 1.0.1

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 23 2017 Travis Kendrick <pouar@pouar.net> - 0.6.0-4
- add man pages

* Sun May 14 2017 Travis Kendrick <pouar@pouar.net> - 0.6.0-3
- wrong directory for ctest
- LICENSE not needed in -devel
- fix "spurious-executable-perm"
- rpmbuild does the cleaning for us, so 'rm -rf %%{buildroot}' isn't needed

* Sat May 13 2017 Travis Kendrick <pouar@pouar.net> - 0.6.0-2
- include libraries and development files

* Sat May 06 2017 Travis Kendrick <pouar@pouar.net> - 0.6.0-1
- Initial build
