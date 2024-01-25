
gvncviewer_deps = [gtk_vnc_dep, gio_unix_dep]

if libpulse_dep.found()
  gvncviewer_deps += [gvncpulse_dep]
endif

gvncviewer = executable(
  'gvncviewer',
  sources: ['gvncviewer.c'],
  c_args: warning_cflags + gtk_vnc_version_check_flags,
  link_args: warning_ldflags,
  dependencies: gvncviewer_deps,
  install: false,
)
