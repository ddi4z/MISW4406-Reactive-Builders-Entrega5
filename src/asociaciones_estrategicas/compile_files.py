import os

# Ruta al directorio que contiene tus archivos.
source_directory = '.'  # Sustituye esto por tu directorio real.
# Nombre del archivo de salida.
output_file_path = 'contents_summary.txt'  # Puedes cambiar esto si deseas otro nombre de archivo o ubicación.

# Directorios y archivos para excluir.
excluded_dirs = ['__pycache__', 'venv','instance','tests','.vscode','.git','.angular','.github','node_modules','docs','.devcontainer','.coveragerc']
excluded_files = ['.gitignore','Jenkinsfile','Dockerfile','docker-compose.yml','requirements.txt','compile_files.py','contents_summary.txt','Pipfile','Pipfile.lock','.env.development','eporra.db']
excluded_extensions = ['.db','.txt','.md','.lock','.pyc','.json','.js','.sh']

def is_excluded(file_name, root):
    # Verifica si el archivo o directorio está excluido.
    if file_name in excluded_files:
        return True
    file_extension = os.path.splitext(file_name)[1]
    if file_extension in excluded_extensions:
        return True
    relative_dir = os.path.relpath(root, source_directory)
    for excluded_dir in excluded_dirs:
        if excluded_dir in relative_dir.split(os.sep):
            return True
    return False

def write_contents_to_file(output_file):
    for root, dirs, files in os.walk(source_directory):
        # Filtra los directorios excluidos.
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        path_from_source = os.path.relpath(root, source_directory)
        output_file.write(f'\n\nDirectory: {path_from_source}\n')
        output_file.write('-' * (len(path_from_source) + 12) + '\n')

        for file_name in files:
            if is_excluded(file_name, root):
                continue  # Si el archivo está en la lista de excluidos, salta al siguiente.

            file_path = os.path.join(root, file_name)

            try:
                with open(file_path, 'r') as file:
                    contents = file.read()

                output_file.write(f'\nFile: {file_name}\n')
                output_file.write(f'Path: {file_path}\n\n')
                output_file.write('Contents:\n')
                output_file.write(contents + '\n')
                output_file.write('=' * 50 + '\n')

            except Exception as e:
                output_file.write(f'Error reading file {file_name}: {str(e)}\n')
                output_file.write('=' * 50 + '\n')

# Abre (o crea) el archivo de salida para escribir en él.
with open(output_file_path, 'w') as output_file:
    write_contents_to_file(output_file)
