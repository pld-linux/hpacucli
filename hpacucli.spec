%define		_enable_debug_packages	0
Summary:	HP Array Configuration Utility CLI
Summary(pl.UTF-8):	Narzędzie CLI do konfiguracji macierzy dyskowych HP (Smart Array i RAID Array)
Name:		hpacucli
Version:	9.30
Release:	15.0
License:	not distributable (Hewlett-Packard End User License Agreement)
Group:		Applications
Source0:	ftp://ftp.hp.com/pub/softlib2/software1/pubsw-linux/p414707558/v77371/%{name}-%{version}-%{release}.i386.rpm
# NoSource0-md5:	41b809499716ea30c67e9dbf81fe150
Source1:	ftp://ftp.hp.com/pub/softlib2/software1/pubsw-linux/p1257348637/v77370/%{name}-%{version}-%{release}.x86_64.rpm
# NoSource1-md5:	37b559c4a2f873e8b23369f6a9b926c
NoSource:	0
NoSource:	1
URL:		http://h20000.www2.hp.com/bizsupport/TechSupport/SoftwareDescription.jsp?swItem=MTX-43192cb759444c33a5e8bdefb1
# hpacucli dlopens libemsdm.so, libqlsdm.so at runtime
Suggests:	fibreutils
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep libstdc++.so.6

%description
The Array Configuration Utility CLI is a commandline-based disk
configuration program for Hewlett-Packard Smart Array Controllers and
RAID Array Controllers.

%description -l pl.UTF-8
HP Array Configuration Utility CLI to działający z linii poleceń
program do konfiguracji dysków w macierzach z kontrolerami Smart Array
i RAID Array firmy Hewlett-Packard.

%prep
%setup -qcT
%ifarch %{ix86}
rpm2cpio %{SOURCE0} | cpio -dimu
mv opt/compaq/hpacucli/bld/hpacucli-*.i386.txt hpacucli.txt
%else
rpm2cpio %{SOURCE1} | cpio -dimu
mv opt/compaq/hpacucli/bld/hpacucli-*.x86_64.txt hpacucli.txt
%endif

mv usr/man .
gzip -d man/*/*.gz

mv opt/compaq/hpacucli/bld/hpacucli.license .

# fix man paths
%{__sed} -i -e '
	s#/opt/compaq/hpacucli/bld/hpacucli-VERSION.linux.txt#%{_docdir}/%{name}-%{version}/hpacucli.txt#
' man/man8/*

# figure out what locks are used
grep touch opt/compaq/hpacucli/bld/mklocks.sh | sort -u > mklocks.sh

cat <<'EOF' > hpacucli
#!/bin/sh
PROGRAM=${0##*/}
if [ $(uname -m) = "ia64" ]; then
	exec prctl --unaligned=silent %{_libdir}/$PROGRAM "$@"
else
	exec %{_libdir}/$PROGRAM "$@"
fi
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir},%{_mandir}/man8}
install -p opt/compaq/hpacucli/bld/.hpacucli $RPM_BUILD_ROOT%{_libdir}/hpacucli
install -p opt/compaq/hpacucli/bld/.hpacuscripting $RPM_BUILD_ROOT%{_libdir}/hpacuscripting
install -p opt/compaq/hpacucli/bld/lib*.so $RPM_BUILD_ROOT%{_libdir}
install -p hpacucli $RPM_BUILD_ROOT%{_sbindir}/hpacucli
ln $RPM_BUILD_ROOT%{_sbindir}/{hpacucli,hpacuscripting}

cp -a man/man8/* $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc hpacucli.txt hpacucli.license
%attr(755,root,root) %{_sbindir}/hpacucli
%attr(755,root,root) %{_sbindir}/hpacuscripting
%attr(755,root,root) %{_libdir}/hpacucli
%attr(755,root,root) %{_libdir}/hpacuscripting
%attr(755,root,root) %{_libdir}/libcpqimgr*.so
%{_mandir}/man8/hpacucli.8*
