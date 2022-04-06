from flag import flag

def chunks(l, n):
    """Split list l into chunks of size n"""

    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))

INT_BITS = 32

def leftRotate(val, number):
    # chad python with it's unlimited int size
    binary = "{0:b}".format(val).rjust(INT_BITS, "0")
    rotated = binary[number:] + binary[:number]
    return int(rotated, base=2) & 0xFFFFFFFF

def rightRotate(x, n):
    return int(f"{x:032b}"[-n:] + f"{x:032b}"[:-n], 2)

class ChaCha20:

    def __init__(self, nonce):
        self.nonce = nonce

        if len(nonce) != 12:
            raise Exception("Invalid nonce length - should be 12 bytes")
        
        self.ROUNDS = 10

        self.counter = 1

    def init_state(self):
        """
               Initial state of ChaCha
            "expa"	"nd 3"	"2-by"	"te k"
            Key	    Key	    Key	    Key
            Key	    Key	    Key	    Key
            Counter	Nonce	Nonce	Nonce
        """
        nonce = chunks(self.nonce, 4)
        self.state = []

        self.state.extend([b"expa", b"nd 3", b"2-by", b"te k"])
        self.state.extend(chunks(self.key, 4))
        self.state.append((self.counter).to_bytes(4, "little"))
        self.state.extend(nonce)

    def encrypt(self, message):
        output = b""

        for chunk in chunks(message, 64):
            self.init_state()

            for i in range(10):
                self.chacha_block()

            self.counter += 1

            concat_state = b"".join(self.state)

            for i in range(len(chunk)):
                output += bytes([int(concat_state[i]) ^ int(chunk[i])])
                
        return output

    def get_key(self, plaintext, encrypted):
        output = b""

        a,b,c,d = 10,20,30,40
        print(self.quarter_round(a,b,c,d))
        print(self.quarter_round_reversed(*self.quarter_round(a,b,c,d)))
        #self.init_state()
        state = []
        for i in range(len(plaintext)):
            state += bytes([int(plaintext[i]) ^ int(encrypted[i])])
            
        self.state = list(chunks(state, 4))

        print(self.state)

        for i in range(10):
            self.chacha_block_reversed()

        concat_state = b"".join(self.state)

        print(concat_state)

        print("Key found:", concat_state[16:48].decode())

    def quarter_round(self, a, b, c, d):
        a = (a + b) & 0xFFFFFFFF
        d ^= a
        d = d & 0xFFFFFFFF
        d = leftRotate(d,16)	

        c = (c + d) & 0xFFFFFFFF 
        b ^= c
        b = b & 0xFFFFFFFF
        b = leftRotate(b,12)	

        a = (a + b) & 0xFFFFFFFF
        d ^= a
        d = d & 0xFFFFFFFF
        d = leftRotate(d, 8)	

        c = (c + d) & 0xFFFFFFFF
        b ^= c
        b = b & 0xFFFFFFFF
        b = leftRotate(b, 7)

        return a, b, c, d

    def quarter_round_reversed(self, a, b, c, d):

        b = rightRotate(b, 7)
        b = b & 0xFFFFFFFF
        b ^= c
        c = (c - d) & 0xFFFFFFFF

        d = rightRotate(d, 8)
        d = d & 0xFFFFFFFF
        d ^= a
        a = (a - b) & 0xFFFFFFFF

        b = rightRotate(b, 12)
        b = b & 0xFFFFFFFF
        b ^= c
        c = (c - d) & 0xFFFFFFFF

        d = rightRotate(d, 16)
        d = d & 0xFFFFFFFF
        d ^= a
        a = (a - b) & 0xFFFFFFFF


        return a, b, c, d

    def chacha_block(self):
        x = [int.from_bytes(data, "little") for data in self.state]

        # QR(x[0], x[4], x[ 8], x[12]); // column 0
		# QR(x[1], x[5], x[ 9], x[13]); // column 1
		# QR(x[2], x[6], x[10], x[14]); // column 2
		# QR(x[3], x[7], x[11], x[15]); // column 3
		# // Even round
		# QR(x[0], x[5], x[10], x[15]); // diagonal 1 (main diagonal)
		# QR(x[1], x[6], x[11], x[12]); // diagonal 2
		# QR(x[2], x[7], x[ 8], x[13]); // diagonal 3
		# QR(x[3], x[4], x[ 9], x[14]); // diagonal 4

        # Odd round
        x[0], x[4], x[8], x[12] = self.quarter_round(x[0], x[4], x[8], x[12])
        x[1], x[5], x[9], x[13] = self.quarter_round(x[1], x[5], x[9], x[13])
        x[2], x[6], x[10], x[14] = self.quarter_round(x[2], x[6], x[10], x[14])
        x[3], x[7], x[11], x[15] = self.quarter_round(x[3], x[7], x[11], x[15])
        # Even round
        x[0], x[5], x[10], x[15] = self.quarter_round(x[0], x[5], x[10], x[15])
        x[1], x[6], x[11], x[12] = self.quarter_round(x[1], x[6], x[11], x[12])
        x[2], x[7], x[8], x[13] = self.quarter_round(x[2], x[7], x[8], x[13])
        x[3], x[4], x[9], x[14] = self.quarter_round(x[3], x[4], x[9], x[14])

        self.state = [(data).to_bytes(4, byteorder="little") for data in x]

    def chacha_block_reversed(self):
        x = [int.from_bytes(data, "little") for data in self.state]

        x[3], x[4], x[9], x[14] = self.quarter_round_reversed(x[3], x[4], x[9], x[14])
        x[2], x[7], x[8], x[13] = self.quarter_round_reversed(x[2], x[7], x[8], x[13])
        x[1], x[6], x[11], x[12] = self.quarter_round_reversed(x[1], x[6], x[11], x[12])
        x[0], x[5], x[10], x[15] = self.quarter_round_reversed(x[0], x[5], x[10], x[15])

        x[3], x[7], x[11], x[15] = self.quarter_round_reversed(x[3], x[7], x[11], x[15])
        x[2], x[6], x[10], x[14] = self.quarter_round_reversed(x[2], x[6], x[10], x[14])
        x[1], x[5], x[9], x[13] = self.quarter_round_reversed(x[1], x[5], x[9], x[13])
        x[0], x[4], x[8], x[12] = self.quarter_round_reversed(x[0], x[4], x[8], x[12])
        # Odd round
        # Even round

        self.state = [(data).to_bytes(4, byteorder="little") for data in x]


nonce = [54, 76, 236, 31, 127, 98, 221, 135, 51, 23, 58, 100]
#chacha20 = ChaCha20(flag.encode(), nonce)
chacha20 = ChaCha20(nonce)
chacha20.get_key(
    b"To the left, Take it back now, y'all, One hop this time, Right foot, let's stomp"[:64], 
    bytes.fromhex("79312bcfe08ae6efb6a7bde2e864704a521686a576361a2c7e44a9948695776ede063ed1f6ae79fb83e939089b92118f95880517700d8d2cb6e0603e8c343d0a60c095956db3e9cf1be77464bf1918a1"[:128])
    )
#print("The text has now been cha cha slid:", chacha20.encrypt().hex())
