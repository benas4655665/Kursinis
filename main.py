import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List


class DataHandler:
    """Handles file operations using composition."""

    @staticmethod
    def save_to_file(filename: str, data: Dict) -> None:
        """Save data to JSON file."""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_from_file(filename: str) -> Dict:
        """Load data from JSON file."""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}


def calorie_burned_decorator(func):
    """Decorator to calculate calories burned."""

    def wrapper(self, *args, **kwargs):
        activity_type = kwargs.get('activity_type', '')
        distance = self.distance if hasattr(self, 'distance') and self.distance else 0

        result = func(self, *args, **kwargs)

        if activity_type == "running":
            calories_burned = distance * 0.063
            print(f"Sudeginta kalorijų: {calories_burned:.3f} kcal")
        elif activity_type == "biking":
            calories_burned = distance * 0.049
            print(f"Sudeginta kalorijų: {calories_burned:.3f} kcal")

        return result
    return wrapper


class Exercise:
    """Represents a single exercise with encapsulation."""

    def __init__(self, name: str, sets: int, reps: int, weight: float = None):
        self._name = name
        self._sets = sets
        self._reps = reps
        self._weight = weight

    @property
    def name(self) -> str:
        """Get exercise name."""
        return self._name

    @property
    def sets(self) -> int:
        """Get number of sets."""
        return self._sets

    @property
    def reps(self) -> int:
        """Get number of repetitions."""
        return self._reps

    @property
    def weight(self) -> float:
        """Get weight used."""
        return self._weight if self._weight is not None else 0

    def to_dict(self) -> Dict:
        """Convert exercise to dictionary."""
        return {
            'name': self._name,
            'sets': self._sets,
            'reps': self._reps,
            'weight': self._weight
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Exercise':
        """Create exercise from dictionary."""
        return cls(data['name'], data['sets'], data['reps'], data.get('weight'))


class Workout:
    """Represents a workout session using composition."""

    def __init__(self, date: str, distance: float = None):
        self._date = date
        self._exercises: List[Exercise] = []
        self._distance = distance

    @property
    def date(self) -> str:
        """Get workout date."""
        return self._date

    @property
    def distance(self) -> float:
        """Get distance covered."""
        return self._distance if self._distance is not None else 0

    @property
    def exercises(self) -> List[Exercise]:
        """Get list of exercises."""
        return self._exercises

    def add_exercise(self, exercise: Exercise) -> None:
        """Add exercise to workout."""
        self._exercises.append(exercise)

    def to_dict(self) -> Dict:
        """Convert workout to dictionary."""
        return {
            'date': self._date,
            'distance': self._distance,
            'exercises': [ex.to_dict() for ex in self._exercises]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Workout':
        """Create workout from dictionary."""
        workout = cls(data['date'], data.get('distance'))
        for ex_data in data.get('exercises', []):
            workout.add_exercise(Exercise.from_dict(ex_data))
        return workout

    def display_gym(self) -> None:
        """Display gym exercises."""
        for ex in self._exercises:
            print(f"🏋️ {ex.name}: {ex.sets}x{ex.reps} @ {ex.weight}kg")

    @calorie_burned_decorator
    def display(self, activity_type: str = "") -> None:
        """Display workout information."""
        print(f"\n📅 Treniruotė atlikta: {self._date}")
        if self._distance is not None:
            print(f"📏 Įveikta: {self._distance} km")
        if self._exercises:
            self.display_gym()


class Athlete(ABC):
    """Abstract base class representing an athlete."""

    def __init__(self, name: str):
        self._name = name
        self._workouts: Dict[str, List[Workout]] = {}
        self._filename = f"{name.lower()}_workouts.json"
        self.load_workouts()

    @property
    def name(self) -> str:
        """Get athlete name."""
        return self._name

    def add_workout(self, workout: Workout) -> None:
        """Add workout to athlete's history."""
        if workout.date not in self._workouts:
            self._workouts[workout.date] = []
        self._workouts[workout.date].append(workout)
        self._save_workouts()

    def _save_workouts(self) -> None:
        """Save workouts to file."""
        data = {
            'athlete_type': self.__class__.__name__,
            'workouts': {
                date: [w.to_dict() for w in workouts]
                for date, workouts in self._workouts.items()
            }
        }
        DataHandler.save_to_file(self._filename, data)

    def load_workouts(self) -> None:
        """Load workouts from file."""
        data = DataHandler.load_from_file(self._filename)
        if data:
            self._workouts = {
                date: [Workout.from_dict(w) for w in workouts]
                for date, workouts in data.get('workouts', {}).items()
            }

    def display_all_workouts(self) -> None:
        """Display all workouts."""
        activity_type = self.get_workout_type()
        for date, workouts in self._workouts.items():
            for workout in workouts:
                workout.display(activity_type=activity_type)

    @abstractmethod
    def display_workouts(self) -> None:
        """Abstract method to display workouts."""
        pass

    def get_workout_type(self) -> str:
        """Get workout type based on athlete class."""
        if isinstance(self, Runner):
            return "running"
        elif isinstance(self, Biker):
            return "biking"
        return "gym"


class Runner(Athlete):
    """Concrete athlete class for runners."""

    def display_workouts(self) -> None:
        """Display runner's workouts."""
        print(f"\n🏃 Bėgiko {self._name} treniruočių istorija:")
        self.display_all_workouts()


class Biker(Athlete):
    """Concrete athlete class for bikers."""

    def display_workouts(self) -> None:
        """Display biker's workouts."""
        print(f"\n🚴 Dviratininko {self._name} treniruočių istorija:")
        self.display_all_workouts()


class Bodybuilder(Athlete):
    """Concrete athlete class for bodybuilders."""

    def display_workouts(self) -> None:
        """Display bodybuilder's workouts."""
        print(f"\n🏋️ Kultūristo {self._name} treniruočių istorija:")
        self.display_all_workouts()


def create_exercise() -> Exercise:
    """Create a new exercise from user input."""
    name = input("Įveskite pratimo pavadinimą: ")
    sets = int(input("Kiek serijų (sets)?: "))
    reps = int(input("Kiek pakartojimų (reps)?: "))
    weight_input = input("Kiek svorio (kg)? (palikite tuščią jei kūno svoris): ")
    weight = float(weight_input) if weight_input.strip() else None
    return Exercise(name, sets, reps, weight)


def create_workout() -> tuple[Workout, str]:
    """Create a new workout from user input."""
    while True:
        date = input("Įveskite treniruotės datą (pvz. 2025-05-01): ")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Netinkamas datos formatas. Bandykite dar kartą.")

    type_choice = input("Ar ši treniruotė yra bėgimo (r), dviračio (b) ar salės (g)? ").lower()
    while type_choice not in ['r', 'b', 'g']:
        print("Netinkamas pasirinkimas. Įveskite 'r', 'b' arba 'g'.")
        type_choice = input("Ar ši treniruotė yra bėgimo (r), dviračio (b) arba salės (g)? ").lower()

    workout = Workout(date)

    if type_choice in ['r', 'b']:
        while True:
            try:
                distance = float(input("Kiek km įveikėte?: "))
                workout._distance = distance
                break
            except ValueError:
                print("Netinkamas atstumas. Įveskite skaičių.")
    else:
        while True:
            workout.add_exercise(create_exercise())
            more = input("Pridėti dar vieną pratimą? (t/n): ").lower()
            if more != 't':
                break

    return workout, type_choice


def main():
    """Main program function."""
    print("🏋️‍♂️ Treniruotės sekimo programa")
    name = input("Įveskite savo vardą: ")

    athlete = None

    while True:
        workout, type_code = create_workout()

        if type_code == 'r':
            if not isinstance(athlete, Runner):
                athlete = Runner(name)
        elif type_code == 'b':
            if not isinstance(athlete, Biker):
                athlete = Biker(name)
        else:
            if not isinstance(athlete, Bodybuilder):
                athlete = Bodybuilder(name)

        athlete.add_workout(workout)

        more = input("\nPridėti dar vieną treniruotę? (t/n): ").lower()
        if more != 't':
            break

    athlete.display_workouts()
    input("\nPaspauskite Enter, kad išeitumėte...")


if __name__ == "__main__":
    main()
