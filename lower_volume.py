import sys
import ffmpeg
import os
import struct 
import binascii

def get_bitrate(file):
   probe = ffmpeg.probe(file)
   video_bitrate = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
   bitrate = video_bitrate['bit_rate']
   return bitrate

def get_samplerate(file):
   probe = ffmpeg.probe(file)
   video_bitrate = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
   samplerate = video_bitrate['sample_rate']
   return samplerate

def get_duration(file):
   probe = ffmpeg.probe(file)
   video_bitrate = next(s for s in probe['streams'] if s['codec_type'] == 'audio')
   duration = video_bitrate['duration']
   return duration

def main(argv):
    # set parameters
    input_dir_name = 'c:\\temp\\p3p\\bgm'
    output_dir_name = 'c:\\temp\\p3p\\bgm_new'
    new_volume = 0.25

    # loop through files in source directory
    for filename in os.listdir(input_dir_name):
        f = os.path.join(input_dir_name, filename)
        # checking if it is a file
        if os.path.isfile(f):
            # output filename
            print(f)

            # get the copyright offset from the original file
            with open(f, 'rb') as f1: 
                f1.seek(0x02)
                source_cp_offset = int.from_bytes(f1.read(2), byteorder='big')
            # define mandatory header as struct
            mandatory_header_format = '>cchBBBBiihBB'
            mandatory_header_fields = ('fixed1','fixed2','cp_offset','enc_type','block_size','sample_depth','channel_count','sample_rate','total_samples','highpass_freq','version','flags')
            optional_header_format = '>hhiiiiiiii'
            v3_optional_header_fields = ('loop_align_samples','loop_enabled','loop_enabled2','loop_begin_sample_index','loop_begin_byte_index','loop_end_sample_index','loop_end_byte_index','not_used1','not_used2','not_used3')
            v4_optional_header_fields = ('not_used1','not_used2','not_used3','not_used4','not_used5','loop_enabled','loop_begin_sample_index','loop_begin_byte_index','loop_end_sample_index','loop_end_byte_index')
            with open(f, 'rb') as f1:
                # read the header into a dict
                byte_buffer = f1.read(struct.calcsize(mandatory_header_format))
                header_tuple = struct.unpack(mandatory_header_format, byte_buffer)
                source_dict = dict(zip(mandatory_header_fields, header_tuple))

                # print out source headers
                print(source_dict)
                
        # last ditch attempt, just try and modify the data directly
        # copy everything up to the data
        output_filename = '%s\\%s'%(output_dir_name, filename)
        if os.path.isfile(output_filename):
            os.remove(output_filename)
        with open(output_filename, 'wb') as f3:
            with open(f, 'rb') as f1: 
                # first copy header from original file
                for pos in range(0x00, source_cp_offset + 4):
                    f3.write(f1.read(1))

                # now get each block and modify scale
                this_block = f1.read(18)
                while this_block:
                    block_byte_array = bytearray(this_block)
                    #print(binascii.hexlify(block_byte_array))
                    byte1 = block_byte_array[0]
                    byte2 = block_byte_array[1]
                    pred = (byte1&11100000)>>5
                    amp = int(byte2+((byte1&0b00011111)<<8))
                    amp = int(float(amp)*new_volume)
                    amp += pred<<13
                    new_word = bytearray(amp.to_bytes(2, 'big'))
                    #print(binascii.hexlify(new_word))
                    block_byte_array[0] = new_word[0]
                    block_byte_array[1] = new_word[1]
                    #print(binascii.hexlify(block_byte_array))
                    this_block = bytes(block_byte_array)
                    f3.write(this_block)
                    this_block = f1.read(18)

    return

if __name__ == "__main__":
    main(sys.argv[1:])
