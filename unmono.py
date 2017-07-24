import sys, gzip
from cStringIO import StringIO
from elftools.elf.elffile import ELFFile

elffile = ELFFile(open(sys.argv[1]))
data = open(sys.argv[1]).read()
is_mkbundle = False


section = elffile.get_section_by_name('.dynsym')
for symbol in section.iter_symbols():
        if symbol['st_shndx']  != 'SHN_UNDEF' and symbol.name == 'mono_mkbundle_init':
                        is_mkbundle = True
                        break
if is_mkbundle:
        print 'This is mkbundle! Now off to extraction!'
else:
        print 'This does not seem like mkbundle, exiting!'
        sys.exit(1)

for symbol in section.iter_symbols():
        if symbol['st_shndx'] != 'SHN_UNDEF' and symbol.name.startswith('assembly_data_'):
                filename = symbol.name[14:-4]
                filename += '.dll'
                with open(filename, 'w') as f:
                        dll_data = data[symbol['st_value']:symbol['st_value']+symbol['st_size']]
                        f.write(gzip.GzipFile(fileobj=StringIO(dll_data)).read())
                print 'Dumped %s' % filename
