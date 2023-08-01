from setuptools import setup, find_packages

setup(
    name='clean_folder',
    version='0.0.1',
    description='Very useful code',
    #url = 'https://github.com/MarsIana1804/My_repository/tree/main/cleanfolder',
    author='Maryna',
    author_email='marina@gmail.com',
    license='MIT',
    classifiers = ["Programming language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent"],
    packages= find_packages(),
    entry_points={'console_scripts':['clean-folder = clean_folder.clean:package_installation']}
    

    )
   