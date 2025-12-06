"""
ARTIFICIAL INTELLIGENCE PROJECT
Organizations Dataset Preprocessing System
Dataset Fields: Index, Organization Id, Name, Website, Country, Description, Founded, Industry, Number of employees
"""

import pandas as pd

class OrganizationsPreprocessor:
    """Main class for organizations data preprocessing operations"""
    
    def __init__(self):
        self.dataset = None
        self.cleaned_data = None
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*65)
        print("ORGANIZATIONS DATA PREPROCESSING SYSTEM")
        print("="*65)
        print("\n1. Load Organizations Dataset")
        print("2. Explore Dataset")
        print("3. Analyze Data Quality")
        print("4. Clean Dataset")
        print("5. Export Cleaned Data")
        print("6. Exit")
        print("="*65)
    
    def load_dataset(self):
        """Load the organizations dataset from CSV file"""
        print("\n[1] LOADING ORGANIZATIONS DATASET")
        print("-"*45)
        
        try:
            self.dataset = pd.read_csv("organizations-100000.csv")
            print("✅ Dataset loaded successfully!")
            print(f"   📊 Records: {len(self.dataset):,}")
            print(f"   📈 Columns: {len(self.dataset.columns)}")
            
            # Display column information
            print("\n   📋 Dataset Structure:")
            print("   " + "-"*40)
            for i, col in enumerate(self.dataset.columns, 1):
                print(f"   {i:2}. {col:20} ({self.dataset[col].dtype})")
            
            return True
        except FileNotFoundError:
            print("❌ Error: 'organizations-100000.csv' not found!")
            print("   Please ensure the file is in the same directory.")
            return False
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
    
    def explore_dataset(self):
        """Explore and describe the dataset"""
        if self.dataset is None:
            print("❌ Please load dataset first (Option 1)")
            return
        
        print("\n[2] DATASET EXPLORATION")
        print("-"*45)
        
        # Basic information
        print("\n📊 BASIC INFORMATION:")
        print(f"   • Total Records: {len(self.dataset):,}")
        print(f"   • Total Columns: {len(self.dataset.columns)}")
        print(f"   • Dataset Shape: {self.dataset.shape}")
        
        # Data types
        print("\n📝 DATA TYPES:")
        dtype_counts = self.dataset.dtypes.value_counts()
        for dtype, count in dtype_counts.items():
            print(f"   • {dtype}: {count} columns")
        
        # First few records
        print("\n👁️  SAMPLE DATA (First 3 records):")
        print(self.dataset.head(3).to_string(index=False))
        
        # Industry distribution
        if 'Industry' in self.dataset.columns:
            print("\n🏢 INDUSTRY DISTRIBUTION:")
            industry_counts = self.dataset['Industry'].value_counts().head(5)
            for industry, count in industry_counts.items():
                percentage = (count / len(self.dataset)) * 100
                print(f"   • {industry}: {count} ({percentage:.1f}%)")
        
        # Country distribution
        if 'Country' in self.dataset.columns:
            print("\n🌍 COUNTRY DISTRIBUTION:")
            country_counts = self.dataset['Country'].value_counts().head(5)
            for country, count in country_counts.items():
                percentage = (count / len(self.dataset)) * 100
                print(f"   • {country}: {count} ({percentage:.1f}%)")
        
        # Employee statistics
        if 'Number of employees' in self.dataset.columns:
            print("\n👥 EMPLOYEE STATISTICS:")
            print(f"   • Min Employees: {self.dataset['Number of employees'].min():,}")
            print(f"   • Max Employees: {self.dataset['Number of employees'].max():,}")
            print(f"   • Avg Employees: {self.dataset['Number of employees'].mean():,.0f}")
            print(f"   • Total Employees: {self.dataset['Number of employees'].sum():,}")
    
    def analyze_quality(self):
        """Analyze data quality issues"""
        if self.dataset is None:
            print("❌ Please load dataset first (Option 1)")
            return
        
        print("\n[3] DATA QUALITY ANALYSIS")
        print("-"*45)
        
        issues = []
        
        # 1. Check for missing values
        print("\n🔍 MISSING VALUES ANALYSIS:")
        missing_data = self.dataset.isnull().sum()
        total_missing = missing_data.sum()
        
        if total_missing > 0:
            issues.append(f"Missing Values ({total_missing} total)")
            print(f"   ❌ Total missing values: {total_missing}")
            for col, count in missing_data.items():
                if count > 0:
                    percentage = (count / len(self.dataset)) * 100
                    print(f"      • {col}: {count} ({percentage:.1f}%)")
        else:
            print("   ✅ No missing values found")
        
        # 2. Check for duplicates
        print("\n🔍 DUPLICATE RECORDS ANALYSIS:")
        duplicates = self.dataset.duplicated().sum()
        
        if duplicates > 0:
            issues.append(f"Duplicate Records ({duplicates} found)")
            print(f"   ❌ Duplicate records: {duplicates}")
            
            # Show duplicate examples
            duplicate_rows = self.dataset[self.dataset.duplicated()]
            print(f"\n   📄 Example of duplicate records:")
            print(duplicate_rows.head(2).to_string(index=False))
        else:
            print("   ✅ No duplicate records found")
        
        # 3. Data validation
        print("\n🔍 DATA VALIDATION:")
        
        # Check website format
        if 'Website' in self.dataset.columns:
            invalid_websites = self.dataset['Website'].apply(
                lambda x: pd.notna(x) and not str(x).startswith('www.')
            ).sum()
            if invalid_websites > 0:
                print(f"   ⚠️  {invalid_websites} websites don't start with 'www.'")
        
        # Check founded year
        if 'Founded' in self.dataset.columns:
            current_year = 2024
            invalid_years = self.dataset['Founded'].apply(
                lambda x: pd.notna(x) and (x < 1800 or x > current_year)
            ).sum()
            if invalid_years > 0:
                print(f"   ⚠️  {invalid_years} invalid founded years")
        
        # Check employee count
        if 'Number of employees' in self.dataset.columns:
            invalid_employees = self.dataset['Number of employees'].apply(
                lambda x: pd.notna(x) and x < 0
            ).sum()
            if invalid_employees > 0:
                print(f"   ⚠️  {invalid_employees} negative employee counts")
        
        # Summary
        print("\n" + "="*45)
        print("QUALITY SUMMARY:")
        if issues:
            print("❌ Issues detected:")
            for issue in issues:
                print(f"   • {issue}")
        else:
            print("✅ Excellent data quality - No issues detected!")
        print("="*45)
    
    def clean_dataset(self):
        """Clean the dataset"""
        if self.dataset is None:
            print("❌ Please load dataset first (Option 1)")
            return
        
        print("\n[4] DATA CLEANING PROCESS")
        print("-"*45)
        
        # Create a copy for cleaning
        self.cleaned_data = self.dataset.copy()
        
        print("Starting cleaning process...\n")
        
        # Step 1: Remove duplicates
        initial_count = len(self.cleaned_data)
        self.cleaned_data = self.cleaned_data.drop_duplicates()
        final_count = len(self.cleaned_data)
        duplicates_removed = initial_count - final_count
        
        if duplicates_removed > 0:
            print(f"✅ STEP 1: Removed {duplicates_removed} duplicate organizations")
        else:
            print("✅ STEP 1: No duplicates to remove")
        
        # Step 2: Handle missing values
        print("\n✅ STEP 2: Handling missing values")
        
        # Fill missing websites
        if 'Website' in self.cleaned_data.columns:
            website_missing = self.cleaned_data['Website'].isnull().sum()
            if website_missing > 0:
                self.cleaned_data['Website'] = self.cleaned_data['Website'].fillna('website-not-available.com')
                print(f"   • Filled {website_missing} missing websites")
        
        # Fill missing descriptions
        if 'Description' in self.cleaned_data.columns:
            desc_missing = self.cleaned_data['Description'].isnull().sum()
            if desc_missing > 0:
                self.cleaned_data['Description'] = self.cleaned_data['Description'].fillna('No description available')
                print(f"   • Filled {desc_missing} missing descriptions")
        
        # Fill missing countries
        if 'Country' in self.cleaned_data.columns:
            country_missing = self.cleaned_data['Country'].isnull().sum()
            if country_missing > 0:
                self.cleaned_data['Country'] = self.cleaned_data['Country'].fillna('Unknown')
                print(f"   • Filled {country_missing} missing countries")
        
        # Fill missing industries
        if 'Industry' in self.cleaned_data.columns:
            industry_missing = self.cleaned_data['Industry'].isnull().sum()
            if industry_missing > 0:
                self.cleaned_data['Industry'] = self.cleaned_data['Industry'].fillna('Other')
                print(f"   • Filled {industry_missing} missing industries")
        
        # Fill missing employee counts with median
        if 'Number of employees' in self.cleaned_data.columns:
            emp_missing = self.cleaned_data['Number of employees'].isnull().sum()
            if emp_missing > 0:
                median_employees = self.cleaned_data['Number of employees'].median()
                self.cleaned_data['Number of employees'] = self.cleaned_data['Number of employees'].fillna(median_employees)
                print(f"   • Filled {emp_missing} missing employee counts with median: {median_employees:,.0f}")
        
        # Step 3: Data standardization
        print("\n✅ STEP 3: Standardizing data formats")
        
        # Standardize website format
        if 'Website' in self.cleaned_data.columns:
            def format_website(url):
                if pd.isna(url):
                    return url
                url = str(url).strip()
                if not url.startswith('http'):
                    return f'https://{url}'
                return url
            
            self.cleaned_data['Website'] = self.cleaned_data['Website'].apply(format_website)
            print("   • Standardized website URLs")
        
        # Fix negative employee counts
        if 'Number of employees' in self.cleaned_data.columns:
            negative_emps = (self.cleaned_data['Number of employees'] < 0).sum()
            if negative_emps > 0:
                self.cleaned_data['Number of employees'] = self.cleaned_data['Number of employees'].apply(
                    lambda x: abs(x) if x < 0 else x
                )
                print(f"   • Fixed {negative_emps} negative employee counts")
        
        # Fix invalid founded years
        if 'Founded' in self.cleaned_data.columns:
            current_year = 2024
            invalid_years = ((self.cleaned_data['Founded'] < 1800) | 
                           (self.cleaned_data['Founded'] > current_year)).sum()
            if invalid_years > 0:
                # Replace with median year
                median_year = self.cleaned_data['Founded'].median()
                self.cleaned_data['Founded'] = self.cleaned_data['Founded'].apply(
                    lambda x: median_year if x < 1800 or x > current_year else x
                )
                print(f"   • Fixed {invalid_years} invalid founded years")
        
        # Summary
        print("\n" + "="*45)
        print("CLEANING COMPLETE!")
        print(f"Original records: {initial_count:,}")
        print(f"Cleaned records: {final_count:,}")
        print(f"Records removed: {duplicates_removed}")
        
        # Show cleaning impact
        print("\n📊 CLEANING IMPACT:")
        print(f"   • Missing values before: {self.dataset.isnull().sum().sum()}")
        print(f"   • Missing values after: {self.cleaned_data.isnull().sum().sum()}")
        print(f"   • Duplicates before: {self.dataset.duplicated().sum()}")
        print(f"   • Duplicates after: {self.cleaned_data.duplicated().sum()}")
        print("="*45)
        
        # Show cleaned data sample
        print("\n📄 CLEANED DATA SAMPLE:")
        print(self.cleaned_data.head(3).to_string(index=False))
    
    def export_data(self):
        """Export cleaned data to CSV"""
        if self.cleaned_data is None:
            print("❌ Please clean dataset first (Option 4)")
            return
        
        print("\n[5] EXPORT CLEANED DATA")
        print("-"*45)
        
        filename = "cleaned_organizations_dataset.csv"
        
        try:
            self.cleaned_data.to_csv(filename, index=False)
            
            print(f"✅ Data exported successfully!")
            print(f"\n📁 FILE DETAILS:")
            print(f"   • Filename: {filename}")
            print(f"   • Records: {len(self.cleaned_data):,}")
            print(f"   • Columns: {len(self.cleaned_data.columns)}")
            print(f"   • File size: ~{len(self.cleaned_data) * len(self.cleaned_data.columns):,} data points")
            
            # Industry summary of exported data
            if 'Industry' in self.cleaned_data.columns:
                print(f"\n🏢 INDUSTRY DISTRIBUTION IN EXPORTED DATA:")
                industry_summary = self.cleaned_data['Industry'].value_counts()
                for industry, count in industry_summary.head(5).items():
                    print(f"   • {industry}: {count} organizations")
            
            # Country summary
            if 'Country' in self.cleaned_data.columns:
                print(f"\n🌍 TOP COUNTRIES IN EXPORTED DATA:")
                country_summary = self.cleaned_data['Country'].value_counts()
                for country, count in country_summary.head(5).items():
                    print(f"   • {country}: {count} organizations")
            
            print(f"\n📍 File saved in: {filename}")
            
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
    
    def run(self):
        """Main program loop"""
        print("\n" + "="*65)
        print("ORGANIZATIONS DATA PREPROCESSING SYSTEM")
        print("="*65)
        print("\nDataset Fields:")
        print("1. Index                2. Organization Id")
        print("3. Name                 4. Website")
        print("5. Country              6. Description")
        print("7. Founded              8. Industry")
        print("9. Number of employees")
        print("="*65)
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self.load_dataset()
            elif choice == '2':
                self.explore_dataset()
            elif choice == '3':
                self.analyze_quality()
            elif choice == '4':
                self.clean_dataset()
            elif choice == '5':
                self.export_data()
            elif choice == '6':
                print("\n" + "="*65)
                print("THANK YOU FOR USING ORGANIZATIONS DATA PREPROCESSING SYSTEM")
                print("="*65)
                break
            else:
                print("❌ Invalid choice! Please enter 1-6")
            
            input("\nPress Enter to continue...")

def main():
    """Main function"""
    processor = OrganizationsPreprocessor()
    processor.run()

if __name__ == "__main__":
    main()