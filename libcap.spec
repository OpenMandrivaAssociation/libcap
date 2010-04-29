%define major 2
%define libname %mklibname cap %{major}
%define develname %mklibname cap -d

Summary: 	Library for getting and setting POSIX.1e capabilities
Name: 		libcap
Version: 	2.19
Release: 	%mkrel 5
Group: 		System/Kernel and hardware
License: 	BSD/GPLv2
URL: 		http://www.kernel.org/pub/linux/libs/security/linux-privs/
Source0:	http://www.kernel.org/pub/linux/libs/security/linux-privs/libcap2/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.4/capfaq-0.2.txt
Patch0:		libcap-2.16-linkage_fix.diff
BuildRequires:	attr-devel
BuildRequires:	pam-devel
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Requires:	%{libname} = %{version}-%{release}
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

install -m644 %{SOURCE1} .

perl -pi -e 's,^man_prefix=.*,man_prefix=\$\(prefix)/share,g' Make.Rules

%build
%serverbuild

# voodoo magic
LDFLAGS=`rpm --eval %%configure|grep LDFLAGS|cut -d\" -f2`
perl -pi -e "s|^CFLAGS\ :=.*|CFLAGS\ :=$CFLAGS|g" Make.Rules
perl -pi -e "s|^LDFLAGS\ :=.*|LDFLAGS\ :=$LDFLAGS|g" Make.Rules

%make prefix=%{_prefix}

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/security

make install prefix=%{_prefix} LIBDIR=%{buildroot}/%{_lib} FAKEROOT=%{buildroot}

# conflics with man-pages
rm -f %{buildroot}%{_mandir}/man2/*

install -m0640 pam_cap/capability.conf %{buildroot}%{_sysconfdir}/security/

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files utils
%defattr(-,root,root)
%doc CHANGELOG License README contrib
%{_sbindir}/capsh
%{_sbindir}/getcap
%{_sbindir}/getpcaps
%{_sbindir}/setcap
%{_mandir}/man8/getcap.8*
%{_mandir}/man8/setcap.8*

%files -n pam_cap
%defattr(-,root,root)
%doc pam_cap/License
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/security/capability.conf
/%{_lib}/security/pam_cap.so

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc capfaq-0.2.txt
%{_includedir}/*
/%{_lib}/*.so
/%{_lib}/*.a
%{_mandir}/man3/*
%{_mandir}/man1/capsh.1.lzma

