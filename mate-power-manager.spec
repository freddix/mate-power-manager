Summary:	MATE Power Manager
Name:		mate-power-manager
Version:	2.30.1
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.mate.org/pub/mate/sources/mate-power-manager/2.30/%{name}-%{version}.tar.bz2
# Source0-md5:	b85178b8db77db5d22e185430549a295
Patch0:		%{name}-dont-spam-tray.patch
URL:		http://www.mate.org/projects/mate-power-manager/
BuildRequires:	GConf-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	docbook-dtd41-sgml
BuildRequires:	docbook-utils
BuildRequires:	mate-doc-utils
BuildRequires:	mate-panel-devel
BuildRequires:	libcanberra-gtk-devel
BuildRequires:	libnotify-devel
BuildRequires:	libtool
BuildRequires:	libunique-devel
BuildRequires:	libwnck-devel
BuildRequires:	pkg-config
BuildRequires:	upower-devel
Requires(post,preun):	GConf
Requires(post,postun):	gtk+
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	rarian
Requires:	ConsoleKit
Requires:	upower
Requires:	xdg-desktop-notification-daemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Uses of MATE Power Manager infrastructure
- A dialogue that warns the user when on UPS power, that automatically
  begins a kind shutdown when the power gets critically low.
- An icon that allows a user to dim the LCD screen with a slider, and
  does do automatically when going from mains to battery power on a
  laptop.
- An icon, that when an additional battery is inserted, updates it's
  display to show two batteries and recalculates how much time
  remaining. Would work for wireless mouse and keyboards, UPS's and
  PDA's.
- A daemon that does a clean shutdown when the battery is critically
  low or does a soft-suspend when you close the lid on your laptop (or
  press the "suspend" button on your PC).
- Tell Totem to use a codec that does low quality processing to
  conserve battery power.
- Postpone indexing of databases (e.g. up2date) or other heavy
  operations until on mains power.
- Presentation programs / movie players don't want the screensaver
  starting or screen blanking.

%package -n mate-applet-pm-brightness
Summary:        Adjusts Laptop panel brightness
Group:          Applications
Requires:	%{name} = %{version}-%{release}
Requires:	mate-panel

%description -n mate-applet-pm-brightness
Adjusts Laptop panel brightness.

%package -n mate-applet-pm-inhibit
Summary:        Allows user to inhibit automatic power saving
Group:          Applications
Requires:	%{name} = %{version}-%{release}
Requires:	mate-panel

%description -n mate-applet-pm-inhibit
Allows user to inhibit automatic power saving.

%prep
%setup -q
%patch0 -p1

# kill mate common deps
sed -i -e 's/mate_COMPILE_WARNINGS.*//g'	\
    -i -e 's/mate_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/mate_COMMON_INIT//g'		\
    -i -e 's/mate_CXX_WARNINGS.*//g'		\
    -i -e 's/mate_DEBUG_CHECK//g' configure.ac

%build
%{__intltoolize}
%{__mate_doc_prepare}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-schemas-install	\
	--disable-scrollkeeper
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	autostartdir=%{_sysconfdir}/xdg/autostart

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}

%find_lang %{name} --with-mate --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install mate-power-manager.schemas
%scrollkeeper_update_post
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall mate-power-manager.schemas

%postun
%scrollkeeper_update_postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/mate-power-bugreport.sh
%attr(755,root,root) %{_bindir}/mate-power-manager
%attr(755,root,root) %{_bindir}/mate-power-preferences
%attr(755,root,root) %{_bindir}/mate-power-statistics

%{_datadir}/dbus-1/services/*.service
%{_datadir}/%{name}
%{_desktopdir}/*
%{_iconsdir}/hicolor/*/*/*
%{_mandir}/man1/*
%{_sysconfdir}/gconf/schemas/mate-power-manager.schemas
%{_sysconfdir}/xdg/autostart/mate-power-manager.desktop

%files -n mate-applet-pm-brightness
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mate-brightness-applet
%{_libdir}/bonobo/servers/mate_BrightnessApplet.server
%{_datadir}/mate-2.0/ui/mate_BrightnessApplet.xml

%files -n mate-applet-pm-inhibit
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mate-inhibit-applet
%{_libdir}/bonobo/servers/mate_InhibitApplet.server
%{_datadir}/mate-2.0/ui/mate_InhibitApplet.xml

