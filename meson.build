project(
  'gtk-vnc','c',
  version: '1.3.1',
  license: 'LGPLv2.1+',
  default_options: [
    'buildtype=debugoptimized',
    'c_std=gnu99',
    'warning_level=2',
  ],
  meson_version: '>= 0.49.0'
)

version_info = meson.project_version().split('.')
version_major = '@0@'.format(version_info[0])
version_minor = '@0@'.format(version_info[1])
version_micro = '@0@'.format(version_info[2])

conf_data = configuration_data()
conf_data.set('version', meson.project_version())
conf_data.set('version_major', version_major)
conf_data.set('version_minor', version_minor)
conf_data.set('version_micro', version_micro)

# ninja dist helper
meson.add_dist_script('build-aux/dist.sh', meson.source_root(), meson.build_root())

git = run_command('test', '-d', '.git', check: false).returncode() == 0

if git
  test(
    'syntax-check',
    find_program('@0@/build-aux/syntax-check'.format(meson.source_root())),
    suite: 'style',
    env: [
        'MESON_SOURCE_ROOT=@0@'.format(meson.source_root()),
    ],
  )
endif

pod2man = find_program('pod2man')

cc = meson.get_compiler('c')

coroutine = get_option('with-coroutine')

uctx_args = []
if host_machine.system() == 'darwin'
  uctx_args += ['-D_XOPEN_SOURCE=600']
endif
has_ucontext = true
foreach uctx_func : ['makecontext', 'swapcontext', 'getcontext']
  if not cc.has_function(uctx_func, prefix: '#include <ucontext.h>', args: uctx_args)
    has_ucontext = false
    break
  endif
endforeach

if coroutine == 'auto'
  if host_machine.system() == 'windows' or not has_ucontext
    coroutine = 'gthread'
  else
    coroutine = 'ucontext'
  endif
endif

if coroutine == 'ucontext'
  if not has_ucontext
    error('ucontext requested, but not available')
  endif
  conf_data.set('WITH_UCONTEXT', true)
elif coroutine != 'gthread'
  error('Unknown coroutine backend')
endif

# gvnc
glib_min_version = '2.56.0'
glib_min_version_symbol='GLIB_VERSION_2_56'
gdk_pixbuf_min_version = '2.36.0'
gcrypt_min_version = '1.8.0'
gnutls_min_version = '3.6.0'
zlib_min_version = '1.2.11'
libsasl_min_version = '2.1.27'

# gtk-vnc
gtk_min_version = '3.22.0'
gtk_min_version_symbol='GDK_VERSION_3_22'
cairo_min_version = '1.15.0'
x11_min_version = '1.6.5'

# gvncpule
libpulse_min_version = '11.0'

# common
gobject_introspection_min_version = '1.56.0'

libm_dep = cc.find_library('m', required : true)
gobject_dep = dependency('gobject-2.0', version: '>= ' + glib_min_version)
gio_dep = dependency('gio-2.0', version: '>= ' + glib_min_version)
gio_unix_dep = dependency('gio-unix-2.0', version: '>= ' + glib_min_version, required: false)
if gio_unix_dep.found()
  conf_data.set('HAVE_GIOUNIX', true)
endif

if coroutine == 'gthread'
  gthread_dep = dependency('gthread-2.0', version: '>= ' + glib_min_version)
else
  gthread_dep = disabler()
endif

gdk_pixbuf_dep = dependency('gdk-pixbuf-2.0', version: '>= ' + gdk_pixbuf_min_version)
gtk_dep = dependency('gtk+-3.0', version: '>= ' + gtk_min_version)
gcrypt_dep = dependency('libgcrypt', version: '>= ' + gcrypt_min_version)
gnutls_dep = dependency('gnutls', version: '>= ' + gnutls_min_version)
cairo_dep = dependency('cairo', version: '>= ' + cairo_min_version)
x11_dep = dependency('x11', version: '>= ' + x11_min_version, required: false)
libpulse_dep = dependency('libpulse-simple', version: '>= ' + libpulse_min_version, required: get_option('pulseaudio'))
if libpulse_dep.found()
  conf_data.set('HAVE_PULSEAUDIO', true)
endif
zlib_dep = dependency('zlib', version: '>= ' + zlib_min_version)
libsasl_dep = dependency('libsasl2', version: '>= ' + libsasl_min_version, required: get_option('sasl'))
if libsasl_dep.found()
  conf_data.set('HAVE_SASL', true)
endif

