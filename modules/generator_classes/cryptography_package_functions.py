from ..packages import Cipher, algorithms, modes
from ..common_functions import random_byte_seed_generator


class CurrentGenerator(object):
    """
    This function use package "cryptography". It uses random key to encrypts null bytes stream,
    and update the stream for each random binary file.
    """

    def __init__(self, seed_length, binary_length, *args, **kwargs):
        key = random_byte_seed_generator(seed_length)
        aes_ctr_nonce = bytearray(seed_length // 2)
        cipher = Cipher(algorithms.AES(key), modes.CTR(aes_ctr_nonce))
        self.encryptor = cipher.encryptor()
        self.nulls = bytearray(binary_length)
        self.binary_length = binary_length

    def random_binary_stream(self, binary_length):
        if binary_length == self.binary_length:
            nulls = self.nulls
        else:
            nulls = bytearray(binary_length)
        return self.encryptor.update(nulls)


def random_binary_files_aes_algorithm(file_num, file_size, random_file_name_iter, output_folder):
    """
    This function use package "cryptography". It uses random key to encrypts null bytes stream,
    and update the stream for each random binary file.
    """
    file_count = 0
    aes_key = os.urandom(aes_seed_length)
    aes_ctr_nonce = b'\0' * (aes_seed_length // 2)
    cipher = Cipher(algorithms.AES(aes_key), modes.CTR(aes_ctr_nonce))
    encryptor = cipher.encryptor()
    nulls = b'\0' * file_size

    while file_count < file_num:
        new_file_name = next(random_file_name_iter)
        new_file_path = "{}/{}".format(output_folder, new_file_name)
        with open(new_file_path, 'wb') as f_out:
            new_file_content = encryptor.update(nulls)
            f_out.write(new_file_content)
        file_count += 1
        if file_count % 100 == 0:
            print("{} files finished".format(file_count))