import itertools
from builtins import hex
import time
from typing import Any, Union

utl_8_BIT_CRC_POLYNOMIAL_D = 0xD9
utl_pa_au8BYTE_CRC8_LUT_TABLE_C = [0x00, 0xD0, 0x13, 0xC3, 0x26, 0xF6, 0x35, 0xE5 , 0x4C, 0x9C, 0x5F, 0x8F, 0x6A, 0xBA, 0x79, 0xA9 , 0x98, 0x48, 0x8B, 0x5B, 0xBE, 0x6E, 0xAD, 0x7D , 0xD4, 0x04, 0xC7, 0x17, 0xF2, 0x22, 0xE1, 0x31 , 0x83, 0x53, 0x90, 0x40, 0xA5, 0x75, 0xB6, 0x66 , 0xCF, 0x1F, 0xDC, 0x0C, 0xE9, 0x39, 0xFA, 0x2A , 0x1B, 0xCB, 0x08, 0xD8, 0x3D, 0xED, 0x2E, 0xFE , 0x57, 0x87, 0x44, 0x94, 0x71, 0xA1, 0x62, 0xB2 , 0xB5, 0x65, 0xA6, 0x76, 0x93, 0x43, 0x80, 0x50 , 0xF9, 0x29, 0xEA, 0x3A, 0xDF, 0x0F, 0xCC, 0x1C , 0x2D, 0xFD, 0x3E, 0xEE, 0x0B, 0xDB, 0x18, 0xC8 , 0x61, 0xB1, 0x72, 0xA2, 0x47, 0x97, 0x54, 0x84 , 0x36, 0xE6, 0x25, 0xF5, 0x10, 0xC0, 0x03, 0xD3 , 0x7A, 0xAA, 0x69, 0xB9, 0x5C, 0x8C, 0x4F, 0x9F , 0xAE, 0x7E, 0xBD, 0x6D, 0x88, 0x58, 0x9B, 0x4B , 0xE2, 0x32, 0xF1, 0x21, 0xC4, 0x14, 0xD7, 0x07 , 0xD9, 0x09, 0xCA, 0x1A, 0xFF, 0x2F, 0xEC, 0x3C , 0x95, 0x45, 0x86, 0x56, 0xB3, 0x63, 0xA0, 0x70 , 0x41, 0x91, 0x52, 0x82, 0x67, 0xB7, 0x74, 0xA4 , 0x0D, 0xDD, 0x1E, 0xCE, 0x2B, 0xFB, 0x38, 0xE8 , 0x5A, 0x8A, 0x49, 0x99, 0x7C, 0xAC, 0x6F, 0xBF , 0x16, 0xC6, 0x05, 0xD5, 0x30, 0xE0, 0x23, 0xF3 , 0xC2, 0x12, 0xD1, 0x01, 0xE4, 0x34, 0xF7, 0x27 , 0x8E, 0x5E, 0x9D, 0x4D, 0xA8, 0x78, 0xBB, 0x6B , 0x6C, 0xBC, 0x7F, 0xAF, 0x4A, 0x9A, 0x59, 0x89 , 0x20, 0xF0, 0x33, 0xE3, 0x06, 0xD6, 0x15, 0xC5 , 0xF4, 0x24, 0xE7, 0x37, 0xD2, 0x02, 0xC1, 0x11 , 0xB8, 0x68, 0xAB, 0x7B, 0x9E, 0x4E, 0x8D, 0x5D , 0xEF, 0x3F, 0xFC, 0x2C, 0xC9, 0x19, 0xDA, 0x0A , 0xA3, 0x73, 0xB0, 0x60, 0x85, 0x55, 0x96, 0x46 , 0x77, 0xA7, 0x64, 0xB4, 0x51, 0x81, 0x42, 0x92 , 0x3B, 0xEB, 0x28, 0xF8, 0x1D, 0xCD, 0x0E, 0xDE]


def utl_vCalculateCrcFor8Bits(input_crc, input_byte):

    return utl_pa_au8BYTE_CRC8_LUT_TABLE_C[input_crc ^ input_byte]



def crc_test():
    correct_results = 0
    for number in range(len(utl_pa_au8BYTE_CRC8_LUT_TABLE_C)):
        crc_result = utl_vCalculateCrcFor8Bits(0x00, number)
        if crc_result != utl_pa_au8BYTE_CRC8_LUT_TABLE_C[number]:
            print(hex(crc_result) + ' : ' + hex(utl_pa_au8BYTE_CRC8_LUT_TABLE_C[number]))
        else:
            correct_results += 1

    print("correct_results : " + str(correct_results))


def main():
    print(" *** START OF TEST *** ")
    start_time = time.time()

    fail_counter = 0

    frame_len = 2 + 1
    no_of_all_bits_in_full_frame = frame_len * 8
    no_of_data_bits_in_frame = (frame_len - 1) * 8
    no_of_corrupted_bits = 2

    all_possible_positions_of_corrupted_bits = list(range(no_of_data_bits_in_frame))
    corrupter_bit_positions = tuple(
        itertools.combinations(all_possible_positions_of_corrupted_bits, no_of_corrupted_bits))

    # for frame in frames:
    for frame in range(2 ** no_of_data_bits_in_frame):
        # create frame data with LSB first
        temp_frame = list(frame.to_bytes((frame_len - 1), 'little'))
        # calculate CRC from frame data bytes
        crc = 0x00
        for byte in temp_frame:
            crc = utl_vCalculateCrcFor8Bits(crc, byte)
        # append the calculated CRC byte to the end of the frame
        tx_full_frame = frame | (crc << (frame_len - 1) * 8)

        for bit_positions_bundle in corrupter_bit_positions:
            # create mask for frame corruption with LSB first
            corrupted_frame_mask = 0x00
            for bit_pos in bit_positions_bundle:
                corrupted_frame_mask = corrupted_frame_mask | (1 << bit_pos)

            # emulate data distortion at transmission - corrupt frame data
            rx_full_frame = tx_full_frame ^ corrupted_frame_mask

            # create frame data with LSB first
            temp_frame = list(rx_full_frame.to_bytes(frame_len, 'little'))
            # calculate CRC from frame data bytes
            crc = 0x00
            for byte in temp_frame[:-1]:
                crc = utl_vCalculateCrcFor8Bits(crc, byte)
            if crc != temp_frame[-1]:
                pass
            else:
                # print("{:d} {:d} {:d}".format(tx_full_frame, rx_full_frame, crc))
                fail_counter += 1

    print("{:d} bits of total {:d} data bits corrupted".format(no_of_corrupted_bits, no_of_data_bits_in_frame))
    print("{:d} combinations of corrupted bits positions".format(len(corrupter_bit_positions)))
    print("{:d} corrupted frames not reveled".format(fail_counter))

    print(" *** END OF TEST *** ")
    print(" test duration {:0.2f}".format(time.time() - start_time))

    return


if __name__ == '__main__':
    main()

