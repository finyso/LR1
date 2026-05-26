"""
Laboratory Work No. 4
Main module for testing all tasks with interactive menu.
Developer: Finsky Pavel
Date: 30.04.2026
"""
import sys

def run_task1():
    """Execute Task 1: Files, classes, serializers."""
    print("\n" + "=" * 50)
    print("Задание 1. Работа с файлами, классами, сериализаторами")
    print("Вариант 24: Данные о поступивших в вуз студентах")
    print("=" * 50)
    from lab4_var24.task1 import (
        save_to_csv, load_from_csv, save_to_pickle, load_from_pickle,
        analyze_data, find_student_by_surname, INITIAL_DATA
    )
    
    print("\n--- Работа с CSV ---")
    save_to_csv(INITIAL_DATA)
    students_csv = load_from_csv()
    analyze_data(students_csv)
    surname = input("\nВведите фамилию студента для поиска: ").strip()
    find_student_by_surname(students_csv, surname)
    
    print("\n--- Работа с Pickle ---")
    save_to_pickle(INITIAL_DATA)
    students_pkl = load_from_pickle()
    analyze_data(students_pkl)
    surname = input("\nВведите фамилию студента для поиска: ").strip()
    find_student_by_surname(students_pkl, surname)


def run_task2():
    """Execute Task 2: Regular expressions and text analysis."""
    print("\n" + "=" * 50)
    print("Задание 2. Регулярные выражения и анализ текста")
    print("Вариант 24: MAC-адрес, слова на строчную букву, общий анализ")
    print("=" * 50)
    from lab4_var24.task2 import TextAnalyzer
    
    print("\nВведите текст для анализа (для примера можно оставить пустым):")
    user_text = input("> ").strip()
    if not user_text:
        user_text = (
            "Hello World! How are you? I am fine. "
            "This is a test: all good. Let's meet at 5. "
            "My MAC is aE:dC:cA:56:76:54. Another one is 01:23:45:67:89:Az. "
            "Prices are in USD. ;-) is a smiley. So is :---[[. "
            "But ] is not. apple banana Apple cherry Date fig Grape."
        )
        print(f"Использован текст по умолчанию:\n{user_text}\n")
    
    analyzer = TextAnalyzer(user_text)
    analyzer.run_all()


def run_task3():
    """Execute Task 3: Series, statistics, and visualization."""
    print("\n" + "=" * 50)
    print("Задание 3. Ряды, статистика и визуализация")
    print("Вариант 24: ln(1-x)")
    print("=" * 50)
    from lab4_var24.task3 import LnSeries, plot_series_vs_math
    
    try:
        x = float(input("\nВведите значение x (|x| < 1, например 0.5): ").strip())
        n_terms = int(input("Введите количество членов ряда (например 10): ").strip())
    except ValueError:
        print("Некорректный ввод. Использованы значения по умолчанию: x=0.5, n=10")
        x = 0.5
        n_terms = 10
    
    try:
        series = LnSeries(x, n_terms)
        results = series.compute_series()
        stats = series.statistics()
        
        print(f"\nРезультаты для x = {x}")
        print(f"Math ln(1-x) = {series.math_value():.10f}")
        print(f"Series approximation = {results[-1]['partial_sum']:.10f}")
        print(f"Absolute error = {abs(series.math_value() - results[-1]['partial_sum']):.2e}")
        print(f"\n--- Статистика членов ряда ---")
        print(f"Среднее арифметическое: {stats['mean']:.6f}")
        print(f"Медиана: {stats['median']:.6f}")
        print(f"Дисперсия: {stats['variance']:.6f}")
        print(f"СКО: {stats['std_dev']:.6f}")
        
        plot_series_vs_math(series)
    except ValueError as e:
        print(f"Ошибка: {e}")


def run_task4():
    """Execute Task 4: Geometric figures with inheritance."""
    print("\n" + "=" * 50)
    print("Задание 4. Геометрические фигуры")
    print("Вариант 24: Равнобедренная трапеция по основанию a,")
    print("           боковой стороне b и углу Y между ними")
    print("=" * 50)
    from lab4_var24.task4 import IsoscelesTrapezoid, draw_trapezoid
    
    while True:
        try:
            print("\nВведите параметры равнобедренной трапеции:")
            a = float(input("  Основание a (нижнее, > 0): ").strip())
            b = float(input("  Боковая сторона b (> 0): ").strip())
            y = float(input("  Угол Y между основанием a и стороной b (в градусах, 0 < Y < 90): ").strip())
            col = input("  Цвет трапеции на английском (например, blue): ").strip()
            if not col:
                col = "blue"
            txt = input("  Текст для подписи фигуры: ").strip()
            if not txt:
                txt = f"Trapezoid a={a}, b={b}, Y={y}°"
            
            trapezoid = IsoscelesTrapezoid(a, b, y, col)
            print(f"\n{trapezoid}")
            draw_trapezoid(trapezoid, txt)
            break
            
        except ValueError as e:
            print(f"\nОшибка ввода: {e}")
            print("Пожалуйста, проверьте введённые значения и попробуйте снова.\n")
            retry = input("Повторить ввод? (y/n, по умолчанию y): ").strip().lower()
            if retry == 'n':
                print("Выполнение задания 4 прервано.")
                break
        except Exception as e:
            print(f"\nНепредвиденная ошибка: {e}")
            break


