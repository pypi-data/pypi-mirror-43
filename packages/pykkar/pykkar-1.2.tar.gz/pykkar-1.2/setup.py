from setuptools import setup

setup(
      name="pykkar",
      version=1.2,
      description="Virtual robot library for teaching programming",
      long_description="Pykkar is simple robot that can be commanded to move and act in user-designed grid world. See https://bitbucket.org/plas/pykkar for samples",
      author="Aivar Annamaa and others",
      url="https://bitbucket.org/plas/pykkar",
      license="MIT",
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "License :: Freeware",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
      ],
      keywords="robot pykkar education karel",
      py_modules=["pykkar"],
)