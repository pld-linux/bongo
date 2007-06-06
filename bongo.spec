# TODO:
# - create -libs (to make -devel installable without server)?
# - are static modules (%{_libdir}/*/*.a) usable for anything?
Summary:	A calendar and mail server
Summary(pl.UTF-8):	Serwer kalendarza i poczty
Name:		bongo
Version:	0.2.0
Release:	1
License:	LGPL
Group:		Daemons
Source0:	http://download.gna.org/bongo/release/bongo-0.2.0.tar.bz2
# Source0-md5:	fe860c172f774d6f8564412f8ed56064
Source1:	%{name}.init
URL:		http://bongo-project.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	sqlite3-devel
BuildRequires:	clucene-core-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	group(bongo)
Provides:	user(bongo)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bongo is a calendar and mail server. The project is focused on building
a calendar and mail server that people love to use, instead of broadly
trying to build a "groupware server" that managers want to deploy.

%description -l pl.UTF-8
Bongo to serwer kalendarza i poczty. Projekt ten skupia się na
stworzeniu serwera kalendarza i poczty, który ludzie lubiliby używać,
zamiast próbować stworzyć "serwer pracy grupowej", który menadżerowie
chcieliby wdrożyć.

%package devel
Summary:	Development files for bongo
Summary(pl.UTF-8):	Pliki programistyczne serwera bongo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for developing add-ons for
bongo.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia dodatków dla serwera
bongo.

%package static
Summary:	Static libraries for bongo
Summary(pl.UTF-8):	Statyczne biblioteki bongo
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libraries for bongo.

%description static -l pl.UTF-8
Statyczne biblioteki bongo.

%prep
%setup -q

%build
%configure \
	--with-user=bongo
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/bongo

