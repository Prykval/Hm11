from datetime import datetime, timedelta
from typing import Optional

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass

    def __str__(self):
        return str(self._value)


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def validate(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError('Phone should be 10 digits')


class Birthday(Field):
    @Field.value.setter
    def validate(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Invalid date format. Use YYYY-MM-DD')



class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value}"

    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        phone.validate(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone.value
        return None

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.validate(new_phone)
                phone.value = new_phone
                return
        raise ValueError(f"Phone {old_phone} not found")

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.now()
            next_birthday = datetime(today.year, *map(int, self.birthday.value.split('-')))
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, *map(int, self.birthday.value.split('-')))
            days_left = (next_birthday - today).days
            return days_left


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact {name} deleted"
        else:
            return f"Contact with name {name} not found"

    def iterator(self, batch_size=10):
        keys = list(self.data.keys())
        for i in range(0, len(keys), batch_size):
            yield [self.data[key] for key in keys[i:i + batch_size]]



