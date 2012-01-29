%define		_enable_debug_packages	0
Summary:	HP Array Configuration Utility CLI
Summary(pl.UTF-8):	Narzędzie CLI do konfiguracji macierzy dyskowych HP (Smart Array i RAID Array)
Name:		hpacucli
Version:	8.70
Release:	8.0
License:	not distributable (Hewlett-Packard End User License Agreement)
Group:		Applications
Source0:	ftp://ftp.hp.com/pub/softlib2/software1/pubsw-linux/p414707558/v63381/%{name}-%{version}-%{release}.noarch.rpm
# NoSource0-md5:	d5105f626ce4e73f77b8be9f1b215300
NoSource:	0
URL:		http://h20000.www2.hp.com/bizsupport/TechSupport/SoftwareDescription.jsp?swItem=MTX-08be00e0ba8b42ff9002a084e7
ExclusiveArch:	%{ix86}
# hpacucli dlopens libemsdm.so, libqlsdm.so at runtime
Suggests:	fibreutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		locksdir	/var/lock/hpacucli

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
rpm2cpio %{SOURCE0} | cpio -dimu

mv usr/man .
gzip -d man/*/*.gz

mv opt/compaq/hpacucli/bld/hpacucli-*.noarch.txt hpacucli.txt
mv opt/compaq/hpacucli/bld/hpacucli.license .

# fix paths
%{__sed} -i -e '
	/APP_LOCK_DIR/ s#/var/opt/compaq/locks#%{locksdir}#
' opt/compaq/hpacucli/bld/mklocks.sh

# fix man paths
%{__sed} -i -e '
	s#/opt/compaq/hpacucli/bld/hpacucli-VERSION.linux.txt#%{_docdir}/%{name}-%{version}/hpacucli.txt#
' man/man8/*

# figure out what locks are used
grep touch opt/compaq/hpacucli/bld/mklocks.sh | sort -u > mklocks.sh

cat <<'EOF' > hpacucli
#!/bin/sh
PROGRAM=${0##*/}
export ACUXE_LOCK_FILES_DIR=%{locksdir}/
if [ $(uname -m) = "ia64" ]; then
	exec prctl --unaligned=silent %{_libdir}/$PROGRAM "$@"
else
	exec %{_libdir}/$PROGRAM "$@"
fi
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir},%{_mandir}/man8,%{locksdir}}
install -p opt/compaq/hpacucli/bld/.hpacucli $RPM_BUILD_ROOT%{_libdir}/hpacucli
install -p opt/compaq/hpacucli/bld/.hpacuscripting $RPM_BUILD_ROOT%{_libdir}/hpacuscripting
install -p opt/compaq/hpacucli/bld/lib*.so $RPM_BUILD_ROOT%{_libdir}
install -p hpacucli $RPM_BUILD_ROOT%{_sbindir}/hpacucli
ln $RPM_BUILD_ROOT%{_sbindir}/{hpacucli,hpacuscripting}

cp -a man/man8/* $RPM_BUILD_ROOT%{_mandir}/man8

# touch locks
APP_LOCK_DIR=$RPM_BUILD_ROOT%{locksdir} sh -x mklocks.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc hpacucli.txt hpacucli.license
%attr(755,root,root) %{_sbindir}/hpacucli
%attr(755,root,root) %{_sbindir}/hpacuscripting
%attr(755,root,root) %{_libdir}/hpacucli
%attr(755,root,root) %{_libdir}/hpacuscripting
%attr(755,root,root) %{_libdir}/libcpqimgr.so
%{_mandir}/man8/hpacucli.8*
%dir %attr(700,root,root) %{locksdir}
%{locksdir}/*
