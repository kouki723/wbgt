import re
import os
import pandas as pd

def parse_address_file(filepath):
    """
    Parses a single address mapping text file using a regex-based approach.
    """
    mappings = []
    in_data_section = False
    last_old_address = ""

    # Regex to capture the first non-space block (old address) and the rest of the line.
    line_regex = re.compile(r'^(\S+)\s+(.+)$')

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line_stripped = line.strip()

            if "旧 表 示" in line and "新 表 示" in line:
                in_data_section = True
                continue

            # Use more specific checks to avoid skipping data lines
            if not line_stripped or "住居表示対照表" in line_stripped or "実施日" in line_stripped or line_stripped.isdigit():
                in_data_section = False
                last_old_address = "" # Reset on page breaks
                continue

            if in_data_section:
                match = line_regex.match(line_stripped)
                if match:
                    old_address = match.group(1)
                    rest_of_line = match.group(2).strip()

                    parts = rest_of_line.split()
                    new_address = parts[0]

                    # Clean up remark
                    if '（変更ナシ）' in new_address:
                        new_address = new_address.replace('（変更ナシ）', '').strip()

                    if old_address:
                        last_old_address = old_address

                    if old_address and new_address:
                        mappings.append({"old": old_address, "new": new_address})
                elif line_stripped and last_old_address:
                    # This handles the case where the line starts with spaces (one-to-many mapping)
                    # and the old address is not repeated.
                    parts = line_stripped.split()
                    if parts:
                        new_address = parts[0]
                        mappings.append({"old": last_old_address, "new": new_address})

    return mappings

def process_all_files():
    """
    Processes all text files in data/txts and saves the combined mapping.
    """
    all_mappings = []
    txt_dir = 'data/txts'
    for filename in sorted(os.listdir(txt_dir)):
        if filename.endswith('.txt'):
            filepath = os.path.join(txt_dir, filename)
            # print(f"Processing {filepath}...")
            file_mappings = parse_address_file(filepath)
            all_mappings.extend(file_mappings)

    df = pd.DataFrame(all_mappings)
    df = df.drop_duplicates().reset_index(drop=True)
    df.to_csv('address_mappings.csv', index=False, encoding='utf-8-sig')

    print(f"\nSuccessfully processed {len(os.listdir(txt_dir))} files.")
    print(f"Created address_mappings.csv with {len(df)} entries.")
    print("\n--- Sample of address_mappings.csv ---")
    print(df.head())

if __name__ == '__main__':
    process_all_files()
