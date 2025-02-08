from lib.unique_id import get_unique_id

unique_id_hex, unique_id_int = get_unique_id()
print("This boards unique ID as an integer:")
print(unique_id_int)

print("This boards unique ID as a hex string:")
print(unique_id_hex)
