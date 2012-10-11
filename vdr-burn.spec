%define pname   burn
%define gver    0.1.3

Name:           vdr-%{pname}
Version:        0.2.0
Release:        3%{?dist}
Summary:        DVD writing plugin for VDR

Group:          Applications/Multimedia
# genindex is GPLv2+, rest GPL+
License:        GPL+ and GPLv2+
URL:            http://projects.vdr-developer.org/projects/plg-burn
Source0:        http://projects.vdr-developer.org/attachments/download/832/%{name}-%{version}.tgz
Source1:        %{name}.conf
Source2:        http://www.muempf.de/down/genindex-%{gver}.tar.gz
# upstream patch >= vdr-1.7.27
# http://projects.vdr-developer.org/news/172
Patch0:         vdr-1.7.27-burn-0.2.0.diff
Patch1:         %{name}-%{version}-config.patch
# upstream patch for Fedora 18
# http://projects.vdr-developer.org/issues/1085
Patch2:         %{name}-%{version}-PRIO_PGRP.patch
# upstream fsf-fix patch
# http://projects.vdr-developer.org/issues/1086
Patch3:         %{name}-%{version}-fsf-fix.patch

BuildRequires:  vdr-devel >= 1.7.30
BuildRequires:  boost-devel
BuildRequires:  gd-devel
Requires:       vdr(abi)%{?_isa} = %{vdr_apiversion}
Requires:       vdrsync
Requires:       ProjectX
Requires:       m2vrequantiser
Requires:       dvdauthor
Requires:       mjpegtools
Requires:       dvd+rw-tools
Requires:       dejavu-lgc-sans-fonts
Conflicts:      ProjectX < 0.90.4.00.b29

%description
This plugin enables VDR to write compliant DVDs from VDR recordings
while being able to control the process and to watch progress from
inside VDRs on-screen-display.  If the selected recordings don't fit
the DVD, the video tracks are requantized (shrinked) automatically.
The created menus support multipage descriptions (in case the
recording summary exceeds one page).


%prep
%setup -q -c -a 2

