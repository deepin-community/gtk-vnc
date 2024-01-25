

gvnccapture = executable(
  'gvnccapture',
  dependencies: [gvnc_dep],
  sources: ['gvnccapture.c'],
  c_args: warning_cflags + gvnc_version_check_flags,
  link_args: warning_ldflags,
  install: true,
  install_dir: gtk_vnc_bindir,
)

pod2man = find_program('pod2man')
if pod2man.found()
  gvnccapture_man = custom_target(
    'gvnccapture.1',
    output: 'gvnccapture.1',
    input: 'gvnccapture.c',
    install: true,
    install_dir: gtk_vnc_man1dir,
    build_by_default: true,
    command: [
      pod2man,
      '-c', 'VNC Tools',
      '-r', meson.project_name() + '-' + meson.project_version(),
      '--name', 'gvnccapture',
      '@INPUT@', '@OUTPUT@']
  )
endif
