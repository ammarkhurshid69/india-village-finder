import pandas as pd
import glob
import os
import re

FOLDER_PATH = "New folder"

files = glob.glob(os.path.join(FOLDER_PATH, "*.*"))
print(f"📂 Found {len(files)} files")

df_list = []

for file in files:
    try:
        if file.endswith(".xlsx"):
            df = pd.read_excel(file, engine="openpyxl")
        elif file.endswith(".xls"):
            df = pd.read_excel(file, engine="xlrd")
        elif file.endswith(".ods"):
            df = pd.read_excel(file, engine="odf")
        else:
            continue

        df.columns = df.columns.str.strip()
        df_list.append(df)
        print(f"✅ Loaded: {os.path.basename(file)} — {len(df)} rows")

    except Exception as e:
        print(f"❌ Error: {file} → {e}")

if not df_list:
    print("❌ No Excel files found!")
    exit()

final_df = pd.concat(df_list, ignore_index=True)
final_df.columns = final_df.columns.str.strip()
print(f"\n🧠 Columns found: {final_df.columns.tolist()}")
print(f"📊 Total rows before clean: {len(final_df)}")

# Auto-detect columns
def find_col(options):
    for name in options:
        if name in final_df.columns:
            return name
    return None

state_col      = find_col(["STATE NAME", "State Name", "state"])
district_col   = find_col(["DISTRICT NAME", "District Name", "district"])
subdistrict_col= find_col(["SUB-DISTR", "SUB-DISTRICT NAME", "SUB_DISTRICT", "sub_district"])
village_col    = find_col(["Area Name", "Village Name", "VILLAGE NAME", "village"])

print(f"\n🔍 Detected columns:")
print(f"  state      → {state_col}")
print(f"  district   → {district_col}")
print(f"  subdistrict→ {subdistrict_col}")
print(f"  village    → {village_col}")

if not all([state_col, district_col, subdistrict_col, village_col]):
    print("\n❌ Could not detect all columns. Please check column names above.")
    exit()

final_df = final_df.rename(columns={
    state_col: "state",
    district_col: "district",
    subdistrict_col: "sub_district",
    village_col: "village"
})

final_df = final_df[["state", "district", "sub_district", "village"]]

# Clean
final_df["village"] = final_df["village"].fillna("").astype(str)
final_df["village"] = final_df["village"].apply(lambda x: re.sub(r"\(.*?\)", "", x)).str.strip()
final_df = final_df.dropna()
final_df = final_df[final_df["village"] != ""]
final_df = final_df.drop_duplicates()

# Remove header rows that got mixed in
for col in ["state", "district", "sub_district", "village"]:
    final_df = final_df[final_df[col].str.lower() != col.lower().replace("_", " ")]
    final_df = final_df[final_df[col].str.lower() != col.lower()]

final_df = final_df.reset_index(drop=True)
print(f"✅ Clean rows: {len(final_df)}")

# Save
output = "india_villages_clean.csv"
final_df.to_csv(output, index=False)
print(f"\n🎉 Saved to {output}")
print(f"   States: {final_df['state'].nunique()}")
print(f"   Districts: {final_df['district'].nunique()}")
print(f"   Villages: {final_df['village'].nunique()}")
