from subprocess import call
import sys
import getopt
from os import listdir, makedirs
from os.path import isfile, join, exists


def copy_file(output_dir, region, file_name, tmp_rom_dir):
    target_dir = join(output_dir, region, file_name[0].upper())
    if not exists(target_dir):
        makedirs(target_dir)
    target_file = join(target_dir, file_name)
    call(["cp", join(tmp_rom_dir, file_name), target_file])


def main(argv):
    input_file = ""
    output_file = ""
    tmp_dir = "/tmp/.EverDriver"
    try:
        opts, args = getopt.getopt(argv, "hi:o:")
    except getopt.GetoptError:
        print "ed_import.py -i <inputfile> -o <outputdir>"
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print "ed_import.py -i <inputfile> -o <outputdir>"
            sys.exit()
        elif opt in "-i":
            input_file = arg
        elif opt in "-o":
            output_file = arg
    print 'Input file is "', input_file
    print 'Output file is "', output_file

    # Unzip the romset
    call(["unzip", "-j", "-d", tmp_dir, input_file])

    # Handle individual roms
    roms = [f for f in listdir(tmp_dir) if f.endswith(".7z")]
    for rom in roms:
        print "Processing %s" % rom
        tmp_rom_dir = join(tmp_dir, f[:-3])
        print "Rom tmp dir %s" % tmp_rom_dir
        call(["7z", "-o%s" % tmp_rom_dir, "x", join(tmp_dir, rom)])
        versions = listdir(tmp_rom_dir)
        for version in versions:
            if "[!]" in version or version.endswith("(E).smc") or version.endswith("(J).smc") or \
                    version.endswith("(U).smc"):
                if "(E)" in version:
                    copy_file(output_file, "PAL", version, tmp_rom_dir)
                if "(J)" in version:
                    copy_file(output_file, "JAP", version, tmp_rom_dir)
                if "(U)" in version or "(JU)" in version:
                    copy_file(output_file, "NTSC", version, tmp_rom_dir)
        call(["rm", "-Rf", tmp_rom_dir])

    call(["rm", "-Rf", tmp_dir])

if __name__ == "__main__":
    main(sys.argv[1:])