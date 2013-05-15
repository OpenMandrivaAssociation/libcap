%define	major	2
%define	libname	%mklibname cap %{major}
%define	devname	%mklibname cap -d

%bcond_without	uclibc

Summary: 	Library for getting and setting POSIX.1e capabilities
Name: 		libcap
Version: 	2.22
Release: 	5
Group: 		System/Kernel and hardware
License: 	BSD/GPLv2
URL: 		http://www.kernel.org/pub/linux/libs/security/linux-privs/
Source0:	http://mirror.nexcess.net/kernel.org/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.gz
Source1:	http://mirror.nexcess.net/kernel.org/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.gz.asc
Source2:	ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.4/capfaq-0.2.txt
Patch0:		libcap-2.16-linkage_fix.diff
Patch1:		libcap-2.22-cross.patch
BuildRequires:	attr-devel
BuildRequires:	pam-devel
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-15
%endif

%description
%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package	utils
Summary:	Administration tools for POSIX.1e capabilities
Group:		System/Kernel and hardware

%description	utils
%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

This package contains utilities to control these capabilities.

%package -n	pam_cap
Summary:	PAM module for getting and setting POSIX.1e capabilities
Group:		System/Libraries

%description -n	pam_cap
The purpose of this module is to enforce inheritable capability sets for a
specified user.

%package -n	%{libname}
Summary:	Library for getting and setting POSIX.1e capabilities
Group:		System/Kernel and hardware
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package -n	uclibc-%{libname}
Summary:	Library for getting and setting POSIX.1e capabilities (uClibc linked)
Group:		System/Kernel and hardware
Provides:	%{name} = %{version}-%{release}

%description -n	uclibc-%{libname}
%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/Kernel
Requires:	%{libname} >= %{version}-%{release}
%if %{with uclibc}
Requires:	uclibc-%{libname} >= %{version}-%{release}
%endif
Provides:	%{name}-devel = %{version}-%{release}
Provides:       cap-devel = %{version}-%{release}
Conflicts:	%{mklibname cap 1 -d}

%description -n	%{devname}
Development files (Headers, libraries for static linking, etc) for %{name}.

%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Install %{name}-devel if you want to develop or compile applications supporting
Linux kernel capabilities.

%prep
%setup -q
%patch0 -p0
%patch1 -p1

install -m644 %{SOURCE2} .

perl -pi -e 's,^man_prefix=.*,man_prefix=\$\(prefix)/share,g' Make.Rules

%build
perl -pi -e "s|^CFLAGS\ :=.*|CFLAGS\ :=%{optflags} -fPIC -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64|g" Make.Rules
perl -pi -e "s|^LDFLAGS\ :=.*|LDFLAGS\ :=%{ldflags}|g" Make.Rules

%if %{with uclibc}
mkdir -p uclibc
# we build without libattr support for now..
%make -C libcap prefix=%{_prefix} CC=%{uclibc_cc} CFLAGS="%{uclibc_cflags} -fPIC -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64" LDCONFIG="%{ldconfig}" LIBATTR=no
mv libcap/libcap*.so* uclibc
make clean
%endif

%make prefix=%{_prefix} CC="%__cc" CFLAGS="%{uclibc_cflags} -fPIC -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64" LDCONFIG="%{ldconfig}"

%install
install -d %{buildroot}%{_sysconfdir}/security

make install prefix=%{_prefix} LIBDIR=%{buildroot}/%{_lib} FAKEROOT=%{buildroot} RAISE_SETFCAP=no
rm -f %{buildroot}/%{_lib}/libcap.so
install -d %{buildroot}%{_libdir}
ln -srf %{buildroot}/%{_lib}/libcap.so.%{major}.* %{buildroot}%{_libdir}/libcap.so
chmod 755 %{buildroot}/%{_lib}/libcap.so.%{major}.*

%if %{with uclibc}
install -d %{buildroot}%{uclibc_root}{/%{_lib},%{_libdir}}
cp -a uclibc/libcap.so.%{major}* %{buildroot}%{uclibc_root}/%{_lib}
ln -srf %{buildroot}%{uclibc_root}/%{_lib}/libcap.so.%{major}.* %{buildroot}%{uclibc_root}%{_libdir}/libcap.so
%endif

