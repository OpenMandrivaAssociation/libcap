%define major 1
%define libname %mklibname cap %{major}

Summary: 	Library for getting and setting POSIX.1e capabilities
Name: 		libcap
Version: 	1.10
Release: 	%mkrel 6
Group: 		System/Kernel and hardware
License: 	BSD/GPL
URL: 		ftp://ftp.kernel.org/pub/linux/libs/security/linux-privs/kernel-2.4
Source:		%{name}-%{version}.tar.bz2
Patch0: 	libcap-1.10-ia64.patch
Patch1: 	libcap-1.10-userland.patch
Patch2: 	libcap-1.10-shared.patch
Patch3: 	libcap-1.10-no_ldconfig.diff
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

%package -n	%{libname}-devel
Summary:	Development files for %{name}
Group:		Development/Kernel
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}

%description -n	%{libname}-devel
Development files (Headers, libraries for static linking, etc) for %{name}.

%{name} is a library for getting and setting POSIX.1e (formerly POSIX 6)
draft 15 capabilities.

Install %{name}-devel if you want to develop or compile applications supporting
Linux kernel capabilities.

%prep

%setup -q
%patch0 -p1 -b .ia64
%patch1 -p1 -b .userland
%patch2 -p1 -b .shared
%patch3 -p0 -b .no_ldconfig

perl -pi -e "s#^COPTFLAGS=.*#COPTFLAG=$RPM_OPT_FLAGS#g" Make.Rules
perl -pi -e 's,^man_prefix=.*,man_prefix=\$\(prefix)/share,g' Make.Rules

%build
make prefix=%{_prefix}

%install
rm -rf %{buildroot}

make install prefix=%{_prefix} LIBDIR=%{buildroot}/%{_lib} FAKEROOT=%{buildroot}

#mkdir %{buildroot}/%{_lib}
#mv %{buildroot}%{_libdir}/* %{buildroot}/%{_lib}/
#rm -rf %{buildroot}%{_libdir}

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

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
/%{_lib}/*.so
%{_mandir}/man3/*


