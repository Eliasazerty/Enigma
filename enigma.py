from json import load as json_load
from string import ascii_lowercase

class Enigma:
    def __init__(self, settings_file, alphabet):
        try:
            with open(settings_file) as file:
                data = json_load(file)
        except:
            print(f"Error while trying to read the setting file\nGiven file path: {settings_file}")
        # "qzertyuiopasdfghjklmwxcvbn": 'a'=1  ==> ciphered as a "q" (first position in this alphabet)
        # "zertyuiopasdfghjklmwxcvbnq": represent the rotor's alphabet at time+1

        self.alpha = [list("".join(data[data["R_used"][0]]).lower()), 1] # [alphabet, number printed on the top of the rotor]
        self.beta = [list("".join(data[data["R_used"][1]]).lower()), 1]
        self.gama = [list("".join(data[data["R_used"][2]]).lower()), 1]

        self.reflector = data[data["Rf_used"]].lower()

        temp_steckerbrett = data["Steckerbrett"] # shortcut
        self.steckerbrett = [temp_steckerbrett, {v:k for k,v in temp_steckerbrett.items()}]
        # self.steckerbrett -> [dictionary, inverted_dictionary]
        

        self.turn_beta = False
        self.turn_gama = False

        self.alphabet = alphabet
    
    def set_position(self, a,b,c):
        if a > 1:
            self.alpha[0] = self.alpha[0][a-1:]+self.alpha[0][:a-1]
        if b > 1:
            self.beta[0] = self.beta[0][b-1:]+self.beta[0][:b-1]
        if c > 1:
            self.gama[0] = self.gama[0][c-1:]+ self.gama[0][:c-1]
    
    def code(self, message):
        msg = ""
        for letter in message.lower():
            if not letter in self.alphabet:
                msg += letter
                continue

            letter = self.crypt_steckerbrett(letter)
            
            self.move_rotor(self.alpha)
            if self.alpha[1] > 26:
                self.alpha[1] = 1
                self.turn_beta = True
            
            alpha_letter1 = self.alpha[0][self.get_number(letter)]

            if self.turn_beta:
                self.turn_beta = False
                self.move_rotor(self.beta)
                if self.beta[1] > 26:
                    self.beta[1] = 1
                    self.turn_gama = True

            beta_letter1 = self.beta[0][self.get_number(alpha_letter1)]

            if self.turn_gama:
                self.turn_gama = False
                self.move_rotor(self.gama)
                if self.gama[1] > 26:
                    self.gama[1] = 1

            gama_letter1 = self.gama[0][self.get_number(beta_letter1)]

            reflector_letter = self.reflector[self.get_number(gama_letter1)]

            gama_letter2 = chr(self.gama[0].index(reflector_letter)+97)
            beta_letter2 = chr(self.beta[0].index(gama_letter2)+97)
            alpha_letter2 = chr(self.alpha[0].index(beta_letter2)+97)

            final_letter = self.crypt_steckerbrett(alpha_letter2)


            msg += final_letter
        return msg
    
    def get_number(self, letter):
        return ord(letter)-97
    
    def move_rotor(self, rotor):
        rotor[0] = rotor[0][1:]+rotor[0][:1]
        rotor[1] += 1
    
    def crypt_steckerbrett(self, letter):
        if letter in self.steckerbrett[0]:
                return self.steckerbrett[0][letter]
        elif letter in self.steckerbrett[1]:
            return self.steckerbrett[1][letter]
        return letter
        
machine = Enigma("settings.json", ascii_lowercase)
machine.set_position(1,1,1)
print(machine.code("This is a message"))