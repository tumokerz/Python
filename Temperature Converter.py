while True:
    print('1.°C->°F 2.°F ->°C 0.Выход')
    choice = input('Выберите 1 или 2: ')
    if choice == '1':
        c = float(input('Введите значение: '))
        f = (c*5/9)+32
        print(round(f,2),'°F')
    elif choice == '2':
        f = float(input('введите значение: '))
        c = (f-32)*5/9
        print(round(c,2),'°C')
    elif choice == '0':
        print('Выход из программы...')
        break
    else:
        print('Неверное значение! Введите 1 или 2')
