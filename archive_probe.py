import os
import json
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

root = r'C:\Users\ian83\OneDrive\文件\DSO576_Music_Project\archive'

def main():
    print('--- README ---')
    readme_path = os.path.join(root, 'README.md')
    with open(readme_path, 'r', encoding='utf-8', errors='replace') as f:
        print(f.read()[:6000])

    print('\n--- METADATA ---')
    meta_path = os.path.join(root, 'metadata', 'metadata.json')
    with open(meta_path, 'r', encoding='utf-8', errors='replace') as f:
        meta = json.load(f)
    print(json.dumps(meta, ensure_ascii=False, indent=2)[:12000])

    print('\n--- FILE NAMES ---')
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            print(rel, os.path.getsize(full))

    print('\n--- FULL DATA PROFILE ---')
    full_candidates = [
        os.path.join(root, 'data', 'full', 'spotify_full.csv.gz'),
        os.path.join(root, 'data', 'full', 'spotify_full.csv')
    ]
    full_path = next((p for p in full_candidates if os.path.exists(p)), full_candidates[0])
    print('full_path', full_path)
    if os.path.exists(full_path):
        df = pd.read_csv(full_path)
        print('shape=', df.shape)
        print('columns=', len(df.columns))
        print('column_names=', list(df.columns))
        print('\nDtypes:')
        print(df.dtypes.to_string())
        print('\nMissing counts:')
        print(df.isna().sum().sort_values(ascending=False).to_string())
        print('\nExact duplicate rows=', int(df.duplicated().sum()))
        print('Repeated track_id count=', int(df['track_id'].duplicated().sum()))
        print('Repeated spotify_id count=', int(df['spotify_id'].duplicated().sum()))
        print('track_popularity summary=', df['track_popularity'].describe().to_dict())
        print('track_popularity null count=', int(df['track_popularity'].isna().sum()))
        if 'genre_l1' in df.columns and 'release_year' in df.columns:
            g = df.groupby(['genre_l1', 'release_year'], dropna=False)['track_popularity'].agg(['count', 'mean', 'min', 'max'])
            print('\nPopularity sample by genre and year:')
            print(g.head(10).to_string())
        print('\nHead rows:')
        print(df.head(3).to_string(index=False))

    print('\n--- TRACK_POPULARITY DEFINITION ---')
    meta_path = os.path.join(root, 'metadata', 'metadata.json')
    with open(meta_path, 'r', encoding='utf-8', errors='replace') as f:
        meta = json.load(f)
    schema = {row['name']: row for row in meta.get('schema', [])}
    tp = schema.get('track_popularity')
    if tp:
        print(tp)
    else:
        print('track_popularity not found in metadata schema')

if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        raise
