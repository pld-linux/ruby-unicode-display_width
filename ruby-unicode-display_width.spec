#
# Conditional build:
%bcond_without	doc			# don't build ri/rdoc

%define pkgname unicode-display_width
Summary:	Determines the monospace display width of a string in Ruby
Name:		ruby-%{pkgname}
Version:	1.4.0
Release:	3
License:	MIT
Source0:	https://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	d1ac23905e70014658ea4ccefd2f16b1
Group:		Development/Languages
URL:		https://github.com/janlelis/unicode-display_width
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Determines the monospace display width of a string in Ruby.
Implementation based on EastAsianWidth.txt and other data, 100% in
Ruby. Other than wcwidth(), which fulfills a similar purpose, it does
not rely on the OS vendor to provide an up-to-date method for
measuring string width.

%package rdoc
Summary:	HTML documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla modułu języka Ruby %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
HTML documentation for Ruby %{pkgname} module.

%description rdoc -l pl.UTF-8
Dokumentacja w formacie HTML dla modułu języka Ruby %{pkgname}.

%package ri
Summary:	ri documentation for Ruby %{pkgname} module
Summary(pl.UTF-8):	Dokumentacja w formacie ri dla modułu języka Ruby %{pkgname}
Group:		Documentation
Requires:	ruby

%description ri
ri documentation for Ruby %{pkgname} module.

%description ri -l pl.UTF-8
Dokumentacja w formacie ri dla modułu języka Ruby %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec

# make gemspec self-contained
ruby -r rubygems -e 'spec = eval(File.read("%{pkgname}.gemspec"))
	File.open("%{pkgname}-%{version}.gemspec", "w") do |file|
	file.puts spec.to_ruby_for_cache
end'

#'

rdoc --ri --op ri lib
rdoc --op rdoc lib
# rm -r ri/NOT_THIS_MODULE_RELATED_DIRS
rm ri/created.rid
rm ri/cache.ri

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%if %{with doc}
install -d $RPM_BUILD_ROOT{%{ruby_rdocdir}/%{name}-%{version},%{ruby_ridir}}
cp -a rdoc/* $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%dir %{ruby_vendorlibdir}/unicode
%{ruby_vendorlibdir}/unicode/display_width.rb
%{ruby_vendorlibdir}/unicode/display_width
%{ruby_specdir}/%{pkgname}-%{version}.gemspec

%if %{with doc}
%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}

%files ri
%defattr(644,root,root,755)
%{ruby_ridir}/Unicode
%endif
