
import argparse
import sys
import venv

MODULE_ARGS_VENV = {
	(3, 8)	: {
		None	: {
			'description'	: 'Virtual environment (venv) package for Python. Based on PEP 405.',
			'epilog'		: 'Copyright (C) 2011-2014 Vinay Sajip.\nLicensed to the PSF under a contributor agreement.'
			},
		True: ({'title': 'venv callables'}, {
			'EnvBuilder'	: (([], {}), {
				None	: {
					'description'	: 'This class exists to allow virtual environment creation to be',
					'epilog'		: "customized. The constructor parameters determine the builder's\nbehaviour when called upon to create a virtual environment.\n\nBy default, the builder makes the system (global) site-packages dir\n*un*available to the created environment.\n\nIf invoked using the Python -m option, the default is to use copying\non Windows platforms but symlinks elsewhere. If instantiated some\nother way, the default is to *not* use symlinks."
				},
				False	: {'__simplifiedapp_': (venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt'), None, (), None)},
				True	: ({'title': 'EnvBuilder methods'}, {
					'clear_directory': (([], {}), {
						None	: {},
						False	: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt'), None, (), None), ('clear_directory', ('path',), None, (), None))},
						'path'	: {}
					}),
					'create': (([], {}), {
						None		: {
							'description': 'Create a virtual environment in a directory.',
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt'), None, (), None), ('create', ('env_dir',), None, (), None))},
						'env_dir'	: {}
					}),
					'create_configuration': (([], {}), {
						None		: {
							'description': "Create a configuration file indicating where the environment's Python",
							'epilog': 'was copied from, and whether the system site-packages should be made\navailable in the environment.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt'), None, (), None), ('create_configuration', ('context',), None, (), None))},
						'context'	: {}
					}),
					'ensure_directories': (([], {}), {
						None		: {
							'description': 'Create the directories for the environment.',
							'epilog': 'Returns a context object which holds paths in the environment,\nfor use by subsequent logic.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt'), None, (), None), ('ensure_directories', ('env_dir',), None, (), None))},
						'env_dir'	: {}
					}),
					'install_scripts': (([], {}), {
						None		: {
							'description'	: 'Install scripts into the created environment from a directory.',
			            },
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt'), None, (), None), ('install_scripts', ('context', 'path'), None, (), None))},
						'context'	: {},
						'path'		: {}
					}),
					'post_setup': (([], {}), {
						None		: {
							'description': 'Hook for post-setup modification of the venv. Subclasses may install',
							'epilog': 'additional packages or scripts here, add activation shell scripts, etc.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt'), None, (), None), ('post_setup', ('context',), None, (), None))},
						'context'	: {}
					}),
					'replace_variables': (([], {}), {
			            None		: {
							'description'	: 'Replace variable placeholders in script text with context-specific',
							'epilog'		: 'variables.\n\nReturn the text passed in , but with variables replaced.'
			            },
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt'), None, (), None), ('replace_variables', ('text', 'context'), None, (), None))},
						'context'	: {},
						'text'		: {}
					}),
					'setup_python': (([], {}), {
						None		: {
							'description'	: 'Set up a Python executable in the environment.',
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt'), None, (), None), ('setup_python', ('context',), None, (), None))},
						'context'	: {}
					}),
					'setup_scripts': (([], {}), {
						None		: {
							'description'	: 'Set up scripts into the created environment from a directory.',
							'epilog'		: "This method installs the default scripts into the environment\nbeing created. You can prevent the default installation by overriding\nthis method if you really need to, or if you need to specify\na different location for the scripts to install. By default, the\n'scripts' directory in the venv package is used as the source of\nscripts to install."
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt'), None, (), None), ('setup_scripts', ('context',), None, (), None))},
						'context'	: {}
					}),
					'symlink_or_copy': (([], {}), {
						None						: {
							'description'	: 'Try symlinking a file, and if that fails, fall back to copying.',
						},
						False						: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt'), None, (), None), ('symlink_or_copy', ('src', 'dst', 'relative_symlinks_ok'), None, (), None))},
						'--relative_symlinks_ok'	: {'action': 'store_true', 'default': False},
						'dst'						: {},
						'src'						: {}
					}),
				}),
				'--clear': {'action': 'store_true', 'default': False},
				'--prompt': {'default': '==SUPPRESS=='},
				'--symlinks': {'action': 'store_true', 'default': False},
				'--system_site_packages': {'action': 'store_true', 'default': False},
				'--upgrade': {'action': 'store_true', 'default': False},
				'--with_pip': {'action': 'store_true', 'default': False}
			}),
			'create': (([], {}), {
				None						: {'description' : 'Create a virtual environment in a directory.'},
				False						: {'__simplifiedapp_' : (getattr(venv, 'create'), ('env_dir', 'system_site_packages', 'clear', 'symlinks', 'with_pip', 'prompt'), None, (), None)},
				'--clear'					: {'action' : 'store_true', 'default' : False},
				'--prompt'					: {'default' : argparse.SUPPRESS},
				'--symlinks'				: {'action' : 'store_true', 'default' : False},
				'--system_site_packages'	: {'action' : 'store_true', 'default' : False},
				'--with_pip'				: {'action' : 'store_true', 'default' : False},
				'env_dir'					: {}
			}),
			'main': (([], {}), {
				None		: {},
				False		: {'__simplifiedapp_' : (getattr(venv, 'main'), ('args',), None, (), None)},
				'--args'	: {'default': argparse.SUPPRESS}
			})
		})
	},
	(3, 9)	: {
		None	: {
			'description'	: 'Virtual environment (venv) package for Python. Based on PEP 405.',
			'epilog'		: 'Copyright (C) 2011-2014 Vinay Sajip.\nLicensed to the PSF under a contributor agreement.'
			},
		True: ({'title': 'venv callables'}, {
			'EnvBuilder'	: (([], {}), {
				None	: {
					'description'	: 'This class exists to allow virtual environment creation to be',
					'epilog'		: "customized. The constructor parameters determine the builder's\nbehaviour when called upon to create a virtual environment.\n\nBy default, the builder makes the system (global) site-packages dir\n*un*available to the created environment.\n\nIf invoked using the Python -m option, the default is to use copying\non Windows platforms but symlinks elsewhere. If instantiated some\nother way, the default is to *not* use symlinks."
				},
				False	: {'__simplifiedapp_': (venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None)},
				True	: ({'title': 'EnvBuilder methods'}, {
					'clear_directory': (([], {}), {
						None	: {},
						False	: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('clear_directory', ('path',), None, (), None))},
						'path'	: {}
					}),
					'create': (([], {}), {
						None		: {
							'description': 'Create a virtual environment in a directory.',
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('create', ('env_dir',), None, (), None))},
						'env_dir'	: {}
					}),
					'create_configuration': (([], {}), {
						None		: {
							'description': "Create a configuration file indicating where the environment's Python",
							'epilog': 'was copied from, and whether the system site-packages should be made\navailable in the environment.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('create_configuration', ('context',), None, (), None))},
						'context'	: {}
					}),
					'ensure_directories': (([], {}), {
						None		: {
							'description': 'Create the directories for the environment.',
							'epilog': 'Returns a context object which holds paths in the environment,\nfor use by subsequent logic.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('ensure_directories', ('env_dir',), None, (), None))},
						'env_dir'	: {}
					}),
					'install_scripts': (([], {}), {
						None		: {
							'description'	: 'Install scripts into the created environment from a directory.',
			            },
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('install_scripts', ('context', 'path'), None, (), None))},
						'context'	: {},
						'path'		: {}
					}),
					'post_setup': (([], {}), {
						None		: {
							'description': 'Hook for post-setup modification of the venv. Subclasses may install',
							'epilog': 'additional packages or scripts here, add activation shell scripts, etc.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('post_setup', ('context',), None, (), None))},
						'context'	: {}
					}),
					'replace_variables': (([], {}), {
			            None		: {
							'description'	: 'Replace variable placeholders in script text with context-specific',
							'epilog'		: 'variables.\n\nReturn the text passed in , but with variables replaced.'
			            },
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('replace_variables', ('text', 'context'), None, (), None))},
						'context'	: {},
						'text'		: {}
					}),
					'setup_python': (([], {}), {
						None		: {
							'description'	: 'Set up a Python executable in the environment.',
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('setup_python', ('context',), None, (), None))},
						'context'	: {}
					}),
					'setup_scripts': (([], {}), {
						None		: {
							'description'	: 'Set up scripts into the created environment from a directory.',
							'epilog'		: "This method installs the default scripts into the environment\nbeing created. You can prevent the default installation by overriding\nthis method if you really need to, or if you need to specify\na different location for the scripts to install. By default, the\n'scripts' directory in the venv package is used as the source of\nscripts to install."
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('setup_scripts', ('context',), None, (), None))},
						'context'	: {}
					}),
					'symlink_or_copy': (([], {}), {
						None						: {
							'description'	: 'Try symlinking a file, and if that fails, fall back to copying.',
						},
						False						: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('symlink_or_copy', ('src', 'dst', 'relative_symlinks_ok'), None, (), None))},
						'--relative_symlinks_ok'	: {'action': 'store_true', 'default': False},
						'dst'						: {},
						'src'						: {}
					}),
					'upgrade_dependencies': (([], {}), {
						None: {},
						False: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('upgrade_dependencies', ('context',), None, (), None))},
						'context': {}
					})
				}),
				'--clear': {'action': 'store_true', 'default': False},
				'--prompt': {'default': '==SUPPRESS=='},
				'--symlinks': {'action': 'store_true', 'default': False},
				'--system_site_packages': {'action': 'store_true', 'default': False},
				'--upgrade': {'action': 'store_true', 'default': False},
				'--upgrade_deps': {'action': 'store_true', 'default': False},
				'--with_pip': {'action': 'store_true', 'default': False}
			}),
			'create': (([], {}), {
				None						: {'description' : 'Create a virtual environment in a directory.'},
				False						: {'__simplifiedapp_' : (getattr(venv, 'create'), ('env_dir', 'system_site_packages', 'clear', 'symlinks', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None)},
				'--clear'					: {'action' : 'store_true', 'default' : False},
				'--prompt'					: {'default' : argparse.SUPPRESS},
				'--symlinks'				: {'action' : 'store_true', 'default' : False},
				'--system_site_packages'	: {'action' : 'store_true', 'default' : False},
				'--upgrade_deps'			: {'action' : 'store_true', 'default' : False},
				'--with_pip'				: {'action' : 'store_true', 'default' : False},
				'env_dir'					: {}
			}),
			'main': (([], {}), {
				None		: {},
				False		: {'__simplifiedapp_' : (getattr(venv, 'main'), ('args',), None, (), None)},
				'--args'	: {'default': argparse.SUPPRESS}
			})
		})
	},
    (3, 10)	: {
		None	: {
			'description'	: 'Virtual environment (venv) package for Python. Based on PEP 405.',
			'epilog'		: 'Copyright (C) 2011-2014 Vinay Sajip.\nLicensed to the PSF under a contributor agreement.'
			},
		True: ({'title': 'venv callables'}, {
			'EnvBuilder'	: (([], {}), {
				None	: {
					'description'	: 'This class exists to allow virtual environment creation to be',
					'epilog'		: "customized. The constructor parameters determine the builder's\nbehaviour when called upon to create a virtual environment.\n\nBy default, the builder makes the system (global) site-packages dir\n*un*available to the created environment.\n\nIf invoked using the Python -m option, the default is to use copying\non Windows platforms but symlinks elsewhere. If instantiated some\nother way, the default is to *not* use symlinks."
				},
				False	: {'__simplifiedapp_': (venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None)},
				True	: ({'title': 'EnvBuilder methods'}, {
					'clear_directory': (([], {}), {
						None	: {},
						False	: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('clear_directory', ('path',), None, (), None))},
						'path'	: {}
					}),
					'create': (([], {}), {
						None		: {
							'description': 'Create a virtual environment in a directory.',
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('create', ('env_dir',), None, (), None))},
						'env_dir'	: {}
					}),
					'create_configuration': (([], {}), {
						None		: {
							'description': "Create a configuration file indicating where the environment's Python",
							'epilog': 'was copied from, and whether the system site-packages should be made\navailable in the environment.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('create_configuration', ('context',), None, (), None))},
						'context'	: {}
					}),
					'ensure_directories': (([], {}), {
						None		: {
							'description': 'Create the directories for the environment.',
							'epilog': 'Returns a context object which holds paths in the environment,\nfor use by subsequent logic.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('ensure_directories', ('env_dir',), None, (), None))},
						'env_dir'	: {}
					}),
					'install_scripts': (([], {}), {
						None		: {
							'description'	: 'Install scripts into the created environment from a directory.',
			            },
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('install_scripts', ('context', 'path'), None, (), None))},
						'context'	: {},
						'path'		: {}
					}),
					'post_setup': (([], {}), {
						None		: {
							'description': 'Hook for post-setup modification of the venv. Subclasses may install',
							'epilog': 'additional packages or scripts here, add activation shell scripts, etc.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('post_setup', ('context',), None, (), None))},
						'context'	: {}
					}),
					'replace_variables': (([], {}), {
			            None		: {
							'description'	: 'Replace variable placeholders in script text with context-specific',
							'epilog'		: 'variables.\n\nReturn the text passed in , but with variables replaced.'
			            },
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('replace_variables', ('text', 'context'), None, (), None))},
						'context'	: {},
						'text'		: {}
					}),
					'setup_python': (([], {}), {
						None		: {
							'description'	: 'Set up a Python executable in the environment.',
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('setup_python', ('context',), None, (), None))},
						'context'	: {}
					}),
					'setup_scripts': (([], {}), {
						None		: {
							'description'	: 'Set up scripts into the created environment from a directory.',
							'epilog'		: "This method installs the default scripts into the environment\nbeing created. You can prevent the default installation by overriding\nthis method if you really need to, or if you need to specify\na different location for the scripts to install. By default, the\n'scripts' directory in the venv package is used as the source of\nscripts to install."
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('setup_scripts', ('context',), None, (), None))},
						'context'	: {}
					}),
					'symlink_or_copy': (([], {}), {
						None						: {
							'description'	: 'Try symlinking a file, and if that fails, fall back to copying.',
						},
						False						: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('symlink_or_copy', ('src', 'dst', 'relative_symlinks_ok'), None, (), None))},
						'--relative_symlinks_ok'	: {'action': 'store_true', 'default': False},
						'dst'						: {},
						'src'						: {}
					}),
					'upgrade_dependencies': (([], {}), {
						None: {},
						False: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('upgrade_dependencies', ('context',), None, (), None))},
						'context': {}
					})
				}),
				'--clear': {'action': 'store_true', 'default': False},
				'--prompt': {'default': '==SUPPRESS=='},
				'--symlinks': {'action': 'store_true', 'default': False},
				'--system_site_packages': {'action': 'store_true', 'default': False},
				'--upgrade': {'action': 'store_true', 'default': False},
				'--upgrade_deps': {'action': 'store_true', 'default': False},
				'--with_pip': {'action': 'store_true', 'default': False}
			}),
			'create': (([], {}), {
				None						: {'description' : 'Create a virtual environment in a directory.'},
				False						: {'__simplifiedapp_' : (getattr(venv, 'create'), ('env_dir', 'system_site_packages', 'clear', 'symlinks', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None)},
				'--clear'					: {'action' : 'store_true', 'default' : False},
				'--prompt'					: {'default' : argparse.SUPPRESS},
				'--symlinks'				: {'action' : 'store_true', 'default' : False},
				'--system_site_packages'	: {'action' : 'store_true', 'default' : False},
				'--upgrade_deps'			: {'action' : 'store_true', 'default' : False},
				'--with_pip'				: {'action' : 'store_true', 'default' : False},
				'env_dir'					: {}
			}),
			'main': (([], {}), {
				None		: {},
				False		: {'__simplifiedapp_' : (getattr(venv, 'main'), ('args',), None, (), None)},
				'--args'	: {'default': argparse.SUPPRESS}
			})
		})
	},
	(3, 11)	: {
		None	: {
			'description'	: 'Virtual environment (venv) package for Python. Based on PEP 405.',
			'epilog'		: 'Copyright (C) 2011-2014 Vinay Sajip.\nLicensed to the PSF under a contributor agreement.'
			},
		True: ({'title': 'venv callables'}, {
			'EnvBuilder'	: (([], {}), {
				None	: {
					'description'	: 'This class exists to allow virtual environment creation to be',
					'epilog'		: "customized. The constructor parameters determine the builder's\nbehaviour when called upon to create a virtual environment.\n\nBy default, the builder makes the system (global) site-packages dir\n*un*available to the created environment.\n\nIf invoked using the Python -m option, the default is to use copying\non Windows platforms but symlinks elsewhere. If instantiated some\nother way, the default is to *not* use symlinks."
				},
				False	: {'__simplifiedapp_': (venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None)},
				True	: ({'title': 'EnvBuilder methods'}, {
					'clear_directory': (([], {}), {
						None	: {},
						False	: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('clear_directory', ('path',), None, (), None))},
						'path'	: {}
					}),
					'create': (([], {}), {
						None		: {
							'description': 'Create a virtual environment in a directory.',
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('create', ('env_dir',), None, (), None))},
						'env_dir'	: {}
					}),
					'create_configuration': (([], {}), {
						None		: {
							'description': "Create a configuration file indicating where the environment's Python",
							'epilog': 'was copied from, and whether the system site-packages should be made\navailable in the environment.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('create_configuration', ('context',), None, (), None))},
						'context'	: {}
					}),
					'ensure_directories': (([], {}), {
						None		: {
							'description': 'Create the directories for the environment.',
							'epilog': 'Returns a context object which holds paths in the environment,\nfor use by subsequent logic.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('ensure_directories', ('env_dir',), None, (), None))},
						'env_dir'	: {}
					}),
					'install_scripts': (([], {}), {
						None		: {
							'description'	: 'Install scripts into the created environment from a directory.',
			            },
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('install_scripts', ('context', 'path'), None, (), None))},
						'context'	: {},
						'path'		: {}
					}),
					'post_setup': (([], {}), {
						None		: {
							'description': 'Hook for post-setup modification of the venv. Subclasses may install',
							'epilog': 'additional packages or scripts here, add activation shell scripts, etc.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('post_setup', ('context',), None, (), None))},
						'context'	: {}
					}),
					'replace_variables': (([], {}), {
			            None		: {
							'description'	: 'Replace variable placeholders in script text with context-specific',
							'epilog'		: 'variables.\n\nReturn the text passed in , but with variables replaced.'
			            },
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('replace_variables', ('text', 'context'), None, (), None))},
						'context'	: {},
						'text'		: {}
					}),
					'setup_python': (([], {}), {
						None		: {
							'description'	: 'Set up a Python executable in the environment.',
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('setup_python', ('context',), None, (), None))},
						'context'	: {}
					}),
					'setup_scripts': (([], {}), {
						None		: {
							'description'	: 'Set up scripts into the created environment from a directory.',
							'epilog'		: "This method installs the default scripts into the environment\nbeing created. You can prevent the default installation by overriding\nthis method if you really need to, or if you need to specify\na different location for the scripts to install. By default, the\n'scripts' directory in the venv package is used as the source of\nscripts to install."
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('setup_scripts', ('context',), None, (), None))},
						'context'	: {}
					}),
					'symlink_or_copy': (([], {}), {
						None						: {
							'description'	: 'Try symlinking a file, and if that fails, fall back to copying.',
						},
						False						: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('symlink_or_copy', ('src', 'dst', 'relative_symlinks_ok'), None, (), None))},
						'--relative_symlinks_ok'	: {'action': 'store_true', 'default': False},
						'dst'						: {},
						'src'						: {}
					}),
					'upgrade_dependencies': (([], {}), {
						None: {},
						False: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('upgrade_dependencies', ('context',), None, (), None))},
						'context': {}
					})
				}),
				'--clear': {'action': 'store_true', 'default': False},
				'--prompt': {'default': '==SUPPRESS=='},
				'--symlinks': {'action': 'store_true', 'default': False},
				'--system_site_packages': {'action': 'store_true', 'default': False},
				'--upgrade': {'action': 'store_true', 'default': False},
				'--upgrade_deps': {'action': 'store_true', 'default': False},
				'--with_pip': {'action': 'store_true', 'default': False}
			}),
			'create': (([], {}), {
				None						: {'description' : 'Create a virtual environment in a directory.'},
				False						: {'__simplifiedapp_' : (getattr(venv, 'create'), ('env_dir', 'system_site_packages', 'clear', 'symlinks', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None)},
				'--clear'					: {'action' : 'store_true', 'default' : False},
				'--prompt'					: {'default' : argparse.SUPPRESS},
				'--symlinks'				: {'action' : 'store_true', 'default' : False},
				'--system_site_packages'	: {'action' : 'store_true', 'default' : False},
				'--upgrade_deps'			: {'action' : 'store_true', 'default' : False},
				'--with_pip'				: {'action' : 'store_true', 'default' : False},
				'env_dir'					: {}
			}),
			'main': (([], {}), {
				None		: {},
				False		: {'__simplifiedapp_' : (getattr(venv, 'main'), ('args',), None, (), None)},
				'--args'	: {'default': argparse.SUPPRESS}
			})
		})
	},
	(3, 12)	: {
		None	: {
			'description'	: 'Virtual environment (venv) package for Python. Based on PEP 405.',
			'epilog'		: 'Copyright (C) 2011-2014 Vinay Sajip.\nLicensed to the PSF under a contributor agreement.'
			},
		True: ({'title': 'venv callables'}, {
			'EnvBuilder'	: (([], {}), {
				None	: {
					'description'	: 'This class exists to allow virtual environment creation to be',
					'epilog'		: "customized. The constructor parameters determine the builder's\nbehaviour when called upon to create a virtual environment.\n\nBy default, the builder makes the system (global) site-packages dir\n*un*available to the created environment.\n\nIf invoked using the Python -m option, the default is to use copying\non Windows platforms but symlinks elsewhere. If instantiated some\nother way, the default is to *not* use symlinks."
				},
				False	: {'__simplifiedapp_': (venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None)},
				True	: ({'title': 'EnvBuilder methods'}, {
					'clear_directory': (([], {}), {
						None	: {},
						False	: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('clear_directory', ('path',), None, (), None))},
						'path'	: {}
					}),
					'create': (([], {}), {
						None		: {
							'description': 'Create a virtual environment in a directory.',
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('create', ('env_dir',), None, (), None))},
						'env_dir'	: {}
					}),
					'create_configuration': (([], {}), {
						None		: {
							'description': "Create a configuration file indicating where the environment's Python",
							'epilog': 'was copied from, and whether the system site-packages should be made\navailable in the environment.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('create_configuration', ('context',), None, (), None))},
						'context'	: {}
					}),
					'ensure_directories': (([], {}), {
						None		: {
							'description': 'Create the directories for the environment.',
							'epilog': 'Returns a context object which holds paths in the environment,\nfor use by subsequent logic.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('ensure_directories', ('env_dir',), None, (), None))},
						'env_dir'	: {}
					}),
					'install_scripts': (([], {}), {
						None		: {
							'description'	: 'Install scripts into the created environment from a directory.',
			            },
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('install_scripts', ('context', 'path'), None, (), None))},
						'context'	: {},
						'path'		: {}
					}),
					'post_setup': (([], {}), {
						None		: {
							'description': 'Hook for post-setup modification of the venv. Subclasses may install',
							'epilog': 'additional packages or scripts here, add activation shell scripts, etc.'
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('post_setup', ('context',), None, (), None))},
						'context'	: {}
					}),
					'replace_variables': (([], {}), {
			            None		: {
							'description'	: 'Replace variable placeholders in script text with context-specific',
							'epilog'		: 'variables.\n\nReturn the text passed in , but with variables replaced.'
			            },
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('replace_variables', ('text', 'context'), None, (), None))},
						'context'	: {},
						'text'		: {}
					}),
					'setup_python': (([], {}), {
						None		: {
							'description'	: 'Set up a Python executable in the environment.',
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('setup_python', ('context',), None, (), None))},
						'context'	: {}
					}),
					'setup_scripts': (([], {}), {
						None		: {
							'description'	: 'Set up scripts into the created environment from a directory.',
							'epilog'		: "This method installs the default scripts into the environment\nbeing created. You can prevent the default installation by overriding\nthis method if you really need to, or if you need to specify\na different location for the scripts to install. By default, the\n'scripts' directory in the venv package is used as the source of\nscripts to install."
						},
						False		: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('setup_scripts', ('context',), None, (), None))},
						'context'	: {}
					}),
					'symlink_or_copy': (([], {}), {
						None						: {
							'description'	: 'Try symlinking a file, and if that fails, fall back to copying.',
						},
						False						: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('symlink_or_copy', ('src', 'dst', 'relative_symlinks_ok'), None, (), None))},
						'--relative_symlinks_ok'	: {'action': 'store_true', 'default': False},
						'dst'						: {},
						'src'						: {}
					}),
					'upgrade_dependencies': (([], {}), {
						None: {},
						False: {'__simplifiedapp_': ((venv.EnvBuilder, ('system_site_packages', 'clear', 'symlinks', 'upgrade', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None), ('upgrade_dependencies', ('context',), None, (), None))},
						'context': {}
					})
				}),
				'--clear': {'action': 'store_true', 'default': False},
				'--prompt': {'default': '==SUPPRESS=='},
				'--symlinks': {'action': 'store_true', 'default': False},
				'--system_site_packages': {'action': 'store_true', 'default': False},
				'--upgrade': {'action': 'store_true', 'default': False},
				'--upgrade_deps': {'action': 'store_true', 'default': False},
				'--with_pip': {'action': 'store_true', 'default': False}
			}),
			'create': (([], {}), {
				None						: {'description' : 'Create a virtual environment in a directory.'},
				False						: {'__simplifiedapp_' : (getattr(venv, 'create'), ('env_dir', 'system_site_packages', 'clear', 'symlinks', 'with_pip', 'prompt', 'upgrade_deps'), None, (), None)},
				'--clear'					: {'action' : 'store_true', 'default' : False},
				'--prompt'					: {'default' : argparse.SUPPRESS},
				'--symlinks'				: {'action' : 'store_true', 'default' : False},
				'--system_site_packages'	: {'action' : 'store_true', 'default' : False},
				'--upgrade_deps'			: {'action' : 'store_true', 'default' : False},
				'--with_pip'				: {'action' : 'store_true', 'default' : False},
				'env_dir'					: {}
			}),
			'main': (([], {}), {
				None		: {},
				False		: {'__simplifiedapp_' : (getattr(venv, 'main'), ('args',), None, (), None)},
				'--args'	: {'default': argparse.SUPPRESS}
			})
		})
	},
}