def run_task5():
    """Execute Task 5: NumPy matrix operations."""
    print("\n" + "=" * 50)
    print("Задание 5. NumPy операции с матрицами")
    print("Вариант 24: Замена наибольших элементов, корреляция")
    print("=" * 50)
    
    try:
        import numpy as np
    except ImportError:
        print("Ошибка: библиотека numpy не установлена.")
        print("Установите ее командой: pip install numpy")
        return
    
    from lab4_var24.task5 import swap_max_elements, correlation_first_last
    
    try:
        rows = int(input("\nВведите количество строк матрицы (по умолчанию 5): ").strip() or "5")
        cols = int(input("Введите количество столбцов матрицы (по умолчанию 4): ").strip() or "4")
    except ValueError:
        print("Некорректный ввод. Использованы значения по умолчанию: 5x4")
        rows, cols = 5, 4
    
    np.random.seed(42)
    A = np.random.randint(1, 100, size=(rows, cols))
    
    print(f"\nИсходная матрица {rows}x{cols}:")
    print(A)
    
    if cols >= 2:
        corr_before = correlation_first_last(A)
        modified_A = swap_max_elements(A.copy())
        
        print("\nМатрица после замены наибольших элементов первого и последнего столбцов:")
        print(modified_A)
        
        corr_after = correlation_first_last(modified_A)
        print(f"\n--- Результаты ---")
        print(f"Коэффициент корреляции (до замены): {corr_before:.2f}")
        print(f"Коэффициент корреляции (после замены): {corr_after:.2f}")
    else:
        print("Матрица должна иметь минимум 2 столбца.")

def run_task6():
    """Execute Task 6: Pandas data analysis."""
    print("\n" + "=" * 50)
    print("Задание 6. Pandas анализ данных")
    print("Вариант 24: Supermarket Sales")
    print("=" * 50)
    
    try:
        import pandas as pd
    except ImportError:
        print("\nОшибка: библиотека pandas не установлена.")
        print("Установите её командой: pip install pandas")
        return
    
    from lab4_var24.task6 import run_full_analysis
    
    try:
        run_full_analysis()
    except FileNotFoundError as e:
        print(f"\n{e}")
        print("\nИнструкция:")
        print("1. Скачайте датасет с Kaggle:")
        print("   https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales")
        print("2. Поместите файл 'SuperMarket Analysis.csv' в папку проекта:")
        print(f"   D:\\453502\\IGI_LR4\\")
        print("3. Запустите программу снова.")
    except Exception as e:
        print(f"\nПроизошла ошибка при анализе данных: {e}")
        import traceback
        traceback.print_exc()

def print_menu():
    """Display the main menu."""
    print("\n" + "=" * 50)
    print("ЛАБОРАТОРНАЯ РАБОТА No. 4")
    print("Разработчик: Finsky Pavel")
    print("Дата: 30.04.2026")
    print("=" * 50)
    print("Меню заданий:")
    print("  1 - Задание 1. Файлы, классы, сериализаторы")
    print("  2 - Задание 2. Регулярные выражения и анализ текста")
    print("  3 - Задание 3. Ряды и визуализация")
    print("  4 - Задание 4. Геометрические фигуры")
    print("  5 - Задание 5. NumPy операции")
    print("  6 - Задание 6. Pandas анализ данных")
    print("  0 - Выход из программы")
    print("-" * 50)


def main():
    """Main function with interactive menu."""
    tasks = {
        "1": run_task1,
        "2": run_task2,
        "3": run_task3,
        "4": run_task4,
        "5": run_task5,
        "6": run_task6,
    }
    
    while True:
        print_menu()
        choice = input("Выберите номер задания (0-6): ").strip()
        
        if choice == "0":
            print("\nВыход из программы. До свидания!")
            sys.exit(0)
        elif choice in tasks:
            try:
                tasks[choice]()
            except ImportError as e:
                print(f"\nОшибка импорта модуля: {e}")
                print("Проверьте, что все файлы находятся в правильных папках.")
                print("Убедитесь, что установлены все необходимые библиотеки:")
                print("  pip install numpy matplotlib pandas")
            except Exception as e:
                print(f"\nПроизошла ошибка при выполнении задания: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("\nНекорректный ввод. Пожалуйста, выберите число от 0 до 6.")
        
        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()