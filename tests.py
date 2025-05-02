import unittest
import json
import os
from main import Exercise, Workout, DataHandler, Runner

class TestExercise(unittest.TestCase):
    """Testai Exercise klasei"""
    
    def test_exercise_creation(self):
        ex = Exercise("Pratai", 3, 10, 50)
        self.assertEqual(ex.name, "Pratai")
        self.assertEqual(ex.sets, 3)
        self.assertEqual(ex.reps, 10)
        self.assertEqual(ex.weight, 50)
        
    def test_exercise_no_weight(self):
        ex = Exercise("Prisitraukimai", 5, 15)
        self.assertEqual(ex.weight, 0)

class TestWorkout(unittest.TestCase):
    """Testai Workout klasei"""
    
    def setUp(self):
        self.workout = Workout("2025-05-01")
        self.exercise = Exercise("Pritūpimai", 4, 12, 20)
        
    def test_add_exercise(self):
        self.workout.add_exercise(self.exercise)
        self.assertEqual(len(self.workout.exercises), 1)
        
    def test_empty_workout(self):
        self.assertEqual(len(self.workout.exercises), 0)

class TestDataHandler(unittest.TestCase):
    """Testai DataHandler klasei"""
    
    def setUp(self):
        self.test_file = "test_data.json"
        self.test_data = {"test": "data"}
        
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
            
    def test_save_and_load(self):
        DataHandler.save_to_file(self.test_file, self.test_data)
        loaded_data = DataHandler.load_from_file(self.test_file)
        self.assertEqual(loaded_data, self.test_data)
        
    def test_load_nonexistent_file(self):
        data = DataHandler.load_from_file("nonexistent.json")
        self.assertEqual(data, {})

class TestRunner(unittest.TestCase):
    """Testai Runner klasei"""
    
    def setUp(self):
        self.runner = Runner("Testuotojas")
        self.workout = Workout("2025-05-01", 5.0)  # 5 km bėgimas
        
    def test_add_workout(self):
        self.runner.add_workout(self.workout)
        self.assertIn("2025-05-01", self.runner._workouts)

if __name__ == "__main__":
    unittest.main()