%define modname inclued
%define soname %{modname}.so
%define inifile A76_%{modname}.ini

Summary:	Clued-in about your inclueds extension for php

Name:		php-%{modname}
Version:	0.1.3
Release:	2
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/inclued/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Patch0:         inclued-0.1.3-php5.5.patch
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	file

%description
Allows you trace through and dump the hierarchy of file inclusions and
class inheritance at runtime.

%prep
%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .
%patch0 -p3

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make

%install

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}/var/log/httpd

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}

[%{modname}]
inclued.dumpdir	= /tmp
inclued.enabled	= On
EOF

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files 
%doc package*.xml INSTALL gengraph.php
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