# remove all .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/connmgr/*.la \
	$RPM_BUILD_ROOT%{_libdir}/bongomdb/*.la \
	$RPM_BUILD_ROOT%{_libdir}/*.la \
	$RPM_BUILD_ROOT%{_libdir}/modweb/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 171 bongo
%useradd -u 171 -c "Bongo" -g 171 -s /sbin/nologin -r bongo

%post
/sbin/ldconfig
/sbin/chkconfig --add bongo
%service bongo restart

%preun
if [ "$1" = 0 ]; then
	%service bongo stop
	/sbin/chkconfig --del bongo
fi

%postun
if [ "$1" = "0" ]; then
	/sbin/ldconfig
	%userremove lula
	%groupremove lula
fi

%files
%defattr(644,root,root,755)
%doc HACKING TODO AUTHORS README style-guide.html
#%attr(754,root,root) /etc/rc.d/init.d/bongo
%attr(755,root,root) %{_bindir}/bongosqlite
%attr(755,root,root) %{_bindir}/mwcomp
%attr(755,root,root) %{_sbindir}/bongoadmin
%attr(755,root,root) %{_sbindir}/bongoantispam
%attr(755,root,root) %{_sbindir}/bongoavirus
%attr(755,root,root) %{_sbindir}/bongobackup
%attr(755,root,root) %{_sbindir}/bongocalagent
%attr(755,root,root) %{_sbindir}/bongocalcmd
%attr(755,root,root) %{_sbindir}/bongoconnmgr
%attr(755,root,root) %{_sbindir}/bongodmc
%attr(755,root,root) %{_sbindir}/bongoforward
%attr(755,root,root) %{_sbindir}/bongogeneric
%attr(755,root,root) %{_sbindir}/bongoimap
%attr(755,root,root) %{_sbindir}/bongoindexer
%attr(755,root,root) %{_sbindir}/bongomailprox
%attr(755,root,root) %{_sbindir}/bongomanager
%attr(755,root,root) %{_sbindir}/bongomodweb
%attr(755,root,root) %{_sbindir}/bongonmap
%attr(755,root,root) %{_sbindir}/bongopluspack
%attr(755,root,root) %{_sbindir}/bongopop3
%attr(755,root,root) %{_sbindir}/bongoqueue
%attr(755,root,root) %{_sbindir}/bongorules
%attr(755,root,root) %{_sbindir}/bongosendmail
%attr(755,root,root) %{_sbindir}/bongosetup
%attr(755,root,root) %{_sbindir}/bongosmtp
%attr(755,root,root) %{_sbindir}/bongostats
%attr(755,root,root) %{_sbindir}/bongoweb
%attr(755,root,root) %{_sbindir}/bongowebadmin
%attr(755,root,root) %{_sbindir}/mdbtool

%dir %{_libdir}/connmgr
%attr(755,root,root) %{_libdir}/connmgr/lib*.so
%dir %{_libdir}/bongomdb
%attr(755,root,root) %{_libdir}/bongomdb/lib*.so
%dir %{_libdir}/modweb
%{_libdir}/modweb/*.ctp
%attr(755,root,root) %{_libdir}/modweb/lib*.so
%dir %{_libdir}/netmail
%dir %{_libdir}/netmail/schemas
%{_libdir}/netmail/schemas/webadmin.sch
%dir %{_pkgconfigdir}
%{_pkgconfigdir}/bongo.pc
%dir %{_libdir}/webadmin
%{_libdir}/webadmin/*.wat

%attr(755,root,root) %{_libdir}/libbongocalcmd.so.0.0.0
%attr(755,root,root) %{_libdir}/libbongoconnio.so.0.0.0
%attr(755,root,root) %{_libdir}/libbongoconnmgr.so.0.0.0
%attr(755,root,root) %{_libdir}/libbongoical.so.0.0.0
%attr(755,root,root) %{_libdir}/libbongoical2.so.0.0.0
%attr(755,root,root) %{_libdir}/libbongolog4c.so.0.0.0
%attr(755,root,root) %{_libdir}/libbongologger.so.0.0.0
%attr(755,root,root) %{_libdir}/libbongomanagement.so.0.0.0
%attr(755,root,root) %{_libdir}/libbongomdb.so.0.0.0
%attr(755,root,root) %{_libdir}/libbongomemmgr.so.0.0.0
%attr(755,root,root) %{_libdir}/libbongomsgapi.so.0.0.0
%attr(755,root,root) %{_libdir}/libbongonmap.so.0.0.0
%attr(755,root,root) %{_libdir}/libbongostreamio.so.0.0.0
%attr(755,root,root) %{_libdir}/libbongoutil.so.0.0.0
%attr(755,root,root) %{_libdir}/libbongoxpl.so.0.0.0
%attr(755,root,root) %{_libdir}/libical-bongo.so.0.0.0
%attr(755,root,root) %{_libdir}/libicalss-bongo.so.0.0.0
%attr(755,root,root) %{_libdir}/libicalvcal-bongo.so.0.0.0
%attr(755,root,root) %{_libdir}/libwacert.so.0.0.0
%attr(755,root,root) %{_libdir}/libwanmail.so.0.0.0
%attr(755,root,root) %{_libdir}/libwastats.so.0.0.0
%attr(755,root,root) %{_libdir}/libwastdobj.so.0.0.0

%dir %{_libdir}/bongo
%attr(755,root,root) %{_libdir}/bongo/bongomonohelper
%{_libdir}/bongo/Bongo.Sharp.dll
%{_libdir}/bongo/Bongo.Sharp.dll.mdb
%{_libdir}/bongo/BongoIndexer.exe
%{_libdir}/bongo/BongoIndexer.exe.config
%{_libdir}/bongo/BongoIndexer.exe.mdb
%{_libdir}/bongo/BongoWeb.exe
%{_libdir}/bongo/BongoWeb.exe.config
%{_libdir}/bongo/BongoWeb.exe.mdb
%{_libdir}/bongo/Lucene.Net.dll
%{_libdir}/bongo/Mono.WebServer.dll

%{_libdir}/bongo/calcmd
%{_libdir}/bongo/dav
%{_libdir}/bongo/import
%{_libdir}/bongo/queue
%{_libdir}/bongo/log4net.dll
%{_libdir}/bongo/search
%{_datadir}/bongo/zoneinfo

%files devel
%defattr(644,root,root,755)
%{_includedir}/bongo
%dir %{_libdir}/webadmin
%{_libdir}/webadmin/9stats.wat
%{_pkgconfigdir}/bongo-sharp.pc

%attr(755,root,root) %{_libdir}/libbongocalcmd.so
%attr(755,root,root) %{_libdir}/libbongoconnio.so
%attr(755,root,root) %{_libdir}/libbongoconnmgr.so
%attr(755,root,root) %{_libdir}/libbongoical.so
%attr(755,root,root) %{_libdir}/libbongoical2.so
%attr(755,root,root) %{_libdir}/libbongolog4c.so
%attr(755,root,root) %{_libdir}/libbongologger.so
%attr(755,root,root) %{_libdir}/libbongomanagement.so
%attr(755,root,root) %{_libdir}/libbongomdb.so
%attr(755,root,root) %{_libdir}/libbongomemmgr.so
%attr(755,root,root) %{_libdir}/libbongomsgapi.so
%attr(755,root,root) %{_libdir}/libbongonmap.so
%attr(755,root,root) %{_libdir}/libbongostreamio.so
%attr(755,root,root) %{_libdir}/libbongoutil.so
%attr(755,root,root) %{_libdir}/libbongoxpl.so
%attr(755,root,root) %{_libdir}/libical-bongo.so
%attr(755,root,root) %{_libdir}/libicalss-bongo.so
%attr(755,root,root) %{_libdir}/libicalvcal-bongo.so
%attr(755,root,root) %{_libdir}/libwacert.so
%attr(755,root,root) %{_libdir}/libwanmail.so
%attr(755,root,root) %{_libdir}/libwastats.so
%attr(755,root,root) %{_libdir}/libwastdobj.so

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%dir %{_libdir}/connmgr
%{_libdir}/connmgr/lib*.a
%dir %{_libdir}/bongomdb
%{_libdir}/bongomdb/lib*.a
%dir %{_libdir}/modweb
%{_libdir}/modweb/lib*.a
