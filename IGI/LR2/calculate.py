#!/usr/bin/env python3
import os
import sys

sys.path.append('/app/geometric_lib')

try:
    import circle
    import square
    print("Библиотека geometric_lib успешно загружена")
except ImportError as e:
    print(f"Ошибка загрузки библиотеки: {e}")
    sys.exit(1)

def main():
    print("=" * 50)
    print("     ГЕОМЕТРИЧЕСКИЙ КАЛЬКУЛЯТОР")
    print("=" * 50)ы
    
    radius = float(os.getenv('RADIUS', 5))
    side = float(os.getenv('SIDE', 4))
    
    print(f"\nИсходные данные:")
    print(f"  Радиус круга: {radius}")
    print(f"  Сторона квадрата: {side}")
    
    print(f"\n КРУГ:")
    print(f"  Площадь: {circle.area(radius):.2f}")
    print(f"  Периметр (длина окружности): {circle.perimeter(radius):.2f}")
    
    print(f"\n КВАДРАТ:")
    print(f"  Площадь: {square.area(side):.2f}")
    print(f"  Периметр: {square.perimeter(side):.2f}")
    
    print("\n" + "=" * 50)
    print("        ВЫЧИСЛЕНИЯ ЗАВЕРШЕНЫ")
    print("=" * 50)

if __name__ == "__main__":
    main()