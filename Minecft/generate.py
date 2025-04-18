import world

# Флаг для задания
flag = "m1N3ctf"

# Открываем мир (укажите правильный путь к вашему плоскому миру)
world = World("./MineCTF")

for char in flag:
    # Получаем ASCII-код символа
    code = ord(char)
    # Рассчитываем координаты так, чтобы x + y + z = code
    # Здесь y = 1, z = 0, поэтому x = code - 1
    x = code - 4
    y = 4
    z = 0
    # Устанавливаем блок бедрока
    world.set_block(x, y, z, "minecraft:bedrock")

# Сохраняем изменения
world.save()
