# gerar_data.py
# Execute: python gerar_data.py relatorio.xlsx
# Gera o data.json para subir no GitHub

import sys, json, pandas as pd
from datetime import datetime

arquivo = sys.argv[1] if len(sys.argv) > 1 else 'relatorio.xlsx'

df = pd.read_excel(arquivo)

col_data = next((c for c in df.columns if 'data' in c.lower() and 'cria' in c.lower()), df.columns[2])
col_foto = next((c for c in df.columns if c.strip().lower() == 'foto'), df.columns[20])

df['_data'] = pd.to_datetime(df[col_data], errors='coerce').dt.date
foto_group = df[df[col_foto].astype(str).str.strip().str.upper() == 'SIM'].groupby('_data').size().reset_index(name='sim')
total_group = df.groupby('_data').size().reset_index(name='total')
result = total_group.merge(foto_group, on='_data', how='left').fillna(0)
result['sim'] = result['sim'].astype(int)
result = result.sort_values('_data')

rows = [{"d": r['_data'].strftime('%d/%m/%Y'), "sim": int(r['sim']), "total": int(r['total'])} for _, r in result.iterrows()]
output = {"updated": datetime.now().strftime('%d/%m/%Y %H:%M'), "rows": rows}

with open('data.json', 'w') as f:
    json.dump(output, f)

print(f"✓ data.json gerado com {len(rows)} dias — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