# conflics with man-pages
rm -f %{buildroot}%{_mandir}/man2/*

install -m0640 pam_cap/capability.conf %{buildroot}%{_sysconfdir}/security/

# cleanup
rm -f %{buildroot}/%{_lib}/*.a

%files utils
%doc CHANGELOG License README contrib
%{_sbindir}/capsh
%{_sbindir}/getcap
%{_sbindir}/getpcaps
%{_sbindir}/setcap
%{_mandir}/man8/getcap.8*
%{_mandir}/man8/setcap.8*

%files -n pam_cap
%doc pam_cap/License
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/security/capability.conf
/%{_lib}/security/pam_cap.so

%files -n %{libname}
/%{_lib}/libcap.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}/%{_lib}/libcap.so.%{major}*
%endif

%files -n %{devname}
%doc capfaq-0.2.txt
%{_includedir}/*
%{_libdir}/libcap.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libcap.so
%endif
%{_mandir}/man3/*.3*
%{_mandir}/man1/capsh.1.*

%changelog
* Wed Dec 12 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.22-5
- rebuild on ABF

* Mon Oct 29 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.22-4
+ Revision: 820500
- fix library permission for stripping (weird..)
- fix location of libcap.so symlink
- cosmetics
- add missing dependency on uclibc library for devel package

* Mon Sep 24 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.22-3
+ Revision: 817465
- do uClibc linked build

* Mon Dec 12 2011 Oden Eriksson <oeriksson@mandriva.com> 2.22-2
+ Revision: 740460
- stupid build system!!!
- fix build
- 2.22
- rediffed P0
- various fixes

* Fri Apr 29 2011 Oden Eriksson <oeriksson@mandriva.com> 2.19-7
+ Revision: 660224
- mass rebuild

* Thu Nov 25 2010 Oden Eriksson <oeriksson@mandriva.com> 2.19-6mdv2011.0
+ Revision: 601038
- rebuild

  + Matthew Dawkins <mattydaw@mandriva.org>
    - removed hardcoded compression extention for the man page

* Thu Apr 29 2010 Christophe Fergeau <cfergeau@mandriva.com> 2.19-5mdv2010.1
+ Revision: 540831
- rebuild so that shared libraries are properly stripped again

* Wed Apr 28 2010 Christophe Fergeau <cfergeau@mandriva.com> 2.19-4mdv2010.1
+ Revision: 540355
- rebuild so that shared libraries are properly stripped again

* Wed Apr 28 2010 Christophe Fergeau <cfergeau@mandriva.com> 2.19-3mdv2010.1
+ Revision: 540032
- rebuild so that shared libraries are properly stripped again

* Wed Apr 28 2010 Christophe Fergeau <cfergeau@mandriva.com> 2.19-2mdv2010.1
+ Revision: 540030
- rebuild so that shared libraries are properly stripped again

* Sun Mar 07 2010 Sandro Cazzaniga <kharec@mandriva.org> 2.19-1mdv2010.1
+ Revision: 515521
- fix file list
- update to 2.19

* Sat Dec 19 2009 Oden Eriksson <oeriksson@mandriva.com> 2.17-1mdv2010.1
+ Revision: 480177
- 2.17
- drop two patches not needed anymore

* Thu Mar 05 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.16-2mdv2009.1
+ Revision: 348913
- Remove workaround for kernel headers from /usr/include/sys/capability.h
  provided by libcap-devel, the inclusion of <sys/capability.h> should
  work with current pristine kernel-headers. Without this capability.h
  provided by libcap can break other packages because the hacking it
  does with defines. This fix build of current coreutils package and
  potentially others.

* Thu Dec 18 2008 Oden Eriksson <oeriksson@mandriva.com> 2.16-1mdv2009.1
+ Revision: 315551
- 2.16
- use CFLAGS from the %%serverbuild macro
- use LDFLAGS from the %%configure macro
- fix linkage

* Wed Jul 02 2008 Oden Eriksson <oeriksson@mandriva.com> 2.10-1mdv2009.0
+ Revision: 230575
- 2.10
- drop redundant patches
- added P0 to built the tools non static
- fix deps
- added the pam_cap sub package

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.10-10mdv2009.0
+ Revision: 222524
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Jan 02 2008 David Walluck <walluck@mandriva.org> 1.10-9mdv2008.1
+ Revision: 140301
- Provides: cap-devel = %%{version}-%%{release}

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Sep 19 2007 Oden Eriksson <oeriksson@mandriva.com> 1.10-8mdv2008.0
+ Revision: 90769
- new devel naming

* Fri Jun 08 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.10-7mdv2008.0
+ Revision: 37599
- sync with ALT Linux
- do parallel build


* Wed Nov 22 2006 Oden Eriksson <oeriksson@mandriva.com> 1.10-6mdv2007.0
+ Revision: 86113
- bunzip patches
- added P3 to avoid running ldconfig at "make install"
- spec file cleanups
- Import libcap

* Mon Jan 09 2006 Anssi Hannula <anssi@mandriva.org> 1.10-5mdk
- %%mkrel
- fix build, we now have comma in %%optflags
- drop false claims about not permitting caps
- fix requires-on-release

* Sat Jan 24 2004 Abel Cheung <deaddog@deaddog.org> 1.10-4mdk
- mklibname
- bzip2 patches
- spec fixes for 64bit
