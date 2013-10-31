Summary:	MATE Power Manager
Name:		mate-power-manager
Version:	1.6.2
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	d53c728b39922514ce2c907b20645e4f
URL:		http://www.mate.org/projects/mate-power-manager/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	libcanberra-gtk-devel
BuildRequires:	libnotify-devel
BuildRequires:	libtool
BuildRequires:	libunique-devel
BuildRequires:	mate-doc-utils
BuildRequires:	mate-panel-devel
BuildRequires:	pkg-config
BuildRequires:	systemd-devel
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	rarian
Requires:	upower
Requires:	xdg-desktop-notification-daemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%package -n mate-panel-applet-pm-brightness
Summary:        Adjusts Laptop panel brightness
Group:          Applications
Requires:	%{name} = %{version}-%{release}
Requires:	mate-panel

%description -n mate-panel-applet-pm-brightness
Adjusts Laptop panel brightness.

%package -n mate-panel-applet-pm-inhibit
Summary:        Allows user to inhibit automatic power saving
Group:          Applications
Requires:	%{name} = %{version}-%{release}
Requires:	mate-panel

%description -n mate-panel-applet-pm-inhibit
Allows user to inhibit automatic power saving.

%prep
%setup -q

# kill mate-common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_CXX_WARNINGS.*/d'		\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-schemas-compile	\
	--disable-scrollkeeper		\
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT				\
	autostartdir=%{_sysconfdir}/xdg/autostart	\
	uidir=%{_datadir}/mate-panel/ui

%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/*.convert
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang %{name} --with-mate --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%scrollkeeper_update_postun
%update_icon_cache hicolor
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/mate-power-bugreport.sh
%attr(755,root,root) %{_bindir}/mate-power-manager
%attr(755,root,root) %{_bindir}/mate-power-preferences
%attr(755,root,root) %{_bindir}/mate-power-statistics
%attr(755,root,root) %{_sbindir}/mate-power-backlight-helper
%{_datadir}/dbus-1/services/*.service
%{_datadir}/polkit-1/actions/org.mate.power.policy
%{_datadir}/glib-2.0/schemas/org.mate.power-manager.gschema.xml
%{_datadir}/%{name}
%{_desktopdir}/*
%{_iconsdir}/hicolor/*/*/*
%{_sysconfdir}/xdg/autostart/mate-power-manager.desktop

%files -n mate-panel-applet-pm-brightness
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mate-brightness-applet
%{_datadir}/mate-panel/applets/org.mate.BrightnessApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/brightness-applet-menu.xml

%files -n mate-panel-applet-pm-inhibit
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mate-inhibit-applet
%{_datadir}/mate-panel/applets/org.mate.InhibitApplet.mate-panel-applet
%{_datadir}/mate-panel/ui/inhibit-applet-menu.xml

