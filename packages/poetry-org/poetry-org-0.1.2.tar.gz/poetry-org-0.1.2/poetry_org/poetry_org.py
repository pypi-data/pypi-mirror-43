from pathlib import Path
import toml
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s :: %(message)s')


def main():
    try:
        toml_data = toml.load('pyproject.toml', _dict=dict)
    except FileNotFoundError as e:
        logging.error('Poetry TOML file not found. \n         ' \
            'Run poetry_org in the Poetry project root directory.')
        return

    app_name = toml_data['tool']['poetry']['name'].replace('-','_')
    app_version = toml_data['tool']['poetry']['version']
    app_name_hyphens = app_name.replace('_','-')

    exclude_files = [ 'pyproject.toml',
                      'poetry.lock',
                      'requirements.txt',
                      'readme.md',
                      'readme.rst',
                      'license',
                      '.gitignore',
                      '__pycache__',
                      'dist',
                      app_name + '.egg-info',
                      'tests',
                      app_name,
                    ]


    proj_dir = Path.cwd()
    items = proj_dir.glob('*')

    '''Make app directory'''
    app_dir = proj_dir / app_name
    app_dir.mkdir(parents=True, exist_ok=True)

    '''Check for app_name.py'''
    app_file = proj_dir / (app_name + '.py')
    if not app_file.exists():
        app_file_hyphens = proj_dir / (app_name_hyphens + '.py')
        if app_file_hyphens.exists():
            app_file_hyphens.rename(app_file)
            logging.warning(f'Renamed {app_name_hyphens}.py to {app_name}.py')
        else:
            new_app_path = app_dir / (app_name + '.py')
            if not new_app_path.exists():
                logging.error(f'App file not found: {app_name}.py')
                return

    '''Copy app files into app directory'''
    for item in items:
        if not item.name.lower() in exclude_files:
            logging.info(f'Moving   ./{item.name}  -->  ./{app_name}/{item.name}')
            new_item_path = app_dir/item.name
            if new_item_path.exists():
                logging.error(f'File ./{app_name}/{new_item_path.name} already exists!\n ** Merge files and re-run script. **')
                return
            item.replace(new_item_path)

    '''Create __init__ file text'''
    pyfiles = app_dir.glob('*.py')
    init_file = app_dir / '__init__.py'
    init_imports = ["__version__ = \'0.1.0\'\n"]
    for pyfile in pyfiles:
        if pyfile.name != '__init__.py':
            init_imports.append('from .' + pyfile.stem + ' import *')

    '''Write __init__.py file'''
    init_file.write_text('\n'.join(init_imports))
    logging.info(f'Updated file __init__.py in ./{app_name}/')

    '''Add test directory if not there.'''
    test_dir = proj_dir / 'tests'
    test_dir.mkdir(parents=True, exist_ok=True)
    test_init_file = Path(test_dir, '__init__.py')
    test_dir_update = False
    if not test_init_file.exists():
        test_init_file.write_text('')
        test_dir_update = True
    test_app_file = Path(test_dir, f'test_{app_name}.py')
    if not test_app_file.exists():
        test_app_file.write_text(f'from {app_name} import __version__\n\n'
        '   def test_version():\n'\
        '       assert __version__ == \'{app_version}\'')
        test_dir_update = True
    if test_dir_update:
        logging.info(f'Updated ./tests/ directory.')


    logging.info(f'Success! File structure of app {app_name} is ready for `poetry build`.\n')
    return

if __name__ == '__main__':
    main()
