from cryptography.fernet import Fernet


class Viecry:
    # key = ''
    cipher_suite = ""
    key_genarated = False

    def __init__(self, dir, host, user):
        self.dir = dir
        self.host = host
        self.user = user

        base_file_name = dir + "/" + host + "_" + user
        self.key_file_name = base_file_name + ".key"
        self.pwd_file_name = base_file_name + ".bin"

    def get_cipher_suite(self):
        return Fernet(self.load_key())

    def generate_key(self):
        # print('Gravar arquivo fr chave', self.key_file_name)
        with open(self.key_file_name, "wb") as file_object:
            file_object.write(Fernet.generate_key())
        self.key_genarated = True

    def load_key(self):
        # print('Carregar arquivo de chave', self.key_file_name)
        with open(self.key_file_name, "rb") as file_obj:
            for key in file_obj:
                return key

    def encrypt(self, pwd):
        if not self.key_genarated:
            self.generate_key()
        ciphered_text = self.get_cipher_suite().encrypt(bytes(pwd, "utf-8"))
        # print('Gravar senha criptografada no arquivo', self.pwd_file_name)
        with open(self.pwd_file_name, "wb") as pwd_file_object:
            pwd_file_object.write(ciphered_text)

    def decrypt(self):
        # print('Carregar senha criptografada do arquivo', self.pwd_file_name)
        with open(self.pwd_file_name, "rb") as pwd_file_object:
            for line in pwd_file_object:
                encrypted_pwd = line

        # print('Descriptografar senha')
        unciphered_text = self.get_cipher_suite().decrypt(encrypted_pwd)
        pwd = bytes(unciphered_text).decode("utf-8")  # convert to string
        return pwd


if __name__ == "__main__":
    cry = Viecry(".", "host", "user")
    cry.encrypt("My Passw0rd")
    pwd = cry.decrypt()
    #print("never print your password!", pwd)
