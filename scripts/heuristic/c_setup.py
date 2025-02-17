from setuptools import setup, Extension
from Cython.Build import cythonize
import os, shutil

path: str = os.path.dirname(os.path.abspath(__file__))

for file in os.listdir(path):
    try:
        if file.endswith('.py') and not '__init__' in file and 'c_setup' not in file:
            file_name = file.replace('.py', '')
            file_path = os.path.join(path, file)
            
            shutil.copy2(file_path, f'{file_path}x')
        
            custom_name: str = f'cython_{file_name}'

            ext_modules: list = [Extension(
                name=custom_name,
                sources=[fr"{file_path}x"],
            )]

            setup(
                name=file_name,
                ext_modules=cythonize(ext_modules),
                options={'build_ext': {'build_lib': path}}
            )
    
    except Exception as e:
        print(f"Error: {e}")
        continue
    