#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	The password hash Argon2, winner of PHC
Summary(pl.UTF-8):	Skrót haseł Argon2 - zwycięzca PHC
Name:		libargon2
Version:	20171227
Release:	1
License:	Apache v2.0, CC0 v1.0
Group:		Libraries
Source0:	https://github.com/P-H-C/phc-winner-argon2/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7d0a85aa3fa02a5962ff751a6e2078c8
Patch0:		makefile.patch
URL:		https://github.com/P-H-C/phc-winner-argon2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the reference C implementation of Argon2, the password-hashing
function that won the Password Hashing Competition (PHC).

Argon2 is a password-hashing function that summarizes the state of the
art in the design of memory-hard functions and can be used to hash
passwords for credential storage, key derivation, or other
applications.

It has a simple design aimed at the highest memory filling rate and
effective use of multiple computing units, while still providing
defense against tradeoff attacks (by exploiting the cache and memory
organization of the recent processors).

%description -l pl.UTF-8
Ta biblioteka jest referencyjną implementacją w C funkcji skrotu haseł
Argon2, która wygrała Password Hashing Competition (PHC).

Argon2 to funkcja skrótu podsumowująca stan techniki w projektowaniu
złożonych pamięciowo funkcji skrótu, które mogą być używane do
haszowania haseł do uwierzytelniania, tworzenia kluczy lub innych
zastosowań.

Funkcja jest zaprojektowana w prosty sposób, nakierowany na najwięszy
współczynnik wypełniania pamięci i efektywne użycie wielu jednostek
obliczeniowych, nadal zapewniając ochronę przeciw atakom kompromisowym
(wykorzystując pamięć podręczną i organizację pamięci współczesnych
procesorów).

%package devel
Summary:	Header files for libargon2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libargon2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libargon2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libargon2.

%package static
Summary:	Static libargon2 library
Summary(pl.UTF-8):	Statyczna biblioteka libargon2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libargon2 library.

%description static -l pl.UTF-8
Statyczna biblioteka libargon2.

%prep
%setup -q -n phc-winner-argon2-%{version}
%patch0 -p1

%build
CFLAGS="%{rpmcflags}" \
%{__make} \
	CC="%{__cc}" \
	%{!?with_static_libs:LIBRARIES='$(LIB_SH)'}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}

%{__make} install \
	INSTALL="install -p" \
	PREFIX=%{_prefix} \
	%{!?with_static_libs:LIBRARIES='$(LIB_SH)'} \
	LIBRARY_REL=%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT

%{__sed} libargon2.pc -e 's#libdir=.*#libdir=${prefix}/%{_lib}#g' \
	-e 's#@UPSTREAM_VER@#%{version}#g' >$RPM_BUILD_ROOT%{_pkgconfigdir}/libargon2.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md LICENSE
%attr(755,root,root) %{_bindir}/argon2
%attr(755,root,root) %ghost %{_libdir}/libargon2.so.1
%attr(755,root,root) %{_libdir}/libargon2.so.1.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/argon2.h
%attr(755,root,root) %{_libdir}/libargon2.so
%{_pkgconfigdir}/libargon2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libargon2.a
%endif
