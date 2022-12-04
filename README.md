# Decree generator
Python script that generates a lot of decrees from samples.
Скрипт для генерации файлов приказов из образцов.

## Usage
```
$ python3 gen.py -h
usage: gen.py [-h] [-i] [-f format] [-s path] [-o path] [-v] size

Decrees generator

positional arguments:
  size                  Max size of output dir. For example: 10KB, 10MB, 10GB

options:
  -h, --help            show this help message and exit
  -i, --image           use images (logo, signature, seal) in decree
  -f format, --format format
                        formats to save (docx: d, pdf: p, jpg: j)
  -s path, --samples path
                        path to dir with samples
  -o path, --out path   path for output files
  -v, --verbose         verbose output

Example: python3 gen.py 50MB -f dp -s samples -o decrees -vv
  
$ python3 gen.py 50MB -i -f dp -s samples/ -o output_decrees/
2022-12-04 20:38:42.542 | WARNING  | __main__:main:169 - Generation is started...
2022-12-04 20:39:15.208 | WARNING  | __main__:generate:136 - Approximate generation time: 1.13 min.
2022-12-04 20:39:52.709 | WARNING  | __main__:generate:124 - Size of output_decrees/ dir: 53422132 bytes
2022-12-04 20:39:52.709 | WARNING  | __main__:main:171 - Generation is finished!
```

## Samples description
![description one](https://github.com/cadnev/decree_gen/blob/main/raw/img/desc1.jpg)
![description two](https://github.com/cadnev/decree_gen/blob/main/raw/img/desc2.jpg)