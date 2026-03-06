"""
Тестовое задание.  Стёпин Руслан @RrshiDev (+79532863360)
Генератор чертежей и 3D-моделей болтов с шестигранной головкой.
Режимы работы:
  1. Пакетная генерация (batch) — по фиксированным диапазонам размеров. (Согласно задаче. Переменные содержат ряд значений для автоматической генерации 3д-модели и dxf-файлов чертежей)
  2. Единичный ввод (single) — пользователь задаёт параметры одного болта. (Добавлена возможно ввода необходимых значений пользователем вручную)
Все результаты сохраняются в папку ./output_bolt.
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import random
import math
import sys
import ezdxf
import cadquery as cq
from cadquery import exporters
import python_minifier


OUTPUT_DIR = "./output_bolt"
os.makedirs(OUTPUT_DIR, exist_ok=True)


BATCH_D_VALUES = [6, 8, 10, 12, 16, 20]
BATCH_L_VALUES = list(range(20, 101, 10))


def head_size(D):
    S = round(1.5 * D + 1, 1)
    K = round(0.65 * D, 1)
    return S, K


def draw_bolt_dxf(D, L, S, K, runout, chamfer_head, timestr, python_code):

    python_code.append("import ezdxf")
    python_code.append("from math import tan, radians")
    python_code.append("import time")
    python_code.append(f"timestr = '{timestr}'")
    python_code.append(f"D = {D}")
    python_code.append(f"L = {L}")
    python_code.append(f"S = {S}")
    python_code.append(f"K = {K}")
    python_code.append(f"runout = {runout}")
    python_code.append(f"chamfer_head = {chamfer_head}")

    doc = ezdxf.new('R2010', setup=True, units=4)
    msp = doc.modelspace()
    python_code.append("doc = ezdxf.new('R2010', setup=True, units=4)")
    python_code.append("msp = doc.modelspace()")

    doc.layers.add(name="Main", color=7, linetype="CONTINUOUS", lineweight=50)
    python_code.append("doc.layers.add(name='Main', color=7, linetype='CONTINUOUS', lineweight=50)")
    doc.layers.add(name="Thread", color=4, linetype="CONTINUOUS", lineweight=25)
    python_code.append("doc.layers.add(name='Thread', color=4, linetype='CONTINUOUS', lineweight=25)")
    doc.layers.add(name="Hatches", color=8, linetype="CONTINUOUS", lineweight=25)
    python_code.append("doc.layers.add(name='Hatches', color=8, linetype='CONTINUOUS', lineweight=25)")
    doc.layers.add(name="Axises", color=6, linetype="CENTER")
    python_code.append("doc.layers.add(name='Axises', color=6, linetype='CENTER')")
    doc.layers.add(name="Measure", color=170, lineweight=25)
    python_code.append("doc.layers.add(name='Measure', color=170, lineweight=25)")

    msp.add_line((-5, 0), (K + L + 5, 0), dxfattribs={"layer": "Axises"})
    python_code.append("msp.add_line((-5, 0), (K + L + 5, 0), dxfattribs={'layer': 'Axises'})")

    p0 = (0, 0)
    p1 = (0, S/2)
    fh = chamfer_head
    p2 = (K - fh, S/2)
    p3 = (K, S/2 - fh * math.tan(math.radians(30)))
    p4 = (K, D/2)
    thr_len = L - runout
    p5 = (K + thr_len, D/2)
    p6 = (K + thr_len + runout, D/2 - runout)
    p7 = (K + L, 0)

    python_code.append(f"p0 = {p0}")
    python_code.append(f"p1 = {p1}")
    python_code.append(f"fh = {fh}")
    python_code.append(f"p2 = {p2}")
    python_code.append(f"p3 = {p3}")
    python_code.append(f"p4 = {p4}")
    python_code.append(f"thr_len = {thr_len}")
    python_code.append(f"p5 = {p5}")
    python_code.append(f"p6 = {p6}")
    python_code.append(f"p7 = {p7}")

    line1 = msp.add_line(p0, p1, dxfattribs={"layer": "Main"})
    python_code.append("line1 = msp.add_line(p0, p1, dxfattribs={'layer': 'Main'})")
    line2 = msp.add_line(p1, p2, dxfattribs={"layer": "Main"})
    python_code.append("line2 = msp.add_line(p1, p2, dxfattribs={'layer': 'Main'})")
    line3 = msp.add_line(p2, p3, dxfattribs={"layer": "Main"})
    python_code.append("line3 = msp.add_line(p2, p3, dxfattribs={'layer': 'Main'})")
    line4 = msp.add_line(p3, p4, dxfattribs={"layer": "Main"})
    python_code.append("line4 = msp.add_line(p3, p4, dxfattribs={'layer': 'Main'})")
    line5 = msp.add_line(p4, p5, dxfattribs={"layer": "Main"})
    python_code.append("line5 = msp.add_line(p4, p5, dxfattribs={'layer': 'Main'})")
    line6 = msp.add_line(p5, p6, dxfattribs={"layer": "Main"})
    python_code.append("line6 = msp.add_line(p5, p6, dxfattribs={'layer': 'Main'})")
    line7 = msp.add_line(p6, p7, dxfattribs={"layer": "Main"})
    python_code.append("line7 = msp.add_line(p6, p7, dxfattribs={'layer': 'Main'})")

    d1 = D - 1.5
    offset = (D - d1) / 2
    python_code.append(f"d1 = {d1}")
    python_code.append(f"offset = {offset}")

    thr_line_start = (p4[0], p4[1] - offset)
    thr_line_end = (p5[0], p5[1] - offset)
    line_thr1 = msp.add_line(thr_line_start, thr_line_end, dxfattribs={"layer": "Thread"})
    python_code.append(f"thr_line_start = {thr_line_start}")
    python_code.append(f"thr_line_end = {thr_line_end}")
    python_code.append("line_thr1 = msp.add_line(thr_line_start, thr_line_end, dxfattribs={'layer': 'Thread'})")

    thr_runout_start = (p5[0], p5[1] - offset)
    thr_runout_end = (p6[0], p6[1] - offset - runout)
    line_thr2 = msp.add_line(thr_runout_start, thr_runout_end, dxfattribs={"layer": "Thread"})
    python_code.append(f"thr_runout_start = {thr_runout_start}")
    python_code.append(f"thr_runout_end = {thr_runout_end}")
    python_code.append("line_thr2 = msp.add_line(thr_runout_start, thr_runout_end, dxfattribs={'layer': 'Thread'})")

    line_thr3 = msp.add_line((p4[0], p4[1]), (p4[0], p4[1] - offset), dxfattribs={"layer": "Thread"})
    python_code.append("line_thr3 = msp.add_line((p4[0], p4[1]), (p4[0], p4[1] - offset), dxfattribs={'layer': 'Thread'})")

    line_thr_boundary = msp.add_line((p5[0], p5[1]), (p5[0], p5[1] - offset - 0.5), dxfattribs={"layer": "Thread"})
    python_code.append("line_thr_boundary = msp.add_line((p5[0], p5[1]), (p5[0], p5[1] - offset - 0.5), dxfattribs={'layer': 'Thread'})")

    def mirror_entity(entity):
        copy = entity.copy()
        msp.add_entity(copy)
        copy.scale(1, -1, 1)

    python_code.append("# Отражение основных линий")
    for name in ["line1", "line2", "line3", "line4", "line5", "line6", "line7"]:
        python_code.append(f"{name}_sym = {name}.copy()")
        python_code.append(f"msp.add_entity({name}_sym)")
        python_code.append(f"{name}_sym.scale(1, -1, 1)")

    python_code.append("# Отражение линий резьбы")
    for name in ["line_thr1", "line_thr2", "line_thr3", "line_thr_boundary"]:
        python_code.append(f"{name}_sym = {name}.copy()")
        python_code.append(f"msp.add_entity({name}_sym)")
        python_code.append(f"{name}_sym.scale(1, -1, 1)")

    dim_attrs = {
        "dimtxt": 2.5,
        "dimtad": 0,
        "dimtvp": 0,
        "dimdle": 0,
        "dimblk": "EZ_ARROW_FILLED",
    }
    python_code.append("dim_attrs = {'dimtxt': 2.5, 'dimtad': 0, 'dimtvp': 0, 'dimdle': 0, 'dimblk': 'EZ_ARROW_FILLED'}")

    dim_total = msp.add_linear_dim(
        base=(K + L + 10, -5),
        p1=(0, 0),
        p2=(K + L, 0),
        dimstyle="STANDARD",
        override=dim_attrs,
        dxfattribs={"layer": "Measure"}
    )
    dim_total.render()
    python_code.append("dim_total = msp.add_linear_dim(base=(K+L+10, -5), p1=(0,0), p2=(K+L,0), dimstyle='STANDARD', override=dim_attrs, dxfattribs={'layer': 'Measure'})")
    python_code.append("dim_total.render()")

    dim_thr_len = msp.add_linear_dim(
        base=(K + L + 15, D/2 + 5),
        p1=(K, D/2),
        p2=(K + thr_len, D/2),
        dimstyle="STANDARD",
        override=dim_attrs,
        dxfattribs={"layer": "Measure"}
    )
    dim_thr_len.render()
    python_code.append("dim_thr_len = msp.add_linear_dim(base=(K+L+15, D/2+5), p1=(K, D/2), p2=(K+thr_len, D/2), dimstyle='STANDARD', override=dim_attrs, dxfattribs={'layer': 'Measure'})")
    python_code.append("dim_thr_len.render()")

    dim_s = msp.add_linear_dim(
        base=(-10, S/2),
        p1=(0, S/2),
        p2=(0, -S/2),
        text=f"S{S}",
        dimstyle="STANDARD",
        angle=90,
        override=dim_attrs,
        dxfattribs={"layer": "Measure"}
    )
    dim_s.render()
    python_code.append(f"dim_s = msp.add_linear_dim(base=(-10, S/2), p1=(0, S/2), p2=(0, -S/2), text='S{S}', dimstyle='STANDARD', angle=90, override=dim_attrs, dxfattribs={{'layer': 'Measure'}})")
    python_code.append("dim_s.render()")

    dim_k = msp.add_linear_dim(
        base=(-5, S/2 + 7.5),
        p1=(0, 0),
        p2=(K, 0),
        dimstyle="STANDARD",
        override=dim_attrs,
        dxfattribs={"layer": "Measure"}
    )
    dim_k.render()
    python_code.append("dim_k = msp.add_linear_dim(base=(-5, S/2+7.5), p1=(0,0), p2=(K,0), dimstyle='STANDARD', override=dim_attrs, dxfattribs={'layer': 'Measure'})")
    python_code.append("dim_k.render()")

    dim_d = msp.add_linear_dim(
        base=(K + L + 22.5, D/2),
        p1=(K + thr_len, D/2),
        p2=(K + thr_len, -D/2),
        text=f"M{D}",
        dimstyle="STANDARD",
        angle=90,
        override=dim_attrs,
        dxfattribs={"layer": "Measure"}
    )
    dim_d.render()
    python_code.append(f"dim_d = msp.add_linear_dim(base=(K+L+22.5, D/2), p1=(K+thr_len, D/2), p2=(K+thr_len, -D/2), text='M{D}', dimstyle='STANDARD', angle=90, override=dim_attrs, dxfattribs={{'layer': 'Measure'}})")
    python_code.append("dim_d.render()")

    vert_line_up = (p2[0], p2[1] + 5)
    ang_dim_head = msp.add_angular_dim_2l(
        base=(K - 5, S/2 + 10),
        line1=(p2, p3),
        line2=(p2, vert_line_up),
        dimstyle="EZ_CURVED",
        override=dim_attrs,
        dxfattribs={"layer": "Measure"}
    )
    ang_dim_head.render()
    python_code.append(f"vert_line_up = {vert_line_up}")
    python_code.append("ang_dim_head = msp.add_angular_dim_2l(base=(K-5, S/2+10), line1=(p2, p3), line2=(p2, vert_line_up), dimstyle='EZ_CURVED', override=dim_attrs, dxfattribs={'layer': 'Measure'})")
    python_code.append("ang_dim_head.render()")

    chamfer_dim = msp.add_linear_dim(
        base=(p5[0] + 10, p5[1] + 8),
        p1=p5,
        p2=p6,
        dimstyle="STANDARD",
        override=dim_attrs,
        text=f"{runout}x45°",
        dxfattribs={"layer": "Measure"}
    )
    chamfer_dim.render()
    python_code.append(f"chamfer_dim = msp.add_linear_dim(base=({p5[0]+10}, {p5[1]+8}), p1=p5, p2=p6, dimstyle='STANDARD', override=dim_attrs, text='{runout}x45°', dxfattribs={{'layer': 'Measure'}})")
    python_code.append("chamfer_dim.render()")

    filename = os.path.join(OUTPUT_DIR, f"{timestr}1.dxf")
    doc.saveas(filename)
    python_code.append(f"doc.saveas('./{timestr}1.dxf')")

def draw_bolt_3d(D, L, S, K, runout, chamfer_head, timestr):
  
    head = cq.Workplane("XY").polygon(6, S).extrude(K)
    head = head.faces(">Z").edges().chamfer(chamfer_head)

    shank = cq.Workplane("XY").circle(D/2).extrude(L)
    shank = shank.faces(">Z").edges().chamfer(runout)
    shank = shank.translate((0, 0, K))

    bolt = head.union(shank)

    filename = os.path.join(OUTPUT_DIR, f"{timestr}2.stp")
    exporters.export(bolt, filename, cq.exporters.ExportTypes.STEP)

def get_positive_float(prompt, min_val=0.1, max_val=1000.0):
    while True:
        try:
            val = float(input(prompt))
            if val < min_val or val > max_val:
                print(f"Ошибка: значение должно быть от {min_val} до {max_val}. Повторите ввод.")
                continue
            return val
        except ValueError:
            print("Ошибка: введите число (используйте точку как разделитель).")

def get_positive_int(prompt, min_val=1, max_val=100):
    while True:
        try:
            val = int(input(prompt))
            if val < min_val or val > max_val:
                print(f"Ошибка: значение должно быть целым от {min_val} до {max_val}.")
                continue
            return val
        except ValueError:
            print("Ошибка: введите целое число.")

def single_mode():
    print("\n--- Режим единичного ввода ---")
    print("Введите параметры болта:")

    D = get_positive_float("Диаметр резьбы D (мм, например 10): ", min_val=3, max_val=48)
    L = get_positive_float("Длина стержня L (мм, например 50): ", min_val=5, max_val=300)

    S, K = head_size(D)
    print(f"Размер под ключ S = {S} мм, высота головки K = {K} мм (расчёт по ГОСТ).")

    choice = input("Задать сбег и фаску вручную? (y/n, по умолчанию случайные): ").lower()
    if choice == 'y':
        runout = get_positive_float("Сбег (фаска на конце стержня) runout (мм, 0.5-2.0): ", min_val=0.1, max_val=5.0)
        chamfer_head = get_positive_float("Фаска на головке chamfer_head (мм, 0.2-2.0): ", min_val=0.1, max_val=5.0)
        if runout >= L:
            print("Ошибка: сбег должен быть меньше длины стержня. Устанавливаю runout = L/2")
            runout = L / 2
    else:
        runout = round(random.uniform(0.5, min(2.0, L/2)), 1)
        chamfer_head = round(random.uniform(0.3, 2.0), 1)
        print(f"Сгенерированы случайные значения: runout = {runout}, chamfer_head = {chamfer_head}")

    num_variants = get_positive_int("Сколько вариантов сгенерировать (1-3)? ", min_val=1, max_val=3)

    for variant in range(num_variants):
        if variant == 0:
            r = runout
            ch = chamfer_head
        else:
            r = round(random.uniform(0.5, min(2.0, L/2)), 1)
            ch = round(random.uniform(0.3, 2.0), 1)

        timestr = time.strftime('%Y%m%d-%H%M%S') + f"-{variant}"
        python_code = []

        draw_bolt_dxf(D, L, S, K, r, ch, timestr, python_code)
        draw_bolt_3d(D, L, S, K, r, ch, timestr)

        full_code_path = os.path.join(OUTPUT_DIR, f"{timestr}3.py")
        with open(full_code_path, "w", encoding="utf-8") as f:
            for line in python_code:
                f.write(line + "\n")

        with open(full_code_path, "r", encoding="utf-8") as f:
            code = f.read()
        minified = python_minifier.minify(
            code,
            combine_imports=True,
            remove_pass=True,
            remove_literal_statements=True,
            hoist_literals=True,
            rename_locals=True,
            rename_globals=True,
            preserve_globals=['str']
        )
        with open(os.path.join(OUTPUT_DIR, f"{timestr}4.py"), "w", encoding="utf-8") as f:
            f.write(minified)

        time.sleep(0.1)

    print(f"Генерация завершена. Файлы сохранены в {OUTPUT_DIR}")

def batch_mode():
    print("\n--- Пакетный режим ---")
    print(f"Генерируются болты для диаметров {BATCH_D_VALUES} и длин {BATCH_L_VALUES}.")
    print("Для каждого сочетания создаются 3 случайных вариации.")

    total = len(BATCH_D_VALUES) * len(BATCH_L_VALUES) * 3
    print(f"Всего будет создано примерно {total * 4} файлов.")

    confirm = input("Продолжить? (y/n): ").lower()
    if confirm != 'y':
        print("Операция отменена.")
        return

    for D in BATCH_D_VALUES:
        S, K = head_size(D)
        for L in BATCH_L_VALUES:
            for variant in range(3):
                runout = round(random.uniform(0.5, min(2.0, L/2)), 1)
                chamfer_head = round(random.uniform(0.3, 2.0), 1)

                timestr = time.strftime('%Y%m%d-%H%M%S') + f"-{variant}"
                python_code = []

                draw_bolt_dxf(D, L, S, K, runout, chamfer_head, timestr, python_code)
                draw_bolt_3d(D, L, S, K, runout, chamfer_head, timestr)

                full_code_path = os.path.join(OUTPUT_DIR, f"{timestr}3.py")
                with open(full_code_path, "w", encoding="utf-8") as f:
                    for line in python_code:
                        f.write(line + "\n")

                with open(full_code_path, "r", encoding="utf-8") as f:
                    code = f.read()
                minified = python_minifier.minify(
                    code,
                    combine_imports=True,
                    remove_pass=True,
                    remove_literal_statements=True,
                    hoist_literals=True,
                    rename_locals=True,
                    rename_globals=True,
                    preserve_globals=['str']
                )
                with open(os.path.join(OUTPUT_DIR, f"{timestr}4.py"), "w", encoding="utf-8") as f:
                    f.write(minified)

                time.sleep(0.1)

    print("Пакетная генерация завершена.")

def main():
    print("=" * 50)
    print("Генератор чертежей и 3D-моделей болтов")
    print("=" * 50)
    print("Выберите режим работы:")
    print("1. Пакетная генерация (по фиксированным диапазонам)")
    print("2. Единичный ввод параметров")
    print("0. Выход")

    choice = input("Ваш выбор (0/1/2): ").strip()
    if choice == '1':
        batch_mode()
    elif choice == '2':
        single_mode()
    elif choice == '0':
        sys.exit(0)
    else:
        print("Неверный выбор. Завершение.")
        sys.exit(1)

if __name__ == "__main__":
    main()