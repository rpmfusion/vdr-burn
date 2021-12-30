%global gver    0.1.3
%global pname   burn
%global __provides_exclude_from ^%{vdr_libdir}/.*\\.so.*$

Name:           vdr-%{pname}
Version:        0.3.0
Release:        24%{?dist}
Summary:        DVD writing plugin for VDR

# genindex is GPLv2+, rest GPL+
License:        GPL+ and GPLv2+
URL:            https://projects.vdr-developer.org/projects/plg-burn
Source0:        https://projects.vdr-developer.org/attachments/download/2028/%{name}-%{version}.tgz
Source1:        %{name}.conf
Source2:        http://www.muempf.de/down/genindex-%{gver}.tar.gz
Patch0:         %{name}-0.3.0-config.patch
Patch1:         %{name}-0.3.0-old-sd-recordings.patch

BuildRequires:  gcc-c++
BuildRequires:  vdr-devel >= 2.0.6
BuildRequires:  boost-devel
BuildRequires:  gd-devel >= 2.0.33-9.3
BuildRequires:  gettext
Requires:       vdr(abi)%{?_isa} = %{vdr_apiversion}
Requires:       ProjectX >= 0.90.4.00.b29
Requires:       m2vrequantiser
Requires:       dvdauthor
Requires:       mjpegtools
Requires:       dvd+rw-tools
Requires:       dejavu-sans-fonts
Requires:       pxsup2dast

%description
This plugin enables VDR to write compliant DVDs from VDR recordings
while being able to control the process and to watch progress from
inside VDRs on-screen-display.  If the selected recordings don't fit
the DVD, the video tracks are requantized (shrinked) automatically.
The created menus support multipage descriptions (in case the
recording summary exceeds one page).


%prep
%setup -q -c -a 2
mv %{pname}-%{version} burn ; cd burn
%patch0 -p2
%patch1 -p0
sed -i -e 's|/var/lib/vdr/|%{vdr_vardir}/|g' chain-archive.c jobs.c scripts/vdrburn-*.sh
sed -i -e 's|"Vera"|"DejaVuSans"|g' skins.c

sed -i -e 's|std::auto_ptr|std::unique_ptr|' jobs.h
sed -i -e 's|std::auto_ptr<chain_vdr> m_process;|std::unique_ptr<chain_vdr> m_process;|' jobs.h
sed -i -e 's|std::auto_ptr<job> m_pending;|std::unique_ptr<job> m_pending;|' manager.h
sed -i -e 's|auto_ptr<process> dtemp( proc );|std::unique_ptr<process> dtemp( proc );|' proctools/chain.cc

cd ../genindex-%{gver}
sed -i -e 's/-g -O2/$(RPM_OPT_FLAGS)/' Makefile
f=README ; iconv -f iso-8859-1 -t utf-8 -o ../README.genindex $f
cd ..


%build
# main build not parallel clean (libvdr-burn.so -> proctools/libproctools.a)
make -C burn ISODIR=%{vdr_videodir} all
make -C genindex-%{gver} %{?_smp_mflags}


%install
make -C burn install-lib install-sh install-res install-i18n DESTDIR=%{buildroot}

install -pm 755 genindex-%{gver}/genindex \
  $RPM_BUILD_ROOT%{vdr_bindir}
install -dm 755 $RPM_BUILD_ROOT%{vdr_configdir}/plugins/burn/skins
install -Dpm 644 burn/config/ProjectX.ini $RPM_BUILD_ROOT%{vdr_configdir}/plugins/burn/
install -Dpm 644 burn/config/vdrburn-dvd.conf $RPM_BUILD_ROOT%{vdr_configdir}/plugins/burn/

