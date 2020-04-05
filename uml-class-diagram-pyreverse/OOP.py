class Dog:
    species: str = "mammal"

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def description(self) -> str:
        return f"{self.name} is {self.age} years old."

    def speak(self, sound: str) -> str:
        return f"{self.name} says {sound}."

    def birthday(self) -> None:
        self.age += 1
