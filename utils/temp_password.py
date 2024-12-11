import random
import string
def generate_temp_password(length=8):
        # Define character sets
        uppercase = string.ascii_uppercase  # A-Z
        lowercase = string.ascii_lowercase  # a-z
        digits = string.digits              # 0-9
        special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/~`"  

        password_chars = [
            random.choice(uppercase),
            random.choice(lowercase),
            random.choice(digits),
            random.choice(special_chars),
        ]
        
        # Fill the rest of the password with random characters from all sets
        all_chars = uppercase + lowercase + digits + special_chars
        password_chars += random.choices(all_chars, k=4)
        
        # Shuffle the characters to ensure randomness
        random.shuffle(password_chars)
        
        # Join them into a string
        temp_password = ''.join(password_chars)
        return temp_password