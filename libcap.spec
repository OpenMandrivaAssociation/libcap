%define major 2
%define libname %mklibname cap %{major}
%define devname %mklibname cap -d

Summary:	Library for getting and setting POSIX.1e capabilities
Name:		libcap
Version:	2.25
Release:	3
Group:		System/Kernel and hardware
License:	BSD/GPLv2
Url:		http://www.kernel.org/pub/linux/libs/security/linux-privs/
Source0:	http://mirror.nexcess.net/kernel.org/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.xz
Source1:	ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.4/capfaq-0.2.txt
Patch0:		libcap-2.24-build-system-fixes.patch
Patch1:		libcap-2.22-no-perl.patch

BuildRequires:	attr-devel
BuildRequires:	pam-devel

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

%package -n pam_cap
Summary:	PAM module for getting and setting POSIX.1e capabilities
Group:		System/Libraries

%description -n	pam_cap
The purpose of this module is to enforce inheritable capability sets for a
specified user.

%package -n %{libname}
Summary:	Library for getting and setting POSIX.1e capabilities
Group:		System/Kernel and hardware
Provides:	%{name} = %{EVRD}

%description -n	%{libname}
%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/Kernel
Requires:	%{libname} >= %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	cap-devel = %{EVRD}
Conflicts:	%{mklibname cap 1 -d}

%description -n	%{devname}
Development files (Headers, libraries for static linking, etc) for %{name}.

%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Install %{name}-devel if you want to develop or compile applications supporting
Linux kernel capabilities.

%prep
%setup -q
%apply_patches

install -m644 %{SOURCE1} .

%build
%setup_compile_flags

# cb ensure fPIC set for i586 as otherwise it is missed causing issues
%make BUILD_CC=%{__cc} CC=%{__cc} PREFIX=%{_prefix} CFLAGS="%{optflags} -fPIC" LDFLAGS="%{ldflags}"

%install
install -d %{buildroot}%{_sysconfdir}/security

make install RAISE_SETFCAP=no \
	DESTDIR=%{buildroot} \
	LIBDIR=/%{_lib} \
	SBINDIR=%{_sbindir} \
	INCDIR=%{_includedir} \
	MANDIR=%{_mandir}/ \
	PKGCONFIGDIR=%{_libdir}/pkgconfig/

rm -f %{buildroot}/%{_lib}/libcap.so
install -d %{buildroot}%{_libdir}
ln -srf %{buildroot}/%{_lib}/libcap.so.%{major}.* %{buildroot}%{_libdir}/libcap.so
chmod 755 %{buildroot}/%{_lib}/libcap.so.%{major}.*

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

%files -n %{devname}
%doc capfaq-0.2.txt
%{_includedir}/*
%{_libdir}/libcap.so
%{_mandir}/man3/*.3*
%{_mandir}/man1/capsh.1.*
%{_libdir}/pkgconfig/libcap.pc
