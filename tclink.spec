%define lib_major 3
%define lib_name_orig libtclink

%define libname %mklibname tclink %lib_major
%define libnamedev %{libname}-devel

%define tclink_c_version 3.4
%define tclink_version 3.4

Summary:	TrustCommerce payment
Name:		tclink
Version:	%{tclink_version}
Release:	%mkrel 6
Group:		System/Servers
License:	LGPL
URL:		http://www.trustcommerce.com/tclink.html
Source0:	%{name}-%{tclink_c_version}-C.tar.bz2
Patch0:		tclink-3.4-C-soname.diff
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

%package -n	%{libnamedev}
Summary:	Headers for developping programs with TCLink
Group:		Development/Other
Requires:	%{libname} = %version-%release
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{libnamedev}
This package contains the header file you need to develop applications
which will use TCLink (Trust Commerce Payment Gateway).

%prep

%setup -q -n %{name}-%{tclink_c_version}-C

%patch0 -p0
perl -pi -e "s|_MAJOR_|%{lib_major}|g" Makefile*

# fix strange perms
chmod 644 README doc/*

%build

%configure2_5x \
    --with-ssl-dir=%{_prefix}

%make CFLAGS="%{optflags} -fPIC"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/%{libname}
install -d %{buildroot}%{_includedir}/%{libname}

install -m0755 %{lib_name_orig}.so.%{lib_major} %{buildroot}%{_libdir}/
ln -snf %{lib_name_orig}.so.%{lib_major} %{buildroot}%{_libdir}/%{lib_name_orig}.so

install -m0755 %{lib_name_orig}.a %{buildroot}%{_libdir}/%{libname}/
install -m0644 tclink.h %{buildroot}%{_includedir}/%{libname}/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%doc README
%{_libdir}/*.so.*

%files -n %{libnamedev}
%defattr(-,root,root)
%doc doc/TCDevGuide.txt doc/TCDevGuide.html
%{_libdir}/*.so
%{_libdir}/%{libname}/*.a
%{_includedir}/%{libname}/*.h


