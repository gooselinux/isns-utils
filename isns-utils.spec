Name:           isns-utils
Version:        0.93
Release:        1.0%{?dist}
Summary:        The iSNS daemon and utility programs

Group:          System Environment/Daemons
License:        LGPLv2+
URL:            http://www.kernel.org/pub/linux/kernel/people/mnc/open-isns
Source0:        http://www.kernel.org/pub/linux/kernel/people/mnc/open-isns/releases/open-isns-%{version}.tar.bz2
Source1:        isnsd.init

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openssl-devel automake pkgconfig
Requires:       /sbin/chkconfig  /sbin/service

%description
The iSNS package contains the daemon and tools to setup a iSNS server,
and iSNS client tools. The Internet Storage Name Service (iSNS) protocol
allows automated discovery, management and configuration of iSCSI and
Fibre Channel devices (using iFCP gateways) on a TCP/IP network.

%prep
%setup -q -n open-isns-%{version}

%build
if pkg-config openssl ; then
        CPPFLAGS=$(pkg-config --cflags openssl) ; export CPPFLAGS
        LDFLAGS=$(pkg-config --libs openssl) ; export LDFLAGS
fi

autoconf
autoheader
%{configure}
%{__sed} -i -e 's|-Wall -g -O2|%{optflags}|' Makefile
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_sbindir}
%{__install} -d %{buildroot}%{_mandir}/man8
%{__install} -d %{buildroot}%{_mandir}/man5
%{__install} -d %{buildroot}%{_initrddir}
%{__install} -d %{buildroot}%{_sysconfdir}/isns
%{__install} -d %{buildroot}%{_var}/lib
%{__install} -d %{buildroot}%{_var}/lib/isns

%{__install} -p -m 644 etc/isnsd.conf %{buildroot}%{_sysconfdir}/isns/isnsd.conf
%{__install} -p -m 644 etc/isnsdd.conf %{buildroot}%{_sysconfdir}/isns/isnsdd.conf
%{__install} -p -m 644 etc/isnsadm.conf %{buildroot}%{_sysconfdir}/isns/isnsadm.conf

%{__install} -p -m 755 isnsd isnsdd isnsadm isnssetup %{buildroot}%{_sbindir}
%{__install} -p -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/isnsd
%{__install} -p -m 644 doc/isns_config.5 %{buildroot}/%{_mandir}/man5/
%{__install} -p -m 644 doc/isnsd.8 doc/isnsdd.8 doc/isnsadm.8 %{buildroot}/%{_mandir}/man8/


%post
/sbin/chkconfig --add isnsd

%postun
if [ "$1" = "1" ] ; then
     /sbin/service isnsd condrestart > /dev/null 2>&1
fi

%preun
if [ "$1" = "0" ] ; then
     /sbin/chkconfig isnsd stop > /dev/null 2>&1
     /sbin/chkconfig --del isnsd
fi

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc COPYING README
%{_sbindir}/isnsd
%{_sbindir}/isnsadm
%{_sbindir}/isnsdd
%{_sbindir}/isnssetup
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_initrddir}/isnsd
%dir %{_sysconfdir}/isns
%dir %{_var}/lib/isns
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/isns/*

%changelog
* Sun Jul 11 2010 Mike Christie <mchristie@redhat.com> - 0.93-1.0
- 585123 Fix service isnsd error return code
- 585120 Add service isnsd force-reload

* Mon Mar 22 2010 Mike Christie <mchristie@redhat.com> - 0.93-0.0
- Rebase to upstream 0.93 to bring in SCN fixes.

* Fri Feb 5 2010 Dennis Gregorovic <dgregor@redhat.com> - 0.91-4.2
- Update spec for pkwrangler issue: comment patches.

* Fri Dec 11 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.91-4.1
- Rebuilt for RHEL 6

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.91-4
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.91-1
- rebuild with new openssl

* Wed Jan 16 2008 Mike Christie <mchristie@redhat.com> - 0.91-0.0
- first build
