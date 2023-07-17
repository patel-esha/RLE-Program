from console_gfx import ConsoleGfx as Gfx


class rle_program:

    def __init__(self):
        self.menu_selection = None
        self.image_data = None  # ensures that the image loads before it is displayed
        self.num_runs = 0
        self.in_progress = True  # keeps program running

    def main_menu(self):
        print('Welcome to the RLE image encoder!') if self.num_runs == 0 else None  # only when program starts
        print() if self.num_runs == 0 else None
        print('Displaying Spectrum Image:') if self.num_runs == 0 else None
        Gfx.display_image(Gfx.test_rainbow) if self.num_runs == 0 else None
        print()  # menu options
        print('RLE Menu')
        print('--------')
        print('0. Exit')
        print('1. Load File')
        print('2. Load Test Image')
        print('3. Read RLE String')
        print('4. Read RLE Hex String')
        print('5. Read Data Hex String')
        print('6. Display Image')
        print('7. Display RLE String')
        print('8. Display Hex RLE Data')
        print('9. Display Hex Flat Data')
        print()
        self.num_runs += 1


    def menu_options(self, menu_selection):  # menu selections and their individual tasks

        self.menu_selection = int(input('Select a Menu Option: '))

        if self.menu_selection == 1:  # load file
            file_name = input('Enter name of file to load: ')  # for zybooks to insert file names

        elif self.menu_selection == 2:  # load test image
            self.image_data = Gfx.test_image  # sets Gfx.test_image to the variable to utilize if option 6 is inputted
            self.num_runs += 1
            print('Test image data loaded.')

        elif self.menu_selection == 3:  # read RLE string
            rle_string = input('Enter an RLE string to be decoded: ')
            self.rle_string = rle_program.string_to_rle(rle_string)
            self.rle_string = rle_program.decode_rle(self.rle_string)

        elif self.menu_selection == 4:  # Read RLE Hex string
            rle_hex_string = input('Enter the hex string holding RLE data: ')
            self.rle_hex = rle_program. string_to_data(rle_hex_string)
            self.rle_hex = rle_program.decode_rle(self.rle_hex)

        elif self.menu_selection == 5:  # Read Data Hex string
            data_hex_string = input('Enter the hex string holding flat data: ')
            self.flat_hex = rle_program.string_to_data(data_hex_string)
            self.flat_hex = rle_program.decode_rle(self.flat_hex)

        elif self.menu_selection == 6:  # display image
            self.num_runs += 1
            print('Displaying image...')  # loading message
            Gfx.display_image(self.image_data)  # displays the image if the image was loaded and then asked to display

        elif self.menu_selection == 7:  # Display RLE string
            self.rle_string = rle_program.encode_rle(self.rle_string)
            self.rle_string = rle_program.to_rle_string(self.rle_string)
            print(f'RLE representation: {self.rle_string}')

        elif self.menu_selection == 8:  # Display RLE Hex data
            self.rle_hex = rle_program.encode_rle(self.rle_hex)
            self.rle_hex = rle_program.to_hex_string(self.rle_hex)
            print(f'RLE hex values: {self.rle_hex}')

        elif self.menu_selection == 9:  # Display Flat Hex data
            self.flat_hex = rle_program.encode_rle(self.flat_hex)
            self.flat_hex = rle_program.to_hex_string(self.flat_hex)
            print(f'Flat hex values: {self.flat_hex}')

    @staticmethod
    def to_hex_string(data):  # to_hex_string([3, 15, 6, 4]) yields string '36f4'
        hex_decimal = ''  # an open string version of a "list" for the converted string to be placed into
        for integer in data:
            if integer in range(10, 16):  # ensures that numbers below 10 go to the else statement
                if integer == 10:  # respective numbers are converted to hexadecimal based off of the chart
                    hex_decimal += 'a'
                elif integer == 11:
                    hex_decimal += 'b'
                elif integer == 12:
                    hex_decimal += 'c'
                elif integer == 13:
                    hex_decimal += 'd'
                elif integer == 14:
                    hex_decimal += 'e'
                elif integer == 15:
                    hex_decimal += 'f'

            else:
                hex_decimal += str(integer)  # numbers under 10 are the same, except they are now strings instead of int
        return hex_decimal

    @staticmethod
    def count_runs(flat_data):  # count_runs([15, 15, 15, 4, 4, 4, 4, 4, 4]) yields integer 2
        num_runs = 0  # total number of new numbers
        carrying_capacity = 0  # to ensure a new run begins for numbers 15 and above
        for i in range(0, len(flat_data)):
            if flat_data[i] != flat_data[i - 1]:  # if i in flat_data is the same as the number behind it
                num_runs += 1
            elif i == 0:  # since the first number does not have a number "behind" it
                num_runs = 1
            elif flat_data[i] == flat_data[i - 1]:  # for the 15 carrying capacity
                carrying_capacity += 1
            if carrying_capacity == 15:
                num_runs += 1
                carrying_capacity = 0
        return num_runs

    @staticmethod
    def encode_rle(flat_data):  # encode_rle([15, 15, 15, 4, 4, 4, 4, 4, 4]) yields list [3, 15, 6, 4]
        encoded_list = []
        num_int = 0
        for i in range(0, len(flat_data)):
            if i == 0:
                num_int = 1
            elif flat_data[i] == flat_data[i - 1]:  # adds one to minimize the flat_data
                num_int += 1
            elif flat_data[i] != flat_data[i - 1]:  # new number has been discovered
                encoded_list.append(num_int)
                encoded_list.append(flat_data[i - 1])
                num_int = 1  # reverts back to 1 in search of a new number
            if num_int == 15:  # carrrying capacity of 15
                encoded_list.append(num_int)
                encoded_list.append(flat_data[i - 1])
                num_int = 0
        encoded_list.append(num_int)
        encoded_list.append(flat_data[-1])
        return encoded_list

    @staticmethod
    def get_decoded_length(rle_data):  # get_decoded_length([3, 15, 6, 4]) yields integer 9
        decoded_length = 0
        for i in range(0, len(rle_data), 2):  # goes by 2's starting from 0 for the multiplier number (3 and 6)
            decoded_length += rle_data[i]  # adds it to the 0 starting point
        return decoded_length

    @staticmethod
    def decode_rle(rle_data):  # decode_rle([3, 15, 6, 4]) yields list [15, 15, 15, 4, 4, 4, 4, 4, 4]
        decoded_list = []  # open dictionary for expanded values
        for i in range(0, len(rle_data), 2):  # counts by 2's starting from 0 (even)
            multiple = rle_data[i]
            for j in range(
                    multiple):  # "multiplies" the int by having it return multiple times in the list per multiple
                for k in range(1, len(rle_data), 2):  # since the k is every other number (odd)
                    num = rle_data[i + 1]
                decoded_list.append(num)
        return decoded_list

    @staticmethod
    def string_to_data(data_string):  # string_to_data('3f64') yields list [3, 15, 6, 4]
        data_list = []  # open dictionary for inverse of hexadecimal conversion
        for hex in data_string:
            if hex == '0':  # for numbers 0 - 9
                data_list.append(0)
            elif hex == '1':
                data_list.append(1)
            elif hex == '2':
                data_list.append(2)
            elif hex == '3':
                data_list.append(3)
            elif hex == '4':
                data_list.append(4)
            elif hex == '5':
                data_list.append(5)
            elif hex == '6':
                data_list.append(6)
            elif hex == '7':
                data_list.append(7)
            elif hex == '8':
                data_list.append(8)
            elif hex == '9':
                data_list.append(9)
            elif hex == 'a':  # for numbers greater than 9, represented through the letters a - f
                data_list.append(10)
            elif hex == 'b':
                data_list.append(11)
            elif hex == 'c':
                data_list.append(12)
            elif hex == 'd':
                data_list.append(13)
            elif hex == 'e':
                data_list.append(14)
            elif hex == 'f':
                data_list.append(15)
        return data_list

    @staticmethod
    def to_rle_string(rle_data):  # [15, 15, 6, 4] -> '15f:64'
        def to_rle_string(rle_data):  # [15, 15, 6, 4] -> '15f:64'
            rle_string = ''
            count = 0
            for element in range(0, len(rle_data)):
                if element in range(0, len(rle_data), 2):
                    add_1 = str(rle_data[element])
                    rle_string += add_1
                    count += 1
                    continue
                elif element in range(1, len(rle_data), 2):
                    if rle_data[element] >= 10:
                        if rle_data[element] == 10:
                            add_2 = 'a'
                            rle_string += add_2
                            count += 1
                        elif rle_data[element] == 11:
                            add_2 = 'b'
                            rle_string += add_2
                            count += 1

                        elif rle_data[element] == 12:
                            add_2 = 'c'
                            rle_string += add_2
                            count += 1

                        elif rle_data[element] == 13:
                            add_2 = 'd'
                            rle_string += add_2
                            count += 1

                        elif rle_data[element] == 14:
                            add_2 = 'e'
                            rle_string += add_2
                            count += 1

                        elif rle_data[element] == 15:
                            add_2 = 'f'
                            rle_string += add_2
                            count += 1

                    elif rle_data[element] < 10:
                        add_2 = str(rle_data[element])
                        rle_string += add_2
                        count += 1
                if count < len(rle_data):
                    rle_string += ':'
            return rle_string

    @staticmethod
    def string_to_rle(rle_string):  # '15f:64' -> [15, 15, 6, 4]
        rle_list = []
        for element in rle_string.split(':'):
            if len(element) == 2:
                add_1 = element[0]
                rle_list += add_1
                if element[1] == 'a':
                    add_2 = '10'
                    rle_list += add_2
                elif element[1] == 'b':
                    add_2 = '11'
                    rle_list += add_2
                elif element[1] == 'c':
                    add_2 = '12'
                    rle_list += add_2
                elif element[1] == 'd':
                    add_2 = '13'
                    rle_list += add_2
                elif element[1] == 'e':
                    add_2 = '14'
                    rle_list += add_2
                elif element[1] == 'f':
                    add_2 = '15'
                    rle_list += add_2
                else:
                    add_2 = element[1]
                    rle_list += add_2

            elif len(element) == 3:
                add_1 = element.split(element[2])
                rle_list += add_1
                if element[2] == 'a':
                    add_2 = '10'
                elif element[2] == 'b':
                    add_2 = '11'
                elif element[2] == 'c':
                    add_2 = '12'
                elif element[2] == 'd':
                    add_2 = '13'
                elif element[2] == 'e':
                    add_2 = '14'
                elif element[2] == 'f':
                    add_2 = '15'
                add_2 = element.split(element[2])
                rle_list += add_2
                while '' in rle_list:
                    rle_list.remove('')
        rle_list = [int(i) for i in rle_list]
        return rle_list

    def run_program(self):  # runs the program in order of the methods
        self.main_menu()
        self.menu_options()


def main():  # runs program
    program = rle_program()

    while program.in_progress:
        program.main_menu()
        program.menu_options()
        program.in_progress = True


main()  # runs program
