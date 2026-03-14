import pandas as pd

def lemmas_to_excel(data, file_id):
    rows = []
    for word, arr in data.items():
        last = arr[-1]
        rest = ','.join(map(str, arr[:-1]))
        rows.append({"Словоформа": word, "Всего": last, "В строках": rest})

    df = pd.DataFrame(rows, columns=["Словоформа", "Всего", "В строках"])
    df.to_excel(f"send-file/Ответ_{file_id}.xlsx", index=False)

    print(f"Данные успешно записаны в Ответ_{file_id}.xlsx")
