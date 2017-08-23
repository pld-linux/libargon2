#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

Summary:	The password hash Argon2, winner of PHC
Name:		libargon2
Version:	20161029
Release:	1
License:	Apache-2.0 CC0-1.0
Group:		Libraries
Source0:	https://github.com/P-H-C/phc-winner-argon2/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bd3476cb8eac9d521a4e0e04d653f5a8
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

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q -n phc-winner-argon2-%{version}

%if %{without static_libs}
sed -i -e 's/LIBRARIES = \$(LIB_SH) \$(LIB_ST)/LIBRARIES = \$(LIB_SH)/' Makefile
%endif
sed -i -e 's/-O3 //' Makefile
sed -i -e 's/-g //' Makefile
sed -i -e "s/-march=\$(OPTTARGET) /%{rpmcflags} /" Makefile
sed -i -e 's/CFLAGS += -march=\$(OPTTARGET)//' Makefile

%build
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md LICENSE
%attr(755,root,root) %{_bindir}/argon2
%{_prefix}/lib/libargon2.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/argon2.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_prefix}/lib/libargon2.a
%endif
