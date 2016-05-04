Name:           openssl
Version:        1.0.2h
Release:        44
License:        OpenSSL
Summary:        Secure Socket Layer
Url:            http://www.openssl.org/
Group:          libs/network
Source0:        http://www.openssl.org/source/openssl-1.0.2h.tar.gz
BuildRequires:  zlib-dev

Patch1: cflags.patch
Patch2: nodes.patch
Patch3: 0001-Remove-warning-in-non-fatal-absence-of-etc-ssl-opens.patch 
Patch4: 0001-Load-ca-certs-from-system-location-only.patch

%description
Secure Socket Layer.

%package lib
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          libs/network

%description lib
Secure Socket Layer.

%package dev
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          devel
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-lib

%description dev
Secure Socket Layer.

%package doc
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          doc

%description doc
Secure Socket Layer.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
export AR=gcc-ar
export RANLIB=gcc-ranlib
export CFLAGS="$CFLAGS -flto -ffunction-sections -fno-semantic-interposition -O3 -falign-functions=32 -falign-loops=32"
export CXXFLAGS="$CXXFLAGS -flto -ffunction-sections -fno-semantic-interposition -O3 "
export CXXFLAGS="$CXXFLAGS -fno-semantic-interposition -O3 -falign-functions=32 -flto "
export CFLAGS_GENERATE="$CFLAGS -fprofile-generate -fprofile-dir=/tmp/pgo "
export FCFLAGS_GENERATE="$FCFLAGS -fprofile-generate -fprofile-dir=/tmp/pgo "
export FFLAGS_GENERATE="$FFLAGS -fprofile-generate -fprofile-dir=/tmp/pgo "
export CXXFLAGS_GENERATE="$CXXFLAGS -fprofile-generate -fprofile-dir=/tmp/pgo "
export CFLAGS_USE="$CFLAGS -fprofile-use -fprofile-dir=/tmp/pgo -fprofile-correction "
export FCFLAGS_USE="$FCFLAGS -fprofile-use -fprofile-dir=/tmp/pgo -fprofile-correction "
export FFLAGS_USE="$FFLAGS -fprofile-use -fprofile-dir=/tmp/pgo -fprofile-correction "
export CXXFLAGS_USE="$CXXFLAGS -fprofile-use -fprofile-dir=/tmp/pgo -fprofile-correction "


export CFLAGS="${CFLAGS_GENERATE}" 
export CXXFLAGS="${CXXFLAGS_GENERATE}" 
export FFLAGS="${FFLAGS_GENERATE}" 
export FCFLAGS="${FCFLAGS_GENERATE}" 

./config shared no-ssl zlib-dynamic no-rc4 no-ssl2 no-ssl3   \
 --prefix=%{_prefix} \
 --openssldir=%{_sysconfdir}/ssl \
 --libdir=lib64

make depend
make

apps/openssl speed 

make clean

export CFLAGS="${CFLAGS_USE}" 
export CXXFLAGS="${CXXFLAGS_USE}" 
export FFLAGS="${FFLAGS_USE}" 
export FCFLAGS="${FCFLAGS_USE}" 

./config shared no-ssl zlib-dynamic no-rc4 no-ssl2 no-ssl3   \
 --prefix=%{_prefix} \
 --openssldir=%{_sysconfdir}/ssl \
 --libdir=lib64

# parallel build is broken
make depend
make


%install
make  INSTALL_PREFIX=%{buildroot} MANDIR=%{_mandir} MANSUFFIX=openssl install

mv %{buildroot}%{_sysconfdir}/ssl/misc/c_hash %{buildroot}%{_bindir}/c_hash

rm -rf %{buildroot}%{_sysconfdir}
rm -rf %{buildroot}%{_libdir}/*.a

%check
make test


%files
%{_bindir}/openssl
%{_bindir}/c_hash
%{_libdir}/engines/*.so

%files lib
%{_libdir}/libcrypto.so.1.0.0
%{_libdir}/libssl.so.1.0.0

%files dev
%{_includedir}/openssl/*.h
%{_libdir}/libcrypto.so
%{_libdir}/libssl.so
%{_libdir}/pkgconfig/libcrypto.pc
%{_libdir}/pkgconfig/libssl.pc
%{_libdir}/pkgconfig/openssl.pc
%{_bindir}/c_rehash

%files doc
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*
