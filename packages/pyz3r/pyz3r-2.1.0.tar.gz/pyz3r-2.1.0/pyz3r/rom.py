from .misc import misc
from .exceptions import alttprException

import hashlib

class romfile:
    def read(srcfilepath):
        expected_rom_sha256='794e040b02c7591b59ad8843b51e7c619b88f87cddc6083a8e7a4027b96a2271'
        sha256_hash = hashlib.sha256()
        with open(srcfilepath,"rb") as f:
            for byte_block in iter(lambda: f.read(4096),b""):
                sha256_hash.update(byte_block)
        if not sha256_hash.hexdigest() == expected_rom_sha256:
            raise alttprException('Expected checksum "{expected_rom_sha256}", got "{actual_checksum}" instead.  Verify the source ROM is an unheadered Japan 1.0 Link to the Past ROM.'.format(
                expected_rom_sha256=expected_rom_sha256,
                actual_checksum=sha256_hash.hexdigest()
            ))
        fr = open(srcfilepath,"rb")
        baserom_array = list(fr.read())
        fr.close()
        return baserom_array

    def write(rom, dstfilepath):
        fw = open(dstfilepath,"wb")
        patchrom = bytes()
        for idx, chunk_array in enumerate(misc.chunk(rom,256)):
            patchrom += bytes(chunk_array)
        fw.write(patchrom)
        fw.close

