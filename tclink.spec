%define major 3
%define libname %mklibname tclink %{major}
%define develname %mklibname tclink -d

Summary:	TrustCommerce payment
Name:		tclink
Version:	3.4.4
Release:	20
Group:		System/Servers
License:	LGPL
URL:		https://www.trustcommerce.com/tclink.html
Source0:	http://www.trustcommerce.com/downloads/tclink-%{version}-C.tar.gz
Patch0:		tclink-3.4-C-soname.diff
Patch1:		tclink-correct_version.diff
Patch2:		tclink-linkage_order_fix.diff
BuildRequires:	openssl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch2 -p0

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
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}

install -m0755 lib%{name}.so.%{major} %{buildroot}%{_libdir}/
ln -snf lib%{name}.so.%{major} %{buildroot}%{_libdir}/lib%{name}.so

install -m0644 lib%{name}.a %{buildroot}%{_libdir}/
install -m0644 tclink.h %{buildroot}%{_includedir}/

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

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


%changelog
* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 3.4.4-9mdv2011.0
+ Revision: 670669
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 3.4.4-8mdv2011.0
+ Revision: 607984
- rebuild

* Fri Apr 09 2010 Funda Wang <fwang@mandriva.org> 3.4.4-7mdv2010.1
+ Revision: 533314
- rebuild

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 3.4.4-6mdv2010.1
+ Revision: 511644
- rebuilt against openssl-0.9.8m

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.4.4-5mdv2010.0
+ Revision: 427286
- rebuild

* Mon Dec 22 2008 Oden Eriksson <oeriksson@mandriva.com> 3.4.4-4mdv2009.1
+ Revision: 317663
- rebuild

* Wed Jul 02 2008 Oden Eriksson <oeriksson@mandriva.com> 3.4.4-3mdv2009.0
+ Revision: 230684
- added P2 to fix linkage
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Oct 28 2007 Oden Eriksson <oeriksson@mandriva.com> 3.4.4-1mdv2008.1
+ Revision: 102764
- 3.4.4


* Tue Oct 31 2006 Oden Eriksson <oeriksson@mandriva.com> 3.4-6mdv2007.0
+ Revision: 74497
- bunzip patches
- use the %%mkrel macro
- Import tclink

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 3.4-5mdk
- rebuilt against openssl-0.9.8a

* Wed Nov 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.4-4mdk
- nuke redundant provides

* Mon May 24 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.4-3mdk
- fix buildrequires

* Sun May 23 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.4-2mdk
- broke out the php extension into its own package
- P0, fix soname (where did it go?)
- update url
- misc spec file fixes

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 3.4-1mdk
- built for php 4.3.4
- TCLink-C 3.4
- TCLink-php 3.4

