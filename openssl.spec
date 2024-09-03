Name:           openssl
Version:        3.3.2
Release:        130
License:        OpenSSL
Summary:        Secure Socket Layer
Url:            http://www.openssl.org/
Group:          libs/network
Source0:        https://github.com/openssl/openssl/releases/download/openssl-3.3.2/openssl-3.3.2.tar.gz
BuildRequires:  zlib-dev
BuildRequires:  zlib-dev32
BuildRequires:  util-linux-extras
BuildRequires:  util-linux-bin
BuildRequires:  gcc-dev32
BuildRequires:  gcc-libgcc32
BuildRequires:  gcc-libstdc++32
BuildRequires:  glibc-dev32
BuildRequires:  glibc-libc32
BuildRequires:  perl(Test::More)
%define debug_package %{nil}
%define __strip /bin/true


Requires:       ca-certs
Requires:       p11-kit

Patch1: 0001-Use-clearlinux-CFLAGS-during-build.patch
Patch2: 0002-Hide-a-symbol-from-Steam.patch
Patch3: 0003-Use-OS-provided-copy-of-openssl.cnf-as-fallback.patch


%description
Secure Socket Layer.

%package lib
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          libs/network
Requires:       p11-kit

%description lib
Secure Socket Layer.

%package dev
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          devel
Requires:       openssl = %{version}-%{release}
Requires:       openssl-lib = %{version}-%{release}

%description dev
Secure Socket Layer.

%package extras
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          devel
Requires:       openssl = %{version}-%{release}
Requires:       openssl-lib = %{version}-%{release}
Requires:	c_rehash

%description extras
Secure Socket Layer.

%package lib32
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          libs/network

%description lib32
Secure Socket Layer.

%package dev32
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          devel
Requires:       openssl = %{version}-%{release}
Requires:       openssl-lib32 = %{version}-%{release}

%description dev32
Secure Socket Layer.

%package doc
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          doc

%description doc
Secure Socket Layer.

%prep
%setup -q
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1

pushd ..
cp -a openssl-3.3.2 build32
cp -a openssl-3.3.2  buildavx2
popd


%build
export AR=gcc-ar
export RANLIB=gcc-ranlib
export CFLAGS="$CFLAGS -flto=auto -fno-semantic-interposition -O3 -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=3 -gno-variable-location-views -gno-column-info -femit-struct-debug-baseonly -gz -g1"
export CXXFLAGS="$CXXFLAGS -flto=auto -ffunction-sections -fno-semantic-interposition -O3 -gno-variable-location-views -gno-column-info -femit-struct-debug-baseonly -gz -g1"
export CXXFLAGS="$CXXFLAGS -flto=auto -fno-semantic-interposition -O3 -falign-functions=32  "
export CFLAGS_GENERATE="$CFLAGS -fprofile-generate -fprofile-dir=/tmp/pgo "
export FCFLAGS_GENERATE="$FCFLAGS -fprofile-generate -fprofile-dir=/tmp/pgo "
export FFLAGS_GENERATE="$FFLAGS -fprofile-generate -fprofile-dir=/tmp/pgo "
export CXXFLAGS_GENERATE="$CXXFLAGS -fprofile-generate -fprofile-dir=/tmp/pgo "
export CFLAGS_USE="$CFLAGS -fprofile-use -fprofile-dir=/tmp/pgo -fprofile-correction "
export FCFLAGS_USE="$FCFLAGS -fprofile-use -fprofile-dir=/tmp/pgo -fprofile-correction "
export FFLAGS_USE="$FFLAGS -fprofile-use -fprofile-dir=/tmp/pgo -fprofile-correction "
export CXXFLAGS_USE="$CXXFLAGS -fprofile-use -fprofile-dir=/tmp/pgo -fprofile-correction "
export LDFLAGS_GENERATE="$LDFLAGS"
export LDFLAGS_USE="$LDFLAGS"

./config shared no-ssl zlib-dynamic no-ssl2 no-ssl3    \
 --prefix=/usr \
 --openssldir=/etc/ssl \
 --libdir=lib64

# parallel build is broken
make depend
make

pushd ../build32
export CFLAGS="$CFLAGS -m32 -fno-lto -mstackrealign"
export LDFLAGS="$LDFLAGS -m32 -fno-lto -mstackrealign"
export CXXFLAGS="$CXXFLAGS -m32 -fno-lto -mstackrealign"
i386 ./config shared no-ssl zlib-dynamic no-ssl2 no-ssl3 no-asm  \
 --prefix=/usr \
 --openssldir=/etc/ssl \
 --libdir=lib32 
make depend
make
popd

pushd ../buildavx2
export CFLAGS="${CFLAGS_GENERATE}  -march=x86-64-v3" 
export CXXFLAGS="${CXXFLAGS_GENERATE}  -march=x86-64-v3" 
export FFLAGS="${FFLAGS_GENERATE}   -march=x86-64-v3" 
export FCFLAGS="${FCFLAGS_GENERATE}   -march=x86-64-v3" 
export LDFLAGS="${LDFLAGS_GENERATE}"
./config shared no-ssl zlib-dynamic no-ssl2 no-ssl3 enable-ktls  \
 --prefix=/usr \
 --openssldir=/etc/ssl \
 --libdir=lib64