gvnc_version_check_flags = [
  '-DGLIB_VERSION_MIN_REQUIRED=@0@'.format(glib_min_version_symbol),
  '-DGLIB_VERSION_MAX_ALLOWED=@0@'.format(glib_min_version_symbol),
]

gtk_vnc_version_check_flags = gvnc_version_check_flags + [
  '-DGDK_VERSION_MIN_REQUIRED=@0@'.format(gtk_min_version_symbol),
  '-DGDK_VERSION_MAX_ALLOWED=@0@'.format(gtk_min_version_symbol),
]

keycodemapdb = subproject('keycodemapdb')

keymapgen = find_program('keymap-gen')
keymapcsv = keycodemapdb.get_variable('keymaps_csv')


gnome = import('gnome')
i18n = import('i18n')

check_cflags = [
  '-Waddress',
  '-Waggressive-loop-optimizations',
  '-Warray-bounds',
  '-Wattributes',
  '-Wbuiltin-macro-redefined',
  '-Wchar-subscripts',
  '-Wclobbered',
  '-Wcomment',
  '-Wcomments',
  '-Wcoverage-mismatch',
  '-Wcpp',
  '-Wdate-time',
  '-Wno-deprecated-declarations',
  '-Wdisabled-optimization',
  '-Wdiv-by-zero',
  '-Wdouble-promotion',
  '-Wempty-body',
  '-Wendif-labels',
  '-Wenum-compare',
  '-Wformat-contains-nul',
  '-Wformat-extra-args',
  '-Wformat-security',
  '-Wformat-y2k',
  '-Wformat-zero-length',
  '-Wfree-nonheap-object',
  '-Wignored-qualifiers',
  '-Wimplicit',
  '-Wimplicit-function-declaration',
  '-Wimplicit-int',
  '-Winit-self',
  '-Winline',
  '-Wint-to-pointer-cast',
  '-Winvalid-memory-model',
  '-Winvalid-pch',
  '-Wjump-misses-init',
  '-Wlogical-op',
  '-Wmain',
  '-Wmaybe-uninitialized',
  '-Wmissing-braces',
  '-Wmissing-declarations',
  '-Wmissing-field-initializers',
  '-Wmissing-parameter-type',
  '-Wmissing-prototypes',
  '-Wmultichar',
  '-Wnarrowing',
  '-Wnested-externs',
  '-Wnonnull',
  '-Wold-style-declaration',
  '-Wold-style-definition',
  '-Wopenmp-simd',
  '-Woverflow',
  '-Woverride-init',
  '-Wpacked',
  '-Wpacked-bitfield-compat',
  '-Wparentheses',
  '-Wpointer-arith',
  '-Wpointer-sign',
  '-Wpointer-to-int-cast',
  '-Wpragmas',
  '-Wreturn-local-addr',
  '-Wreturn-type',
  '-Wsequence-point',
  '-Wshadow',
  '-Wsizeof-pointer-memaccess',
  '-Wstack-protector',
  '-Wstrict-aliasing',
  '-Wstrict-overflow',
  '-Wstrict-prototypes',
  '-Wsuggest-attribute=const',
  '-Wsuggest-attribute=format',
  '-Wsuggest-attribute=noreturn',
  '-Wsuggest-attribute=pure',
  '-Wswitch',
  '-Wswitch-default',
  '-Wsync-nand',
  '-Wtrampolines',
  '-Wtrigraphs',
  '-Wtype-limits',
  '-Wuninitialized',
  '-Wunknown-pragmas',
  '-Wunsafe-loop-optimizations',
  '-Wunused',
  '-Wunused-but-set-parameter',
  '-Wunused-but-set-variable',
  '-Wunused-function',
  '-Wunused-label',
  '-Wunused-local-typedefs',
  '-Wunused-parameter',
  '-Wunused-result',
  '-Wunused-value',
  '-Wunused-variable',
  '-Wvarargs',
  '-Wvariadic-macros',
  '-Wvector-operation-performance',
  '-Wvla',
  '-Wvolatile-register-var',
  '-Wwrite-strings',
  '-Wnormalized=nfc',
  '-Wno-sign-compare',
  '-Wno-sign-conversion',
  '-Wno-conversion',
  '-Wno-unsafe-loop-optimizations',
  '-Wno-cast-function-type',
  '-Wjump-misses-init',
  '-Wframe-larger-than=40096',
  '-fexceptions',
  '-fasynchronous-unwind-tables',
  '-fdiagnostics-show-option',
  '-funit-at-a-time',
  '-fipa-pure-const',
  '-Wno-suggest-attribute=pure',
  '-Wno-suggest-attribute=const',
]

