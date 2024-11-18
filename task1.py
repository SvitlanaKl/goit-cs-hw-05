import asyncio
import os
import shutil
from pathlib import Path
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def read_folder(source_folder: Path, output_folder: Path):
    """
    Асинхронно читає всі файли у вихідній папці та її підпапках.
    """
    try:
        tasks = []
        entries = await asyncio.to_thread(lambda: list(source_folder.iterdir()))  # Отримуємо список файлів синхронно
        for entry in entries:
            if entry.is_dir():
                tasks.append(read_folder(entry, output_folder))  # Рекурсія для папок
            elif entry.is_file():
                tasks.append(copy_file(entry, output_folder))  # Копіювання файлів
        await asyncio.gather(*tasks)  # Виконуємо всі завдання
    except Exception as e:
        logger.error(f"Error reading folder {source_folder}: {e}")

async def copy_file(file_path: Path, output_folder: Path):
    """
    Асинхронно копіює файл у відповідну підпапку в залежності від розширення.
    """
    try:
        file_extension = file_path.suffix[1:] or "no_extension"
        target_folder = output_folder / file_extension
        await asyncio.to_thread(lambda: target_folder.mkdir(parents=True, exist_ok=True))
        target_path = target_folder / file_path.name
        await asyncio.to_thread(shutil.copy2, file_path, target_path)
        logger.info(f"Copied {file_path} to {target_path}")
    except Exception as e:
        logger.error(f"Error copying file {file_path}: {e}")

def main():
    # Шлях до папки для сортування
    source_folder = Path(r"C:\Users\WORK\Desktop\GoIT\Repository\Computer_Systems\goit-cs-hw-05\Files_to_sort").resolve()
    output_folder = source_folder.parent / "Sorted_Files"

    if not source_folder.is_dir():
        logger.error(f"Source folder {source_folder} does not exist or is not a directory.")
        return

    try:
        asyncio.run(read_folder(source_folder, output_folder))
    except Exception as e:
        logger.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()
