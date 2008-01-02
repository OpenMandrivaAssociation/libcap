%define major 1
%define libname %mklibname cap %{major}
%define develname %mklibname cap -d

Summary: 	Library for getting and setting POSIX.1e capabilities
Name: 		libcap
Version: 	1.10
Release: 	%mkrel 9
Group: 		System/Kernel and hardware
License: 	BSD/GPL
URL: 		ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.4
Source0:	ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.4/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.4/capfaq-0.2.txt
Patch0: 	libcap-1.10-ia64.patch
Patch4:		libcap-1.10-alt-makefile.patch
Patch5:		libcap-1.10-alt-cap_free.patch
Patch6:		libcap-1.10-alt-bound.patch
Patch7:		libcap-1.10-alt-warnings.patch
Patch8:		libcap-1.10-rh-alt-makenames.patch
Patch9:		libcap-1.10-alt-userland.patch
Patch10:	libcap-1.10-alt-cap_file.patch
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

%package	utils
Summary:	Administration tools for POSIX.1e capabilities
Group:		System/Kernel and hardware
Requires:	%{libname} = %{version}

%description	utils
%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

This package contains utilities to control these capabilities.

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
Obsoletes:	%{mklibname cap 1 -d} < %{version}-%{release}

%description -n	%{develname}
Development files (Headers, libraries for static linking, etc) for %{name}.

%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Install %{name}-devel if you want to develop or compile applications supporting
Linux kernel capabilities.

%prep

%setup -q
%patch0 -p1 -b .ia64
%patch4 -p1 -b .makefile
%patch5 -p1 -b .cap_free
%patch6 -p1 -b .warnings
%patch8 -p1 -b .makenames
%patch9 -p1 -b .userland
%patch10 -p1 -b .cap_file

install -m644 %{SOURCE1} .

perl -pi -e "s#^COPTFLAGS=.*#COPTFLAG=$RPM_OPT_FLAGS#g" Make.Rules
perl -pi -e 's,^man_prefix=.*,man_prefix=\$\(prefix)/share,g' Make.Rules

%build
%make prefix=%{_prefix}

%install
rm -rf %{buildroot}

make install prefix=%{_prefix} LIBDIR=%{buildroot}/%{_lib} FAKEROOT=%{buildroot}

# conflics with man-pages
rm -f %{buildroot}%{_mandir}/man2/*

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files utils
%defattr(-,root,root)
%doc CHANGELOG License README
%{_sbindir}/*

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc capfaq-0.2.txt
%{_includedir}/*
/%{_lib}/*.so
%{_mandir}/man3/*
