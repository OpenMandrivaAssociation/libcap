# libcap is used by systemd, libsystemd is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif
# For bootstrapping:
# libcap depends on pam
# pam depends on libsystemd (logind), which in turn depends on libcap
%bcond_without pam

%define _disable_ld_no_undefined 1

%define major 2
%define oldlibname %mklibname cap 2
%define libname %mklibname cap
%define oldlibpsx %mklibname psx 2
%define libpsx %mklibname psx
%define devname %mklibname cap -d
%define oldlib32name libcap2
%define lib32name libcap
%define oldlib32psx libpsx2
%define lib32psx libpsx
%define dev32name libcap-devel

Summary:	Library for getting and setting POSIX.1e capabilities
Name:		libcap
Version:	2.69
Release:	1
Group:		System/Kernel and hardware
License:	BSD/GPLv2
Url:		http://www.kernel.org/pub/linux/libs/security/linux-privs/
Source0:	https://mirrors.edge.kernel.org/pub/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.xz
Source1:	ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.4/capfaq-0.2.txt
#Patch0:		libcap-2.29-build-system-fixes.patch
BuildRequires:	pkgconfig(libattr)
%if %{with pam}
BuildRequires:	pam-devel
%endif
%if %{with compat32}
BuildRequires:	devel(libattr)
BuildRequires:	libc6
%endif
%if %{with compat32}
# Since the lib32name is libcap, the main package
# doubles as lib32package
%rename %{oldlib32name}
%endif
%if "%{libname}" == "%{name}"
# Same if we're on a 32-bit platform
%rename %{oldlibname}
%endif

%description
%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package utils
Summary:	Administration tools for POSIX.1e capabilities
Group:		System/Kernel and hardware

%description utils
%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

This package contains utilities to control these capabilities.

%package	docs
Summary:	Docs for %{libname}
Group:		System/Kernel and hardware

%description docs
%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package -n pam_cap
Summary:	PAM module for getting and setting POSIX.1e capabilities
Group:		System/Libraries

%description -n pam_cap
The purpose of this module is to enforce inheritable capability sets for a
specified user.

%if "%{libname}" != "%{name}"
%package -n %{libname}
Summary:	Library for getting and setting POSIX.1e capabilities
Group:		System/Kernel and hardware
%rename %{oldlibname}

%description -n %{libname}
%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.
%endif

%package -n %{libpsx}
Summary:	Library for getting and setting POSIX.1e capabilities
Group:		System/Kernel and hardware
%rename %{oldlibpsx}

%description -n %{libpsx}
%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/Kernel
Requires:	%{libname} >= %{EVRD}
Requires:	%{libpsx} >= %{EVRD}
Requires:	%{name}-utils >= %{EVRD}
Provides:	cap-devel = %{EVRD}
Conflicts:	%{mklibname cap 1 -d} < 2.27-2

%description -n	%{devname}
Development files (Headers, libraries for static linking, etc) for %{name}.

%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Install %{name}-devel if you want to develop or compile applications supporting
Linux kernel capabilities.

%if %{with compat32}
%package -n %{lib32psx}
Summary:	Library for getting and setting POSIX.1e capabilities (32-bit)
Group:		System/Kernel and hardware
%rename %{oldlib32psx}

%description -n %{lib32psx}
%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package -n %{dev32name}
Summary:	Development files for %{name} (32-bit)
Group:		Development/Kernel
Requires:	%{devname} >= %{EVRD}
Requires:	%{lib32name} >= %{EVRD}
Requires:	%{lib32psx} >= %{EVRD}
Requires:	libc6

%description -n %{dev32name}
Development files (Headers, libraries for static linking, etc) for %{name}.

%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Install %{name}-devel if you want to develop or compile applications supporting
Linux kernel capabilities.
%endif

%prep
%autosetup -p1
sed -i 's!--static!!g' tests/Makefile progs/Makefile

install -m644 %{SOURCE1} .

%build
%set_build_flags

