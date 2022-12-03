import setuptools

#Si tienes un readme
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='DarwinexDownloader',  #nombre del paquete
     version='0.0.1', #versión
     scripts=['DarwinexDownloader.py'] , #nombre del ejecutable
     author="Ivan Garcia-Ferreira", #autor
     author_email="ivan@garcia-ferreira.es", #email
     description="Un paquete para traducir a números romanos", #Breve descripción
     long_description=long_description,
	 long_description_content_type="text/markdown", #Incluir el README.md si lo has creado
     url="https://github.com/igarciaferreira/DarwinexDownloader", #url donde se encuentra tu paquete en Github
     packages=setuptools.find_packages(), #buscamos todas las dependecias necesarias para que tu paquete funcione (por ejemplo numpy, scipy, etc.)
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
		 "Topic :: Office/Business :: Financial",
		 "Topic :: Office/Business :: Financial :: Investment",
		 "Development Status :: 3 - Alpha"
     ],
 )