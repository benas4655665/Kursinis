Tikslas
Sistema skirta stebėti treniruotes bėgikams, dviratininkams ir kultūristams, įrašant pratimus, treniruočių datas, atstumus ir sudegintas kalorijas. Duomenys saugomi JSON faile.

Klasės aprašymai

DataHandler: Atsakingas už duomenų įrašymą į failą ir nuskaitymą.
	save_to_file(filename, data): Išsaugo duomenis į failą.
	load_from_file(filename): Nuskaitymo duomenis iš failo.

Exercise: Apibrėžia pratimą su pavadinimu, serijomis, pakartojimais ir svoriu. Naudoja encapsulation.
	to_dict(): Konvertuoja pratimą į žodyną.
	from_dict(): Sukuria pratimą iš žodyno.

Workout: Apibrėžia treniruotę su data, atstumu ir pratimais. Naudoja kompoziciją.
	add_exercise(exercise): Prideda pratimą.
	display(): Rodo treniruotės informaciją ir kalorijas (naudojant dekoratorių).

Athlete (abstract): Abstrakti klasė, paveldima bėgikams, dviratininkams ir kultūristams. Valdo treniruotes.
	add_workout(workout): Prideda treniruotę.
	display_workouts(): Parodo visų treniruočių istoriją.

Runner, Biker, Bodybuilder: Paveldėtos klasės, skirtos atitinkamiems sportininkams. Rodoma treniruočių istorija pagal sporto šaką.

Svarbūs metodai
calorie_burned_decorator: Apskaičiuoja sudegintas kalorijas pagal aktyvumo tipą:
	Bėgimui: calories = distance * 0.063
	Dviračiui: calories = distance * 0.049

Naudotojo sąsaja
	Vartotojas įveda savo vardą, pasirenka treniruotės tipą, įveda pratimus ir įveiktą atstumą. Treniruotės išsaugomos ir gali būti peržiūrimos vėliau.

Pavyzdys
	Vartotojas įveda datą ir atstumą (bėgimui) arba pratimus (salės treniruotėms).
	Treniruotės išsaugomos į JSON failą ir gali būti vėl peržiūrimos.

Išvados
Sistema leidžia stebėti įvairias treniruotes, įrašyti pratimus ir kalorijas. Kompozicija ir paveldėjimas užtikrina lankstumą ir paprastą pritaikymą.

Ateities galimybės
	Pridėti kitas sporto šakas.
	Integracija su sveikatingumo programėlėmis.
	Išplėstinė treniruočių analizė ir progresas.
