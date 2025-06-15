import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import os

duration = 5  # секунды записи
sample_rate = 44100

recognizer = sr.Recognizer()
translator = Translator()
score = 0
mistakes = 0
max_mistakes = 3
highscore_file = "highscore.txt"

words_by_level_ru = {
    "super_easy": ["я", "ты", "он", "кот", "дом", "мама", "мяч", "да", "нет", "нос"],
    "easy": ["рыба", "еда", "чай", "зуб", "нога"],
    "medium": ["машина", "учитель", "здание", "дорога", "поезд"],
    "hard": ["воображение", "предложение", "исследование", "впечатление", "объяснение"],
    "very_hard": ["непредсказуемость", "самореализация", "ответственность", "многообразие", "противоречивость"],
    "hardcore": [
        "гиперсензитивность", "деидеологизация", "интертекстуальность",
        "метафизичность", "антиконституционность", "рефлексивность",
        "инфраструктуризация", "контргегемоничность", "дихотомичность", "метафоризация"
    ]
}

words_by_level_en = {
    "super_easy": ["cat", "dog", "sun", "yes", "no", "hat", "car", "man", "mom", "pen"],
    "easy": ["apple", "fish", "tea", "leg", "tooth"],
    "medium": ["teacher", "building", "train", "road", "window"],
    "hard": ["imagination", "proposal", "research", "expression", "explanation"],
    "very_hard": ["unpredictability", "selfrealization", "responsibility", "diversity", "controversy"],
    "hardcore": [
        "hypersensitivity", "deideologization", "intertextuality",
        "metaphysicality", "unconstitutionality", "reflexivity",
        "infrastructurization", "counterhegemony", "dichotomy", "metaphorization"
    ]
}

words_by_level_de = {
    "super_easy": ["ich", "du", "er", "katze", "haus", "mama", "ball", "ja", "nein", "nase"],
    "easy": ["fisch", "essen", "tee", "zahn", "bein"],
    "medium": ["auto", "lehrer", "gebäude", "straße", "zug"],
    "hard": ["vorstellungskraft", "satz", "forschung", "eindruck", "erklärung"],
    "very_hard": ["unvorhersehbarkeit", "selbstverwirklichung", "verantwortung", "vielfalt", "widersprüchlichkeit"],
    "hardcore": [
        "hypersensitivität", "deideologisierung", "intertextualität",
        "metaphysischkeit", "verfassungswidrigkeit", "reflexivität",
        "infrastrukturierung", "konterhegemonie", "dichotomie", "metaphorisierung"
    ]
}

def load_highscore():
    if os.path.exists(highscore_file):
        with open(highscore_file, "r") as f:
            return int(f.read().strip())
    return 0

def save_highscore(new_score):
    with open(highscore_file, "w") as f:
        f.write(str(new_score))

print("""
  _____                                                         __          __           _ 
 |  __ \                                                 /\     \ \        / /          | |
 | |__) | __ ___  _ __   ___  _   _ _ __   ___ ___      /  \     \ \  /\  / /__  _ __ __| |
 |  ___/ '__/ _ \| '_ \ / _ \| | | | '_ \ / __/ _ \    / /\ \     \ \/  \/ / _ \| '__/ _` |
 | |   | | | (_) | | | | (_) | |_| | | | | (_|  __/   / ____ \     \  /\  / (_) | | | (_| |
 |_|   |_|  \___/|_| |_|\___/ \__,_|_| |_|\___\___|  /_/    \_\     \/  \/ \___/|_|  \__,_|
                                                                                           
                                                                                           """)
print("🎮 Добро пожаловать в игру 'Произнеси слово'!")

# Выбор языка
while True:
    lang_input = input("\nВыбери язык (ru/en/de): ").strip().lower()
    if lang_input == "ru":
        language_code = "ru-RU"
        words_by_level = words_by_level_ru
        translate_to = "en"
        print("✅ Язык: Русский")
        break
    elif lang_input == "en":
        language_code = "en-US"
        words_by_level = words_by_level_en
        translate_to = "ru"
        print("✅ Language: English")
        break
    elif lang_input == "de":
        language_code = "de-DE"
        words_by_level = words_by_level_de
        translate_to = "ru"
        print("✅ Sprache: Deutsch")
        break
    else:
        print("❌ Неверный ввод. Введите 'ru', 'en' или 'de'.")