# remove bundling font
rm -rf $RPM_BUILD_ROOT%{vdr_resdir}/plugins/burn/{counters,fonts/*}
ln -s %{_datadir}/fonts/dejavu/DejaVuSans.ttf \
  $RPM_BUILD_ROOT%{vdr_resdir}/plugins/burn/fonts/

install -Dpm 644 burn/config/counters/standard \
  $RPM_BUILD_ROOT%{vdr_vardir}/burn/config/counters/standard

install -Dpm 644 %{SOURCE1} \
  $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/vdr-plugins.d/%{pname}.conf
%find_lang %{name}


%files -f %{name}.lang
%doc burn/HISTORY burn/README README.genindex
%license burn/COPYING
%config(noreplace) %{_sysconfdir}/sysconfig/vdr-plugins.d/%{pname}.conf
%config(noreplace) %{vdr_configdir}/plugins/%{pname}/
%{vdr_resdir}/plugins/%{pname}/
%{vdr_bindir}/genindex
%{vdr_bindir}/vdrburn-archive.sh
%{vdr_bindir}/vdrburn-dvd.sh
%{vdr_libdir}/libvdr-%{pname}.so.%{vdr_apiversion}
%defattr(-,%{vdr_user},root)
%config(noreplace) %{vdr_vardir}/burn/
%defattr(-,root,root,-)


%changelog
* Thu Dec 30 2021 Martin Gansser <martinkg@fedoraproject.org> - 0.3.0-24
- Rebuilt for new VDR API version

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 30 2021 Martin Gansser <martinkg@fedoraproject.org> - 0.3.0-22
- Rebuilt for new VDR API version

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 04 2021 Martin Gansser <martinkg@fedoraproject.org> - 0.3.0-20
- Rebuilt for new VDR API version

* Wed Oct 21 2020 Martin Gansser <martinkg@fedoraproject.org> - 0.3.0-19
- Rebuilt for new VDR API version

* Fri Aug 28 2020 Martin Gansser <martinkg@fedoraproject.org> - 0.3.0-18
- Rebuilt for new VDR API version

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 01 2019 Martin Gansser <martinkg@fedoraproject.org> - 0.3.0-14
- Rebuilt for new VDR API version 2.4.1

* Sun Jun 30 2019 Martin Gansser <martinkg@fedoraproject.org> - 0.3.0-13
- Rebuilt for new VDR API version

* Tue Jun 18 2019 Martin Gansser <martinkg@fedoraproject.org> - 0.3.0-12
- Rebuilt for new VDR API version

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Martin Gansser <martinkg@fedoraproject.org> - 0.3.0-10
- Add BR  gcc-c++

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 0.3.0-9
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 18 2018 Martin Gansser <martinkg@fedoraproject.org> - 0.3.0-7
- Rebuilt for vdr-2.4.0

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jun 25 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.3.0-3
- rebuild due new libvpx version

* Sat May 07 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.3.0-2
- Added vdr-burn-0.3.0-old-sd-recordings.patch

* Sun Apr 03 2016 Martin Gansser <martinkg@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0

* Tue Mar 17 2015 Martin Gansser <martinkg@fedoraproject.org> - 0.2.2-8
- added vdr-burn-vdr2.1.2-compat.patch
- mark license files as %%license where available

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 0.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Mar 30 2014 Martin Gansser <martinkg@fedoraproject.org> - 0.2.2-6
- Rebuild

* Thu Jun 13 2013 Martin Gansser <martinkg@fedoraproject.org> - 0.2.2-5
- changes for the new Makefile style 
- specfile cleanups

* Wed Jun 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.2.2-4
- Rebuilt for GD 2.1.0

* Sun Apr 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.2.2-3
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Apr 22 2013 Martin Gansser <martinkg@fedoraproject.org> - 0.2.2-2
- added Makefile locale fix
- changed build option for new plugin Makefile
- removed vdrsync Requirement
- fixed typos
- rebuild

* Sat Feb 23 2013 Martin Gansser <martinkg@fedoraproject.org> - 0.2.2-1
- rebuild for new release

* Mon Feb 18 2013 Martin Gansser <martinkg@fedoraproject.org> - 0.2.1-1
- rebuild for new release
- specfile cleanups

* Thu Oct 11 2012 Martin Gansser <linux4martin@gmx.de> - 0.2.0-3
- rebuild for Fedora 18

* Wed Oct 10 2012 Martin Gansser <linux4martin@gmx.de> - 0.2.0-2
- removed vdrsync Requirement
- removed no-subtitle patch

* Sun Oct 07 2012 Martin Gansser <linux4martin@gmx.de> - 0.2.0-1
- spec file cleanup
- rebuild for new release
- Adapt to VDR 1.7.30
- added priority header patch for Fedora 18

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

* Sat Nov 4 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.0.009-16
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
- Rebuild for VDR 1.3.32

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

