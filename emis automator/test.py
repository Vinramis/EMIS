import os
from automator import find_files

TOPICS_FOLDER = "test"

# print("Разделение файлов тем и домашних заданий...")
# topic_keywords = ["кл", "лек", "урок"]
# homework_keywords = ["дз", "дом", "", "", "", "", ""]

# all_files = os.listdir(TOPICS_FOLDER)
# topic_files = find_files(TOPICS_FOLDER, True, topic_keywords)
# all_files = [f for f in all_files if f not in topic_files]
# homework_files = find_files(TOPICS_FOLDER, True, homework_keywords)
# all_files = [f for f in all_files if f not in homework_files]
# if len(all_files) > 0:
#     print(f"Остались нераспределенные файлы в папке '{TOPICS_FOLDER}': {all_files}")
#     print("(?) Просто добавьте ключевые слова в ЛЮБОМ РЕГИСТРЕ в имена оставшихся файлов и перезапустите скрипт.")
#     print(f"\n(?) --- Ключевые слова ---")
#     print(f"(?) Для классных работа: {topic_keywords}")
#     print(f"(?) Для домашних заданий: {homework_keywords}\n")
#     print(f"(?) Если в названиях уже есть ключевые слова, ")
    
#     exit(0)

# ALL_FOLDER = TOPICS_FOLDER
# TOPICS_FOLDER = os.path.join(os.path.dirname(ALL_FOLDER), "КЛ")
# HOMEWORK_FOLDER = os.path.join(os.path.dirname(ALL_FOLDER), "ДЗ")
# os.makedirs(TOPICS_FOLDER, exist_ok=True)
# os.makedirs(HOMEWORK_FOLDER, exist_ok=True)
# # Move files to respective folders
# for file in topic_files:
#     os.rename(os.path.join(ALL_FOLDER, file), os.path.join(TOPICS_FOLDER, file))
# for file in homework_files:
#     os.rename(os.path.join(ALL_FOLDER, file), os.path.join(HOMEWORK_FOLDER, file))
# if (os.listdir(ALL_FOLDER) == []):
#     os.rmdir(ALL_FOLDER)  # Remove the original folder if empty
#     print(f"Файлы успешно разделены на папки '{TOPICS_FOLDER}' и '{HOMEWORK_FOLDER}'.")
# else:
#     print(f"[КРИТИЧЕСКАЯ ОШИБКА] Не удалось полностью разделить файлы. Проверьте папку '{ALL_FOLDER}'.")
#     print("(?) Просто распределите оставшиеся файлы вручную и перезапустите скрипт.")
#     exit(0)

