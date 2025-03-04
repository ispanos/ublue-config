Name:           ublue-os-just
Packager:       ublue-os
Vendor:         ublue-os
Version:        0.39
Release:        1%{?dist}
Summary:        ublue-os just integration
License:        MIT
URL:            https://github.com/ublue-os/config

BuildArch:      noarch
Requires:       just
Requires:       ublue-os-luks
Requires:       powerstat

Source1:        00-default.just
Source2:        10-update.just
Source3:        20-clean.just
Source4:        30-distrobox.just
Source5:        40-nvidia.just
Source6:        50-akmods.just
Source7:        60-custom.just
Source8:        15-luks.just
Source9:        ujust
Source10:       ugum
Source11:       header.just
Source12:       ujust.sh
Source13:       libcolors.sh
Source14:       libformatting.sh
Source15:       libfunctions.sh
Source16:       libdistrobox.sh
Source17:       apps.ini
Source18:       distrobox.ini
Source19:       user-motd.sh
Source20:       libtoolbox.sh
Source21:       toolbox.ini
Source22:       31-toolbox.just
Source23:       brew.sh
Source24:       15-ublue-config.md

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^ublue%-os%-", ""); print(t)}

%description
Adds ublue-os just integration for easier setup

%prep
%setup -q -c -T

%build

mkdir -p -m0755  %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}
install -Dm755 %{SOURCE19}  %{buildroot}%{_sysconfdir}/profile.d/user-motd.sh
install -Dm755 %{SOURCE23}  %{buildroot}%{_sysconfdir}/profile.d/brew.sh
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE22} %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}

mkdir -p -m0755  %{buildroot}%{_datadir}/%{VENDOR}/motd/tips
cp %{SOURCE24} %{buildroot}%{_datadir}/%{VENDOR}/motd/tips

