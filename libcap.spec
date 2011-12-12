%define major 2
%define libname %mklibname cap %{major}
%define develname %mklibname cap -d

Summary: 	Library for getting and setting POSIX.1e capabilities
Name: 		libcap
Version: 	2.22
Release: 	1
Group: 		System/Kernel and hardware
License: 	BSD/GPLv2
URL: 		http://www.kernel.org/pub/linux/libs/security/linux-privs/
Source0:	http://mirror.nexcess.net/kernel.org/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.gz
Source1:	http://mirror.nexcess.net/kernel.org/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.gz.asc
Source2:	ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.4/capfaq-0.2.txt
Patch0:		libcap-2.16-linkage_fix.diff
BuildRequires:	attr-devel
BuildRequires:	pam-devel

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

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/Kernel
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:       cap-devel = %{version}-%{release}
Conflicts:	%{mklibname cap 1 -d}

%description -n	%{develname}
Development files (Headers, libraries for static linking, etc) for %{name}.

%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Install %{name}-devel if you want to develop or compile applications supporting
Linux kernel capabilities.

%prep

%setup -q
%patch0 -p0

install -m644 %{SOURCE2} .

perl -pi -e 's,^man_prefix=.*,man_prefix=\$\(prefix)/share,g' Make.Rules

%build
%serverbuild

perl -pi -e "s|^CFLAGS\ :=.*|CFLAGS\ :=$CFLAGS -fPIC -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64|g" Make.Rules
perl -pi -e "s|^LDFLAGS\ :=.*|LDFLAGS\ :=%{ldflags}|g" Make.Rules

%make prefix=%{_prefix}

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/security

make install prefix=%{_prefix} LIBDIR=%{buildroot}/%{_lib} FAKEROOT=%{buildroot} RAISE_SETFCAP=no

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
/%{_lib}/lib*.so.%{major}*

%files -n %{develname}
%doc capfaq-0.2.txt
%{_includedir}/*
/%{_lib}/*.so
%{_mandir}/man3/*
%{_mandir}/man1/capsh.1.*
