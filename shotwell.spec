Name:           shotwell
Version:        0.31.3
Release:        1
Summary:        A photo organizer for the GNOME desktop
License:        LGPLv2+ and CC-BY-SA
URL:            https://wiki.gnome.org/Apps/Shotwell
Source0:        https://download.gnome.org/sources/shotwell/0.31/shotwell-%{version}.tar.xz
BuildRequires:  vala
BuildRequires:  desktop-file-utils
BuildRequires:  appstream-glib >= 0.7.3
BuildRequires:  gettext
BuildRequires:  itstool
BuildRequires:  meson
BuildRequires:  pkgconfig(atk)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(champlain-0.12)
BuildRequires:  pkgconfig(champlain-gtk-0.12)
BuildRequires:  pkgconfig(clutter-1.0)
BuildRequires:  pkgconfig(clutter-gtk-1.0)
BuildRequires:  pkgconfig(gcr-3)
BuildRequires:  pkgconfig(gcr-ui-3)
BuildRequires:  pkgconfig(gdk-3.0)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gdk-x11-3.0)
BuildRequires:  pkgconfig(gee-0.8) >= 0.8.5
BuildRequires:  pkgconfig(gexiv2) >= 0.10.4
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.20
BuildRequires:  pkgconfig(glib-2.0) >= 2.40.0
BuildRequires:  pkgconfig(gmodule-2.0) >= 2.24.0
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.0.0
BuildRequires:  pkgconfig(gstreamer-base-1.0) >= 1.0.0
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0) >= 1.0.0
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0) >= 1.0.0
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.14.0
BuildRequires:  pkgconfig(gudev-1.0) >= 145
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libexif) >= 0.6.16
BuildRequires:  pkgconfig(libgdata)
BuildRequires:  pkgconfig(libgphoto2) >= 2.5.0
BuildRequires:  pkgconfig(libraw) >= 0.13.2
BuildRequires:  pkgconfig(libsoup-2.4) >= 2.42.0
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libwebpdemux)
BuildRequires:  pkgconfig(libxml-2.0) >= 2.6.32
BuildRequires:  pkgconfig(sqlite3) >= 3.5.9
BuildRequires:  pkgconfig(webkit2gtk-4.0) >= 2.6.3
BuildRequires:  pkgconfig(libsecret-1)

# Needed by the publishing plugins
BuildRequires:  pkgconfig(rest-0.7) >= 0.7

# used by shotwell-settings-migrator
Requires:       dconf

%description
Shotwell is an easy-to-use, fast photo organizer designed for the GNOME
desktop.  It allows you to import photos from your camera or disk, organize
them by date and subject matter, even ratings.  It also offers basic photo
editing, like crop, red-eye correction, color adjustments, and straighten.
Shotwell's non-destructive photo editor does not alter your master photos,
making it easy to experiment and correct errors.


%prep
%setup


%build
export LANG=C.UTF-8
export GCC_IGNORE_WERROR=1
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export CFLAGS="$CFLAGS -O3 -ffat-lto-objects -flto=4 "
export FCFLAGS="$CFLAGS -O3 -ffat-lto-objects -flto=4 "
export FFLAGS="$CFLAGS -O3 -ffat-lto-objects -flto=4 "
export CXXFLAGS="$CXXFLAGS -O3 -ffat-lto-objects -flto=4 "
CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" LDFLAGS="$LDFLAGS" meson --libdir=lib64 --prefix=/usr --buildtype=plain -Dinstall-apport-hook=false  builddir
ninja -v -C builddir

%install
DESTDIR=%{buildroot} ninja -C builddir install


%find_lang %{name} --with-gnome


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Shotwell.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Shotwell-Viewer.desktop

%post -p /usr/bin/ldconfig

%postun -p /usr/bin/ldconfig

%files -f %{name}.lang
%license COPYING
%doc README.md NEWS THANKS AUTHORS
%{_bindir}/shotwell
%{_libdir}/shotwell
%{_libdir}/libshotwell-authenticator.so.*
%exclude %{_libdir}/libshotwell-authenticator.so
%{_libdir}/libshotwell-plugin-common.so.*
%exclude %{_libdir}/libshotwell-plugin-common.so
%{_libdir}/libshotwell-plugin-dev-1.0.so.*
%exclude %{_libdir}/libshotwell-plugin-dev-1.0.so
%{_libexecdir}/shotwell
%{_datadir}/applications/org.gnome.Shotwell.desktop
%{_datadir}/applications/org.gnome.Shotwell-Viewer.desktop
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/icons/hicolor/*/apps/org.gnome.Shotwell.png
%{_datadir}/icons/hicolor/symbolic/apps/org.gnome.Shotwell-symbolic.svg
%{_datadir}/metainfo/org.gnome.Shotwell.appdata.xml
%{_mandir}/man1/*
/usr/share/apport/package-hooks/shotwell.py


%changelog
# based on https://src.fedoraproject.org/rpms/shotwell/blob/master/f/shotwell.spec
