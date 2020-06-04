def binaryToDec(n):                                                                                         # BINARY TO DECIMAL AND BACKWARDS CONVERSION FUNCTIONS
    return int(n, 2)

def decimalToBinary(n):
    return bin(n).replace("0b", "")

def decimal_formatter(ip):                                                                                   # RETURNS THE IP ADDRESS PASSED AS ARGUMENT AS AN ARRAY OF 4x8 BINARY NUMBERS
    result_array = [decimalToBinary(int(x)).rjust(8,'0') for x in ip.split('.')]                             # create a 32 bit representation of the IP
    ret_str = str(result_array).strip("[]'").replace("', '", '')
    assert len(ret_str) == 32, 'This is supposed to return a 32 bit string'
    return ret_str

def mask_generator(input_array):
    binary_ip_array = [decimal_formatter(x) for x in input_array]                                            # LET'S CREATE A LIST TO FEED TO THE MASK FINDING FUNCTION
    #print(binary_ip_array)
    fdb_array = []
    for i in range(len(binary_ip_array)):                                                                    # FINDING FIRST DIFFERENT BIT IN THE IP ARRAY TURNED INTO BINARY
        for j in range(len(binary_ip_array)):                                                                # TO GENERATE THE MINIMAL SUBNET MASK
            for bit in range(len(binary_ip_array[i])):
                for another_bit in range(len(binary_ip_array[j])):
                    if binary_ip_array[i][bit] != binary_ip_array[j][bit]:
                        fdb_array.append(bit)
    first_different_bit = min(fdb_array)
    mask_binary = ('1' * (first_different_bit)).ljust(32, '0')                                               # HERE'S THE BINARY REPRESENTATION OF MASK
    assert len(mask_binary) == 32, 'Binary mask is to be a 32 bit string as well'

    ip_octets = [binaryToDec(binary_ip_array[0][i:i + 8]) for i in range(0, len(binary_ip_array[0]), 8)]     # NOW LET'S BREAK IN DOWN INTO OCTETS AND CONVERT BACK TO DECIMAL
    mask_octets = [binaryToDec(mask_binary[i:i + 8]) for i in range(0, len(mask_binary), 8)]                 # WE NEED ONLY TO TAKE ONE IP AND DO THE BINARY AND OPERATION FOR IT AND THE MASK TO FIND THE NETWORK ADDRESS

    subnet_ip = [ip & mask_octets[num] for num, ip in enumerate(ip_octets)]                                  # HERE IT IS : THE NETWORK ADDRESS

    #print(ip_octets, mask_octets)

    print('Minimum mask length for the given ip list is ' + str(first_different_bit) + ' bits. \nBinary mask : ' + str(mask_binary))
    print('Network address is : ' + str(subnet_ip).replace(',','.').strip('[]'))

    return mask_binary


###############################################################################################################################################################################

ip_list = ['192.168.2.25', '192.168.5.68', '192.168.10.15', '192.168.15.254']                                # FEEL FREE TO TEST IT WITH DIFFERENT IP SETS

mask_generator(ip_list)