# Create justfile which contains all .just files included in this package
# Apply header first due to default not working in included justfiles
cp %{SOURCE11} "%{buildroot}%{_datadir}/%{VENDOR}/justfile"
for justfile in %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}/*.just; do
	echo "import \"%{_datadir}/%{VENDOR}/%{sub_name}/$(basename ${justfile})\"" >> "%{buildroot}%{_datadir}/%{VENDOR}/justfile"
done

# Add global "ujust" script to run just with --unstable
mkdir -p -m0755  %{buildroot}%{_bindir}
install -Dm755 %{SOURCE9} %{buildroot}%{_bindir}/ujust
install -Dm755 %{SOURCE10} %{buildroot}%{_bindir}/ugum

# Add bash library for use in just
mkdir -p -m0755 %{buildroot}/%{_exec_prefix}/lib/ujust/
install -Dm644 %{SOURCE12} %{buildroot}/%{_exec_prefix}/lib/ujust
install -Dm644 %{SOURCE13} %{buildroot}/%{_exec_prefix}/lib/ujust
install -Dm644 %{SOURCE14} %{buildroot}/%{_exec_prefix}/lib/ujust
install -Dm644 %{SOURCE15} %{buildroot}/%{_exec_prefix}/lib/ujust
install -Dm644 %{SOURCE16} %{buildroot}/%{_exec_prefix}/lib/ujust
install -Dm644 %{SOURCE20} %{buildroot}/%{_exec_prefix}/lib/ujust

# Add default manifest files for distrobox
mkdir -p -m0755 %{buildroot}/%{_sysconfdir}/distrobox
install -Dm644 %{SOURCE17} %{buildroot}/%{_sysconfdir}/distrobox
install -Dm644 %{SOURCE18} %{buildroot}/%{_sysconfdir}/distrobox

# Add default manifest file for toolbox
mkdir -p -m0755 %{buildroot}/%{_sysconfdir}/toolbox
install -Dm644 %{SOURCE21} %{buildroot}/%{_sysconfdir}/toolbox

%files
%dir %attr(0755,root,root) %{_datadir}/%{VENDOR}/%{sub_name}
%attr(0755,root,root) %{_sysconfdir}/profile.d/user-motd.sh
%attr(0755,root,root) %{_sysconfdir}/profile.d/brew.sh
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/*.just
%attr(0644,root,root) %{_datadir}/%{VENDOR}/justfile
%attr(0644,root,root) %{_datadir}/%{VENDOR}/motd/tips/*.md
%attr(0755,root,root) %{_bindir}/ujust
%attr(0755,root,root) %{_bindir}/ugum
%attr(0644,root,root) %{_exec_prefix}/lib/ujust/ujust.sh
%attr(0644,root,root) %{_exec_prefix}/lib/ujust/lib*.sh
%attr(0644,root,root) %{_sysconfdir}/distrobox/*.ini
%attr(0644,root,root) %{_sysconfdir}/toolbox/*.ini

%post
# Generate ujust bash completion
just --completions bash | sed -E 's/([\(_" ])just/\1ujust/g' > %{_datadir}/bash-completion/completions/ujust
chmod 644 %{_datadir}/bash-completion/completions/ujust

# Generate ujust zsh completion
just --completions zsh | sed -E 's/([\(_" ])just/\1ujust/g' > %{_datadir}/zsh/site-functions/_ujust
chmod 644 %{_datadir}/zsh/site-functions/_ujust

%changelog
* Mon Feb 17 2025 Tulip Blossom <tulilirockz@outlook.com> - 0.39
- Remove ublue-os-just.sh from /etc/profile.d

* Sun Feb 09 2025 renner0e <Renner03@protonmail.com> - 0.38
- Added ujust tab completion file for zsh generated from just --completions zsh

* Fri Nov 29 2024 HikariKnight <hk@bazzite.gg> - 0.37
- Remove obs-studio-portable

* Fri Sep 20 2024 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.36
- Remove no longer needed brew commands, now on image

* Fri May 31 2024 HikariKnight <2557889+HikariKnight@users.noreply.github.com> - 0.35
- Make toggle-updates smarter and detect if ublue-update is installed

* Sat May 18 2024 m2Giles <69128853+m2Giles@users.noreply.github.com> - 0.34
- Fix missing sourcefile for just split out

* Wed May 15 2024 m2Giles <69128853+m2Giles@users.noreply.github.com> - 0.33
- Split brew just file out

* Wed May 01 2024 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.32
- Add powerstat

* Tue Apr 30 2024 Benjamin Sherman <benjamin@holyarmy.org> - 0.31
- Add LUKS TPM autounlock support

* Sun Mar 24 2024 gerblesh <101901964+gerblesh@users.noreply.github.com> - 0.30
- Add brew config to /etc/profile.d

* Fri Feb 23 2024 HikariKnight <2557889+HikariKnight@users.noreply.github.com> - 0.29
- Add option to use toolbox in ujust

* Thu Feb 22 2024 Benjamin Sherman <benjamin@holyarmy.org> - 0.28
- Remove nix justfile

* Mon Jan 29 2024 RJ Trujillo <eyecantcu@pm.me> - 0.27
- Add bluefin-cli and wolfi-toolbox to distrobox assemble config

* Mon Jan 29 2024 Benjamin Sherman <benjamin@holyarmy.org> - 0.26
- Improve versatility of user-motd

* Sat Jan 27 2024 Benjamin Sherman <benjamin@holyarmy.org> - 0.25
- Add user-motd and just toggle

* Sat Jan 20 2024 HikariKnight <2557889+HikariKnight@users.noreply.github.com> - 0.24
- Add default distrobox manifests as part of rpm

* Thu Jan 18 2024 HikariKnight <2557889+HikariKnight@users.noreply.github.com> - 0.23
- Added tooling for distrobox

* Sun Jan 14 2024 HikariKnight <2557889+HikariKnight@users.noreply.github.com> - 0.22
- Added sourcable libraries for just recipes

* Wed Jan 10 2024 HikariKnight <2557889+HikariKnight@users.noreply.github.com> - 0.21
- Added ujust tab completion file generated from just --completions bash

* Thu Jan 04 2024 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.20
- Update with support for the newest version of just

* Wed Dec 20 2023 HikariKnight <2557889+HikariKnight@users.noreply.github.com> - 0.10
- Add ugum, a helper for user input for use in just

* Tue Nov 28 2023 RJ Trujillo <eyecantcu> - 0.9
- Copy nix justfile to correct location and restore ujust

* Sat Nov 25 2023 RJ Trujillo <eyecantcu@pm.me> - 0.8
- Integrate justfile for nix

* Fri Oct 13 2023 bri <284789+b-@users.noreply.github.com> - 0.7
- Add ujust runner
- Add chsh task

* Mon Oct 2 2023 ArtikusHG <24320212+ArtikusHG@users.noreply.github.com> - 0.6
- Add commands to disable and enable automatic updates to 60-updates.just

* Sat Sep 23 2023 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.5
- Remove fish shell support

* Thu Sep 21 2023 Benjamin Sherman <benjamin@holyarmy.org> - 0.4
- Correct justfile include paths

* Thu Sep 21 2023 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.3
- Modify just files to be numbered for ordered loading
- Move to using a single master justfile
- Clean up previous installs to point to new file
- Add support for fish shell

* Sat May 13 2023 Benjamin Sherman <benjamin@holyarmy.org> - 0.2
- Refactor directory structure
- Rename justfile to main.just
- Add nvidia.just and custom.just
- Make profile script intelligent about including nvidia.just

* Sun Mar 05 2023 Joshua Stone <joshua.gage.stone@gmail.com> - 0.1
- Add justfile integration
