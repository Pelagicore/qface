#!/usr/bin/env python3
from qface.generator import FileSystem, Generator

system = FileSystem.parse_dir('./examples')


generator = Generator()

ctx = {'system': system}
generator.write('out/packages.csv', 'packages.csv', ctx)
