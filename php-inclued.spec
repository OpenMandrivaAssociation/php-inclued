%define modname inclued
%define soname %{modname}.so
%define inifile A76_%{modname}.ini

Summary:	Clued-in about your inclueds extension for php
Name:		php-%{modname}
Version:	0.1.3
Release:	%mkrel 1
Group:		Development/PHP
License:	PHP License
URL:		http://pecl.php.net/package/inclued/
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Allows you trace through and dump the hierarchy of file inclusions and
class inheritance at runtime.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

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
rm -rf %{buildroot}

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
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml INSTALL gengraph.php
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Wed Jun 20 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.3-1mdv2012.0
+ Revision: 806391
- 0.1.3
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-7
+ Revision: 761260
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-6
+ Revision: 696436
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-5
+ Revision: 695411
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-4
+ Revision: 646653
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-3mdv2011.0
+ Revision: 629815
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-2mdv2011.0
+ Revision: 628136
- ensure it's built without automake1.7

* Wed Dec 01 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.2-1mdv2011.0
+ Revision: 604429
- 0.1.2

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-4mdv2011.0
+ Revision: 600500
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-3mdv2011.0
+ Revision: 588838
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-2mdv2010.1
+ Revision: 514563
- rebuilt for php-5.3.2

* Tue Feb 23 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.1-1mdv2010.1
+ Revision: 510103
- 0.1.1

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-11mdv2010.1
+ Revision: 485397
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-10mdv2010.1
+ Revision: 468179
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-9mdv2010.0
+ Revision: 451283
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0.1.0-8mdv2010.0
+ Revision: 397541
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-7mdv2010.0
+ Revision: 377001
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-6mdv2009.1
+ Revision: 346507
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-5mdv2009.1
+ Revision: 341769
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-4mdv2009.1
+ Revision: 321808
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-3mdv2009.1
+ Revision: 310279
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2mdv2009.0
+ Revision: 238406
- rebuild

* Fri Feb 29 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2008.1
+ Revision: 176843
- import php-inclued


* Fri Feb 29 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2008.1
- initial Mandriva package
