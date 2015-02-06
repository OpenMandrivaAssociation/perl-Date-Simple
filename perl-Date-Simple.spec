%define upstream_version 3.03_03

Summary:	Simple date object for perl
Name:		perl-Date-Simple
Version:	%perl_convert_version %{upstream_version}
Release:	3
License:	GPL+ or Artistic
Group:		Development/Perl 
Url:		http://search.cpan.org/dist/Date-Simple/
Source0:	http://www.cpan.org/authors/id/I/IZ/IZUT/Date-Simple-%{upstream_version}.tar.gz
#Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:	perl(ExtUtils::MakeMaker), perl(Test::More)
BuildRequires:	perl-devel

# Don't "provide" private Perl libs
# % global _use_internal_dependency_generator 0
#% global __deploop() while read FILE; do /usr/lib/rpm/rpmdeps -%{1} ${FILE}; done | /bin/sort -u
#% global __find_provides /bin/sh -c "%{__grep} -v '%{perl_vendorarch}/.*\\.so$' | %{__deploop P}"
#% global __find_requires /bin/sh -c "%{__deploop R}"

%description
%{summary}.

%prep
%setup -q -n Date-Simple-%{upstream_version}

# Spurious exec permissions in files from tarball
/usr/bin/find lib -type f -exec %{__chmod} -x {} ';'
%{__chmod} -x ChangeLog COPYING README Simple.xs

# The NoXS.pm file provides a pure-perl alternative to the C implementation
# of the module. This results in duplicate "Provides:" entries, which rpmlint
# whinges about. This kludge removes the redundant file, which has the added
# benefit of shutting up rpmlint.
%{__rm} -f lib/Date/Simple/NoXS.pm
%{__sed} -i -e '/^lib\/Date\/Simple\/NoXS\.pm$/d' MANIFEST

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="-fPIC"
%make

%install
%{__make} pure_install PERL_INSTALL_ROOT=%{buildroot}
/usr/bin/find %{buildroot} -type f -name .packlist -exec %{__rm} -f {} ';'
/usr/bin/find %{buildroot} -type f -name '*.bs' -a -size 0 -exec %{__rm} -f {} ';'
/usr/bin/find %{buildroot} -depth -type d -exec /bin/rmdir {} ';' 2>/dev/null
%{__chmod} -R u+w %{buildroot}

%check
%make test

%files
%doc ChangeLog COPYING README
%{perl_vendorarch}/Date/
%{perl_vendorarch}/auto/Date/
%{_mandir}/man3/Date::Simple*.3pm*


%changelog
* Wed Jan 25 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 3.03-2
+ Revision: 768358
- svn commit -m mass rebuild of perl extension against perl 5.14.2

* Wed Sep 21 2011 Alexander Barakin <abarakin@mandriva.org> 3.03-1
+ Revision: 700688
- imported package perl-Date-Simple