warning_cflags = []
warning_ldflags = []
if get_option('warning_level') == '2'
  foreach cflag: check_cflags
    if cc.has_argument(cflag)
      warning_cflags += [cflag]
    endif
  endforeach

  if host_machine.system() in [ 'linux', 'freebsd', 'windows' ]
    # we prefer -fstack-protector-strong but fallback to -fstack-protector-all
    fstack_cflags = cc.first_supported_argument([
      '-fstack-protector-strong',
      '-fstack-protector-all',
    ])
    warning_cflags += fstack_cflags

    # When building with mingw using -fstack-protector requires libssp library
    # which is included by using -fstack-protector with linker.
    if fstack_cflags.length() == 1 and host_machine.system() == 'windows'
      warning_ldflags = fstack_cflags
    endif
  endif
endif

gtk_vnc_prefix = get_option('prefix')
gtk_vnc_bindir = join_paths(gtk_vnc_prefix, get_option('bindir'))
gtk_vnc_libdir = join_paths(gtk_vnc_prefix, get_option('libdir'))
gtk_vnc_localedir = join_paths(gtk_vnc_prefix, get_option('localedir'))
gtk_vnc_datadir = join_paths(gtk_vnc_prefix, get_option('datadir'))
gtk_vnc_sysconfdir = join_paths(gtk_vnc_prefix, get_option('sysconfdir'))
gtk_vnc_includedir = join_paths(gtk_vnc_prefix, get_option('includedir'))
gtk_vnc_mandir = join_paths(gtk_vnc_prefix, get_option('mandir'))
gtk_vnc_man1dir = join_paths(gtk_vnc_mandir, 'man1')

gtk_vnc_girdir = join_paths(gtk_vnc_datadir, 'gir-1.0')
gtk_vnc_typelibdir = join_paths(gtk_vnc_libdir, 'girepository-1.0')
gtk_vnc_pkgconfdir = join_paths(gtk_vnc_libdir, 'pkgconfig')

conf_data.set('sysconfdir', gtk_vnc_sysconfdir)
conf_data.set('localedir', gtk_vnc_localedir)

gtk_vnc_pkgdatadir = join_paths(gtk_vnc_datadir, meson.project_name())

po_dir = join_paths(meson.source_root(), 'po')

conf_data.set('tls_priority', get_option('with-tls-priority'))

configure_file(
  input: 'config.h.in',
  output: 'config.h',
  configuration: conf_data
)

top_incdir = include_directories('.')
src_incdir = include_directories('src')

gir = find_program('g-ir-scanner', required: get_option('introspection'))
with_gir = gir.found()

vala_opt = get_option('with-vala')
with_vala = false
if not vala_opt.disabled()
  if not with_gir
    if vala_opt.enabled()
      error('Vala API requires GObject introspection (-Dintrospection=true)')
    endif
  else
    with_vala = add_languages('vala', required: vala_opt)
  endif
endif

subdir('src')
subdir('tools')
subdir('examples')
subdir('po')

pkgdata = configuration_data()
pkgdata.set('prefix', gtk_vnc_prefix)
pkgdata.set('exec_prefix', gtk_vnc_prefix)
pkgdata.set('libdir', gtk_vnc_libdir)
pkgdata.set('includedir', gtk_vnc_includedir)
pkgdata.set('VERSION', meson.project_version())
pkgdata.set('GLIB_REQUIRED', glib_min_version)
pkgdata.set('GTK_REQUIRED', gtk_min_version)

pkg = import('pkgconfig')
pkg.generate(
  gvnc,
  description: 'GObject for VNC client connections',
  requires: [gobject_dep],
  subdirs: 'gvnc-1.0',
)

if libpulse_dep.found()
  pkg.generate(
    gvncpulse,
    description: 'Pulse audio bridge for VNC client connections',
    requires: [gvnc],
    subdirs: 'gvncpulse-1.0',
  )
endif

pkg.generate(
  gtk_vnc,
  description: 'GTK widget for a VNC client',
  requires: [gtk_dep, gvnc],
  subdirs: 'gtk-vnc-2.0',
)

configure_file(
  input: 'gtk-vnc.spec.in',
  output: 'gtk-vnc.spec',
  configuration: pkgdata,
)

configure_file(
  input: 'mingw-gtk-vnc.spec.in',
  output: 'mingw-gtk-vnc.spec',
  configuration: pkgdata,
)
