Summary:	HP Array Configuration Utility CLI
Summary(pl.UTF-8):	Narzędzie CLI do konfiguracji macierzy dyskowych HP (Smart Array i RAID Array)
Name:		hpacucli
Version:	7.85
Release:	18
License:	not distributable (Hewlett-Packard End User License Agreement)
Group:		Applications
Source0:	ftp://ftp.hp.com/pub/softlib2/software1/pubsw-linux/p308169736/v41554/%{name}-%{version}-18.linux.rpm
# NoSource0-md5:	9c324442c9a15ce1461f05c48f494f73
NoSource:	0
URL:		http://h20000.www2.hp.com/bizsupport/TechSupport/SoftwareDescription.jsp?swItem=MTX-8d3c35f1321042e69094ef3dd3
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Array Configuration Utility CLI is a commandline-based disk
configuration program for Hewlett-Packard Smart Array Controllers
and RAID Array Controllers.

%description -l pl.UTF-8
HP Array Configuration Utility CLI to działający z linii poleceń
program do konfiguracji dysków w macierzach z kontrolerami Smart
Array i RAID Array firmy Hewlett-Packard.

%prep
%setup -qcT
rpm2cpio %{SOURCE0} | cpio -dimu

mv opt/compaq/hpacucli/bld/hpacucli-*.linux.txt hpacucli-linux.txt
mv opt/compaq/hpacucli/bld/hpacucli.license .
rm -f opt/compaq/hpacucli/bld/hpacucli # same as one in sbin, however we write better one

cat <<'EOF' > hpacucli
#!/bin/sh
export ACUXE_LOCK_FILES_DIR=/var/run/hpacucli
if [ $(uname -m) = "ia64" ]; then
	exec prctl --unaligned=silent %{_libdir}/hpacucli ${1:+"$@"}
else
	exec %{_libdir}/hpacucli ${1:+"$@"}
fi
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir},/var/run/hpacucli}
install opt/compaq/hpacucli/bld/.hpacucli $RPM_BUILD_ROOT%{_libdir}/hpacucli
install opt/compaq/hpacucli/bld/lib*.so $RPM_BUILD_ROOT%{_libdir}
install hpacucli $RPM_BUILD_ROOT%{_sbindir}/hpacucli
touch $RPM_BUILD_ROOT/var/run/hpacucli/CPQACU_MUTEX

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch /var/run/hpacucli/CPQACU_MUTEX

%files
%defattr(644,root,root,755)
%doc hpacucli-linux.txt hpacucli.license
%attr(755,root,root) %{_sbindir}/hpacucli
%attr(755,root,root) %{_libdir}/hpacucli
%attr(755,root,root) %{_libdir}/libcpqimgr.so
%attr(755,root,root) %{_libdir}/libhwmim3.so
%attr(755,root,root) %{_libdir}/libossingleton.so
%dir %attr(700,root,root) /var/run/hpacucli
%ghost %attr(600,root,root) /var/run/hpacucli/CPQACU_MUTEX