cd burn-0.2.0
find -name CVS | xargs rm -rf
chmod -c -x *.[ch] genindex/*.[ch] proctools/*.cc proctools/*.h README
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0

sed -i -e 's|/var/lib/vdr/|%{vdr_vardir}/|g' chain-archive.c jobs.c vdrburn-*.sh
sed -i -e 's|"Vera"|"DejaVuLGCSans"|g' skins.c

cd ../genindex-%{gver}
sed -i -e 's/-g -O2/$(RPM_OPT_FLAGS)/' Makefile
f=README ; iconv -f iso-8859-1 -t utf-8 -o ../README.genindex $f
cd ..


%build
make -C burn-%{version} %{?_smp_mflags} LIBDIR=. LOCALEDIR=./locale VDRDIR=%{_libdir}/vdr all
make -C genindex-%{gver} %{?_smp_mflags}


%install
install -dm 755 $RPM_BUILD_ROOT%{vdr_plugindir}/bin
install -pm 755 burn-%{version}/libvdr-%{pname}.so.%{vdr_apiversion} $RPM_BUILD_ROOT%{vdr_plugindir}
install -pm 755 burn-%{version}/*.sh genindex-%{gver}/genindex \
  $RPM_BUILD_ROOT%{vdr_plugindir}/bin
install -dm 755 $RPM_BUILD_ROOT%{vdr_configdir}/plugins/burn/skins
cp -pR burn-%{version}/burn/* $RPM_BUILD_ROOT%{vdr_configdir}/plugins/burn
rm -rf $RPM_BUILD_ROOT%{vdr_configdir}/plugins/burn/{counters,fonts/*}
ln -s %{_datadir}/fonts/dejavu/DejaVuLGCSans.ttf \
  $RPM_BUILD_ROOT%{vdr_configdir}/plugins/burn/fonts/
install -Dpm 644 burn-%{version}/burn/counters/standard \
  $RPM_BUILD_ROOT%{vdr_vardir}/burn/counters/standard
install -Dpm 644 %{SOURCE1} \
  $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/vdr-plugins.d/%{pname}.conf


%post
if [ $1 -gt 1 ] ; then # maybe upgrading from < 0.1.0?
  %{__perl} -pi -e 's/^.*(burnmark|handlearchived)\.sh.*\n$//' \
    %{vdr_configdir}/reccmds.conf >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%doc burn-%{version}/COPYING burn-%{version}/HISTORY burn-%{version}/README README.genindex
%config(noreplace) %{_sysconfdir}/sysconfig/vdr-plugins.d/%{pname}.conf
%config(noreplace) %{vdr_configdir}/plugins/%{pname}/
%{vdr_plugindir}/bin/genindex
%{vdr_plugindir}/bin/vdrburn-archive.sh
%{vdr_plugindir}/bin/vdrburn-dvd.sh
%{vdr_plugindir}/libvdr-%{pname}.so.%{vdr_apiversion}
%defattr(-,%{vdr_user},root)
%config(noreplace) %{vdr_vardir}/burn/


%changelog
* Thu Oct 11 2012 Martin Gansser <linux4martin@gmx.de> - 0.2.0-3
- rebuild for Fedora 18.

* Wed Oct 10 2012 Martin Gansser <linux4martin@gmx.de> - 0.2.0-2
- removed vdrsync Requirenment
- removed no-subtitle patch

* Sun Oct 07 2012 Martin Gansser <linux4martin@gmx.de> - 0.2.0-1
- spec file cleanup
- rebuild for new release
- Adapt to VDR 1.7.30.
- added priority header patch for Fedora 18.

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.1.0-0.20.pre21
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.1.0-0.19.pre21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Mar 27 2009 Felix Kaechele <felix at fetzig dot org> - 0.1.0-0.18.pre21
- and again

* Sat Jan 03 2009 Felix Kaechele <felix at fetzig dot org> - 0.1.0-0.17.pre21
- fixed font deps (once again)

* Mon Dec 15 2008 Felix Kaechele <felix at fetzig dot org> - 0.1.0-0.16.pre21
- fixed dejavu-lgc-* deps

* Thu Nov 27 2008 Felix Kaechele <felix at fetzig dot org> - 0.1.0-0.15.pre21
- rebuilt due to path adjustments in vdr main package

* Mon Aug 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.1.0-0.14.pre21
- rebuild

* Tue Apr 22 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.1.0-0.13.pre21
- Use UTF-8 with VDR 1.6.x.
- Disable subtitles with VDR 1.6.x and ProjectX by default (demux problems).

* Tue Apr  8 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.1.0-0.12.pre21
- Patch to fix build with GCC 4.3's cleaned up C++ headers.

* Tue Apr  8 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.1.0-0.11.pre21
- Rebuild for VDR 1.6.0.

* Sat Dec  1 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.1.0-0.10.pre21
- Use /dev/dvdrw as the default writer device, udev >= 115 no longer creates
  /dev/dvdwriter.

* Sun Nov 18 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.1.0-0.9.pre21
- Adjust font paths for dejavu-lgc-fonts 2.21+.
- Drop old gd-devel missing dependency workaround.

* Wed Aug 22 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.1.0-0.8.pre21
- Use DejaVu LGC fonts instead of Bitstream Vera.
- Improve comments in burn.conf.
- License: GPL+ and GPLv2+

* Sun Jan  7 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.1.0-0.7.pre21
- Rebuild for VDR 1.4.5.

* Tue Dec 12 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.1.0-0.6.pre21
- 0.1.0-pre21, include private copy of genindex (0.1.3) for now.

* Sat Nov  4 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-16
- Rebuild for VDR 1.4.4.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.0.009-15
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sat Sep 23 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-14
- Rebuild for VDR 1.4.3.

* Sun Aug  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-13
- Rebuild for VDR 1.4.1-3.

* Sun Jun 11 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-12
- Rebuild for VDR 1.4.1.

* Sun Apr 30 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-11
- Rebuild for VDR 1.4.0.

* Mon Apr 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-10
- Rebuild/adjust for VDR 1.3.47, require versioned vdr(abi).
- Trim pre-RLO %%changelog entries.

* Sun Mar 26 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-9
- Rebuild for VDR 1.3.45.

* Sat Mar 18 2006 Thorsten Leemhuis <fedora at leemhuis.info> - 0.0.009-8
- drop 0.lvn

* Wed Mar  1 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-0.lvn.8
- Decrease default DVD size to 4420 to accommodate more requant inaccuracy.
- Rebuild for VDR 1.3.44.

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Sun Feb 19 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-0.lvn.7
- Rebuild for VDR 1.3.43.

* Sun Feb  5 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-0.lvn.6
- Rebuild for VDR 1.3.42.

* Sun Jan 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-0.lvn.5
- Rebuild for VDR 1.3.40.

* Sun Jan 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-0.lvn.4
- Rebuild for VDR 1.3.39.

* Sun Jan  8 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-0.lvn.3
- Rebuild for VDR 1.3.38.

* Sat Dec 31 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-0.lvn.2
- Q'n'd fix for ISO creation with recordings whose title contain "/".
- Fix storing of the "clean up after # jobs" configuration option.
- Don't chmod everything in results to 0777 in author only mode.
- Use tcmplex-panteltje by default again.
- Translation improvements.
- Fix up some paths in README.
- Ship TODO.

* Sun Nov 13 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-0.lvn.1
- 0.0.009 + Finnish translations from Rolf Ahrenberg, config patch
  applied upstream.

* Sat Nov 12 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.0.007-0.lvn.1
- 0.0.007, endstatus and burndefault patches applied/obsoleted upstream.

* Sun Nov  6 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.0.6k-0.lvn.2
- Rebuild for VDR 1.3.36.

* Tue Nov  1 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.0.6k-0.lvn.1
- 0.0.6k, commands and VDR >= 1.3.25 patches applied upstream.
- Improve default burn settings.
- Fix burn status at end when not verifying.

* Mon Oct  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.0.6g-1.lvn.8.pre3
- Rebuild for VDR 1.3.34.

* Sun Sep 25 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.0.6g-1.lvn.7.pre3
- Rebuild for VDR 1.3.33.

* Sun Sep 11 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.0.6g-1.lvn.6.pre3
- Rebuild for VDR 1.3.32.

* Tue Aug 30 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.0.6g-1.lvn.5.pre3
- Rebuild for VDR 1.3.31.

* Sun Aug 21 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.0.6g-1.lvn.4.pre3
- Rebuild for VDR 1.3.30.

* Fri Aug 19 2005 Dams <anvil[AT]livna.org> - 0.0.6g-1.lvn.3.pre3
- Redirected vdr-config invocation standard error to /dev/null

* Tue Aug 16 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.0.6g-1.lvn.2.pre3
- Try to avoid build system problems by not using %%expand with vdr-config.

* Fri Aug 12 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.0.6g-1.lvn.1.pre3
- Update URLs.
