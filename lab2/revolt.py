def reverse_string(text: str) -> str:
    return text[::-1]

def main():
    while True:
        text = input("\nВведите текст для переворота: ")
        
        if not text:
            print("Вы ввели пустую строку! Попробуйте снова.")
            continue
            
        reversed_text = reverse_string(text)
        
        print(f"\nИсходный текст: '{text}'")
        print(f"Перевернутый текст: '{reversed_text}'")
        
        continue_choice = input("\nХотите перевернуть другую строку? (да/нет): ").lower()
        if continue_choice not in ['да', 'д', 'yes', 'y']:
            print("До свидания!")
            break

if __name__ == "__main__":
    main()
