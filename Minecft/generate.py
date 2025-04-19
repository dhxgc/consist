from pymclevel import MCInfdevOldLevel, MCEditLevel
import os

def place_pink_wool(world_folder, coords_list):
    """
    Ставит розовую шерсть (35:6) в указанные координаты.
    :param world_folder: Путь к папке мира (не zip, а распакованная папка)
    :param coords_list: Список кортежей [(x1, y1, z1), (x2, y2, z2), ...]
    """
    # Проверяем путь
    if not os.path.exists(world_folder):
        raise FileNotFoundError("Папка мира не найдена!")
    
    # Загружаем мир
    world = MCInfdevOldLevel(world_folder)  # Для 1.12.2
    
    # ID блока (35 = шерсть, 6 = розовая)
    PINK_WOOL = (35, 6)
    
    # Проходим по всем координатам
    for x, y, z in coords_list:
        # Проверяем, что координаты в допустимых пределах
        if y < 0 or y > 255:
            print(f"Координата Y={y} вне допустимого диапазона (0-255)! Пропускаем.")
            continue
        
        # Ставим блок
        world.setBlockAt(x, y, z, PINK_WOOL[0])  # ID блока (35 = шерсть)
        world.setBlockDataAt(x, y, z, PINK_WOOL[1])  # DataValue (6 = розовая)
    
    # Сохраняем изменения!
    world.saveInPlace()
    print(f"Изменения сохранены. Всего блоков изменено: {len(coords_list)}")

# Пример использования
if __name__ == "__main__":
    # Распакованный мир (не ZIP!)
    WORLD_PATH = "/путь/к/папке/мира/"
    
    # Координаты, куда поставить розовую шерсть [(x, y, z), ...]
    COORDS = [
        (100, 64, 200),
        (150, 70, -300),
        (0, 80, 0)
    ]
    
    place_pink_wool(WORLD_PATH, COORDS)
