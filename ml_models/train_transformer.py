import os, json; os.makedirs('export', exist_ok=True); json.dump({'model':'transformer_stub'}, open('export/model.json','w'))
