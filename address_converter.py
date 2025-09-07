import pandas as pd

class AddressConverter:
    def __init__(self, mapping_csv_path='address_mappings.csv'):
        """
        Initializes the converter by loading the address mappings.
        """
        try:
            self.mapping_df = pd.read_csv(mapping_csv_path)
            # Create a dictionary for faster lookups
            self.address_map = pd.Series(self.mapping_df.new.values, index=self.mapping_df.old).to_dict()
        except FileNotFoundError:
            raise RuntimeError(f"Mapping file not found at {mapping_csv_path}")

    def convert_address(self, old_address):
        """
        Converts a single old address to a new address.
        """
        return self.address_map.get(old_address) # Returns None if not found

    def convert_list(self, old_addresses):
        """
        Converts a list of old addresses and returns a DataFrame.
        """
        results = []
        for old_addr in old_addresses:
            new_addr = self.convert_address(old_addr)
            results.append({
                'old_address': old_addr,
                'new_address': new_addr if new_addr else 'Not Found'
            })
        return pd.DataFrame(results)

def main():
    """
    Demonstrates the use of the AddressConverter.
    """
    print("Initializing address converter...")
    try:
        converter = AddressConverter()
    except RuntimeError as e:
        print(e)
        return

    # Since we don't have the user's list, we'll use a sample from the mapping file.
    sample_old_addresses = [
        "桟橋通三丁目２８番１９号",
        "百石町二丁目１４番５号",
        "ThisAddressDoesNotExist" # Example of a failed lookup
    ]

    print("\nConverting a sample list of addresses:")
    print(f"Input: {sample_old_addresses}")

    results_df = converter.convert_list(sample_old_addresses)

    print("\nConversion Results:")
    print(results_df)

    # Save the results to a new CSV file
    output_filename = 'converted_addresses.csv'
    results_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"\nResults saved to {output_filename}")

if __name__ == '__main__':
    main()