%if %{with compat32}
mkdir build32
cp -a $(ls -1 |grep -v build32) build32/
cd build32
%make_build BUILD_CC="clang" CC="gcc -m32" PREFIX=%{_prefix} CFLAGS="$(echo %{optflags} |sed -e 's,-m64,,g;s,-mx32,,g') -m32" LDFLAGS="$(echo %{build_ldflags} |sed -e 's,-m64,,g;s,-mx32,,g') -m32" LIBDIR=%{_prefix}/lib lib=lib PAM_CAP=no GOLANG=no
cd ..
%endif

# cb ensure fPIC set for i586 as otherwise it is missed causing issues
# FIXME get rid of GOLANG=no once we know why it's failing to build
%make_build BUILD_CC="clang" CC="%{__cc}" PREFIX=%{_prefix} CFLAGS="%{optflags} -Oz -fPIC" %{?with_pam:LDFLAGS="%{build_ldflags} -lpam"} LIBDIR=%{_libdir} lib=%{_lib} GOLANG=no OBJCOPY=llvm-objcopy PAM_CAP=%{?with_pam:yes}%{!?with_pam:no}

%install
install -d %{buildroot}%{_sysconfdir}/security

%if %{with compat32}
cd build32
%make_install RAISE_SETFCAP=no \
	DESTDIR=%{buildroot} \
	lib=lib \
	LIBDIR=%{_prefix}/lib \
	SBINDIR=%{_sbindir} \
	INCDIR=%{_includedir} \
	MANDIR=%{_mandir}/ \
	PAM_CAP=no GOLANG=no \
	PKGCONFIGDIR=%{_prefix}/lib/pkgconfig/
rm -f %{buildroot}/%{_prefix}/lib/*.a
cd ..
%endif

%make_install RAISE_SETFCAP=no \
	DESTDIR=%{buildroot} \
	lib=%{_lib} \
	LIBDIR=%{_libdir} \
	SBINDIR=%{_sbindir} \
	INCDIR=%{_includedir} \
	MANDIR=%{_mandir}/ \
	GOLANG=no \
	PKGCONFIGDIR=%{_libdir}/pkgconfig/ \
	PAM_CAP=%{?with_pam:yes}%{!?with_pam:no}

# conflicts with man-pages
rm -f %{buildroot}%{_mandir}/man2/*

%if %{with pam}
install -m0640 pam_cap/capability.conf %{buildroot}%{_sysconfdir}/security/
%endif

# cleanup
rm -f %{buildroot}%{_libdir}/*.a

# -L%{_libdir} is evil
# Using find here so compat32 stuff is included
find %{buildroot} -name "*.pc" |xargs sed -i -e 's,-L\${libdir} ,,g'

%files utils
%{_sbindir}/getcap
%{_sbindir}/getpcaps
%{_sbindir}/setcap
%{_sbindir}/capsh
%doc %{_mandir}/man8/*.8*

%files docs
%doc CHANGELOG License README contrib

%if %{with pam}
%files -n pam_cap
%doc pam_cap/License
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/security/capability.conf
%{_libdir}/security/pam_cap.so
%endif

%files -n %{libname}
%{_libdir}/libcap.so.%{major}*

%files -n %{libpsx}
%{_libdir}/libpsx.so.%{major}*

%files -n %{devname}
%doc capfaq-0.2.txt
%{_includedir}/*
%{_libdir}/libcap.so
%{_libdir}/libpsx.so
%doc %{_mandir}/man3/*.3*
%doc %{_mandir}/man1/capsh.1.*
%{_libdir}/pkgconfig/libcap.pc
%{_libdir}/pkgconfig/libpsx.pc

%if %{with compat32}
%files
%{_prefix}/lib/libcap.so.%{major}*

%files -n %{lib32psx}
%{_prefix}/lib/libpsx.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libcap.so
%{_prefix}/lib/libpsx.so
%{_prefix}/lib/pkgconfig/libcap.pc
%{_prefix}/lib/pkgconfig/libpsx.pc
%endif