CLASS_ARGS_DICT = {
	(3, 8)	: {
		None			: {
			'description'	: 'dict() -> new empty dictionary',
			'epilog'		: '\n'.join([
				"dict(mapping) -> new dictionary initialized from a mapping object\'s",
				'    (key, value) pairs',
				'dict(iterable) -> new dictionary initialized as if via:',
				'    d = {}',
				'    for k, v in iterable:',
				'        d[k] = v',
				'dict(**kwargs) -> new dictionary initialized with the name=value pairs',
				'    in the keyword argument list.  For example:  dict(one=1, two=2)',
			]),
		},
		False			: {'__simplifiedapp_': (dict, (), 'args', (), 'kwargs')},
		True			: ({'title': 'dict methods'}, {
			'__new__': (([], {}), {
				None: {
					'description': 'Create and return a new object.  See help(type) for accurate signature.',
				},
				False: {'__simplifiedapp_': (dict.__new__, (), 'args', (), 'kwargs')},
				'--kwargs': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args': {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'clear': (([], {}), {
				None		: {
					'description'	: 'D.clear() -> None.  Remove all items from D.',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('clear', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action' : 'extend', 'default' : [], 'help' : '(Use the key=value format for each entry)', 'nargs' : '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'copy': (([], {}), {
				None	: {
					'description'	: 'D.copy() -> a shallow copy of D',
				},
				False	: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('copy', (), 'args', (), 'kwargs'))},
				'--kwargs': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args': {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'fromkeys': (([], {}), {
				None		: {
					'description'	: 'Create a new dictionary with keys from iterable and values set to value.',
				},
				False		: {'__simplifiedapp_': ((dict.fromkeys, ('iterable', 'value'), None, (), None))},
				'--value'	: {'default': argparse.SUPPRESS},
				'iterable'	: {},
			}),
			'get'			: (([], {}), {
				None		: {
					'description'	: 'Return the value for key if key is in the dictionary, else default.',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('get', ('key', 'default'), None, (), None))},
				'--default'	: {'default': argparse.SUPPRESS},
				'key'		: {}
			}),
			'items': (([], {}), {
				None		: {
					'description'	: 'D.items() -> a set-like object providing a view on D\'s items',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('items', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'keys': (([], {}), {
				None		: {
					'description'	: 'D.keys() -> a set-like object providing a view on D\'s keys',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('keys', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'pop': (([], {}), {
				None		: {
					'description'	: 'D.pop(k[,d]) -> v, remove specified key and return the corresponding value.',
					'epilog'		: 'If key is not found, d is returned if given, otherwise KeyError is raised'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('pop', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}}
			),
			'popitem'		: (([], {}), {
				None	: {
					'description'	: 'Remove and return a (key, value) pair as a 2-tuple.',
					'epilog'		: 'Pairs are returned in LIFO (last-in, first-out) order.\nRaises KeyError if the dict is empty.'
				},
				False	: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('popitem', (), None, (), None))}
			}),
			'setdefault'	: (([], {}), {
				None		: {
					'description'	: 'Insert key with a value of default if key is not in the dictionary.',
					'epilog'		: 'Return the value for key if key is in the dictionary, else default.'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('setdefault', ('key', 'default'), None, (), None))},
				'--default'	: {'default': argparse.SUPPRESS},
				'key'		: {}
			}),
			'update': (([], {}), {
				None		: {
					'description'	: 'D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.',
					'epilog'		: 'If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]\nIf E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v\nIn either case, this is followed by: for k in F:  D[k] = F[k]'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('update', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'values': (([], {}), {
				None		: {
					'description'	: 'D.values() -> an object providing a view on D\'s values',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('values', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			})
		}),
		'--kwargs'		: {'action' : 'extend', 'default' : [], 'help' : '(Use the key=value format for each entry)', 'nargs' : '+'},
		'args'			: {'action': 'extend', 'default': [], 'nargs': '*'},
	},
	(3, 9)	: {
		None			: {
			'description'	: 'dict() -> new empty dictionary',
			'epilog'		: '\n'.join([
				"dict(mapping) -> new dictionary initialized from a mapping object\'s",
				'    (key, value) pairs',
				'dict(iterable) -> new dictionary initialized as if via:',
				'    d = {}',
				'    for k, v in iterable:',
				'        d[k] = v',
				'dict(**kwargs) -> new dictionary initialized with the name=value pairs',
				'    in the keyword argument list.  For example:  dict(one=1, two=2)',
			]),
		},
		False			: {'__simplifiedapp_': (dict, (), 'args', (), 'kwargs')},
		True			: ({'title': 'dict methods'}, {
			'__new__': (([], {}), {
				None: {
					'description': 'Create and return a new object.  See help(type) for accurate signature.',
				},
				False: {'__simplifiedapp_': (dict.__new__, (), 'args', (), 'kwargs')},
				'--kwargs': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args': {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'clear': (([], {}), {
				None		: {
					'description'	: 'D.clear() -> None.  Remove all items from D.',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('clear', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action' : 'extend', 'default' : [], 'help' : '(Use the key=value format for each entry)', 'nargs' : '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'copy': (([], {}), {
				None	: {
					'description'	: 'D.copy() -> a shallow copy of D',
				},
				False	: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('copy', (), 'args', (), 'kwargs'))},
				'--kwargs': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args': {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'fromkeys': (([], {}), {
				None		: {
					'description'	: 'Create a new dictionary with keys from iterable and values set to value.',
				},
				False		: {'__simplifiedapp_': ((dict.fromkeys, ('iterable', 'value'), None, (), None))},
				'--value'	: {'default': argparse.SUPPRESS},
				'iterable'	: {},
			}),
			'get'			: (([], {}), {
				None		: {
					'description'	: 'Return the value for key if key is in the dictionary, else default.',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('get', ('key', 'default'), None, (), None))},
				'--default'	: {'default': argparse.SUPPRESS},
				'key'		: {}
			}),
			'items': (([], {}), {
				None		: {
					'description'	: 'D.items() -> a set-like object providing a view on D\'s items',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('items', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'keys': (([], {}), {
				None		: {
					'description'	: 'D.keys() -> a set-like object providing a view on D\'s keys',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('keys', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'pop': (([], {}), {
				None		: {
					'description'	: 'D.pop(k[,d]) -> v, remove specified key and return the corresponding value.',
					'epilog'		: 'If key is not found, default is returned if given, otherwise KeyError is raised'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('pop', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}}
			),
			'popitem'		: (([], {}), {
				None	: {
					'description'	: 'Remove and return a (key, value) pair as a 2-tuple.',
					'epilog'		: 'Pairs are returned in LIFO (last-in, first-out) order.\nRaises KeyError if the dict is empty.'
				},
				False	: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('popitem', (), None, (), None))}
			}),
			'setdefault'	: (([], {}), {
				None		: {
					'description'	: 'Insert key with a value of default if key is not in the dictionary.',
					'epilog'		: 'Return the value for key if key is in the dictionary, else default.'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('setdefault', ('key', 'default'), None, (), None))},
				'--default'	: {'default': argparse.SUPPRESS},
				'key'		: {}
			}),
			'update': (([], {}), {
				None		: {
					'description'	: 'D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.',
					'epilog'		: 'If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]\nIf E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v\nIn either case, this is followed by: for k in F:  D[k] = F[k]'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('update', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'values': (([], {}), {
				None		: {
					'description'	: 'D.values() -> an object providing a view on D\'s values',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('values', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			})
		}),
		'--kwargs'		: {'action' : 'extend', 'default' : [], 'help' : '(Use the key=value format for each entry)', 'nargs' : '+'},
		'args'			: {'action': 'extend', 'default': [], 'nargs': '*'},
	},
    (3, 10)	: {
		None			: {
			'description'	: 'dict() -> new empty dictionary',
			'epilog'		: '\n'.join([
				"dict(mapping) -> new dictionary initialized from a mapping object\'s",
				'    (key, value) pairs',
				'dict(iterable) -> new dictionary initialized as if via:',
				'    d = {}',
				'    for k, v in iterable:',
				'        d[k] = v',
				'dict(**kwargs) -> new dictionary initialized with the name=value pairs',
				'    in the keyword argument list.  For example:  dict(one=1, two=2)',
			]),
		},
		False			: {'__simplifiedapp_': (dict, (), 'args', (), 'kwargs')},
		True			: ({'title': 'dict methods'}, {
			'__new__': (([], {}), {
				None: {
					'description': 'Create and return a new object.  See help(type) for accurate signature.',
				},
				False: {'__simplifiedapp_': (dict.__new__, (), 'args', (), 'kwargs')},
				'--kwargs': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args': {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'clear': (([], {}), {
				None		: {
					'description'	: 'D.clear() -> None.  Remove all items from D.',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('clear', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action' : 'extend', 'default' : [], 'help' : '(Use the key=value format for each entry)', 'nargs' : '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'copy': (([], {}), {
				None	: {
					'description'	: 'D.copy() -> a shallow copy of D',
				},
				False	: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('copy', (), 'args', (), 'kwargs'))},
				'--kwargs': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args': {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'fromkeys': (([], {}), {
				None		: {
					'description'	: 'Create a new dictionary with keys from iterable and values set to value.',
				},
				False		: {'__simplifiedapp_': ((dict.fromkeys, ('iterable', 'value'), None, (), None))},
				'--value'	: {'default': argparse.SUPPRESS},
				'iterable'	: {},
			}),
			'get'			: (([], {}), {
				None		: {
					'description'	: 'Return the value for key if key is in the dictionary, else default.',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('get', ('key', 'default'), None, (), None))},
				'--default'	: {'default': argparse.SUPPRESS},
				'key'		: {}
			}),
			'items': (([], {}), {
				None		: {
					'description'	: 'D.items() -> a set-like object providing a view on D\'s items',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('items', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'keys': (([], {}), {
				None		: {
					'description'	: 'D.keys() -> a set-like object providing a view on D\'s keys',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('keys', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'pop': (([], {}), {
				None		: {
					'description'	: 'D.pop(k[,d]) -> v, remove specified key and return the corresponding value.',
					'epilog'		: 'If the key is not found, return the default if given; otherwise,\nraise a KeyError.'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('pop', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}}
			),
			'popitem'		: (([], {}), {
				None	: {
					'description'	: 'Remove and return a (key, value) pair as a 2-tuple.',
					'epilog'		: 'Pairs are returned in LIFO (last-in, first-out) order.\nRaises KeyError if the dict is empty.'
				},
				False	: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('popitem', (), None, (), None))}
			}),
			'setdefault'	: (([], {}), {
				None		: {
					'description'	: 'Insert key with a value of default if key is not in the dictionary.',
					'epilog'		: 'Return the value for key if key is in the dictionary, else default.'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('setdefault', ('key', 'default'), None, (), None))},
				'--default'	: {'default': argparse.SUPPRESS},
				'key'		: {}
			}),
			'update': (([], {}), {
				None		: {
					'description'	: 'D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.',
					'epilog'		: 'If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]\nIf E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v\nIn either case, this is followed by: for k in F:  D[k] = F[k]'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('update', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'values': (([], {}), {
				None		: {
					'description'	: 'D.values() -> an object providing a view on D\'s values',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('values', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			})
		}),
		'--kwargs'		: {'action' : 'extend', 'default' : [], 'help' : '(Use the key=value format for each entry)', 'nargs' : '+'},
		'args'			: {'action': 'extend', 'default': [], 'nargs': '*'},
	},
	(3, 11)	: {
		None			: {
			'description'	: 'dict() -> new empty dictionary',
			'epilog'		: '\n'.join([
				"dict(mapping) -> new dictionary initialized from a mapping object\'s",
				'    (key, value) pairs',
				'dict(iterable) -> new dictionary initialized as if via:',
				'    d = {}',
				'    for k, v in iterable:',
				'        d[k] = v',
				'dict(**kwargs) -> new dictionary initialized with the name=value pairs',
				'    in the keyword argument list.  For example:  dict(one=1, two=2)',
			]),
		},
		False			: {'__simplifiedapp_': (dict, (), 'args', (), 'kwargs')},
		True			: ({'title': 'dict methods'}, {
			'__new__': (([], {}), {
				None: {
					'description': 'Create and return a new object.  See help(type) for accurate signature.',
				},
				False: {'__simplifiedapp_': (dict.__new__, (), 'args', (), 'kwargs')},
				'--kwargs': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args': {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'clear': (([], {}), {
				None		: {
					'description'	: 'D.clear() -> None.  Remove all items from D.',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('clear', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action' : 'extend', 'default' : [], 'help' : '(Use the key=value format for each entry)', 'nargs' : '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'copy': (([], {}), {
				None	: {
					'description'	: 'D.copy() -> a shallow copy of D',
				},
				False	: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('copy', (), 'args', (), 'kwargs'))},
				'--kwargs': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args': {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'fromkeys': (([], {}), {
				None		: {
					'description'	: 'Create a new dictionary with keys from iterable and values set to value.',
				},
				False		: {'__simplifiedapp_': ((dict.fromkeys, ('iterable', 'value'), None, (), None))},
				'--value'	: {'default': argparse.SUPPRESS},
				'iterable'	: {},
			}),
			'get'			: (([], {}), {
				None		: {
					'description'	: 'Return the value for key if key is in the dictionary, else default.',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('get', ('key', 'default'), None, (), None))},
				'--default'	: {'default': argparse.SUPPRESS},
				'key'		: {}
			}),
			'items': (([], {}), {
				None		: {
					'description'	: 'D.items() -> a set-like object providing a view on D\'s items',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('items', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'keys': (([], {}), {
				None		: {
					'description'	: 'D.keys() -> a set-like object providing a view on D\'s keys',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('keys', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'pop': (([], {}), {
				None		: {
					'description'	: 'D.pop(k[,d]) -> v, remove specified key and return the corresponding value.',
					'epilog'		: 'If the key is not found, return the default if given; otherwise,\nraise a KeyError.'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('pop', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}}
			),
			'popitem'		: (([], {}), {
				None	: {
					'description'	: 'Remove and return a (key, value) pair as a 2-tuple.',
					'epilog'		: 'Pairs are returned in LIFO (last-in, first-out) order.\nRaises KeyError if the dict is empty.'
				},
				False	: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('popitem', (), None, (), None))}
			}),
			'setdefault'	: (([], {}), {
				None		: {
					'description'	: 'Insert key with a value of default if key is not in the dictionary.',
					'epilog'		: 'Return the value for key if key is in the dictionary, else default.'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('setdefault', ('key', 'default'), None, (), None))},
				'--default'	: {'default': argparse.SUPPRESS},
				'key'		: {}
			}),
			'update': (([], {}), {
				None		: {
					'description'	: 'D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.',
					'epilog'		: 'If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]\nIf E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v\nIn either case, this is followed by: for k in F:  D[k] = F[k]'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('update', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'values': (([], {}), {
				None		: {
					'description'	: 'D.values() -> an object providing a view on D\'s values',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('values', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			})
		}),
		'--kwargs'		: {'action' : 'extend', 'default' : [], 'help' : '(Use the key=value format for each entry)', 'nargs' : '+'},
		'args'			: {'action': 'extend', 'default': [], 'nargs': '*'},
	},
	(3, 12)	: {
		None			: {
			'description'	: 'dict() -> new empty dictionary',
			'epilog'		: '\n'.join([
				"dict(mapping) -> new dictionary initialized from a mapping object\'s",
				'    (key, value) pairs',
				'dict(iterable) -> new dictionary initialized as if via:',
				'    d = {}',
				'    for k, v in iterable:',
				'        d[k] = v',
				'dict(**kwargs) -> new dictionary initialized with the name=value pairs',
				'    in the keyword argument list.  For example:  dict(one=1, two=2)',
			]),
		},
		False			: {'__simplifiedapp_': (dict, (), 'args', (), 'kwargs')},
		True			: ({'title': 'dict methods'}, {
			'__new__': (([], {}), {
				None: {
					'description': 'Create and return a new object.  See help(type) for accurate signature.',
				},
				False: {'__simplifiedapp_': (dict.__new__, (), 'args', (), 'kwargs')},
				'--kwargs': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args': {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'clear': (([], {}), {
				None		: {
					'description'	: 'D.clear() -> None.  Remove all items from D.',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('clear', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action' : 'extend', 'default' : [], 'help' : '(Use the key=value format for each entry)', 'nargs' : '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'copy': (([], {}), {
				None	: {
					'description'	: 'D.copy() -> a shallow copy of D',
				},
				False	: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('copy', (), 'args', (), 'kwargs'))},
				'--kwargs': {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args': {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'fromkeys': (([], {}), {
				None		: {
					'description'	: 'Create a new dictionary with keys from iterable and values set to value.',
				},
				False		: {'__simplifiedapp_': ((dict.fromkeys, ('iterable', 'value'), None, (), None))},
				'--value'	: {'default': argparse.SUPPRESS},
				'iterable'	: {},
			}),
			'get'			: (([], {}), {
				None		: {
					'description'	: 'Return the value for key if key is in the dictionary, else default.',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('get', ('key', 'default'), None, (), None))},
				'--default'	: {'default': argparse.SUPPRESS},
				'key'		: {}
			}),
			'items': (([], {}), {
				None		: {
					'description'	: 'D.items() -> a set-like object providing a view on D\'s items',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('items', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'keys': (([], {}), {
				None		: {
					'description'	: 'D.keys() -> a set-like object providing a view on D\'s keys',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('keys', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'pop': (([], {}), {
				None		: {
					'description'	: 'D.pop(k[,d]) -> v, remove specified key and return the corresponding value.',
					'epilog'		: 'If the key is not found, return the default if given; otherwise,\nraise a KeyError.'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('pop', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}}
			),
			'popitem'		: (([], {}), {
				None	: {
					'description'	: 'Remove and return a (key, value) pair as a 2-tuple.',
					'epilog'		: 'Pairs are returned in LIFO (last-in, first-out) order.\nRaises KeyError if the dict is empty.'
				},
				False	: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('popitem', (), None, (), None))}
			}),
			'setdefault'	: (([], {}), {
				None		: {
					'description'	: 'Insert key with a value of default if key is not in the dictionary.',
					'epilog'		: 'Return the value for key if key is in the dictionary, else default.'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('setdefault', ('key', 'default'), None, (), None))},
				'--default'	: {'default': argparse.SUPPRESS},
				'key'		: {}
			}),
			'update': (([], {}), {
				None		: {
					'description'	: 'D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.',
					'epilog'		: 'If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]\nIf E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v\nIn either case, this is followed by: for k in F:  D[k] = F[k]'
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('update', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			}),
			'values': (([], {}), {
				None		: {
					'description'	: 'D.values() -> an object providing a view on D\'s values',
				},
				False		: {'__simplifiedapp_': ((dict, (), 'args', (), 'kwargs'), ('values', (), 'args', (), 'kwargs'))},
				'--kwargs'	: {'action': 'extend', 'default': [], 'help': '(Use the key=value format for each entry)', 'nargs': '+'},
				'args'		: {'action': 'extend', 'default': [], 'nargs': '*'}
			})
		}),
		'--kwargs'		: {'action' : 'extend', 'default' : [], 'help' : '(Use the key=value format for each entry)', 'nargs' : '+'},
		'args'			: {'action': 'extend', 'default': [], 'nargs': '*'},
	},
}

def module_args_venv():
	return MODULE_ARGS_VENV[tuple(sys.version_info)[:2]]

def class_args_dict():
	return CLASS_ARGS_DICT[tuple(sys.version_info)[:2]]
