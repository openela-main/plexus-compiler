%bcond_with bootstrap

Name:       plexus-compiler
Version:    2.8.8
Release:    6%{?dist}
Summary:    Compiler call initiators for Plexus
# extras subpackage has a bit different licensing
# parts of compiler-api are ASL2.0/MIT
License:    MIT and ASL 2.0
URL:        https://github.com/codehaus-plexus/plexus-compiler
BuildArch:  noarch

Source0:    https://github.com/codehaus-plexus/%{name}/archive/%{name}-%{version}.tar.gz
Source1:    https://www.apache.org/licenses/LICENSE-2.0.txt
Source2:    LICENSE.MIT

BuildRequires:  maven-local
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-components:pom:)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
%endif

%description
Plexus Compiler adds support for using various compilers from a
unified api. Support for javac is available in main package. For
additional compilers see %{name}-extras package.

%package extras
Summary:        Extra compiler support for %{name}
# ASL 2.0: src/main/java/org/codehaus/plexus/compiler/util/scan/
#          ...codehaus/plexus/compiler/csharp/CSharpCompiler.java
# ASL 1.1/MIT: ...codehaus/plexus/compiler/jikes/JikesCompiler.java
License:        MIT and ASL 2.0 and ASL 1.1

%description extras
Additional support for csharp, eclipse and jikes compilers

%package pom
Summary:        Maven POM files for %{name}

%description pom
This package provides %{summary}.

%package javadoc
Summary:        Javadoc for %{name}
License:        MIT and ASL 2.0 and ASL 1.1

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

find -name '.class' -delete

cp %{SOURCE1} LICENSE
cp %{SOURCE2} LICENSE.MIT

%pom_disable_module plexus-compiler-aspectj plexus-compilers
# missing com.google.errorprone:error_prone_core
%pom_disable_module plexus-compiler-javac-errorprone plexus-compilers

%pom_disable_module plexus-compiler-eclipse plexus-compilers

# don't build/install compiler-test module, it needs maven2 test harness
%pom_disable_module plexus-compiler-test

# don't install sources jars
%mvn_package ":*::sources:" __noinstall

%mvn_package ":plexus-compiler{,s}" pom
%mvn_package ":*{csharp,eclipse,jikes}*" extras

# don't generate requires on test dependency (see #1007498)
%pom_xpath_remove "pom:dependency[pom:artifactId[text()='plexus-compiler-test']]" plexus-compilers

%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin

%pom_remove_dep -r org.codehaus.plexus:plexus-compiler-javac-errorprone

%build
# Tests are skipped because of unavailable plexus-compiler-test artifact
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE LICENSE.MIT
%files extras -f .mfiles-extras
%files pom -f .mfiles-pom

%files javadoc -f .mfiles-javadoc
%doc LICENSE LICENSE.MIT

%changelog
* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 2.8.8-6
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed Jun 09 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8.8-5
- Rebuild to workaround DistroBaker issue

* Wed Jun 09 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8.8-4
- Non-bootstrap build

* Tue Jun 08 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8.8-3
- Bootstrap Maven for CentOS Stream 9

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8.8-2
- Bootstrap build
- Non-bootstrap build

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 11 2020 Marian Koncek <mkoncek@redhat.com> - 2.8.8-1
- Update to upstream version 2.8.8

* Fri Aug 28 2020 Fabio Valentini <decathorpe@gmail.com> - 0:2.8.8-1
- Update to version 2.8.8.

* Sun Aug 16 2020 Fabio Valentini <decathorpe@gmail.com> - 0:2.8.7-1
- Update to version 2.8.7.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 0:2.8.6-2
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Mon Feb 17 2020 Alexander Scheel <ascheel@redhat.com> - 0:2.8.6-1
- Update to version 2.8.6

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8.5-3
- Mass rebuild for javapackages-tools 201902

* Tue Aug 20 2019 Fabio Valentini <decathorpe@gmail.com> - 0:2.8.5-1
- Update to version 2.8.5.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8.5-2
- Mass rebuild for javapackages-tools 201901

* Mon May 13 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.8.5-1
- Update to upstream version 2.8.5

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 11 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.8.2-1
- Update to upstream version 2.8.2

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 25 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.8.1-4
- Add eclipse build-conditional

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 02 2016 Michael Simacek <msimacek@redhat.com> - 0:2.8.1-2
- Add patch to fix tycho compatibility

* Mon Oct 31 2016 Michael Simacek <msimacek@redhat.com> - 0:2.8.1-1
- Update to upstream version 2.8.1

* Fri Jul  8 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.7-3
- Remove unneeded build-requires

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0:2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.7-1
- Update to upstream version 2.7

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr  1 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-2
- Update upstream URL

* Mon Oct 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4-1
- Update to upstream version 2.4

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.3-6
- Fix build-requires on POM packages

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.3-4
- Rebuild to regenerate Maven auto-requires

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.3-3
- Use Requires: java-headless rebuild (#1067528)

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.3-2
- Fix unowned directory
- Regenerate build-requires

* Fri Sep 13 2013 Michal Srb <msrb@redhat.com> - 0:2.3-1
- Update to upstream version 2.3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 15 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-4
- Fix license tag
- Install MIT license file

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-3
- Remove auxiliary aliases

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.2-2
- Add auxiliary aliases

* Tue Mar 05 2013 Michal Srb <msrb@redhat.com> - 0:2.2-1
- Update to upstream version 2.2
- Add license file (Resolves: #903268)

* Tue Mar 05 2013 Michal Srb <msrb@redhat.com> - 0:2.1-3
- Remove auxiliary aliases

* Tue Mar 05 2013 Michal Srb <msrb@redhat.com> - 0:2.1-2
- Build with original POM files

* Wed Jan 23 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.1-1
- Update to upstream version 2.1
- Build with xmvn

* Wed Dec 5 2012 Michal Srb <msrb@redhat.com> - 0:1.9.2-3
- Replaced dependency to plexus-container-default with plexus-containers-container-default

* Tue Nov 13 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.9.2-2
- Fix up licensing properly

* Mon Oct 29 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.9.2-1
- Update to upstream version 1.9.2

* Wed Aug  8 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.9.1-3
- Fix FTBFS by adding ignoreOptionalProblems function
- Use new pom_ macros instead of patches

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.9.1-1
- Update to upstream 1.9.1 release

* Fri Jan 13 2012 Alexander Kurtakov <akurtako@redhat.com> 0:1.8.3-1
- Update to upstream 1.8.3 release.
- For some reason junit is strong (not test) dependency.

* Thu Dec  1 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.8-3
- Build with maven 3
- Don't install compiler-test module (nothing should use it anyway)
- Fixes accoding to current guidelines
- Install depmaps into extras separately

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.8-1
- Update to latest version (1.8)
- Create extras subpackage with optional compilers
- Provide maven depmaps
- Versionless jars & javadocs

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.2-4.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.5.2-3.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.5.2-2.3
- drop repotag

* Thu Mar 15 2007 Deepak Bhole <dbhole@redhat.com> - 0:1.5.2-2jpp.2
- Fix bug in spec that prevented unversioned symlink creation

* Thu Mar 08 2007 Deepak Bhole <dbhole@redhat.com> - 0:1.5.2-2jpp.1
- Fix license
- Disable aspectj compiler until we can put that into Fedora
- Remove vendor and distribution tags
- Removed javadoc post and postuns, with dirs being marked %%doc now
- Fix buildroot per Fedora spec

* Fri Jun 02 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.5.2-2jpp
- Fix jar naming to previous plexus conventions

* Tue May 30 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.5.2-1jpp
- First JPackage build