print("\nВыбери режим:")
print("1. 🔘 Случайный уровень")
print("2. 👤 Выбор вручную")

while True:
    mode_input = input("Введите 1 или 2: ")
    if mode_input == "1":
        manual_mode = False
        print("✅ Режим: Случайный уровень")
        break
    elif mode_input == "2":
        manual_mode = True
        print("✅ Режим: Ручной выбор уровня")
        break
    else:
        print("❌ Неверный выбор. Попробуйте снова.")

if manual_mode:
    print("\nВыбери уровень сложности:")
    for i, level in enumerate(words_by_level.keys(), 1):
        print(f"{i}. {level}")

    while True:
        try:
            choice = int(input("Введите номер уровня (1-6): "))
            selected_level = list(words_by_level.keys())[choice - 1]
            break
        except (ValueError, IndexError):
            print("❌ Неверный ввод. Попробуйте снова.")
    print(f"✅ Уровень: {selected_level}")

highscore = load_highscore()
print(f"🏆 Рекорд: {highscore}")

while mistakes < max_mistakes:
    level = selected_level if manual_mode else random.choice(list(words_by_level.keys()))
    word = random.choice(words_by_level[level])
    print(f"\n🎯 Уровень: {level}")
    print(f"🧠 Произнеси слово: {word}")

    print("🎙 Говори...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write("output.wav", sample_rate, recording)

    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        recognized = recognizer.recognize_google(audio, language=language_code).lower()
        print(f"🗣 Ты сказал: {recognized}")

        if recognized == word.lower():
            print("✅ Верно!")
            score += 1
        else:
            print("❌ Неверно.")
            mistakes += 1

        translation = translator.translate(recognized, dest=translate_to)
        print(f"🌐 Перевод: {translation.text}")

    except sr.UnknownValueError:
        print("⚠️ Не удалось распознать речь.")
        mistakes += 1
    except sr.RequestError as e:
        print(f"⚠️ Ошибка сервиса распознавания речи: {e}")
        break

    print(f"🎯 Очки: {score} | ❌ Ошибки: {mistakes}/{max_mistakes}")

if score > highscore:
    print(f"\n🎉 Новый рекорд! {score} очков!")
    save_highscore(score)
else:
    print(f"\n📊 Твой счёт: {score}. Рекорд: {highscore}")

print("🛑 Игра окончена.")
print("""
                                                                     .-'''-.                                                           ___      ___      ___   
                                                                    '   _    \                                                      .'/   \  .'/   \  .'/   \  
                    __  __   ___         __.....__                /   /` '.   \.----.     .----.   __.....__                       / /     \/ /     \/ /     \ 
  .--./)           |  |/  `.'   `.   .-''         '.             .   |     \  ' \    \   /    /.-''         '.                     | |     || |     || |     | 
 /.''\\            |   .-.  .-.   ' /     .-''"'-.  `.           |   '      |  ' '   '. /'   //     .-''"'-.  `. .-,.--.           | |     || |     || |     | 
| |  | |      __   |  |  |  |  |  |/     /________\   \          \    \     / /  |    |'    //     /________\   \|  .-. |          |/`.   .'|/`.   .'|/`.   .' 
 \`-' /    .:--.'. |  |  |  |  |  ||                  |           `.   ` ..' /   |    ||    ||                  || |  | |           `.|   |  `.|   |  `.|   |  
 /("'`    / |   \ ||  |  |  |  |  |\    .-------------'              '-...-'`    '.   `'   .'\    .-------------'| |  | |            ||___|   ||___|   ||___|  
 \ '---.  `" __ | ||  |  |  |  |  | \    '-.____...---.                           \        /  \    '-.____...---.| |  '-             |/___/   |/___/   |/___/  
  /'""'.\  .'.''| ||__|  |__|  |__|  `.             .'                             \      /    `.             .' | |                 .'.--.   .'.--.   .'.--.  
 ||     ||/ /   | |_                   `''-...... -'                                '----'       `''-...... -'   | |                | |    | | |    | | |    | 
 \'. __// \ \._,\ '/                                                                                             |_|                \_\    / \_\    / \_\    / 
  `'---'   `--'  `"                                                                                                                  `''--'   `''--'   `''--'  
""")
print("Спасибо за игру! До новых встреч!")