Summary:	GNOME-DB widget library
Summary(pl.UTF-8):	Biblioteka widgetów GNOME-DB
Name:		libgnomedb3
Version:	3.1.2
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/libgnomedb/3.1/libgnomedb-%{version}.tar.bz2
# Source0-md5:	9896bd66451c3f1e2bdd1cd79d524348
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-gtk-doc.patch
URL:		http://www.gnome-db.org/
BuildRequires:	GConf2-devel >= 2.0
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.8
# only checked for, not used
#BuildRequires:	evolution-data-server-devel >= 1.2
BuildRequires:	gettext-devel
BuildRequires:	gnome-common >= 2.12.0
BuildRequires:	goocanvas-devel >= 0.9
BuildRequires:	gtk+2-devel >= 2:2.10.0
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	gtksourceview-devel >= 1.0
BuildRequires:	intltool
BuildRequires:	libgda3-devel >= 3.1.2
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libgladeui-devel >= 3.4.0
BuildRequires:	libgnomecanvas-devel >= 2.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	scrollkeeper
# hildon-libs (only checked, not used)
Requires(post):	/sbin/ldconfig
Requires(post,preun):	GConf2 >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libgnomedb is a library that eases the task of writing GNOME database
programs.

%description -l pl.UTF-8
libgnomedb jest biblioteką ułatwiającą pisanie programów bazodanowych.

%package devel
Summary:	GNOME-DB widget library development
Summary(pl.UTF-8):	Dla programistów widgetu GNOME-DB
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	GConf2-devel >= 2.0
Requires:	gtk+2-devel >= 2:2.10.0
Requires:	gtksourceview-devel >= 1.0
Requires:	libgda3-devel >= 3.1.1
Requires:	libglade2-devel >= 1:2.6.0
# for libgnomedb_graph only
Requires:	libgnomecanvas-devel >= 2.0

%description devel
libgnomedb is a library that eases the task of writing GNOME database
programs. This package contains development files.

%description devel -l pl.UTF-8
libgnomedb jest biblioteką ułatwiającą pisanie programów bazodanowych.
Ten podpakiet zawiera pliki dla programistów używających libgda.

%package static
Summary:	GNU Data Access static libraries
Summary(pl.UTF-8):	Statyczne biblioteki GNU Data Access
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
GNOME-DB widget static libraries.

%description static -l pl.UTF-8
Statyczne biblioteki widgetu GNOME-DB.

%package apidocs
Summary:	libgnomedb API documentation
Summary(pl.UTF-8):	Dokumentacja API libgnomedb
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libgnomedb API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libgnomedb.

%package -n gnome-database-access-properties3
Summary:	Database access properties
Summary(pl.UTF-8):	Właściwości dostępu do baz danych
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires(post,postun):	scrollkeeper

%description -n gnome-database-access-properties3
Allows to configure database access properties in GNOME.

%description -n gnome-database-access-properties3 -l pl.UTF-8
Pozwala na konfigurację dostępu do baz danych w GNOME.

%package -n glade3-libgnomedb3
Summary:	libgnomedb3 support for glade3
Summary(pl.UTF-8):	Wsparcie dla libgnomedb3 w glade3.
Group:		Development/Building
Requires:	%{name} = %{version}-%{release}
Requires:	glade3

%description -n glade3-libgnomedb3
libgnomedb3 support for glade3.

%description -n glade3-libgnomedb3 -l pl.UTF-8
Wsparcie dla libgnomedb3 w glade3.

%prep
%setup -q -n libgnomedb-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install \
	--enable-gnome \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no static modules and *.la for glade and libgnomedb modules
rm -f $RPM_BUILD_ROOT%{_libdir}/{glade3/modules,libglade/2.0,gnome-db-3.0/plugins/}/*.{la,a}

# move to examplesdir?
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome-db-3.0/demo

%find_lang libgnomedb-3.0

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install libgnomedb-3.0.schemas

%preun
%gconf_schema_uninstall libgnomedb-3.0.schemas

%postun	-p /sbin/ldconfig

%post apidocs
%scrollkeeper_update_post

%postun apidocs
%scrollkeeper_update_postun

%files -f libgnomedb-3.0.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS
%attr(755,root,root) %{_libdir}/libgnomedb-3.0.so.*.*.*
%attr(755,root,root) %{_libdir}/libgnomedb_extra-3.0.so.*.*.*
%attr(755,root,root) %{_libdir}/libgnomedb_goo-3.0.so.*.*.*
%attr(755,root,root) %{_libdir}/libgnomedb_graph-3.0.so.*.*.*
%dir %{_libdir}/gnome-db-3.0
%dir %{_libdir}/gnome-db-3.0/plugins
%attr(755,root,root) %{_libdir}/gnome-db-3.0/plugins/libgnomedb_entry_builtin_plugins.so
# libglade2 module (include it here as lib requires libglade2 anyway)
%attr(755,root,root) %{_libdir}/libglade/2.0/libgnomedb-3.0.so
# for libgnomedb
%dir %{_datadir}/gnome-db-3.0
%{_datadir}/gnome-db-3.0/server_operation.glade
%{_datadir}/gnome-db-3.0/gnome-db-entry-*.xml
%{_datadir}/gnome-db-3.0/import_encodings.xml
%{_pixmapsdir}/gnome-db-3.0
# for libgnomedb_extra
%{_sysconfdir}/gconf/schemas/libgnomedb-3.0.schemas

%files -n glade3-libgnomedb3
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/glade3/modules/libgladegnomedb.so
%{_datadir}/glade3/catalogs/gnomedb.xml
%{_datadir}/glade3/catalogs/gnomedb.xml.in
%{_datadir}/glade3/pixmaps/*/*/*/*.png

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnomedb-3.0.so
%attr(755,root,root) %{_libdir}/libgnomedb_extra-3.0.so
%attr(755,root,root) %{_libdir}/libgnomedb_goo-3.0.so
%attr(755,root,root) %{_libdir}/libgnomedb_graph-3.0.so
%{_libdir}/libgnomedb-3.0.la
%{_libdir}/libgnomedb_extra-3.0.la
%{_libdir}/libgnomedb_goo-3.0.la
%{_libdir}/libgnomedb_graph-3.0.la
%{_includedir}/libgnomedb-3.0
%{_pkgconfigdir}/libgnomedb-3.0.pc
%{_pkgconfigdir}/libgnomedb-extra-3.0.pc
%{_pkgconfigdir}/libgnomedb-goo-3.0.pc
%{_pkgconfigdir}/libgnomedb-graph-3.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgnomedb-3.0.a
%{_libdir}/libgnomedb_extra-3.0.a
%{_libdir}/libgnomedb_goo-3.0.a
%{_libdir}/libgnomedb_graph-3.0.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libgnomedb-3.0
%{_omf_dest_dir}/libgnomedb

%files -n gnome-database-access-properties3
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gnome-database-properties-3.0
%attr(755,root,root) %{_bindir}/gnome-db-browser
%attr(755,root,root) %{_bindir}/gnome-db-demo
%{_desktopdir}/database-properties-3.0.desktop
%{_pixmapsdir}/libgnomedb-3.0
%{_pixmapsdir}/libgnomedb-3.0/gnome-db.png