make depend
make

#apps/openssl speed 
LD_PRELOAD="./libcrypto.so ./libssl.so" apps/openssl speed rsa sha256 aes

make clean

export CFLAGS="${CFLAGS_USE}   -march=x86-64-v3" 
export CXXFLAGS="${CXXFLAGS_USE}   -march=x86-64-v3" 
export FFLAGS="${FFLAGS_USE}  -march=x86-64-v3" 
export FCFLAGS="${FCFLAGS_USE}  -march=x86-64-v3" 
export LDFLAGS="${LDFLAGS_USE}"

./config shared no-ssl zlib-dynamic no-ssl2 no-ssl3 enable-ktls    \
 --prefix=/usr \
 --openssldir=/etc/ssl \
 --libdir=lib64

# parallel build is broken
make depend
make
popd

%install

CFLAGS_ORIG="$CFLAGS"
LDFLAGS_ORIG="$LDFLAGS"
CXXFLAGS_ORIG="$CXXFLAGS"

pushd ../build32
export CFLAGS="$CFLAGS_ORIG -m32 -fno-lto -mstackrealign"
export LDFLAGS="$LDFLAGS_ORIG -m32 -fno-lto -mstackrealign"
export CXXFLAGS="$CXXFLAGS_ORIG -m32 -fno-lto -mstackrealign"
make  DESTDIR=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=openssl install
pushd %{buildroot}/usr/lib32/pkgconfig
for i in *.pc ; do cp $i 32$i ; done
popd
popd

pushd ../buildavx2
export CFLAGS="$CFLAGS_ORIG -flto=auto  -march=x86-64-v3 "
export LDFLAGS="$LDFLAGS_ORIG  -flto=auto   -march=x86-64-v3 "
export CXXFLAGS="$CXXFLAGS_ORIG  -flto=auto  -march=x86-64-v3 "
make  DESTDIR=%{buildroot}-v3 MANDIR=/usr/share/man MANSUFFIX=openssl install
popd

export CFLAGS="$CFLAGS_ORIG -m64 -flto"
export LDFLAGS="$LDFLAGS_ORIG -m64 -flto"
export CXXFLAGS="$CXXFLAGS_ORIG -m64 -flto"
make  DESTDIR=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=openssl install

install -D -m0644 apps/openssl.cnf %{buildroot}/usr/share/defaults/ssl/openssl.cnf
rm -rf %{buildroot}*/etc/ssl
rm -rf %{buildroot}*/usr/lib64/*.a
rm -rf %{buildroot}*/usr/share/doc/openssl/html

/usr/bin/elf-move.py avx2 %{buildroot}-v3 %{buildroot} %{buildroot}/usr/share/clear/filemap/filemap-%{name}

%check
make test

%files
/usr/bin/openssl
/V3/usr/bin/openssl
/usr/share/defaults/ssl/openssl.cnf

%files lib
/usr/lib64/libcrypto.so.3
/usr/lib64/libssl.so.3
/usr/lib64/engines-3/afalg.so
/usr/lib64/engines-3/capi.so
/usr/lib64/engines-3/padlock.so
/usr/lib64/engines-3/loader_attic.so
/usr/lib64/ossl-modules/legacy.so
/V3/usr/lib64/libcrypto.so.3
/V3/usr/lib64/libssl.so.3
/V3/usr/lib64/engines-3/afalg.so
/V3/usr/lib64/engines-3/capi.so
/V3/usr/lib64/engines-3/padlock.so
/V3/usr/lib64/engines-3/loader_attic.so
/V3/usr/lib64/ossl-modules/legacy.so

%files lib32
/usr/lib32/libcrypto.so.3
/usr/lib32/libssl.so.3
/usr/lib32/engines-3/afalg.so
/usr/lib32/engines-3/capi.so
/usr/lib32/engines-3/padlock.so
/usr/lib32/engines-3/loader_attic.so
/usr/lib32/ossl-modules/legacy.so

%files dev
/usr/include/openssl/*.h
/usr/lib64/libcrypto.so
/usr/lib64/libssl.so
/usr/lib64/pkgconfig/libcrypto.pc
/usr/lib64/pkgconfig/libssl.pc
/usr/lib64/pkgconfig/openssl.pc
/usr/lib64/cmake/OpenSSL/OpenSSLConfig.cmake
/usr/lib64/cmake/OpenSSL/OpenSSLConfigVersion.cmake
%files extras
%exclude /usr/bin/c_rehash

%files dev32
/usr/lib32/libcrypto.so
/usr/lib32/libssl.so
/usr/lib32/pkgconfig/32libcrypto.pc
/usr/lib32/pkgconfig/32libssl.pc
/usr/lib32/pkgconfig/32openssl.pc
/usr/lib32/pkgconfig/libcrypto.pc
/usr/lib32/pkgconfig/libssl.pc
/usr/lib32/pkgconfig/openssl.pc
/usr/lib32/libcrypto.a
/usr/lib32/libssl.a
/usr/lib32/cmake/OpenSSL/OpenSSLConfig.cmake
/usr/lib32/cmake/OpenSSL/OpenSSLConfigVersion.cmake

%files doc
/usr/share/man/man1/*
/usr/share/man/man3/*
/usr/share/man/man5/*
/usr/share/man/man7/*
