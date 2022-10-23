# Decree generator
Python script that generates a lot of decrees from samples

## Usage
```
$ python3 gen.py -h                               
usage: gen.py [-h] [-s path] [-o path] [-v] size

positional arguments:
  size                  Max size of output dir. For example: 10KB, 10MB, 10GB

options:
  -h, --help            show this help message and exit
  -s path, --samples path
                        Path to dir with samples
  -o path, --out path   Path for output files
  -v, --verbose
  
$ python3 gen.py 50MB -s samples -o output_decrees
2022-10-24 01:19:09.021 | WARNING  | __main__:load_samples:37 - Approximate number of different decrees: 653184
2022-10-24 01:19:09.022 | WARNING  | __main__:main:114 - Approximate generation time: 0.42 min.
2022-10-24 01:19:35.995 | WARNING  | __main__:generate:94 - Size of output_decrees dir: 52605387 bytes
2022-10-24 01:19:35.996 | WARNING  | __main__:main:116 - Generation is finished!
```