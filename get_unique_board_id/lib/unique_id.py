import ubinascii
import machine


def get_unique_id():
    unique_id = machine.unique_id()
    unique_id_hex = ubinascii.hexlify(unique_id).decode()
    unique_id_int = int.from_bytes(unique_id, 'big')
    return unique_id_hex, unique_id_int
