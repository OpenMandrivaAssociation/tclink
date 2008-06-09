%define major 3
%define libname %mklibname tclink %{major}
%define develname %mklibname tclink -d

Summary:	TrustCommerce payment
Name:		tclink
Version:	3.4.4
Release:	%mkrel 1
Group:		System/Servers
License:	LGPL
URL:		http://www.trustcommerce.com/tclink.html
Source0:	http://www.trustcommerce.com/downloads/tclink-%{version}-C.tar.gz
Patch0:		tclink-3.4-C-soname.diff
Patch1:		tclink-correct_version.diff
BuildRequires:	openssl-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
TCLink is a thin client library to allow your e-commerce servers to
connect to the TrustCommerce payment gateway easily and consistently.
The protocol (which is the same across all platforms and languages) is
well-documented in the Web Developer's Guide, so please consult it for
any questions you may have about the protocol syntax itself.

The TrustCommerce web site is at http://www.trustcommerce.com

%package -n	%{libname}
Summary:	Main library for tclink
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with tclink (Trust Commerce Payment Gateway).

%package -n	%{develname}
Summary:	Headers for developping programs with TCLink
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	%{mklibname tclink 3 -d} = %{version}-%{release}
Obsoletes:	%{mklibname tclink 3 -d}

%description -n	%{develname}
This package contains the header file you need to develop applications
which will use TCLink (Trust Commerce Payment Gateway).

%prep

%setup -q -n %{name}-%{version}-C

%patch0 -p0
perl -pi -e "s|_MAJOR_|%{major}|g" Makefile*

%patch1 -p0

# fix strange perms
chmod 644 LICENSE README doc/*

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure.in

%build
rm -f configure
autoconf

%configure2_5x \
    --with-ssl-dir=%{_prefix}

%make MYFLAGS="" CFLAGS="%{optflags} -fPIC"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}

install -m0755 lib%{name}.so.%{major} %{buildroot}%{_libdir}/
ln -snf lib%{name}.so.%{major} %{buildroot}%{_libdir}/lib%{name}.so

install -m0644 lib%{name}.a %{buildroot}%{_libdir}/
install -m0644 tclink.h %{buildroot}%{_includedir}/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%doc LICENSE README
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc doc/TCDevGuide.txt doc/TCDevGuide.html
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
