from setuptools import setup, find_packages

setup(name='server_chat_bai',
      version='0.8',
      description='Server packet',
      packages=find_packages(),
      author_email='darth-maul@mail.ru',
      author='Aleksey Blagodetelevi',
      install_requeres=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )