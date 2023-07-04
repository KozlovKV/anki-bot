from core.CRUD import card as CardCRUD

if __name__ == '__main__':
    CardCRUD.create(1, 'Hello, worm!', 'Привет, мир!')
    print(CardCRUD.readOne(1))
    CardCRUD.update(1, 18, 'Fixed', 'Починено')
    print(CardCRUD.readOne(1))
