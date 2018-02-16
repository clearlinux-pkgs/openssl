Name:           openssl
Version:        1.0.2n
Release:        74
License:        OpenSSL
Summary:        Secure Socket Layer
Url:            http://www.openssl.org/
Group:          libs/network
Source0:        http://www.openssl.org/source/openssl-1.0.2n.tar.gz
BuildRequires:  zlib-dev
BuildRequires:  zlib-dev32
BuildRequires:  util-linux-extras
BuildRequires:  util-linux-bin
BuildRequires:  gcc-dev32
BuildRequires:  gcc-libgcc32
BuildRequires:  gcc-libstdc++32
BuildRequires:  glibc-dev32
BuildRequires:  glibc-libc32

Requires:       ca-certs
Requires:       p11-kit

Patch1: 0001-Add-Clear-Linux-standard-CFLAGS.patch
Patch2: 0002-Remove-warning-in-non-fatal-absence-of-etc-ssl-opens.patch
Patch3: 0003-Make-openssl-stateless-configuration.patch
Patch4: 0004-Hide-a-symbol-from-Steam.patch
Patch5: cve-2016-2178.patch

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
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-lib

%description dev
Secure Socket Layer.

%package extras
License:        OpenSSL
Summary:        Secure Socket Layer
Group:          devel
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-lib
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
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-lib32

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
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
pushd ..
cp -a openssl-1.0.2n build32
popd


%build
export AR=gcc-ar
export RANLIB=gcc-ranlib
export CFLAGS="$CFLAGS -flto=8 -ffunction-sections -fsemantic-interposition -O3 -falign-functions=32 -falign-loops=32"
export CXXFLAGS="$CXXFLAGS -flto=8 -ffunction-sections -fsemantic-interposition -O3 "
export CXXFLAGS="$CXXFLAGS -flto=8 -fsemantic-interposition -O3 -falign-functions=32  "
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

./config shared no-ssl zlib-dynamic no-rc4 no-ssl2 no-ssl3  \
 --prefix=%{_prefix} \
 --openssldir=/etc/ssl \
 --openssldir_defaults=/usr/share/defaults/ssl \
 --libdir=lib64

make depend
make

#apps/openssl speed 
LD_PRELOAD="./libcrypto.so ./libssl.so" apps/openssl speed rsa

make clean

export CFLAGS="${CFLAGS_USE}" 
export CXXFLAGS="${CXXFLAGS_USE}" 
export FFLAGS="${FFLAGS_USE}" 
export FCFLAGS="${FCFLAGS_USE}" 

./config shared no-ssl zlib-dynamic no-rc4 no-ssl2 no-ssl3    \
 --prefix=%{_prefix} \
 --openssldir=/etc/ssl \
 --openssldir_defaults=/usr/share/defaults/ssl \
 --libdir=lib64

# parallel build is broken
make depend
make

pushd ../build32
export CFLAGS="$CFLAGS -m32 -fno-lto" 
export LDFLAGS="$LDFLAGS -m32 -fno-lto" 
export CXXFLAGS="$CXXFLAGS -m32 -fno-lto" 
i386 ./config shared no-ssl zlib-dynamic no-rc4 no-ssl2 no-ssl3 no-asm  \
 --prefix=%{_prefix} \
 --openssldir=/etc/ssl \
 --openssldir_defaults=/usr/share/defaults/ssl \
 --libdir=lib32 
make depend
make
popd


%install
pushd ../build32
export CFLAGS="$CFLAGS -m32 -fno-lto" 
export LDFLAGS="$LDFLAGS -m32 -fno-lto" 
export CXXFLAGS="$CXXFLAGS -m32 -fno-lto" 
make  INSTALL_PREFIX=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=openssl install
pushd %{buildroot}/usr/lib32/pkgconfig
for i in *.pc ; do mv $i 32$i ; done
popd
popd

export CFLAGS="$CFLAGS -m64 -flto" 
export LDFLAGS="$LDFLAGS -m64 -flto" 
export CXXFLAGS="$CXXFLAGS -m64 -flto" 

make  INSTALL_PREFIX=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=openssl install

mv %{buildroot}/etc/ssl/misc/c_hash %{buildroot}/usr/bin/c_hash
mv %{buildroot}/etc/ssl/openssl.cnf %{buildroot}/usr/share/defaults/ssl/openssl.cnf
rm -rf %{buildroot}/etc/ssl
rm -rf %{buildroot}/usr/lib64/*.a



%check
make test


%files
/usr/bin/openssl
/usr/bin/c_hash
/usr/lib64/engines/*.so
/usr/share/defaults/ssl/openssl.cnf

%files lib
/usr/lib64/libcrypto.so.1.0.0
/usr/lib64/libssl.so.1.0.0

%files lib32
/usr/lib32/libcrypto.so.1.0.0
/usr/lib32/libssl.so.1.0.0
/usr/lib32/engines/lib4758cca.so
/usr/lib32/engines/libaep.so
/usr/lib32/engines/libatalla.so
/usr/lib32/engines/libcapi.so
/usr/lib32/engines/libchil.so
/usr/lib32/engines/libcswift.so
/usr/lib32/engines/libgmp.so
/usr/lib32/engines/libgost.so
/usr/lib32/engines/libnuron.so
/usr/lib32/engines/libpadlock.so
/usr/lib32/engines/libsureware.so
/usr/lib32/engines/libubsec.so

%files dev
/usr/include/openssl/*.h
/usr/lib64/libcrypto.so
/usr/lib64/libssl.so
/usr/lib64/pkgconfig/libcrypto.pc
/usr/lib64/pkgconfig/libssl.pc
/usr/lib64/pkgconfig/openssl.pc

%files extras
%exclude /usr/bin/c_rehash

%files dev32
/usr/lib32/libcrypto.so
/usr/lib32/libssl.so
/usr/lib32/pkgconfig/32libcrypto.pc
/usr/lib32/pkgconfig/32libssl.pc
/usr/lib32/pkgconfig/32openssl.pc
/usr/lib32/libcrypto.a
/usr/lib32/libssl.a

%files doc
/usr/share/man/man1/*
/usr/share/man/man3/*
/usr/share/man/man5/*
/usr/share/man/man7/*
